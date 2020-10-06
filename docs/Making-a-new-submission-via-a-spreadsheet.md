# Making a new submission via a spreadsheet

For instructions on how to create the spreadsheet see the [[Data Contributors Spreadsheet Quick Guide]].

# Prereqs
1. You are able to login to the Ingest submission UI because your e-mail is in the domain of one of the DCP development organizations
2. You have installed the [hca cli tool](https://data.humancellatlas.org/guides/installing-the-hca-cli).

# Steps
1. [Login to the Ingest Submission UI](https://ui.ingest.data.humancellatlas.org/login).
2. Click the "Start a new submission" button.
3. Make sure the Create radio button is selected. Select your spreadsheet via the Browse button.
4. Hit the Upload button.
5. The UI will say "We’ve got your spreadsheet, and we’re currently importing and validating the data. Nothing else for you to do - check back later.". After a short while, if there are no errors at this stage you will see a page with Overview, Metadata and Data tabs. There will be a Submit tab but if there area any data files to be uploaded this will be greyed out.

   a. If the UI reports an error, correct the problem in the spreadsheet and start a new submission. You can delete the problem submission by using the My "Submissions" link at the top to go back to submissions and then clicking the trashcan icon by the relevant entry.

6. The data tab will show the files that need to be uploaded. At the bottom of the screen you will see an s3 upload area location with a format something like `s3://org-humancellatlas-upload-prod/17df2fab-f4fe-42ea-ba3c-236cb5e5fd76/`

7. In a terminal window, set the hca tool to this upload area with the command `hca upload select <s3-location>`. You will get a response something like:

```
$ hca upload select s3://org-humancellatlas-upload-prod/17df2fab-f4fe-42ea-ba3c-236cb5e5fd76/
Upload area 17df2fab-f4fe-42ea-ba3c-236cb5e5fd76 selected.
In future you may refer to this upload area using the alias "1"
```

8. Upload your files with the command `hca upload files <path>+`. You will get a response something like:

```
$ hca upload files SRR3562314_*

Starting upload of 2 files to upload area 17df2fab-f4fe-42ea-ba3c-236cb5e5fd76
Checksumming took 6.41 milliseconds to compute
Checksumming took 9.83 milliseconds to compute
Upload complete of SRR3562314_2.fastq.gz to upload area s3://org-humancellatlas-upload-prod/17df2fab-f4fe-42ea-ba3c-236cb5e5fd76/
Upload complete of SRR3562314_1.fastq.gz to upload area s3://org-humancellatlas-upload-prod/17df2fab-f4fe-42ea-ba3c-236cb5e5fd76/
Completed upload of 2 files to upload area 17df2fab-f4fe-42ea-ba3c-236cb5e5fd76
```

9. Switch back to the data tab in the Ingest submission UI. After a while, both files should show a state of valid.

10. Go to the submit tab and hit the submit button.

11. The UI will switch back to the overview tab. You can see the status of the submission in the top-right corner. As time goes by this will go Submitted -> Processing -> Cleanup -> Complete.

12. Congratulations, you've completed the submission.