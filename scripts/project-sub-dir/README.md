# Moving files to project subdirectories

Per [DCP/2 MVP documentation](https://docs.google.com/document/d/1NsibP8g-NeLnksxlcBWQsSj5Zg_uimCDaAF1qB_qkjg/edit?ts=5ec6e28b&pli=1#heading=h.926y8csy88ms)
> For new DCP/2 datasets wrangled by EBI/UCSC, each project will be treated as one source and will have its own staging area. All staging areas for such projects appear in the staging bucket under a common folder. There is no requirement that all new datasets are segregated into one staging area per project.

> This will allow us to:
>    * start the import even when not all projects are exported yet
>    * import a small set and verify some things on the snapshot creation before doing everything
>    * easily exclude projects from snapshots which are not ready for analysis yet
>    * easily delete a project in the bucket

Example paths for ingest areas:
```
(dev) gs://broad-dsp-monster-hca-dev-ebi-staging/dev/<project-uuid>
(staging) gs://broad-dsp-monster-hca-dev-ebi-staging/staging/<project-uuid>
(prod) gs://broad-dsp-monster-hca-prod-ebi-storage/prod/<project-uuid>

```

GitHub Issue: ebi-ait/dcp-ingest-central#61

## Steps:
1. Use `scripts/spreadsheet-id-mapper/spreadsheet_id_mapper.py` to get the uuids of all contents of the projects
   ```
   $ python spreadsheet_id_mapper.py https://api.ingest.archive.data.humancellatlas.org/ dcp2_project_uuids.json
   ```
    This will output `mapping_<project_uuid>_<submission_uuid>` files.

1. Get all list of files in prod staging area
   ```
   gsutil ls -lr gs://broad-dsp-monster-hca-prod-ebi-storage/prod/ | awk '{if($3 != "")print $3}' > ls_staging_area.txt
   
   // remove last line (summary info)
   ```

1. Use the `scripts/map_ingest_uuid_to_staging_area/map_uuids_to_staging_area.py`  to get all the filepaths per project in staging area
   ```
   $ python map_uuids_to_staging_area.py <directory-of-mapping-files-from-step1> ls_staging_area.txt
   ```
    This will output `all_files_by_project.json` file.

     
1. Use the `all_files_by_project.json` as input to `scripts/project-sub-dir/move_files_to_project_dir.py`. 

   ```
   $ python move_files_to_project_dir.py all_files_by_project.json
   ```
   This will copy all the files to project subdirectories to a `prod2` directory in the staging area   
   
   This will also output `output.json` file, check for any errors. If there are any errors, fix it then just rerun if not successful.

1. Verify files in `prod2` directory

1. Rename staging area `prod` to `bak`

1. Rename staging area `prod2` to `prod`

1. Request for snapshot

1. Delete the `bak` after successful snapshot 

## Artifacts

All output files are found in AIT shared drive [AIT/HCA Ingest/Documentation/Operations/project-sub-dir](https://drive.google.com/drive/u/1/folders/1faEc9hwIYJCPPyL6d1DejP-Eegbq0XoW)   