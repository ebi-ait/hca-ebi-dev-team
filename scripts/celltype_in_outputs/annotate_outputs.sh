# Create the celltype csvs for all available cell types
# Rscript create_celltype_csvs.R

# Create outputs
# Install requirements if needed
# pip3 install -r requirements.txt

# WongRetina - DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Atlas-Adult-Retina-10x/2020-Mar-Atlas-Adult-Retina-10x.loom \
# -h5 r-release_output_files/2020-Mar-Atlas-Adult-Retina-10x/2020-Mar-Atlas-Adult-Retina-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Atlas-Adult-Retina-10x/2020-Mar-Atlas-Adult-Retina-10x.scp.metadata.txt \
# -c celltype_csvs/WongRetinaCelltype.csv \
# -lp 10x

# BaderLiverLandscape - DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Landscape-Adult-Liver-10x/2020-Mar-Landscape-Adult-Liver-10x.loom \
# -h5 r-release_output_files/2020-Mar-Landscape-Adult-Liver-10x/2020-Mar-Landscape-Adult-Liver-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Landscape-Adult-Liver-10x/2020-Mar-Landscape-Adult-Liver-10x.scp.metadata.txt \
# -c celltype_csvs/BaderLiverLandscape-10x_cell_type_2020-03-10.csv \
# -lp 10x 

# TissueSensitivity 
# Lung
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Lung-10x.loom \
# -h5 r-release_output_files2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Lung-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Lung-10x.scp.metadata.txt \
# -c celltype_csvs/TissueSensitivity-Lung-10x_cell_type_2020-03-10.csv \
# -lp 10x 

# Spleen
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Sensitivity-Adult-Spleen-10x/2020-Mar-Sensitivity-Adult-Spleen-10x.loom \
# -h5 r-release_output_files2020-Mar-Sensitivity-Adult-Spleen-10x/2020-Mar-Sensitivity-Adult-Spleen-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Sensitivity-Adult-Spleen-10x/2020-Mar-Sensitivity-Adult-Spleen-10x.scp.metadata.txt \
# -c celltype_csvs/TissueSensitivity-Spleen-10x_cell_type_2020-03-10.csv \
# -lp 10x 

# Oesophagus
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Sensitivity-Adult-Esophagus-10x/2020-Mar-Sensitivity-Adult-Esophagus-10x.loom \
# -h5 r-release_output_files2020-Mar-Sensitivity-Adult-Esophagus-10x/2020-Mar-Sensitivity-Adult-Esophagus-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Sensitivity-Adult-Esophagus-10x/2020-Mar-Sensitivity-Adult-Esophagus-10x.scp.metadata.txt \
# -c celltype_csvs/TissueSensitivity-Oeso-10x_cell_type_2020-03-10.csv \
# -lp 10x 


# SpatioTemporalKidney
# Adult
python3 celltype_in_outputs.py \
-l r-release_output_files/2020-Mar-SpatioTemporal-Adult-Kidney-10x/2020-Mar-SpatioTemporal-Adult-Kidney-10x.loom \
-h5 r-release_output_files/2020-Mar-SpatioTemporal-Adult-Kidney-10x/2020-Mar-SpatioTemporal-Adult-Kidney-10x.seurat.h5ad \
-m r-release_output_files/2020-Mar-SpatioTemporal-Adult-Kidney-10x/2020-Mar-SpatioTemporal-Adult-Kidney-10x.scp.metadata.txt \
-c celltype_csvs/SpatioTemporalKidney-Adult-10x_cell_type_2020-03-10.csv \
-lp 10x \
-u abe1a013-af7a-45ed-8c26-f3793c24a1f4

# Fetal
python3 celltype_in_outputs.py \
-l r-release_output_files/2020-Mar-SpatioTemporal-Fetal-Kidney-10x/2020-Mar-SpatioTemporal-Fetal-Kidney-10x.loom \
-h5 r-release_output_files/2020-Mar-SpatioTemporal-Fetal-Kidney-10x/2020-Mar-SpatioTemporal-Fetal-Kidney-10x.seurat.h5ad \
-m r-release_output_files/2020-Mar-SpatioTemporal-Fetal-Kidney-10x/2020-Mar-SpatioTemporal-Fetal-Kidney-10x.scp.metadata.txt \
-c celltype_csvs/SpatioTemporalKidney-Fetal-10x_cell_type_2020-03-10.csv \
-lp 10x \
-u abe1a013-af7a-45ed-8c26-f3793c24a1f4