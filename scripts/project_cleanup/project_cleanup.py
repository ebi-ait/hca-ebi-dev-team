from typing import List
from ingest.api.ingestapi import IngestApi
from functools import reduce
from itertools import chain
from typing import Dict, Iterable


class ProjectCleanup:

    def __init__(self, ingest_client: IngestApi):
        self.ingest_client = ingest_client

    def find_all_submissions_to_delete(self, projects_to_keep: List[str]) -> Iterable[str]:
        submissions_to_keep = reduce(lambda l1, l2: l1 + l2,
                                     [self.submissions_for_project(p) for p in projects_to_keep])
        analysis_submissions_to_keep = self.analysis_submissions_for_primary_submissions(ProjectCleanup.self_urls(submissions_to_keep), projects_to_keep)

        all_submissions = set(ProjectCleanup.self_urls(self.ingest_client.getSubmissions()))
        all_submissions_to_keep = set(submissions_to_keep + analysis_submissions_to_keep)
        submissions_to_delete = all_submissions.difference(all_submissions_to_keep)

        return submissions_to_delete

    def submissions_for_project(self, project_url: str):
        project = self.ingest_client.get(project_url).json()
        return list(self.ingest_client.get_related_entities("submissionEnvelopes", project, "submissionEnvelopes"))

    def analysis_submissions_to_keep(self, projects_to_keep: List[str]) -> List[str]:
        projects_to_keep_set = set(projects_to_keep)

        all_processes_url = f'{self.ingest_client.url}/processes'
        all_processes = self.ingest_client.get_all(all_processes_url, "processes")
        process_projects_maps = (dict(process=process,
                                      projects=set(self.projects_for_process(process)))
                                 for process in all_processes)

        # filter processes that refer to the projects to keep
        processes_to_keep = map(lambda process_project_map: process_project_map["process"],
                                filter(lambda process_project_map: process_project_map["projects"].issubset(projects_to_keep_set),
                                       process_projects_maps))

        # get submissions for those processes
        submissions_to_keep = [self.ingest_client.get_related_entities("submissionEnvelopes", process, "submissionEnvelopes")
                               for process in processes_to_keep]

        return ProjectCleanup.self_urls(submissions_to_keep)

    def analysis_submissions_for_primary_submissions(self, primary_submission_urls: List[str], projects_to_keep: Iterable[str]) -> List[str]:
        projects_to_keep_set = set(projects_to_keep)
        primary_submissions = [self.ingest_client.get_submission(s_url) for s_url in primary_submission_urls]
        primary_files = reduce(lambda g1, g2: chain(g1, g2),
                               (self.ingest_client.get_related_entities("files", p_sub, "files")
                                for p_sub in primary_submissions))

        potential_analysis_processes = reduce(lambda g1, g2: chain(g1, g2),
                                              (self.ingest_client.get_related_entities("inputToProcesses", f, "processes")
                                               for f in primary_files))

        analysis_processes = filter(lambda process: set(self.projects_for_process(process)).issubset(projects_to_keep_set),
                                    potential_analysis_processes)

        analysis_submissions = reduce(lambda g1, g2: chain(g1, g2),
                                      (self.ingest_client.get_related_entities("submissionEnvelopes", process, "submissionEnvelopes")
                                       for process in analysis_processes))

        return ProjectCleanup.self_urls(analysis_submissions)

    def projects_for_process(self, process: dict) -> List[str]:
        return [ProjectCleanup.self_url(p)
                for p in self.ingest_client.get_related_entities("projects", process, "projects")]

    @staticmethod
    def self_urls(entities: Iterable[dict]) -> List[str]:
        return [ProjectCleanup.self_url(e) for e in entities]

    @staticmethod
    def self_url(entity: dict) -> str:
        return entity["_links"]["self"]["href"]

    def cleanup(self, project_list: List[str]):
        pass

    def run(self, project_uuids_to_keep: List[str]):
        projects = [self.ingest_client.get_project_by_uuid(p_uuid) for p_uuid in project_uuids_to_keep]
        project_urls = [ProjectCleanup.self_url(p) for p in projects]
        submissions_to_delete = self.find_all_submissions_to_delete(project_urls)
        x = 1
