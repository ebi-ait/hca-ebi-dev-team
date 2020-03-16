"""
celltypes_in_outputs.py

This script will be used to edit loom, h5ad and metadata output files from the cumulus pipeline.

The aim is to add the cell type annotations from publications into the matrix and metadata files

--celltype_csv is a csv with required columns:
    - biomaterial uuid such as 'cell_suspension.provenance.document_id'
    - 'barcode': the nucelotide string barcode (if 10X)
    - biomaterial local id such as 'cell_suspension.biomaterial_core.biomaterial_id'
    - annotated_cell_identity.text: The name the contributor gave the cell type
    - annotated_cell_identity.ontology: The ontology curie for the curated cell type
    - annotated_cell_identity.ontology_label: The ontology label for the curated cell type
--loom_file: The path to the original loom file
--h5ad_file: The path to the original h5ad file
--metadata_file: The path to the metadata txt file

The script also requires a whitelist text file that identifies the columns that should be retained in the metadata txt
file and thus will be shown to users as options for annotation in the 'explore' part of the SCP.

Author: Marion Shadbolt, mshadbolt@ebi.ac.uk
Last updated: 2020-03-14

"""


import loompy as lp
import scanpy as sc
import pandas as pd
import argparse
import subprocess
import sys
import requests as rq


def main():
    parser = define_parser()
    args = parser.parse_args()
    cell_type_df = pd.read_csv(args.celltype_csv)
    with lp.connect(args.input_loom) as ds:
        loom_cols = set(ds.ca.keys())
    # Figure out which biomaterial type used as identifier
    shared_columns = list(loom_cols.intersection(set(cell_type_df.columns)))
    # print(shared_columns)
    id_column = [i for i in shared_columns if "id" in i][0]
    biomaterial_id_type = id_column.split(".")[0]
    with lp.connect(args.input_loom) as ds:
        biomaterial_uuids = set(ds.ca[f"{biomaterial_id_type}.provenance.document_id"])
    # Make input dictionaries
    local_id_dict = make_local_id_dict(biomaterial_id_type, cell_type_df, biomaterial_uuids)
    this_ct_dict = create_cell_type_dictionary(cell_type_df, id_column, biomaterial_id_type, args.lib_prep)
    # ct_dict_df = pd.DataFrame.from_dict(this_ct_dict, orient="index")
    # ct_dict_df.to_csv("~/Desktop/test_ct_dict.csv")

    # Update the files
    update_loom_file(args.input_loom, this_ct_dict, id_column, biomaterial_id_type, local_id_dict, args.lib_prep,
                     args.project_uuid)
    update_metadata_txt(args.input_metadata, cell_type_df, biomaterial_id_type, local_id_dict, args.lib_prep)
    update_h5ad_file(args.input_h5ad, cell_type_df, biomaterial_id_type, local_id_dict, args.lib_prep,
                     args.project_uuid)


# TODO: work out how to upload original files to s3 bucket after creating annotated versions
# TODO: work out how to upload to portal automatically?

def define_parser():
    """defines the parser to parse command line arguments"""
    parser = argparse.ArgumentParser(description="Parser for the arguments")
    parser.add_argument("--celltype_csv", "-c", action="store", dest="celltype_csv", type=str,
                        help="Path to input csv with cell type annotations, expected columns are:")
    parser.add_argument("--loom_file", "-l", action="store", dest="input_loom", type=str,
                        help="Path to the input loom file that needs to be edited")
    parser.add_argument("--h5ad_file", "-h5", action="store", dest="input_h5ad", type=str,
                        help="path to the input h5ad file that needs to be edited")
    parser.add_argument("--metadata_file", "-m", action="store", dest="input_metadata", type=str,
                        help="path to the input metadata txt file")
    parser.add_argument("--lib-prep", "-lp", action="store", dest="lib_prep", type=str,
                        choices=["10x", "10X", "ss2", "SS2"],
                        help="Library prep type, either '10x' or 'SS2'")
    parser.add_argument("--project-uuid", "-u", action="store", dest="project_uuid", type=str,
                        help="Optional: The project uuid a.k.a. 'project.provenance.document_id'",
                        nargs='?')
    return parser


