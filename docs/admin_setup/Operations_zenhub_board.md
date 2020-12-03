# Operations Zenhub Board pipeline

This page summarizes the pipeline used on the [Operations Zenhub board pipeline](https://app.zenhub.com/workspaces/operations-5fa2d8f2df78bb000f7fb2b5/board?repos=232300832,261790554) 

The operations board is to track tasks in operations which are not data wrangling that need to be completed in the near future. This may include things like bug fixes and system optimizations, stakeholder conversations which aren't data wrangling or documentation tasks

The operations board follows a [kanban style](https://en.wikipedia.org/wiki/Kanban_(development)) with no sprint specific to do list

The pipeline is

*New* - Issues to be reviewed and prioritized in the to do list.
*To Do* - This is the prioritized to do list. The first 2 or 3 tasks should be done first when starting a new task before other tasks
*In Progress* - Tasks that have been started by someone in the team. Once started they shouldn't move backward even if they get paused for other priorities
*Review/QA* - Issues open to the team for review Documentation/Process/Code complete, pending feedback. Tickets that don't need review can skip this stage.
*Done* - This is where tasks completed within a two week cycle are put. This column is to faciliate tracking statistics in zenhub
*Closed* - Closed tickets
