---
layout: default
title: Upload a new submission
parent: User documentation
---
NEEDS UPDATING
{: .label .label-red }

# Upload a new submission to a project

You can add data and metadata to an existing project by making further submissions to it. Let's start off with the situation where you want to add a new experiment that doesn't reference any existing entities in the project. That is, it will add everything from a new donor down to the FASTQ files. You can also add metadata that references existing entities such as donor that was added in a previous submission. For more information on this, see the section that follows the steps below.

# Steps 
1. In the [Ingest UI](https://contribute.data.humancellatlas.org/) navigate to the project to which you want to add meta/data. If necessary you can find this using keyword search.

2. On the project details page, in _Data Upload_ tab. There will be a button

[[https://github.com/HumanCellAtlas/ingest-central/blob/master/wiki/img/project-details.png]]

3. Prepare a spreadsheet with the metadata you want to add. This MUST NOT contain any of the project tabs.

4. Upload the spreadsheet using the Create option (not Update).

5. If the metadata is validated successfully, [upload the data using the HCA CLI tool as usual](https://github.com/HumanCellAtlas/ingest-central/wiki/Making-a-new-submission-via-a-spreadsheet).

6. Once the data is validated click the Submit button on the submit tab as usual.

7. When the submission enters the Completed state then the new data has been added to the project. On the project details page you should be able to see that the new submission has been added to the submissions list.

There can only be one uncompleted submission for a project at a time. If you make a mistake in a submission (e.g. metadata is not valid) then you must first delete the invalid submission before starting a new one with corrected metadata. If another wrangler has an open submission on the project then that submission must be completed or deleted before you can start yours.

To delete a submission, find it in the submissions page and click the delete icon.

# Linking new metadata to existing metadata
In the spreadsheet, the new metadata are linked to existing metadata by specifying the UUID of an existing metadata entity in the linking column field in the spreadsheet.

Example:

For the "Specimen from organism" worksheet, to link the specimen to a donor, the linking column field in the spreadsheet could either be:
 - `donor_organism.biomaterial_core.biomaterial_id` : This should contain the id of the donor organism entity in the same spreadsheet
 - `donor_organism.uuid` : This should contain the uuid of the donor organism which was previously submitted

specimen_from_organism.biomaterial_core.biomaterial_id | specimen_from_organism.biomaterial_core.biomaterial_name | donor_organism.uuid | collection_protocol.uuid
--- | --- | --- | ---
specimen_ID_1 | This is a dummy specimen | fb2494d7-34cd-4269-a946-1463f0b9c3af | d6b756fe-fb40-466c-b1c0-c6e20fbd8b20

Please see (TODO ask wrangler for a link to the guide, insert link to the guide) for more information on how to fill out the spreadsheet.

One way to find these UUIDs is to look in the Ingest submission UI for the metadata tab of the submission which added it.