def create_cell_type_dictionary(cell_type_df, id_field, id_type, library_prep):
    """
    Creates a cell type dictionary that links each barcoded cell to its annotated cell type.

    :param cell_type_df: pandas dataframe containing cell type annotations
    :param id_field: the name of the field that contains the uuid of the biomaterial
    :param id_type: the type of identified biomaterial
    :param library_prep: the type of library either 10x or SS2
    :return: A dictionary with barcode and uuid as the keys and a list with
             biomaterial local id
             annotated_cell_identity.text
             annotated_cell_identity.ontology
             annotated_cell_identity.ontology_label
    """
    cell_type_dict = {}
    biomaterial_id = id_type + ".biomaterial_core.biomaterial_id"
    if library_prep.lower() == "10x":
        for index, row in cell_type_df.iterrows():
            if (row['barcode'], row[id_field]) in cell_type_dict:
                print("Cell in Dictionary")
                print(row['barcode'])
                print(row[id_field])
                print(row['barcode'] + " " + row[id_field])
            cell_id = row["barcode"] + "-" + row[id_field]
            cell_type_dict[cell_id] = [row[biomaterial_id], row['annotated_cell_identity.text'],
                                                               row['annotated_cell_identity.ontology'],
                                                               row['annotated_cell_identity.ontology_label']]
    elif library_prep.lower() == "ss2":
        for index, row in cell_type_df.iterrows():
            cell_type_dict[row[id_field]] = [row[biomaterial_id], row['annotated_cell_identity.text'],
                                             row['annotated_cell_identity.ontology'],
                                             row['annotated_cell_identity.ontology_label']]
    return cell_type_dict


def get_cell_type(cell_identifier, biomaterial_uuid, ct_dict, local_id_dict):
    """
    Given cell barcode and biomaterial uuid, returns the list of biomaterial local id and cell type annotations
    :param cell_identifier should be cell_suspension.provenance.document_id for ss2 or a tuple of the cell barcode and
    the <biomaterial_type>.provenance.document_id for 10x experiments.
    """
    try:
        cell_type = ct_dict[cell_identifier]
    except KeyError:
        cell_type = [local_id_dict[biomaterial_uuid], "unannotated", "unannotated", "unannotated"]
    return cell_type


def make_local_id_dict(biomaterial_type, cell_type_df, uuids):
    """Makes a dictionary to match biomaterial uuids to local ids."""
    local_id_field = biomaterial_type + ".biomaterial_core.biomaterial_id"
    uuid_field = biomaterial_type + ".provenance.document_id"
    group_dict = cell_type_df.groupby([uuid_field, local_id_field])
    local_id_dict = {}
    for item in group_dict.groups.keys():
        local_id_dict[item[0]] = item[1]
    # check all biomaterial uuids in the loom file are also in the local_id_dict
    missing_uuids = uuids.difference(set(local_id_dict.keys()))
    if len(missing_uuids) > 0:
        print(missing_uuids)
        for uuid in missing_uuids:
            api_url = f"https://dss.data.humancellatlas.org/v1/files/{uuid}?replica=aws"
            print(f"Biomaterial not found in annotations, Getting biomaterial id from DSS API: {api_url}")
            response = rq.get(api_url)
            response_json = response.json()
            local_id_dict[uuid] = response_json['biomaterial_core']['biomaterial_id']
    return local_id_dict


def get_project_info(project_uuid):
    proj_info_df = pd.read_csv("config_files/project_info_mapping.csv")
    proj_row = proj_info_df[proj_info_df['project.provenance.document_id'] == project_uuid]
    short_name = proj_row.iloc[0]['project.project_core.project_short_name']
    project_title = proj_row.iloc[0]['project.project_core.project_title']
    return [short_name, project_title]


