---
layout: default
title: Spreadsheet quick guide
parent: User documentation
---

NEEDS UPDATING
{: .label .label-red }

# Data Contibutors Spreadsheet Quick Guide

Google Sheets and Excel spreadsheets are used to gather metadata about your project. Ths document is a brief walkthrough to help you get started filling out an HCA metadata spreadsheet.

If you have any questions, please contact the data wrangling team at: \
`wrangler-team@data.humancellatlas.org`.


## Before you start


Metadata is represented in a spreadsheet with tabs that relate to the experimental design. For example, an 'Organoid' tab would be included if a project includes organoid samples. If you think your spreadsheet is missing fields or tabs to properly describe your experiment, please contact a data wrangler.

## Spreadsheet tab organization

Metadata is collected at multiple levels, for example: project, donor, sequence file, and dissociation protocol. Each of these levels or **entities** has a separate tab in the spreadsheet.

Each row in every tab corresponds to one entity described by the tab name. For example, in the 'Donor organism' tab, each row describes one donor. In the 'Sequence file' tab, each row describes one sequence file. Only one row in the 'Project' tab should be filled in to describe the whole project.

### All tabs share some common properties

* The first row is the metadata field name.
* The second row is the field description.
* The third row contains one or two example values and guidelines, when appropriate.
* The fourth row is used for programmatic spreadsheet processing and is hidden.
* The fifth row is intentionally left blank.
* You should enter your values from the sixth row down.
​
​
​
### The following tabs *should* be in your spreadsheet as they apply to most projects
​
​
- Project (only fill out one row)
- Project - Contributors
- Project - Funders
- Project - Publications  (only if your data has been published)
​
​
### The following tabs *may* be in your sheet depending on your experimental design
​
​
**Metadata about Biomaterials:**
​
​
- Donor organism
- Specimen from organism
- Cell suspension
- Cell line
- Organoid
- Imaged specimen
​
​
**Metadata about Files:**
​
​
Every data or supplementary file we need to ingest requires an entry in one of these tabs.
​
​
- Sequence file
- Image file
- Supplementary file (for listing supplementary protocol files)
​
​
**Metadata about Protocols:**
​
​
- Aggregate generation protocol (organoid only)
- Collection protocol
- Differentiation protocol (cell line, organoid only)
- Dissociation protocol
- Enrichment protocol
- iPSC induction protocol (cell line only)
- Imaging preparation protocol (imaging transcriptomics only)
- Imaging protocol (imaging transcriptomics only)
   - Probe (imaging only)
   - Channel (imaging only)
- Library preparation protocol (sequencing only)
- Sequencing protocol (sequencing only)
​
​
## How to link biomaterials, files, and protocols
​
### Linking biomaterials and files
​
The first 'ID' columns in the Biomaterial and Protocols tabs are unique identifiers for each row in that tab. Similarly, the 'File Name' columns in the File tabs are unique identifiers for each row in that tab. Values in these columns must be unique within the spreadsheet. These unique identifiers are used to link entities together.
​
For example, consider an experiment with entities that are linked as follows:
​
Donor -> Specimen from organism -> Cell suspension -> Sequence file
​
In each of these tabs, one entity (row) is assigned an ID. For example: 'donor1', 'tissue1', 'cell_suspension1', and 'sequence_file_R1.fastq.gz', respectively. 
​
- Link 'tissue1' to 'donor1' by entering 'donor1' in the Derived From column in the Specimen from organism tab.
- Link 'cell_suspension1' to 'tissue1' by entering 'tissue1' in the Derived From column in the Cell suspension tab.
- Link 'sequence_file_R1.fastq.gz' to 'cell_suspension1' by entering 'cell_suspension1' in the Derived From column in the Sequence file tab.
​
### Linking biomaterials and protocols
​
Biomaterial entities are linked to the protocols used to generate them by entering the protocols' IDs (from the corresponding Protocol tab) in the respective 'ID' columns in the Biomaterial tab.
​
For example, consider an experiment that followed a dissociation protocol to produce a cell suspension from a tissue sample.
​
Specimen from organism -> Dissociation protocol -> Cell suspension
​
In each of these tabs, one entity is assigned an ID. For example: 'tissue1', 'dissociation_protocol1', and 'cell_suspension1', respectively. 
​
- We can link 'cell_suspension1' to 'dissociation_protocol1' (the protocol that derived the cell suspension) by entering 'dissociation_protocol1' in the Dissociation Protocol ID column in the Cell suspension tab.
​
## How to indicate a library preparation was sequenced more than once
​
If the same library preparation has been sequenced more than once, this can be indicated in the spreadsheet by providing a unique identifier for each library preparation in the **library preparation ID** field in the Sequencing file tab.
​
For example:
​
| File Name | Library Preparation ID |
| :------------ |:-------------|
| file100_R1.fastq.gz | lib_prep_1 |
| file101_R1.fastq.gz | lib_prep_1 |
| file102_R1.fastq.gz | lib_prep_2 |
| file103_R1.fastq.gz | lib_prep_2 |
​
indicates that files file100_R1.fastq.gz and file101_R1.fastq.gz were both generated from the same library preparation, and files file102_R1.fastq.gz and file103_R1.fastq.gz were both generated from a different library preparation.
​
## Additional resources for HCA metadata
​
More information about HCA metadata can be found here `https://github.com/HumanCellAtlas/metadata-schema/tree/master/docs`