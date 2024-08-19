# CITS3200 Team 14 meeting W5 - client

Time and location: Monday 19 Aug 2024 1pm, EZONE 202B + Teams\
Present: Heidi, Vinita, Paul, Shuai, Ryan, Cameron, client (Melinda)\
Apologies: -\
Absent: -

**Meeting opened 1:00pm**

## From team meeting

### Questions

-   Admin access to repo to modify workflow?
    -   Invite us to nlp organisation to make a new project (or have Melinda to make the project)?
    -   Protect main branch
-   Does Melinda want the deployment up for sprint 2? Or a locally working demo is fine and we'll do it properly for sprint 3?
-   List of domain names (Namecheap)
    -   isodatavis.com / isodatavisualisation.com
    -   isordldata.com
    -   rdl15926.com
    -   15926vis.com / 15926visualisation.com
    -   15926data.com / 15926datavis.com
    -   iso15926vis.com/ iso15926data.com
    -   isovisualiser.com / iso-visualiser.com
-   Consistent weekly meeting?
    -   Snapshots of what is currently done?

#### Answers

-   Admin access set up now - Heidi and Cameron have admin access (Heidi to work on project, Cameron to set up workflow)
-   Deployment - The sooner the better
    -   Next Monday 26th in-person meeting (or right after meeting), try to set up AWS + Namecheap
    -   Check out Namecheap higher grade accounts
-   Week of 2nd Melinda away - coincides with midsem break for team. Cancel meeting for that break
-   Leave meeting slot in calendar
    -   Friday decide on whether we want meetings or not
    -   Updates at our discretion - need to not surprise Melinda but don't update on every single thing
-   Namecheap - Melinda likes iso15926vis.com

### Current time planning for sprint 2 (for Melinda's reference)

Note: To be changed by the team later based on answers above

-   W5

    -   Landing page / visualisation pages setup
    -   Visualisation page - Hierarchical view on mock data, trying on different libraries available
    -   Backend - Store data as JSON from source of truth (mock database)
    -   Setup testing frameworks + add to workflow

-   W6

    -   Graphing tree should be good to go on mock data, with mouse and scroll navigation
    -   Frontend getting data from backend API to graph. Data storage system should be tested and decided on by end of week
    -   UI for sidepane, filters and search - can be non-functional for now
    -   Simple documentation page to show up from the site

-   Midsem break

    -   If above not done, catchup
    -   Frontend getting full size data from backend and being able to graph it properly
    -   Database / data storage model finalised with proper setup

-   W7

    -   Filters and search functionality working
    -   Node interaction - click to select and get data in right sidepane
    -   Basic CLI for updating data and some basic validation
    -   Number of levels above / below
    -   Non-functional UI for export

-   W8 (Wednesday due)
    -   Nothing new - lots of testing (first half of week)
    -   Prep for demo

After W8 (sprint 2) due (but still before end of week 3):

-   More extensive validation of data and auto rollback for CLI
-   Export functionality
-   Collapsible nodes
-   Any other optional requirements if there is the time
-   Full deployment on AWS + gunicorn and nginx

## Next meeting

### Time and location

Monday 26 Aug 2024 1pm, System Health Lab

### Action items

-   Upload minutes to Github
-   Ready for setting up AWS for meeting next week
-   Coding up the project!

**Meeting closed 1:15pm**