def update_metadata_txt(metadata_path, annotation_df, id_type, local_id_dict, library_prep):
    """
    Takes as input the cell type annotation file and the metadata file, filters the metadata file to the agreed upon
    columns in the whitelist file and adds the cell type annotation and local biomaterial id columns.

    :param metadata_path:
    :param annotation_df:
    :param id_type: the type of bioamterial
    :param local_id_dict: the dictionary linking local ids to uuids
    :return:
    """

    id_field = id_type + ".provenance.document_id"
    local_id_field = id_type + ".biomaterial_core.biomaterial_id"

    # read in the existing metadata file and merge with new annotations
    metadata_txt = pd.read_table(metadata_path)
    if library_prep.lower() == "10x":
        annotated_metadata_txt = pd.merge(metadata_txt, annotation_df, on=["barcode", id_field], how="left",
                                          validate="one_to_one")
        with open("config_files/10x_column_whitelist.txt") as whitelist:
            contents = whitelist.read()
            white_list = contents.splitlines()
            numeric_fields = ["total_umis", "genes_detected"]
    elif library_prep.lower() == "ss2":
        annotated_metadata_txt = pd.merge(metadata_txt, annotation_df, on=[id_field], how="left",
                                          validate="one_to_one")
        with open("config_files/ss2_column_whitelist.txt") as whitelist:
            contents = whitelist.read()
            white_list = contents.splitlines()
            numeric_fields = ["genes_detected"]

    # fill in 'group' labels on new columns in first row
    category_row = annotated_metadata_txt.xs(0)
    null_values = annotated_metadata_txt.xs(0).isnull()
    category_row[null_values] = "group"
    annotated_metadata_txt.loc[0] = category_row

    # change category to numeric for numeric fields
    annotated_metadata_txt.loc[0][numeric_fields] = "numeric"

    # fill in missing biomaterial local ids
    uuid_col = annotated_metadata_txt.xs(id_field, axis=1)
    local_id_dict["group"] = "group"
    biomaterial_local_ids = []
    for uuid in uuid_col:
        biomaterial_local_ids.append(local_id_dict[uuid])
    annotated_metadata_txt[local_id_field] = biomaterial_local_ids

    # fill in missing cell annotations with 'unannotated'
    annotated_metadata_txt.loc[annotated_metadata_txt["annotated_cell_identity.text"].isna(),
                               ["annotated_cell_identity.text", "annotated_cell_identity.ontology_label"]] = "unannotated"

    # filter to the reduced list of annotation columns
    both = set(white_list).intersection(set(annotated_metadata_txt.columns))
    white_list_indices = [white_list.index(x) for x in both]
    white_list_indices.sort()
    white_list = [white_list[i] for i in white_list_indices]
    annotated_metadata_txt = annotated_metadata_txt[white_list]

    output_txt = metadata_path.split(".")[0] + "_annotated_v1.scp.metadata.txt"
    annotated_metadata_txt.to_csv(output_txt, sep="\t", index=False)
    print("Updated metadata txt file saved to " + output_txt)


def update_loom_file(loom_path, ct_dict, id_field, id_type, local_id_dict, library_prep, project_uuid=None):
    """
    Takes as input the cell type annotation file and the loom path. The script copies the loom before updating the loom
    file with the cell type annotation.

    :param loom_path: path to the loom file that needs to be updated
    :param ct_dict: output from create_cell_type_dictionary
    :param id_field: the field name in the dict that was used to match barcode to biomaterial
    :param id_type: the type of biomaterial, i.e. donor_organism, cell_suspension etc.
    :param local_id_dict: a dict with biomaterial uuids as keys and local ids as items created by make_local_id_dict
    :param library_prep: the library prep type, either 10x or ss2
    :return: void function that copies the loom file and edits the copy in place
    """
    biomaterial_id = id_type + ".biomaterial_core.biomaterial_id"
    annotated_loom = loom_path.split(".")[0] + "_annotated_v1.loom"
    subprocess.run(["cp", loom_path, annotated_loom])
    celltype_text_list = []
    celltype_ontology_list = []
    celltype_ontology_label_list = []
    biomaterial_id_list = []
    with lp.connect(annotated_loom) as ds:
        for i in range(ds.shape[1]):
            if library_prep.lower() == "10x":
                cell_id = ds.ca["barcode"][i] + "-" + ds.ca[id_field][i]
                # print(cell_id)
                annotation_row = get_cell_type(cell_id, ds.ca[id_field][i], ct_dict, local_id_dict)
                # print(annotation_row)
            elif library_prep.lower() == "ss2":
                annotation_row = get_cell_type(ds.ca[id_field][i], ds.ca[id_field][i], ct_dict, local_id_dict)
            else:
                print("lib prep not found")
                sys.exit()
            biomaterial_id_list.append(annotation_row[0])
            if annotation_row[1] != annotation_row[1]: # check for nan value
                celltype_text_list.append("unannotated")
                celltype_ontology_list.append("unannotated")
                celltype_ontology_label_list.append("unannotated")
            else:
                celltype_text_list.append(annotation_row[1])
                celltype_ontology_list.append(annotation_row[2])
                celltype_ontology_label_list.append(annotation_row[3])
        ds.ca["annotated_cell_identity.text"] = celltype_text_list
        ds.ca["annotated_cell_identity.ontology"] = celltype_ontology_list
        ds.ca["annotated_cell_identity.ontology_label"] = celltype_ontology_label_list
        ds.ca[biomaterial_id] = biomaterial_id_list
        try:
            this_project_uuid = ds.ca["project.provenance.document_id"][0]
        except AttributeError:
            print("Project uuid not found, using " + project_uuid)
            this_project_uuid = project_uuid
        project_info = get_project_info(this_project_uuid)
        print(project_info)
        ds.ca["project.project_core.project_title"] = [project_info[1]] * ds.shape[1]
        ds.ca["project.project_core.project_short_name"] = [project_info[0]] * ds.shape[1]
    print("Updated loom file saved to " + annotated_loom)
    with lp.connect(annotated_loom) as ds:
        annotated_cell_types = set(ds.ca["annotated_cell_identity.text"])
        annotated_cell_labels = set(ds.ca["annotated_cell_identity.ontology_label"])
        annotated_cell_ontologies = set(ds.ca["annotated_cell_identity.ontology"])
    print("annotated cell type set: " + str(annotated_cell_types))
    print("annotated cell labels set: " + str(annotated_cell_labels))
    print("annotated cell ontologies set: " + str(annotated_cell_ontologies))


