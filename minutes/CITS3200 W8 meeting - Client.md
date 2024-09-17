# CITS3200 Team 14 meeting W8 - client

Time and location: Monday 16 Sep 2024 1pm, EZONE 202B + Teams\
Present: Heidi, Vinita, Paul, Shuai, Ryan, Cameron, client (Melinda)\
Apologies: -\
Absent: -

**Meeting opened 1:00pm**

## Agenda

* Questions + Feedback
* Informal Project Demonstration
* Client Retrospective (on separate document)

### Condensed Team retrospective from team meeting

* Encountered issues with database size, causing delays in both frontend and backend architecture decisions. Currently behind on sprint 2 progress but everything is still on track. We have decided on all the libraries and the database to use, so we can move on faster now.
* Team members have been working diligently. We believe we can still complete the previously discussed stories within the project timeline, that is with no additional scope.
* Apology for the deadline changes. We will make an effort to avoid overpromising in the future.

### Updates from Demo

* Dynamic loading is currently a work in progress, expected to be completed by the end of sprint 2 (Wednesday 5pm).

### Questions

* Are we to graph nodes from different subgraphs, `\rdl`, `\dm`, `\lci`, as there are some disconnected nodes if not e.g. - can't find `Valve` as it's in `\lci` under `FunctionalObject`
  * Do we need to consult Onno on this?
* Is the Disclaimer on the landing page well written?

### Answers and Comments

* Everything under `Thing` needs to be graphed
  * `\rdl` - Reference Data Library
  * `\dm` - Data Model
  * `\lci` - Extended Data Model
  * `\coco` - ClassOfClassOf - grouping

* Disclaimer
  * "This Project is an initiative of the University of Western Australia (UWA) NLP-TLP Group and is intended to assist the ISO/TC 184/SC 4/WG3 Committee"
* Add to the Landing page
  * a date of the last update to the project ("This was developed by ... in ... and released in October 2024")
  * link to the GitHub repository
  * System health lab gmail address as a contact: [systemhealthlab@gmail.com](mailto:systemhealthlab@gmail.com) ("Any questions, contact us here")
* Graph with 2 levels of hierarchy looks good, third level currently expands out all possible nodes up to that level - should be fixed with dynamic loading.
* Alphabetic sorting of labels would be good to have if possible.
* In information panel, only list
  * label
  * type
  * definition
  * subClassOf
  * id

## Next meeting

* None needed next week at this stage but scheduled if necessary
  
### Time and location

TBD

### Action items

* @everyone provide list of personal/student emails for Melinda to contact us in the future if needed

**Meeting closed 1:35pm**
