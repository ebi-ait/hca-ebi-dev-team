---
layout: default
title: Operations Zenhub Board Pipeline and Process
parent: Operations tasks
---

# Operations Zenhub Board Pipeline and Process

This page summarizes the pipeline used on the [Operations Zenhub board pipeline](https://app.zenhub.com/workspaces/operations-5fa2d8f2df78bb000f7fb2b5/board?repos=232300832,261790554) 

Tickets with the operations label appear in this zenhub board.   

The operations board is to track tasks in operations which are not data wrangling that need to be completed in the near future. This may include things like issues blocking data flow and system optimizations, documentation or stakeholder conversations which aren't data wrangling.  

This board is not meant to be a place holder for tasks that we might do at some point in the future

The operations board follows a [kanban style](https://en.wikipedia.org/wiki/Kanban_(development)) with no sprint specific to do list.  

The pipeline is:

**New** - Issues to be reviewed and prioritized in the to do list.   
**To Do** - This is the prioritized to do list. The first 2 or 3 tasks should be done first when starting a new task before other tasks.   
**In Progress** - Tasks that have been started by someone in the team. Once started they shouldn't move backward even if they get paused for other priorities.   
**Review/QA** - Issues open to the team for review Documentation/Process/Code complete, pending feedback. Tickets that don't need review can skip this stage.   
**Done** - This is where tasks completed within a two week cycle are put. This column is to faciliate tracking statistics in zenhub.   
**Closed** - Closed tickets.   

During [Wednesday morning operation meetings](https://www.google.com/url?q=https://docs.google.com/document/d/1O2nCBtnFY-AWh_1_s188xLTyvaZpwbUUp3Pvs_aV_jc/edit?ts%3D5f1816b8%23&sa=D&source=calendar&ust=1607435802282000&usg=AOvVaw0uFk9fs3hHHBusLGQwFE_u) there should be a review of the tasks in each column with unfinished tasks, starting with Review/QA and a prioritization discussion for the to do list, identifying 2-3 tasks in that list which should be done next as tasks in progress are completed.

The majority of tasks in the operations board should be able to be completed in <1 week. Some tasks such as stakeholder communication might take longer if that conversation needs to have several exchanges to reach a conclusion.

To help with tracking productivity, tickets should be moved to the **DONE** column when they are finished and then on every Wednesday a new product development sprint starts, done tasks are closed.

Where possible, we should aim to define tasks which are 1-5 days to complete because this improves our efficiency. However, sometimes there are exceptions where tasks can end up taking longer than two weeks because,for example,they involve a high level of external dependencies such as stakeholder engagement or refining SOPs for interactions with other teams.

Every sprint review, a summary of the highlights from the last two weeks of operations and the number of tickets closed is presented in this slide deck
