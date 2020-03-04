# Rscript shebang

'''
R script that creates cell type csv files for all uuid matching files in "cell_barcode_uuid_matching/"
'''
# check if packages are installed, what is equivalent of requirements in R? if not installed then install
library(tidyverse)
library(readxl)

cell_types <- read_xlsx(read_xlsx("~/Google Drive File Stream/Shared drives/AIT/HCA - Wrangler tasks/r-Release/Cell type annotations/celltypes_annotated_harmonized_v2.xlsx",
                                          sheet = "deduped and harmonized"))
celltype_csv_output <- "celltype_csvs/"

create_celltype_csv <- function(harmonised_cell_terms_df,
                                uuid_matching_csv_path,
                                output_path){
  filtered_cell_types <- harmonised_cell_terms_df %>%
    select(inferred_cell_type = `CONTRIBUTOR'S INFERRED CELL IDENTITY`,
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
           barcode,
           annotated_cell_identity.text = harmonized_cell_type,
           annotated_cell_identity.ontology = ontology_terms,
           annotated_cell_identity.ontology_label = ontology_labels)
  
  write_csv(ontologised_cell_types,
            paste0(output_path, file_root, "_cell_type.csv"))
  #return(ontologised_cell_types)
}

matching_paths <- list.files("cell_barcode_uuid_matching/", full.names = T)

lapply(matching_paths, function(x) create_celltype_csv(cell_types, x, 
                                                       celltype_csv_output))

# to run for a single input 
# create_celltype_csv(cell_types, <matching_csv_path>, cell_types_output_path)
