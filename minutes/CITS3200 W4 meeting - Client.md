# CITS3200 Team 14 meeting W4 - client
Time and location: Monday 12 Aug 2024 1pm, EZONE 202B + Teams
Present: Heidi, Vinita, Paul, Shuai, Ryan, Cameron, client (Melinda)
Apologies: -
Absent: -

**Meeting opened 1:00pm**

## Agenda
* Hundred dollar test, show proposal doc
* Misc questions for proposal doc

## Proposal doc
### Client answers to team questions
* Metadata of node - might include subclasses
    * Don't want clutter but might be better than trying to figure out all the subclasses from graph
    * Not sure, will need to be decided when it gets implemented and we can actually see everything
* Responsiveness to phone is a yes
* Just node and what's above or below instead of full graph and peers
    * As mentioned before, up to 2 above and 2 below
    * More specific implementation details can be decided later - for now we'll show only those nodes based on search
    * Maybe see Neo4j **(have to use a apoch plugin for a hierarchical view)
* Last year's team didn't do hundred dollar test
* Seek further knowledge on cloudflare for deployment through Michael Stewart - expert of web apps.
    * Check about AWS protections first
* Expected number of users up to 4 or 5 at one time (except more during demo)
    * Even ok to limit users if we can't deal with, as long as its specified so users know
* Melinda will decide preferences when she sees them, Namecheap preference list needs to be made

### Other client comments
* Split requirements so that each on the list only covers one thing
    * More specific examples / descriptions, no waffle - answers are yes or no
    * Takes out 'ands'
    * See IEEE guide
* User stories types of users:
    * Maintainer
    * User
    * Admin
* For risk analysis derisking - want to see how specific code testing can work
* Acceptance tests
    * As before, more specific 
    * Uncluttered interface, documentation of code as well as infrastructure to maintain site
    * Can be one-to-one with the requirements etc.

### Other notes
* Add another column for cost/ranking
* Add functionality - documentation button on web interface

## Examples given by client
### Documentation
* IndEAAv2 (https://indeaav2-docs.systemhealthlab.com/developer/)
    * Github hosted documentation using makedoc
    * A little higher level information than what the github is at
    * This one also has a public repo
    * Documentation button present on web interface
* Living Lab
    * Look and feel is great - navigation bars, names etc. 

### Github projects for general tasks
* Can be used for not just code - can even do without linking to code issues
* Preferred by Melinda - easier to keep track of student projects

### Neo4j
* Neo4j demo on official site - has a bunch of different demos
* Select and deselect nodes - can see all nodes in graph vs see just one and its connections 
    * Although, having to click and hold onto the node to focus onto it is annoying
* Example - https://nlp-tlp.org/maintenance_kg/

## Next meeting
### Time 
Monday 26 Aug 2024 1pm

### Action items
* Changes for proposal doc from comments and answers above
* Upload minutes to Github later
* Finish up on proposal doc by lunchtime Tuesday. Ping Melinda after 2pm Tuesday for feedback 
    * $100 test with this - add column for the requirements table
* Ask / investigate about whether cloudflare is necessary
    * Check about AWS protections, maybe ask Dr. Michael Stewart (michael.stewart@research.uwa.edu.au) 
* Make a preference list of possible domains available through Namecheap for the deployed site.
* Make a github project to use for issues (future work - probably sprint 2 on)

**Meeting closed 1:50pm**
