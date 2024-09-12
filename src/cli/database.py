import time
import os
import csv
import logging
import yaml
import psutil
from io import StringIO
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SKOS
from SPARQLWrapper import SPARQLWrapper, CSV

from history import history_add_db, get_next_db_filename  # Import history functions

BASE_URI = "http://data.15926.org/iso/"
META = Namespace("http://data.15926.org/meta/")  # Set up namespace for `/meta`

# Load the config file
with open("../db/config.yml", "r") as file:
    config = yaml.safe_load(file)

# Set up logging based on config file
log_level = getattr(
    logging, config.get("log_level", "WARNING").upper(), logging.WARNING
)
logging.basicConfig(
    filename="database.log",
    level=log_level,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


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
    logging.debug(f"{message} - Memory Usage: {memory_usage_mb:.2f} MB")


# Execute the SPARQL query and retrieve results in CSV format
def execute_sparql_query(endpoint_url, offset=0, limit=10000):
    sparql = SPARQLWrapper(endpoint_url)
    query = config["query_source"]
    query += f"\nLIMIT {limit}\nOFFSET {offset}"
    sparql.setQuery(query)
    sparql.setReturnFormat(CSV)

    # Execute the query and return the results as CSV
    result_csv = sparql.query().convert().decode("utf-8")
    logging.debug(
        f"SPARQL query executed successfully with OFFSET {offset} and LIMIT {limit}."
    )
    return result_csv


# Insert the SPARQL query results into the RDFLib graph
def insert_results_into_rdflib(graph, results_csv):
    # Parse the CSV data
    csv_reader = csv.DictReader(StringIO(results_csv))

    for result in csv_reader:
        try:
            # Ensure IRIs are absolute
            subject_iri = URIRef(ensure_absolute_iri(result["id"]))  # The subject (id)
            predicate_iri = URIRef(
                ensure_absolute_iri(result["predicate"])
            )  # The predicate
            object_value = result["object"]

            # Determine whether the object is an IRI or a literal
            if object_value.startswith("http://") or object_value.startswith(
                "https://"
            ):
                object_iri = URIRef(ensure_absolute_iri(object_value))
                graph.add(
                    (subject_iri, predicate_iri, object_iri)
                )  # Add triple with IRI object
            else:
                # If it's a literal, sanitize it and add it as a literal
                sanitized_object = sanitize_literal(object_value)
                graph.add(
                    (subject_iri, predicate_iri, Literal(sanitized_object))
                )  # Add triple with literal object

        except Exception as e:
            logging.error(f"Error processing result: {result}")
            logging.error(f"Exception: {e}")
            continue  # Skip to the next result

    logging.debug(
        f"Finished inserting results into RDFLib graph. True total length: {len(graph)}"
    )


# Save the RDFLib graph to a file with a dynamic filename
def save_graph_to_file(graph):

    # Path to the storage directory
    storage_dir = "../db/storage"

    # Ensure the storage directory exists, create it if not
    os.makedirs(storage_dir, exist_ok=True)

    # Get the next available filename from history
    db_filename = (
        get_next_db_filename()
    )  # This returns the filename and updates the history

    # Save the graph using the generated filename
    graph.serialize(destination=os.path.join(storage_dir, db_filename), format="turtle")
    logging.info(f"Graph saved to '{db_filename}'.")
    return db_filename


# Main update function that fetches SPARQL data and inserts it into the RDFLib graph
def update_db():
    sparql_endpoint_url = config["sparql_endpoint_url"]
    batch_size = config["batch_size"]
    offset = 0
    total_triples = 0
    success = 0

    # Start timing
    start_time = time.time()
    logging.debug("Starting the database update process.")

    # Check memory first
    monitor_memory_usage("Before updating database")

    # Initialize the RDFLib graph
    graph = Graph()

    try:
        while True:
            # Fetch data from the SPARQL endpoint in CSV format
            results_csv = execute_sparql_query(sparql_endpoint_url, offset, batch_size)

            # If no results are returned, break the loop
            num_lines = results_csv.count("\n") - 1  # Number of lines minus header

            if num_lines == 0:
                print("No new data fetched; stopping the process.")
                break

            # Insert the results into RDFLib
            insert_results_into_rdflib(graph=graph, results_csv=results_csv)

            # Increment the offset for the next batch
            offset += batch_size

            # Update the total triples count
            total_triples += num_lines
            print(f"Inserted {num_lines} triples. Total so far: {total_triples}.")

    except Exception as e:
        logging.critical(f"An error occurred during the update process: {e}")
        print(f"An error occurred: {e}")
        return  # Exit the function to avoid saving an incomplete database

    else:
        try:
            # Save the RDFLib graph to a file after processing all batches
            db_filename = save_graph_to_file(graph=graph)

            # End timing
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Get true graph length
            true_length = len(graph)

            print(
                f"\nTotal triples inserted: {total_triples} (True length: {true_length})"
            )
            print(f"Database saved as: {db_filename}")
            print(f"Time taken: {elapsed_time:.2f} seconds")

            # History update happens here only after everything was successful
            if true_length > 0:
                print("Updating the history file with the new database.")
                history_add_db(
                    filename=db_filename
                )  # Ensure history is updated after database is saved successfully
                logging.info("Updating the history file with the new database.")
                success = 1
            else:
                print("No data was fetched, so the history will not be updated.")
                logging.warning(
                    "No data was fetched, so the history will not be updated."
                )

        except Exception as save_error:
            logging.critical(
                f"An error occurred while saving the database: {save_error}"
            )
            print(f"Failed to save the database: {save_error}")
            return  # Exit the function if saving fails to avoid history update

    finally:
        # Always check memory usage at the end, even if errors occur
        monitor_memory_usage("Final memory usage after update process")
        logging.debug(
            f"Database update process completed with status: {'SUCCESS' if success else 'FAILURE'}."
        )
