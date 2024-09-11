import time
import csv
import requests
import logging
from io import StringIO
from SPARQLWrapper import SPARQLWrapper, CSV

# Set up logging to a file
logging.basicConfig(
    filename="graphdb_insertion_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

BASE_URI = "http://data.15926.org/iso/"


# Helper function to ensure IRIs are absolute
def ensure_absolute_iri(iri, base_uri=BASE_URI):
    if not iri.startswith("http://") and not iri.startswith("https://"):
        return base_uri + iri
    return iri


# Sanitize the literal by replacing control characters
def sanitize_literal(value):
    # Replace newline, tab, and carriage return characters with spaces or escape sequences
    value = value.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return value


# Execute the SPARQL query and retrieve results in CSV format.
def execute_sparql_query(endpoint_url, offset=0, limit=10000):
    sparql = SPARQLWrapper(endpoint_url)
    query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX meta: <http://data.15926.org/meta/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT DISTINCT ?id ?label ?type ?definition ?parentId ?deprecationDate
        WHERE {{
          GRAPH <http://data.15926.org/rdl> {{
            ?id rdfs:label ?label.
            ?id rdf:type ?type.
            OPTIONAL {{ ?id skos:definition ?definition. }}
            OPTIONAL {{ ?id meta:valDeprecationDate ?deprecationDate. }}
            OPTIONAL {{ ?id rdfs:subClassOf ?parentId. }}
          }}
        }}
        LIMIT {limit}
        OFFSET {offset}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(CSV)

    # Execute the query and return the results as CSV
    result_csv = sparql.query().convert().decode("utf-8")
    return result_csv


# Insert the SPARQL query results into GraphDB.
def insert_results_into_graphdb(endpoint_url, results_csv, graph_uri):
    # Parse the CSV data
    csv_reader = csv.DictReader(StringIO(results_csv))

    # Initialize a list to collect multiple INSERT DATA statements
    bulk_insert_query = f"INSERT DATA {{ GRAPH <{graph_uri}> {{\n"

    for result in csv_reader:
        try:
            # Ensure IRIs are absolute
            subject_iri = ensure_absolute_iri(result["id"])
            type_iri = ensure_absolute_iri(result["type"])
            parent_id_iri = (
                ensure_absolute_iri(result["parentId"]) if result["parentId"] else None
            )

            # Sanitize and validate literals
            label = sanitize_literal(result["label"]) if result.get("label") else None
            definition = (
                sanitize_literal(result["definition"])
                if result.get("definition")
                else None
            )
            deprecation_date = (
                sanitize_literal(result["deprecationDate"])
                if result.get("deprecationDate")
                else None
            )

            # Construct the SPARQL update for each triple, using sanitized values
            if label:
                bulk_insert_query += f"""
                    <{subject_iri}> <http://www.w3.org/2000/01/rdf-schema#label> "{label}" .
                    <{subject_iri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{type_iri}> .
                """
            if definition:
                bulk_insert_query += f'<{subject_iri}> <http://www.w3.org/2004/02/skos/core#definition> "{definition}" .\n'
            if deprecation_date:
                bulk_insert_query += f'<{subject_iri}> <http://data.15926.org/meta/valDeprecationDate> "{deprecation_date}" .\n'
            if parent_id_iri:
                bulk_insert_query += f"<{subject_iri}> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <{parent_id_iri}> .\n"

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
            raise Exception(
                f"Failed to insert data. Status Code: {response.status_code}. Response: {response.text}"
            )

    except Exception as e:
        logging.error("Failed to execute the SPARQL update query.")
        logging.error(f"SPARQL query: {bulk_insert_query}")
        logging.error(f"Exception: {e}")
        raise  # Re-raise the exception after logging


def update_db():
    endpoint_url = "http://190.92.134.58:8890/sparql"
    graphdb_endpoint_url = (
        "http://localhost:7200/repositories/deployment/statements"  # GraphDB repository
    )
    graph_uri = "http://iso15926vis.org/graph/" + "proper"
    batch_size = 10000
    offset = 0
    total_triples = 0

    # Start timing
    start_time = time.time()

    while True:
        # Fetch data from the SPARQL endpoint in CSV format
        results_csv = execute_sparql_query(endpoint_url, offset, batch_size)

        # If no results are returned, break the loop
        num_lines = results_csv.count("\n") - 1  # Number of lines minus header

        if num_lines == 0:
            print("No new data fetched; stopping the process.")
            break

        # Insert the results directly into GraphDB
        insert_results_into_graphdb(
            graphdb_endpoint_url, results_csv, graph_uri=graph_uri
        )

        # Increment the offset for the next batch
        offset += batch_size

        # Update the total triples count
        total_triples += num_lines
        print(f"Inserted {num_lines} triples. Total so far: {total_triples}.")

    # End timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTotal triples inserted: {total_triples}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
