# CITS3200 Team 14 meeting W7 - client

Time and location: Monday 9 Sep 2024 1pm, EZONE 202B + Teams\
Present: Heidi, Vinita, Paul, Shuai, Ryan, Cameron, client (Melinda)\
Apologies: -\
Absent: -

**Meeting opened 1:00pm**

## From team meeting

- Progress Update

### Questions

- Animation on graph collapsibility? (Will hinder performance)
- Arrows towards parent still good with the Bezier curves? (we have in opposite direction for now just testing)
- click for node info and collapsibility (right click / left click? click node / click label?)
- What is the root node, as 'Thing' is in a different graph `/dm` instead of `/rdl` -> are we only querying the RDL, or do we include more graphs?
        - Note that she did say that just to do RDL. Just say that this could mean multiple roots and also no "Thing"
- Does Melinda want any docs?

### Answers and Comments

- 'Thing' needs to be in the graph as the top level node.
  - Check if 'Thing' is the only root node in Onno's site (should have been updated to be the only root).
  - 'PossibleIndividual' is a subclass of 'Thing' and hence should be a child node of 'Thing'.
- Arrows can point to children from parents in this case; although in ontologies they usually point the other way.
- She likes that the nodes are coloured differently when expanded as opposed to when collapsed as this highlights what nodes have been collapsed.
- Labels should be clicked for getting more node information
- Nodes should be clicked for expandability and collapsibility
- Use mainstream packages/libraries - to be included in maintainer documentation.
- [Living lab](https://livinglabproject.com/) - preferred colour scheme/design.
- [IndEEA](https://indeaa-docs.systemhealthlab.com/developer/) preferred documentation format
- User stories document for sprint 3 - can incorporate into the flyer.

## Next meeting

- Monday next week meeting - retrospective on sprint 2.
  
### Time and location

TBD

### Action items

- Get some rdf data on website for sending screenshots/flyer to Onno by mid week.
  - Flyer with screenshots? Static webpage - coming soon? So Melinda can circulate.
  - Add user stories from sprint 2 doc to flyer.
- Create a list of all dependencies of project in the maintenance docs - will move to sprint 3 when we do the documentation.

**Meeting closed 1:20pm**