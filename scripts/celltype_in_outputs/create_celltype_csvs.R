#! /usr/local/bin/Rscript

# R script that creates cell type csv files for all uuid matching files in "cell_barcode_uuid_matching/"
# check if packages are installed, what is equivalent of requirements in R? if not installed then install
if (!require("readr")) install.packages("readr")
if (!require("dplyr")) install.packages("dplyr")
if (!require("stringr")) install.packages("stringr")
if (!require("readxl")) install.packages("readxl")
library(readr)
library(dplyr)
library(stringr)
library(readxl)

cell_types <- read_csv("~/Google Drive File Stream/Shared drives/AIT/HCA - Wrangler tasks/r-Release/Cell type annotations/celltypes_annotated_harmonized_v3.csv")
celltype_csv_output <- "celltype_csvs/"

create_celltype_csv <- function(harmonised_cell_terms_df,
                                uuid_matching_csv_path,
                                output_path){
  filtered_cell_types <- harmonised_cell_terms_df %>%
    select(inferred_cell_type,
           harmonized_cell_type = `HARMONIZED CELL IDENTITY`, 
           ontology_labels = `ONTOLOGY TERM LABEL(S)`,
           ontology_terms = `ONTOLOGY TERM(S)`) %>%
    mutate(ontology_labels = str_replace_all(ontology_labels, " \\|\\| ", "||"),
           ontology_terms = str_replace_all(ontology_terms, " \\|\\| ", "||"),
           ontology_terms = str_replace_all(ontology_terms, "_", ":"))
  
  uuid_matching_df <- read_csv(uuid_matching_csv_path)
  
  filename = str_split(uuid_matching_csv_path, "/", simplify = T)[length(str_split(uuid_matching_csv_path, "/", simplify = T))]
  
  file_root <- str_split(filename, "_cell_barcode",
                         simplify = T)[1]
  message(paste0(output_path, file_root, "_cell_type.csv"))
  
  ontologised_cell_types <- uuid_matching_df %>%
    left_join(filtered_cell_types) %>%
    select(ends_with("_id"),
           annotated_cell_identity.text = harmonized_cell_type,
           annotated_cell_identity.ontology = ontology_terms,
           annotated_cell_identity.ontology_label = ontology_labels,
           any_of("barcode"))
  
  write_csv(ontologised_cell_types,
            paste0(output_path, file_root, "_cell_type_", Sys.Date(), ".csv"))
  #return(ontologised_cell_types)
}

matching_paths <- list.files("cell_barcode_uuid_matching/", full.names = T, 
                             pattern = ".csv")
print(matching_paths)
lapply(matching_paths, function(x) create_celltype_csv(cell_types, x,
                                                       celltype_csv_output))

# to run for a single input 
# create_celltype_csv(cell_types, <matching_csv_path>, cell_types_output_path)
