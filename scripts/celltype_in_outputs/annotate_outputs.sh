# Create the celltype csvs for all available cell types
# Rscript create_celltype_csvs.R

# Create outputs
# Install requirements if needed
# pip3 install -r requirements.txt

# WongRetina - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Atlas-Adult-Retina-10x/2020-Mar-Atlas-Adult-Retina-10x.loom \
# -h5 r-release_output_files/2020-Mar-Atlas-Adult-Retina-10x/2020-Mar-Atlas-Adult-Retina-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Atlas-Adult-Retina-10x/2020-Mar-Atlas-Adult-Retina-10x.scp.metadata.txt \
# -c celltype_csvs/WongRetinaCelltype.csv \
# -lp 10x
# rsync -r r-release_output_files/2020-Mar-Atlas-Adult-Retina-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms
# rm r-release_output_files/2020-Mar-Atlas-Adult-Retina-10x/2020-Mar-Atlas-Adult-Retina-10x.loom 
# rm r-release_output_files/2020-Mar-Atlas-Adult-Retina-10x/2020-Mar-Atlas-Adult-Retina-10x.seurat.h5ad

# BaderLiverLandscape - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Landscape-Adult-Liver-10x/2020-Mar-Landscape-Adult-Liver-10x.loom \
# -h5 r-release_output_files/2020-Mar-Landscape-Adult-Liver-10x/2020-Mar-Landscape-Adult-Liver-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Landscape-Adult-Liver-10x/2020-Mar-Landscape-Adult-Liver-10x.scp.metadata.txt \
# -c celltype_csvs/BaderLiverLandscape-10x_cell_type_2020-03-10.csv \
# -lp 10x 
# rsync -r r-release_output_files/2020-Mar-Landscape-Adult-Liver-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# TissueSensitivity 
# Lung - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Lung-10x.loom \
# -h5 r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Lung-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Lung-10x.scp.metadata.txt \
# -c celltype_csvs/TissueSensitivity-Lung-10x_cell_type_2020-03-12.csv \
# -lp 10x \
# -u c4077b3c-5c98-4d26-a614-246d12c2e5d7
# 
# rsync -r r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms
# rm r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Lung-10x.loom


# Spleen - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Sensitivity-Adult-Spleen-10x/2020-Mar-Sensitivity-Adult-Spleen-10x.loom \
# -h5 r-release_output_files/2020-Mar-Sensitivity-Adult-Spleen-10x/2020-Mar-Sensitivity-Adult-Spleen-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Sensitivity-Adult-Spleen-10x/2020-Mar-Sensitivity-Adult-Spleen-10x.scp.metadata.txt \
# -c celltype_csvs/TissueSensitivity-Spleen-10x_cell_type_2020-03-12.csv \
# -lp 10x \
# -u c4077b3c-5c98-4d26-a614-246d12c2e5d7
# rsync -r r-release_output_files/2020-Mar-Sensitivity-Adult-Spleen-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms
# rm r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Spleen-10x.loom

# Oesophagus - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Sensitivity-Adult-Esophagus-10x/2020-Mar-Sensitivity-Adult-Esophagus-10x.loom \
# -h5 r-release_output_files/2020-Mar-Sensitivity-Adult-Esophagus-10x/2020-Mar-Sensitivity-Adult-Esophagus-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Sensitivity-Adult-Esophagus-10x/2020-Mar-Sensitivity-Adult-Esophagus-10x.scp.metadata.txt \
# -c celltype_csvs/TissueSensitivity-Oeso-10x_cell_type_2020-03-12.csv \
# -lp 10x \
# -u c4077b3c-5c98-4d26-a614-246d12c2e5d7
# rsync -r r-release_output_files/2020-Mar-Sensitivity-Adult-Esophagus-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms
# rm r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Esophagus-10x.loom

# rm r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Lung-10x_annotated_v1.loom
# rm r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Spleen-10x_annotated_v1.loom
# rm r-release_output_files/2020-Mar-Sensitivity-Adult-Lung-10x/2020-Mar-Sensitivity-Adult-Esophagus-10x_annotated_v1.loom