def update_h5ad_file(h5ad_path, annotation_df, id_type, local_id_dict, library_prep, project_uuid=None):
    """
    Takes as input the cell type annotation file and the h5ad path. The function saves a new copy of the h5ad file.

    :param h5ad_path: Path to the h5ad file to be updated
    :param annotation_df: The dataframe that contains ontologised cell type annotations
    :param id_type: The type of biomaterial
    :param local_id_dict: the dictionary that links the biomaterial uuid to it's local id

    """
    id_field = id_type + ".provenance.document_id"
    local_id_field = id_type + ".biomaterial_core.biomaterial_id"
    h5_object = sc.read(h5ad_path)
    output_h5 = h5ad_path.split(".")[0] + "_annotated_v1.seurat.h5ad"
    original_indices = h5_object.obs.index

    # join the annData obs dataframe to the annotated cell type
    if library_prep.lower() == "10x":
        annotated_obs = pd.merge(h5_object.obs, annotation_df, on=[id_field, 'barcode'],
                                 how="left", left_index=True, validate="one_to_one")
    elif library_prep.lower() == "ss2":
        annotated_obs = pd.merge(h5_object.obs, annotation_df, on=[id_field],
                                 how="left", left_index=True, validate="one_to_one")

    annotated_obs.index = original_indices # double check order remains the same after the merge

    # fill in missing biomaterial local ids
    uuid_col = annotated_obs.xs(id_field, axis=1)
    biomaterial_local_ids = []
    for uuid in uuid_col:
        biomaterial_local_ids.append(local_id_dict[uuid])
    annotated_obs[local_id_field] = biomaterial_local_ids

    # fill in missing cell annotations with 'unannotated'
    annotated_obs.loc[annotated_obs["annotated_cell_identity.text"].isna(),
                                   ["annotated_cell_identity.text",
                                    "annotated_cell_identity.ontology_label",
                                    "annotated_cell_identity.ontology"]] = "unannotated"
    try:
        this_project_uuid = annotated_obs["project.provenance.document_id"][0]
    except KeyError:
        print("Project uuid not found, using " + project_uuid)
        this_project_uuid = project_uuid
    project_info = get_project_info(this_project_uuid)
    annotated_obs["project.project_core.project_short_name"] = project_info[0]
    annotated_obs["project.project_core.project_title"] = project_info[1]

    h5_object.obs = annotated_obs
    h5_object.write_h5ad(output_h5)
    print("Updated h5ad file updated and written to " + output_h5)


if __name__ == "__main__":
    main()
