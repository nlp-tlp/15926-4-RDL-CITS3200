import time
import csv
import logging
import psutil
from io import StringIO
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SKOS
from SPARQLWrapper import SPARQLWrapper, CSV

# Set up logging to a file
logging.basicConfig(filename='rdflib_insertion_errors.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URI = "http://data.15926.org/iso/"

# Set up namespaces
ISO = Namespace("http://data.15926.org/meta/")

# Initialize the RDFLib graph
graph = Graph()

# Helper function to ensure IRIs are absolute
def ensure_absolute_iri(iri, base_uri=BASE_URI):
    if not iri.startswith("http://") and not iri.startswith("https://"):
        return base_uri + iri
    return iri

# Sanitize the literal by replacing control characters
def sanitize_literal(value):
    value = value.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return value

# Monitor memory usage and log it periodically
def monitor_memory_usage(message=""):
    memory_info = psutil.Process().memory_info()
    memory_usage_mb = memory_info.rss / (1024 * 1024)  # Convert from bytes to MB
    logging.info(f"{message} - Memory Usage: {memory_usage_mb:.2f} MB")

# Execute the SPARQL query and retrieve results in CSV format
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
    result_csv = sparql.query().convert().decode('utf-8')
    return result_csv

# Insert the SPARQL query results into the RDFLib graph
def insert_results_into_rdflib(results_csv):
    # Parse the CSV data
    csv_reader = csv.DictReader(StringIO(results_csv))

    for result in csv_reader:
        try:
            # Ensure IRIs are absolute
            subject_iri = URIRef(ensure_absolute_iri(result['id']))
            type_iri = URIRef(ensure_absolute_iri(result['type']))
            parent_id_iri = URIRef(ensure_absolute_iri(result['parentId'])) if result['parentId'] else None

            # Sanitize and validate literals
            label = Literal(sanitize_literal(result['label'])) if result.get('label') else None
            definition = Literal(sanitize_literal(result['definition'])) if result.get('definition') else None
            deprecation_date = Literal(sanitize_literal(result['deprecationDate'])) if result.get('deprecationDate') else None

            # Add triples to the RDFLib graph
            if label:
                graph.add((subject_iri, RDFS.label, label))
                graph.add((subject_iri, RDF.type, type_iri))
            if definition:
                graph.add((subject_iri, SKOS.definition, definition))
            if deprecation_date:
                graph.add((subject_iri, ISO.valDeprecationDate, deprecation_date))
            if parent_id_iri:
                graph.add((subject_iri, RDFS.subClassOf, parent_id_iri))

        except Exception as e:
            logging.error(f"Error processing result: {result}")
            logging.error(f"Exception: {e}")
            continue  # Skip to the next result

# Save the RDFLib graph to a file (in Turtle format)
def save_graph_to_file(file_path):
    graph.serialize(destination=file_path, format='turtle')

# Main update function that fetches SPARQL data and inserts it into the RDFLib graph
def update_db_to_rdflib():
    sparql_endpoint_url = "http://190.92.134.58:8890/sparql"
    batch_size = 10000
    offset = 0
    total_triples = 0

    # Start timing
    start_time = time.time()

    while True:
        monitor_memory_usage("Before fetching new batch")

        # Fetch data from the SPARQL endpoint in CSV format
        results_csv = execute_sparql_query(sparql_endpoint_url, offset, batch_size)

        # If no results are returned, break the loop
        num_lines = results_csv.count('\n') - 1  # Number of lines minus header

        if num_lines == 0:
            print("No new data fetched; stopping the process.")
            break

        # Insert the results into RDFLib
        insert_results_into_rdflib(results_csv)

        # Increment the offset for the next batch
        offset += batch_size

        # Update the total triples count
        total_triples += num_lines
        print(f"Inserted {num_lines} triples. Total so far: {total_triples}.")

        monitor_memory_usage(f"After inserting {num_lines} triples")

    # Save the RDFLib graph to a file after processing all batches
    save_graph_to_file("iso15926_ontology.ttl")

    # End timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTotal triples inserted: {total_triples}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    monitor_memory_usage("Final memory usage after entire process")

# Run the update process when the script is executed
if __name__ == "__main__":
    update_db_to_rdflib()
