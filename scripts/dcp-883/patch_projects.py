from hca_ingest.api.ingestapi import IngestApi
from assertpy import assert_that, soft_assertions

api_url = 'https://api.ingest.archive.data.humancellatlas.org'
new_schema = 'https://schema.data.humancellatlas.org/type/project/17.0.0/project'
token = 'your_token_here'

api = IngestApi(api_url)
api.set_token(f'Bearer {token}')

# Get and classify projects by schema version
target_projects = []
old_projects = []
new_projects = []
error_projects = []
all_projects = api.get_all(f'{api_url}/projects', 'projects')
for project in all_projects:
    schema = project.get('content', {}).get('describedBy', '')
    if schema:
        split_schema = schema.split('/')
        if len(split_schema) == 7:
            version = split_schema[5]
            split_version = version.split(".")
            if len(split_version) == 3:
                major_version = int(split_version[0])
                if major_version < 15:
                    old_projects.append(project)
                elif major_version > 16:
                    new_projects.append(project)
                else:
                    target_projects.append(project)
                continue
    error_projects.append(project)
print(f'Target Projects (v15 & v16): {len(target_projects)}, Old Projects (<15): {len(old_projects)}, New Projects (>16): {len(new_projects)}, Errors: {len(error_projects)}')

# the error project has no schema defined by so patching it now helps us in the future
target_projects.extend(error_projects)

# Print list of projects that cannot be patched
for project in target_projects:
    has_submission = project.get('hasOpenSubmission')
    if has_submission:
        print(f'UUID: {project.get("uuid", {}).get("uuid", "")} ShortName: {project.get("content", {}).get("project_core", {}).get("project_short_name", "")}, Wrangling State: {project.get("wranglingState", "")}')

# Patch Projects with new schema version
patched_projects = {}
error_projects = {}
skipped_projects = []
for project in target_projects:
    has_submission = project.get('hasOpenSubmission')
    if not has_submission:
        url = project.get('_links', {}).get('self', {}).get('href')
        if url not in patched_projects and url not in error_projects:
            patch = project.get('content')
            if url and patch:
                patch['describedBy'] = new_schema
                response = api.session.patch(url, json={'content': patch}, headers=api.get_headers())
                if response.ok:
                    patched_project = response.json()
                    patched_projects[url] = patched_project
                else:
                    error_projects[url] = response.content
            else:
                skipped_projects.append(project)
api.session.cache.clear()
print(f'Patched Projects: {len(patched_projects)}, Error Project: {len(error_projects)}, Skipped Projects: {len(skipped_projects)}')

# Assert project content and validationState matched before and after
with soft_assertions():
    for project in target_projects:
        url = project.get('_links', {}).get('self', {}).get('href')
        if url in patched_projects:
            patched_project = patched_projects.get(url)
            assert_that(project).is_equal_to(patched_project, include=['content','validationState'])

# Print Errors
for url, error in error_projects.items():
    print(f'link: {url} Error: {error}')
