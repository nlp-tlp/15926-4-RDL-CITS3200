from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask
from app.models import db, ApiData


def update_db():
    # SPARQL endpoint URL
    sparql_endpoint = "https://data.15926.org/sparql"

    # Set up SPARQL Wrapper
    sparql = SPARQLWrapper(sparql_endpoint)
    sparql.setReturnFormat(JSON)

    # Your SPARQL query
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX meta: <http://data.15926.org/meta/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT DISTINCT ?id ?label ?type ?definition ?parentId ?spreadsheetId ?spreadsheetLabel ?deprecationDate
    WHERE {
      ?id rdfs:label ?label.
      ?id rdf:type ?type.
      OPTIONAL { ?id skos:definition ?definition. }
      OPTIONAL { ?id meta:valDeprecationDate ?deprecationDate. }
      OPTIONAL { ?id rdfs:subClassOf ?parentId. }
      OPTIONAL {
        GRAPH ?coco { ?id rdf:type ?spreadsheetId }
        ?spreadsheetId rdfs:label ?spreadsheetLabel.
      }
    }
    ORDER BY ASC(?id)
    LIMIT 100
    """

    # Set the query
    sparql.setQuery(query)

    # Fetch the results
    results = sparql.query().convert()

    # Check if results are correctly parsed as a dictionary
    if not isinstance(results, dict):
        raise ValueError("The response could not be converted to JSON")

    # Insert data into the database using SQLAlchemy
    for result in results["results"]["bindings"]:
        # Extracting data from the result
        id_value = result["id"]["value"]
        label = result["label"]["value"]
        type_value = result["type"]["value"]
        definition = result.get("definition", {}).get("value", None)
        parentId = result.get("parentId", {}).get("value", None)
        spreadsheetId = result.get("spreadsheetId", {}).get("value", None)
        spreadsheetLabel = result.get("spreadsheetLabel", {}).get("value", None)
        deprecationDate = result.get("deprecationDate", {}).get("value", None)

        # Check if the record already exists
        existing_record = ApiData.query.get(id_value)
        if not existing_record:
            # Create a new record
            new_record = ApiData(
                id=id_value,
                label=label,
                type=type_value,
                definition=definition,
                parentId=parentId,
                spreadsheetId=spreadsheetId,
                spreadsheetLabel=spreadsheetLabel,
                deprecationDate=deprecationDate,
            )
            db.session.add(new_record)

    # Commit the session
    db.session.commit()