# SpatioTemporalKidney
# Adult  - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-SpatioTemporal-Adult-Kidney-10x/2020-Mar-SpatioTemporal-Adult-Kidney-10x.loom \
# -h5 r-release_output_files/2020-Mar-SpatioTemporal-Adult-Kidney-10x/2020-Mar-SpatioTemporal-Adult-Kidney-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-SpatioTemporal-Adult-Kidney-10x/2020-Mar-SpatioTemporal-Adult-Kidney-10x.scp.metadata.txt \
# -c celltype_csvs/SpatioTemporalKidney-Adult-10x_cell_type_2020-03-11.csv \
# -lp 10x \
# -u abe1a013-af7a-45ed-8c26-f3793c24a1f4
# rsync -r r-release_output_files/2020-Mar-SpatioTemporal-Adult-Kidney-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# Fetal  - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-SpatioTemporal-Fetal-Kidney-10x/2020-Mar-SpatioTemporal-Fetal-Kidney-10x.loom \
# -h5 r-release_output_files/2020-Mar-SpatioTemporal-Fetal-Kidney-10x/2020-Mar-SpatioTemporal-Fetal-Kidney-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-SpatioTemporal-Fetal-Kidney-10x/2020-Mar-SpatioTemporal-Fetal-Kidney-10x.scp.metadata.txt \
# -c celltype_csvs/SpatioTemporalKidney-Fetal-10x_cell_type_2020-03-11.csv \
# -lp 10x \
# -u abe1a013-af7a-45ed-8c26-f3793c24a1f4
# rsync -r r-release_output_files/2020-Mar-SpatioTemporal-Fetal-Kidney-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# Immune cell Atlas
# Blood   - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Census-Adult-Blood-10x/2020-Mar-Census-Adult-Blood-10x.loom \
# -h5 r-release_output_files/2020-Mar-Census-Adult-Blood-10x/2020-Mar-Census-Adult-Blood-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Census-Adult-Blood-10x/2020-Mar-Census-Adult-Blood-10x.scp.metadata.txt \
# -c celltype_csvs/CensusImmune-CordBlood-10x_cell_type_2020-03-12.csv \
# -lp 10x \
# -u cc95ff89-2e68-4a08-a234-480eca21ce79
# rsync -r r-release_output_files/2020-Mar-Census-Adult-Blood-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# Immune  - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Census-Adult-Immune-10x/2020-Mar-Census-Adult-Immune-10x.loom \
# -h5 r-release_output_files/2020-Mar-Census-Adult-Immune-10x/2020-Mar-Census-Adult-Immune-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Census-Adult-Immune-10x/2020-Mar-Census-Adult-Immune-10x.scp.metadata.txt \
# -c celltype_csvs/CensusImmune-BoneMarrow-10x_cell_type_2020-03-12.csv \
# -lp 10x \
# -u cc95ff89-2e68-4a08-a234-480eca21ce79
# rsync -r r-release_output_files/2020-Mar-Census-Adult-Immune-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# Fetal Maternal Interface - DONE
# Blood 10x  - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-FetalMaternal-Adult-Blood-10x/2020-Mar-FetalMaternal-Adult-Blood-10x.loom \
# -h5 r-release_output_files/2020-Mar-FetalMaternal-Adult-Blood-10x/2020-Mar-FetalMaternal-Adult-Blood-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-FetalMaternal-Adult-Blood-10x/2020-Mar-FetalMaternal-Adult-Blood-10x.scp.metadata.txt \
# -c celltype_csvs/FetalMaternal-Blood-10x_cell_type_2020-03-12.csv \
# -lp 10x \
# -u f83165c5-e2ea-4d15-a5cf-33f3550bffde
# rsync -r r-release_output_files/2020-Mar-FetalMaternal-Adult-Blood-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# Blood SS2  - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-FetalMaternal-Adult-Blood-SS2/2020-Mar-FetalMaternal-Adult-Blood-SS2.loom \
# -h5 r-release_output_files/2020-Mar-FetalMaternal-Adult-Blood-SS2/2020-Mar-FetalMaternal-Adult-Blood-SS2.seurat.h5ad \
# -m r-release_output_files/2020-Mar-FetalMaternal-Adult-Blood-SS2/2020-Mar-FetalMaternal-Adult-Blood-SS2.scp.metadata.txt \
# -c celltype_csvs/FetalMaternal-Blood-SS2_cell_type_2020-03-12.csv \
# -lp SS2 \
# -u f83165c5-e2ea-4d15-a5cf-33f3550bffde
# rsync -r r-release_output_files/2020-Mar-FetalMaternal-Adult-Blood-SS2/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# Decidua 10x  - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-FetalMaternal-Adult-Decidua-10x/2020-Mar-FetalMaternal-Adult-Decidua-10x.loom \
# -h5 r-release_output_files/2020-Mar-FetalMaternal-Adult-Decidua-10x/2020-Mar-FetalMaternal-Adult-Decidua-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-FetalMaternal-Adult-Decidua-10x/2020-Mar-FetalMaternal-Adult-Decidua-10x.scp.metadata.txt \
# -c celltype_csvs/FetalMaternal-Decidua-10x_cell_type_2020-03-12.csv \
# -lp 10x \
# -u f83165c5-e2ea-4d15-a5cf-33f3550bffde
# rsync -r r-release_output_files/2020-Mar-FetalMaternal-Adult-Decidua-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# Decidua SS2  - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-FetalMaternal-Adult-Decidua-SS2/2020-Mar-FetalMaternal-Adult-Decidua-SS2.loom \
# -h5 r-release_output_files/2020-Mar-FetalMaternal-Adult-Decidua-SS2/2020-Mar-FetalMaternal-Adult-Decidua-SS2.seurat.h5ad \
# -m r-release_output_files/2020-Mar-FetalMaternal-Adult-Decidua-SS2/2020-Mar-FetalMaternal-Adult-Decidua-SS2.scp.metadata.txt \
# -c celltype_csvs/FetalMaternal-decidua-SS2_cell_type_2020-03-12.csv \
# -lp SS2 \
# -u f83165c5-e2ea-4d15-a5cf-33f3550bffde
# rsync -r r-release_output_files/2020-Mar-FetalMaternal-Adult-Decidua-SS2/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# Placenta 10x  - RE-DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-FetalMaternal-Fetal-Placenta-10x/2020-Mar-FetalMaternal-Fetal-Placenta-10x.loom \
# -h5 r-release_output_files/2020-Mar-FetalMaternal-Fetal-Placenta-10x/2020-Mar-FetalMaternal-Fetal-Placenta-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-FetalMaternal-Fetal-Placenta-10x/2020-Mar-FetalMaternal-Fetal-Placenta-10x.scp.metadata.txt \
# -c celltype_csvs/FetalMaternal-Placenta-10x_cell_type_2020-03-12.csv \
# -lp 10x \
# -u f83165c5-e2ea-4d15-a5cf-33f3550bffde
# rsync -r r-release_output_files/2020-Mar-FetalMaternal-Fetal-Placenta-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# HumanHematopoieticProfiling - DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Profiling-Adult-BoneMarrow-10x/2020-Mar-Profiling-Adult-BoneMarrow-10x.loom \
# -h5 r-release_output_files/2020-Mar-Profiling-Adult-BoneMarrow-10x/2020-Mar-Profiling-Adult-BoneMarrow-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Profiling-Adult-BoneMarrow-10x/2020-Mar-Profiling-Adult-BoneMarrow-10x.scp.metadata.txt \
# -c celltype_csvs/HaematopoieticProfiling-10x_cell_type_2020-03-12.csv \
# -lp 10x
# rsync -r r-release_output_files/2020-Mar-Profiling-Adult-BoneMarrow-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# # T cell activation
# ## Blood -DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Tcell-Adult-Blood-10x/2020-Mar-Tcell-Adult-Blood-10x.loom \
# -h5 r-release_output_files/2020-Mar-Tcell-Adult-Blood-10x/2020-Mar-Tcell-Adult-Blood-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Tcell-Adult-Blood-10x/2020-Mar-Tcell-Adult-Blood-10x.scp.metadata.txt \
# -c celltype_csvs/TCellActivation-Blood-10x_cell_type_2020-03-11.csv \
# -lp 10x \
# -u 4a95101c-9ffc-4f30-a809-f04518a23803
# rsync -r r-release_output_files/2020-Mar-Tcell-Adult-Blood-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# ## Bone Marrow -DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Tcell-Adult-BoneMarrow-10x/2020-Mar-Tcell-Adult-BoneMarrow-10x.loom \
# -h5 r-release_output_files/2020-Mar-Tcell-Adult-BoneMarrow-10x/2020-Mar-Tcell-Adult-BoneMarrow-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Tcell-Adult-BoneMarrow-10x/2020-Mar-Tcell-Adult-BoneMarrow-10x.scp.metadata.txt \
# -c celltype_csvs/TCellActivation-bone-marrow-10x_cell_type_2020-03-11.csv \
# -lp 10x \
# -u 4a95101c-9ffc-4f30-a809-f04518a23803
# rsync -r r-release_output_files/2020-Mar-Tcell-Adult-BoneMarrow-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# ## Lung -DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Tcell-Adult-Lung-10x/2020-Mar-Tcell-Adult-Lung-10x.loom \
# -h5 r-release_output_files/2020-Mar-Tcell-Adult-Lung-10x/2020-Mar-Tcell-Adult-Lung-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Tcell-Adult-Lung-10x/2020-Mar-Tcell-Adult-Lung-10x.scp.metadata.txt \
# -c celltype_csvs/TCellActivation-lung-10x_cell_type_2020-03-11.csv \
# -lp 10x \
# -u 4a95101c-9ffc-4f30-a809-f04518a23803
# rsync -r r-release_output_files/2020-Mar-Tcell-Adult-Lung-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# ## LymphNode -DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Tcell-Adult-LymphNode-10x/2020-Mar-Tcell-Adult-LymphNode-10x.loom \
# -h5 r-release_output_files/2020-Mar-Tcell-Adult-LymphNode-10x/2020-Mar-Tcell-Adult-LymphNode-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Tcell-Adult-LymphNode-10x/2020-Mar-Tcell-Adult-LymphNode-10x.scp.metadata.txt \
# -c celltype_csvs/TCellActivation-lymph-node-10x_cell_type_2020-03-11.csv \
# -lp 10x \
# -u 4a95101c-9ffc-4f30-a809-f04518a23803
# rsync -r r-release_output_files/2020-Mar-Tcell-Adult-LymphNode-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# Somatic pancreas
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Somatic-Adult-Pancreas-SS2/2020-Mar-Somatic-Adult-Pancreas-SS2.loom \
# -h5 r-release_output_files/2020-Mar-Somatic-Adult-Pancreas-SS2/2020-Mar-Somatic-Adult-Pancreas-SS2.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Somatic-Adult-Pancreas-SS2/2020-Mar-Somatic-Adult-Pancreas-SS2.scp.metadata.txt \
# -c celltype_csvs/scPancreas-SS2_cell_type_2020-03-11.csv \
# -lp SS2 
# rsync -r r-release_output_files/2020-Mar-Somatic-Adult-Pancreas-SS2/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# Organoids - error in files
python3 celltype_in_outputs.py \
-l r-release_output_files/2020-Mar-InterOrganoid-Adult-Brain-10x/2020-Mar-InterOrganoid-Adult-Brain-10x.loom \
-h5 r-release_output_files/2020-Mar-InterOrganoid-Adult-Brain-10x/2020-Mar-InterOrganoid-Adult-Brain-10x.seurat.h5ad \
-m r-release_output_files/2020-Mar-InterOrganoid-Adult-Brain-10x/2020-Mar-InterOrganoid-Adult-Brain-10x.scp.metadata.txt \
-c celltype_csvs/HPSI-organoids-10x_cell_type_2020-03-17.csv \
-lp 10x
rsync -r r-release_output_files/2020-Mar-InterOrganoid-Adult-Brain-10x/*annotated_v1.* \
mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# Colonic Mesenchyme IBD - DONE
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-IBD-Adult-Colon-10x/2020-Mar-IBD-Adult-Colon-10x.loom \
# -h5 r-release_output_files/2020-Mar-IBD-Adult-Colon-10x/2020-Mar-IBD-Adult-Colon-10x.seurat.h5ad \
# -m r-release_output_files/2020-Mar-IBD-Adult-Colon-10x/2020-Mar-IBD-Adult-Colon-10x.scp.metadata.txt \
# -c celltype_csvs/ColonicMesenchyme-10x_cell_type_2020-03-13.csv \
# -lp 10x
# rsync -r r-release_output_files/2020-Mar-IBD-Adult-Colon-10x/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms

# InVitro Neuro Diff
# python3 celltype_in_outputs.py \
# -l r-release_output_files/2020-Mar-Diff-Fetal-Neuron-SS2/2020-Mar-Diff-Fetal-Neuron-SS2.loom \
# -h5 r-release_output_files/2020-Mar-Diff-Fetal-Neuron-SS2/2020-Mar-Diff-Fetal-Neuron-SS2.seurat.h5ad \
# -m r-release_output_files/2020-Mar-Diff-Fetal-Neuron-SS2/2020-Mar-Diff-Fetal-Neuron-SS2.scp.metadata.txt \
# -c celltype_csvs/InVitroInterNeuron-SS2_cell_type_2020-03-16.csv \
# -lp SS2  
# rsync -r r-release_output_files/2020-Mar-Diff-Fetal-Neuron-SS2/*annotated_v1.* \
# mshadbolt@tool.archive.data.humancellatlas.org:/home/mshadbolt/annotated_looms