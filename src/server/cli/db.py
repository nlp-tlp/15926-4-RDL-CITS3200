import sqlite3
import os
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON

from history import history_file_add_db

def update_db():
    # SPARQL endpoint URL
    sparql_endpoint = "http://190.92.134.58:8890/sparql"

    # Set up SPARQL Wrapper
    sparql = SPARQLWrapper(sparql_endpoint)
    sparql.setReturnFormat(JSON)

    # Your SPARQL query
    query_old = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX meta: <http://data.15926.org/meta/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?id ?label ?type ?definition ?parentId ?spreadsheetId ?spreadsheetLabel ?deprecationDate
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

    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX meta: <http://data.15926.org/meta/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT DISTINCT ?id ?label ?type ?definition ?parentId ?deprecationDate
    WHERE {
      ?id rdfs:label ?label.
      ?id rdf:type ?type.
      OPTIONAL { ?id skos:definition ?definition. }
      OPTIONAL { ?id meta:valDeprecationDate ?deprecationDate. }
      OPTIONAL { ?id rdfs:subClassOf ?parentId. }
    }
    ORDER BY ASC(?id)
    LIMIT 10000
    """

    # Set the query
    sparql.setQuery(query)

    # Fetch the results
    results = sparql.query()

    # # Print the raw response (in bytes)
    # raw_response = results.response.read()

    # # Decode the bytes to a string
    # decoded_response = raw_response.decode('utf-8')
    # print(decoded_response)

    # Convert to JSON or dictionary using SPARQLWrapper's convert method
    results = sparql.query().convert()

    # Print the converted results (this should be a dictionary)
    print(results)

    # Check if results are correctly parsed as a dictionary
    if not isinstance(results, dict):
        raise ValueError("The response could not be converted to JSON")
    
    # Make db and get connection and cursor into the file
    conn, cursor = make_db()

    # Create table (modify schema according to your needs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ApiData (
            id TEXT PRIMARY KEY,
            label TEXT,
            type TEXT,
            definition TEXT,
            parentId TEXT,
            deprecationDate TEXT
        )
    ''')

    # Insert data into the database using SQLAlchemy
    for result in results["results"]["bindings"]:
        # Extracting data from the result
        id_value = result["id"]["value"]
        label = result["label"]["value"]
        type_value = result["type"]["value"]
        definition = result.get("definition", {}).get("value", None)
        parentId = result.get("parentId", {}).get("value", None)
        # spreadsheetId = result.get("spreadsheetId", {}).get("value", None)
        # spreadsheetLabel = result.get("spreadsheetLabel", {}).get("value", None)
        deprecationDate = result.get("deprecationDate", {}).get("value", None)

        
        # Insert the record into the SQLite database
        cursor.execute('''
            INSERT OR IGNORE INTO ApiData (
                id, label, type, definition, parentId, deprecationDate
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (id_value, label, type_value, definition, parentId, deprecationDate))

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


def get_db_name(base_dir="../instance/"):
    # Get the current date
    date_str = datetime.now().strftime("%d-%m-%Y")
    
    # Start with the basic filename
    db_filename = os.path.join(base_dir, f"{date_str}.db")
    
    # Initialize a counter to append to the filename if needed
    counter = 1
    
    # Check if the file already exists, and if so, increment the counter
    while os.path.exists(db_filename):
        db_filename = os.path.join(base_dir, f"{date_str}-{counter}.db")
        counter += 1
    
    return db_filename


def make_db():
    # Get the database filename
    filename = get_db_name()

    # Create and connect to the SQLite database
    try:
        conn = sqlite3.connect(filename)
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return  # Exit the function if the database connection fails
    
    cursor = conn.cursor()

    # Add new db to history file
    history_file_add_db(filename)

    # return the cursor
    return conn, cursor