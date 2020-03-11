# Cell type in outputs repo

This repo contains files and scripts that were used to annotate loom, h5ad and metadata files as part of the March 2020 HCA mini-release. The outputted files were then uploaded to the relevant project on the [Single Cell Portal](https://singlecell.broadinstitute.org/single_cell?scpbr=human-cell-atlas-march-2020-release) 

## Scripts

### `annotate_outputs.sh`

A run through script to show how the scripts are run to create outputs.

### `create_celltype_csvs.R`

Creates the 'celltype csvs' required for each dataset by `celltypes_in_outputs.py` by using files in the `cell_barcode_uuid_matching` directory. One cell type csv is created per file in this directory. Inputs are the barcode uuid matching file and the harmonised celltype file. It adds the columns `annotated_cell_type.text`, `annotated_cell_type.ontology` and `annotated_cell_type.ontology_label` to the barcode-uuid matching file.

### `celltypes_in_outputs.py`

This script creates updated loom, h5ad and metadata.txt files based on inputs. Usage and functions are documented within the code file.

### `requirements.txt`

Required packages for the `celltypes_in_outputs.py` script to run.

## Directories

### cell_barcode_uuid_matching

Contains csvs that contain matching between the contributor given cell type, some hca biomaterial id and the associated hca biomaterial uuid.

### celltype_csvs

Contains celltype csvs that are created as a result of running the `create_celltype_csvs.R` script.

### config_files
Directory that contains files required by the `celltypes_in_outputs.py` script.
