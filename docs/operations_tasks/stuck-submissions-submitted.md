---
layout: default
title: Stuck in Submitted
parent: Investigate Stuck Submissions
grand_parent: Operations tasks
---

## Problem: submission stuck in "Submitted"
![Screenshot 2022-09-27 at 16 44 35](https://user-images.githubusercontent.com/13031259/192577769-b5aef581-c479-4752-9f79-435ae2f1140b.png)

1. Find the submission ID
    - Clicking on the See Ingest API JSON button will take you to Submission Envelope
    - The url will be something like `https://too.many.domains/submissionEnvelopes/id`
    - ![Screenshot 2022-09-27 at 16 44 52](https://user-images.githubusercontent.com/13031259/192577851-283d9434-e5d3-4e27-9d18-6bacb6719a7c.png)
1. Find the Export Job List for the submission
    - /submissionEnvelopes/**id**/exportJobs
    - ![Screenshot 2022-09-27 at 17 07 23](https://user-images.githubusercontent.com/13031259/192578326-9d889a07-3268-46c2-8a31-54a12a9ff4cc.png)
1. Find the Export Job ID for the latest export Job
    - this latest one is the one with the highest number exportJob[**X**]
    - The ID is listed in the self / exportJob link
    - ![Screenshot 2022-09-27 at 16 45 25](https://user-images.githubusercontent.com/13031259/192577903-7193369b-8dc3-4a8a-9c19-33169cbb5455.png)
1. Use the gcloud cli to monitor the transfer
    - *todo: write a tutorial on downloading and configuring the gcloud cli*
    - `gcloud transfer jobs monitor 6333167779c78d5fd8f7d099`
    - Should return something link the following example when the file transfer is still in progress
    ```
    Polling for latest operation name...done.                                                                                                                                                              
    Operation name: transferJobs-6333167779c78d5fd8f7d099-1664292478189663
    Parent job: 6333167779c78d5fd8f7d099
    Start time: 2022-09-27T15:27:58.227188389Z
    IN_PROGRESS | 91% (78.8GiB of 86.3GiB) | Skipped: 0B | Errors: 0 -
    ```
    ![Screenshot 2022-09-27 at 16 46 34](https://user-images.githubusercontent.com/13031259/192578015-f6cc853c-7c66-438c-be29-6b95068c5833.png)
