import time
import csv
import logging
import psutil  # Import psutil for monitoring system resources
from io import StringIO
from SPARQLWrapper import SPARQLWrapper, CSV
import owlready2
from owlready2 import get_ontology, Thing, sync_reasoner, types

# Set up logging to a file
logging.basicConfig(filename='ontology_insertion_errors.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Base URIs for ontology and SPARQL results
BASE_URI = "http://data.15926.org/iso/"
ONTOLOGY_IRI = "http://iso15926vis.org/ontology/"

# Create an Owlready2 ontology
onto = get_ontology(ONTOLOGY_IRI)

# Define the basic entity class in the ontology
with onto:
    class Entity(Thing):
        pass

# Helper function to ensure IRIs are absolute
def ensure_absolute_iri(iri, base_uri=BASE_URI):
    if not iri.startswith("http://") and not iri.startswith("https://"):
        return base_uri + iri
    return iri

# Sanitize the literal by replacing control characters
def sanitize_literal(value):
    value = value.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return value

# Helper function to get or create a class in the ontology
def get_or_create_class(iri):
    # Check if the class already exists in the ontology
    if iri in onto:
        return onto[iri]
    else:
        # Create a new class dynamically if it doesn't exist
        with onto:
            new_class = types.new_class(iri, (Thing,))
            return new_class

# Monitor RAM usage and log it periodically
def monitor_ram_usage():
    memory_info = psutil.virtual_memory()
    logging.info(f"RAM Usage: {memory_info.percent}% used ({memory_info.used / (1024 * 1024)} MB used out of {memory_info.total / (1024 * 1024)} MB total)")

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

# Insert the SPARQL query results into the Owlready2 ontology
def insert_results_into_ontology(results_csv):
    csv_reader = csv.DictReader(StringIO(results_csv))

    for result in csv_reader:
        try:
            subject_iri = ensure_absolute_iri(result['id'])
            type_iri = ensure_absolute_iri(result['type'])  # Still ensure it's absolute
            parent_id_iri = ensure_absolute_iri(result['parentId']) if result['parentId'] else None

            label = sanitize_literal(result['label']) if result.get('label') else None
            definition = sanitize_literal(result['definition']) if result.get('definition') else None
            deprecation_date = sanitize_literal(result['deprecationDate']) if result.get('deprecationDate') else None

            # Create the individual (entity)
            entity = Entity(iri=subject_iri)

            # Store the type_iri as a string literal property instead of creating a class
            if type_iri:
                entity.has_type = [type_iri]  # Create a new property to store the type as a string

            if label:
                entity.label = [label]
            if definition:
                entity.comment = [definition]
            if deprecation_date:
                entity.deprecationDate = deprecation_date

            # Handle parent ID if provided (this can still be treated as a class, if required)
            if parent_id_iri:
                parent_entity = Entity(iri=parent_id_iri)  # You can avoid class creation for parents
                entity.is_a.append(parent_entity)

        except Exception as e:
            logging.error(f"Error processing result: {result}")
            logging.error(f"Exception: {e}")
            continue

    # After adding entities, sync the reasoner to ensure consistency
    #sync_reasoner()

# Save the ontology to a file
def save_ontology_to_file(file_path):
    onto.save(file_path, format="rdfxml")

# Main update function that fetches SPARQL data and inserts it into the ontology
def update_db_to_ontology():
    sparql_endpoint_url = "http://190.92.134.58:8890/sparql"
    batch_size = 10000
    offset = 0
    total_triples = 0

    start_time = time.time()

    while True:
        monitor_ram_usage()  # Monitor RAM at the start of each loop

        results_csv = execute_sparql_query(sparql_endpoint_url, offset, batch_size)
        num_lines = results_csv.count('\n') - 1

        if num_lines == 0:
            print("No new data fetched; stopping the process.")
            break

        insert_results_into_ontology(results_csv)
        offset += batch_size
        total_triples += num_lines
        print(f"Inserted {num_lines} triples. Total so far: {total_triples}.")

    save_ontology_to_file("iso15926_ontology.owl")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTotal triples inserted: {total_triples}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

# Run the update process when the script is executed
if __name__ == "__main__":
    update_db_to_ontology()
