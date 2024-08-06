# CITS3200 Team 14 meeting W2 - Client

Time and location: Tuesday 6 Aug 2024 12pm, Microsoft Teams\
Present: Heidi, Paul, Shuai, Cameron, Melinda (client)\
Apologies: Vinita, Ryan\
Absent: -

**Meeting opened 12:00pm**

## Requirement question answers

### Web interface

-   Landing view
    -   Nice looking introduction to the tool and project
    -   Instructions for main interface
    -   Details about collaboration with ISO and purpose of project
    -   Our names
    -   Link to Onno's website
    -   Button to main graph interface
-   Main graph interface
    -   Tree not graph
    -   No preference between top-down / left-right tree
    -   Searching can either be done by searchbar string searching, or by exploring the graph
    -   Don't show descriptions with nodes, too messy, just labels (if toggled on)
-   Sidepanes
    -   Left sidepane for search and filtering, right sidepane to display information associated with selected node
    -   Both sidepanes collapsible to not hinder graph view
    -   No need for links in nodes info - too many, and they easily break
-   Navigation
    -   Click into area / draw box within graph and zoom to that area to see more details
    -   Mouse drag to move graph around, and mouse scroll / touchpad zoom to zoom
    -   Collapsible nodes
-   Searching
    -   _Nice to have_ - Persistant search and filtering
    -   Dropdown to select what to search string by.
        -   Definitely by labels and URI
        -   _Nice to have / uncertain_ - By description
    -   _Nice to have_ - Search by sparql?
        -   You can already do it on Onno's website
-   Graph toggles
    -   On / off deprecated classes - off by default
    -   On / off class labels - off by default
    -   Like checkboxes
-   Colours
    -   _For now_ - Different for different levels of hierarchy
-   Export
    -   No need for data export, already available on Onno's site
    -   Export graph visually into diagram, as png, jpg etc.

### Admin

-   Keep admin functionality out of the web interface - just instructions and capabilities through the backend is fine
-   There should be a version of the data downloaded already on the backend (AWS), that is known to be correctly working with the web interface
    -   If possible, also have data stored in local storage
-   When Onno makes a change on his website, prompt the admin to update (not automatic, button?)
-   When an update is triggered, and there is an error, give an error message and rollback to the previous working dataset

### Other

-   Leave the idea of translations for now
-   See google maps for an idea for search and navigation
-   See lucidchart for some nice diagram export functionality
    -   Ability to automatically snip only active area is nice. Otherwise normal snipping is also fine
-   Source of truth for data - Onno's website

## Next meeting

### Time and location

Monday 1pm-1:45pm, format of meeting to be decided closer to the time

### Action items

-   AWS setup free tier next week (or the week after, if we need the time for the proposal doc)
-   Have a look at Namecheap names
-   Make up some user stories from question answers - make sure it reflects that we really understand the data inside and the purpose of our project
-   Put minutes on github
-   Any other requirement questions, ping Melinda on Teams

**Meeting closed 12:45pm**
