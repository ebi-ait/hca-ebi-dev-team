---
layout: default
title: End to End Tests
parent: Operations tasks
---

This page defines a standard set of end-to-end (e2e) tests that should be done regularly. Eventually, these may be replicated with an automated tool (e.g. [Selenium](https://www.selenium.dev/)). Until automation is done, these tests provide a reference for areas to check when large, potentially breaking changes happen.

These tests should preferentially be done with the new feature on the staging environment and functionality and "look & feel" compared to the production environment. Some screenshots are included for reference in areas that are unlikely to change frequently.

**You will need the WRANGLER role to perform these tests.**

# Front page
1. Ensure page load times are not drastically affected (just by eye - no metrics required).
2. Check "Log in", "New Project", and "My Projects" are present and clickable
3. Compare UI to screenshot (below)

![Home Page](/images/e2e_home.png)

# Log in page
1. Navigate to [https://staging.contribute.data.humancellatlas.org/](https://staging.contribute.data.humancellatlas.org/)
2. Compare UI to screenshot (below)
3. Click Register and ensure it navigates you to the Elixir service (you do not need to register an account)
4. Return to [https://staging.contribute.data.humancellatlas.org/](https://staging.contribute.data.humancellatlas.org/)
5. Attempt login flow and ensure it logs you in

![Login page](/images/e2e_login.png)

# New project page
1. Navigate to [https://staging.contribute.data.humancellatlas.org/projects/new](https://staging.contribute.data.humancellatlas.org/projects/new)
2. Follow the flow to create a new project

*N.B. be sure to delete the project after finishing tests* 

# My projects
1. Navigate to [https://staging.contribute.data.humancellatlas.org/projects](https://staging.contribute.data.humancellatlas.org/projects)
2. Ensure the "Generate Metadata Spreadsheet" and "New Project" buttons are present and clickable
3. Ensure projects are listed correctly in the table (you will need to create a project first)