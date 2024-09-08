import time
from SPARQLWrapper import SPARQLWrapper, POST, JSON, BASIC
from dotenv import load_dotenv
import os
import requests
import logging

# Set up logging to a file
logging.basicConfig(filename='graphdb_insertion_errors.log', 
                    level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Execute the SPARQL query with a given offset and limit.
def execute_sparql_query(endpoint_url, offset=0, limit=10000):
    sparql = SPARQLWrapper(endpoint_url)
    query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX meta: <http://data.15926.org/meta/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT DISTINCT ?id ?label ?type ?definition ?parentId ?deprecationDate
        WHERE {{
          ?id rdfs:label ?label.
          ?id rdf:type ?type.
          OPTIONAL {{ ?id skos:definition ?definition. }}
          OPTIONAL {{ ?id meta:valDeprecationDate ?deprecationDate. }}
          OPTIONAL {{ ?id rdfs:subClassOf ?parentId. }}
        }}
        LIMIT {limit}
        OFFSET {offset}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and return the results
    return sparql.query().convert()

def insert_results_into_graphdb(endpoint_url, results, graph_uri):
    # Initialize a list to collect multiple INSERT DATA statements
    bulk_insert_query = f"INSERT DATA {{ GRAPH <{graph_uri}> {{\n"
    
    for result in results["results"]["bindings"]:
        try:
            # Construct the SPARQL update for each triple
            bulk_insert_query += f"""
                <{result['id']['value']}> <http://www.w3.org/2000/01/rdf-schema#label> "{result['label']['value']}" .
                <{result['id']['value']}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{result['type']['value']}> .
            """
            if "definition" in result:
                bulk_insert_query += f'<{result["id"]["value"]}> <http://www.w3.org/2004/02/skos/core#definition> "{result["definition"]["value"]}" .\n'
            if "deprecationDate" in result:
                bulk_insert_query += f'<{result["id"]["value"]}> <http://data.15926.org/meta/valDeprecationDate> "{result["deprecationDate"]["value"]}" .\n'
            if "parentId" in result:
                bulk_insert_query += f'<{result["id"]["value"]}> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <{result["parentId"]["value"]}> .\n'

        except Exception as e:
            # Log the problematic data and the error message to the file
            logging.error(f"Error processing result: {result}")
            logging.error(f"Exception: {e}")
            continue  # Skip to the next result

    # Close the SPARQL Update query
    bulk_insert_query += "}}"

    try:
        # Send the entire bulk insert query in one request
        headers = {"Content-Type": "application/sparql-update"}
        response = requests.post(endpoint_url, headers=headers, data=bulk_insert_query)

        if response.status_code != 204:
            raise Exception(f"Failed to insert data. Status Code: {response.status_code}. Response: {response.text}")

    except Exception as e:
        logging.error("Failed to execute the SPARQL update query.")
        logging.error(f"SPARQL query: {bulk_insert_query}")
        logging.error(f"Exception: {e}")
        raise  # Re-raise the exception after logging


def update_db():
    endpoint_url = "http://190.92.134.58:8890/sparql"
    graphdb_endpoint_url = "http://localhost:7200/repositories/default/statements"  # GraphDB repository
    graph_uri = "http://iso15926vis.org/graph/"+"v2"
    # dba_password = get_dba_password()
    batch_size = 10000
    offset = 0
    total_triples = 0

    # Start timing
    start_time = time.time()

    while True:
        # Fetch data from the SPARQL endpoint
        results = execute_sparql_query(endpoint_url, offset, batch_size)

        # If no results are returned, break the loop
        if not results["results"]["bindings"]:
            break

        # Insert the results directly into the Virtuoso server
        insert_results_into_graphdb(graphdb_endpoint_url, results, graph_uri=graph_uri)

        # Increment the offset for the next batch
        offset += batch_size

        # Update the total triples count
        total_triples += len(results["results"]["bindings"])
        print(f"Inserted {len(results['results']['bindings'])} triples. Total so far: {total_triples}.")

    # End timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTotal triples inserted: {total_triples}")
    print(f"Time taken: {elapsed_time:.2f} seconds")


def test_graphdb_insert():
    # Define the GraphDB endpoint URL
    repository_id = "test"  # Replace with your actual repository ID
    endpoint_url = f"http://localhost:7200/repositories/{repository_id}/statements"

    # SPARQL Update query to insert data
    sparql_update = """
    INSERT DATA {
        GRAPH <http://example.com/graph2> {
            <http://example.com/subject> <http://example.com/predicate> "object3" .
        }
    }
    """

    # Headers for the request
    headers = {
        "Content-Type": "application/sparql-update",
    }

    # Send the POST request to the GraphDB endpoint
    try:
        response = requests.post(endpoint_url, headers=headers, data=sparql_update)
        
        # Check if the request was successful
        if response.status_code == 204:
            print("Insert successful.")
        else:
            print(f"Failed to insert data. HTTP Status Code: {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"Error executing SPARQL query: {e}")


# def get_dba_password():
#     # Load the .env file from the parent directory
#     env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
#     load_dotenv(dotenv_path=env_path)
    
#     # Get the DBA_PASSWORD from the environment variables
#     dba_password = os.getenv('DBA_PASSWORD')
    
#     if not dba_password:
#         raise ValueError("DBA_PASSWORD not found in the .env file.")
    
#     return dba_password


# def test():
#     # Initialize SPARQLWrapper with dba credentials
#     endpoint_url = "http://localhost:8890/sparql"
#     sparql = SPARQLWrapper(endpoint_url)
#     sparql.setMethod(POST)

#     dba_password = get_dba_password()
#     sparql.setCredentials("dba", "MyS3cR3tP455w0Rd")
#     sparql.setHTTPAuth(BASIC)

#     # Example of setting a query
#     sparql.setQuery("""
#     INSERT INTO GRAPH <http://example.com/graph> {
#         <http://example.com/subject> <http://example.com/predicate> "object" .
#     }
#     """)
#     sparql.query()

# Insert the SPARQL query results directly into the Virtuoso server.
# def insert_results_into_virtuoso(endpoint_url, results, graph_uri, dba_pass):
#     sparql = SPARQLWrapper(endpoint_url)
#     sparql.setMethod(POST)
#     sparql.setCredentials("dba", dba_pass)
#     sparql.setHTTPAuth(BASIC)

#     for result in results["results"]["bindings"]:
#         insert_query = f"""
#             INSERT INTO GRAPH <{graph_uri}> {{
#                 <{result['id']['value']}> <http://www.w3.org/2000/01/rdf-schema#label> "{result['label']['value']}" .
#                 <{result['id']['value']}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{result['type']['value']}> .
#         """
#         if "definition" in result:
#             insert_query += f'<{result["id"]["value"]}> <http://www.w3.org/2004/02/skos/core#definition> "{result["definition"]["value"]}" .\n'
#         if "deprecationDate" in result:
#             insert_query += f'<{result["id"]["value"]}> <http://data.15926.org/meta/valDeprecationDate> "{result["deprecationDate"]["value"]}" .\n'
#         if "parentId" in result:
#             insert_query += f'<{result["id"]["value"]}> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <{result["parentId"]["value"]}> .\n'

#         insert_query += "}"
#         sparql.setQuery(insert_query)
#         sparql.query()