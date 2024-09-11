import time
from SPARQLWrapper import SPARQLWrapper, JSON
from dotenv import load_dotenv
import os
from neo4j import GraphDatabase


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


# Insert the SPARQL query results directly into the Neo4j database in batches.
def insert_results_into_neo4j(driver, results, version, batch_size=100):
    with driver.session() as session:
        batch = []
        node_counter = 0

        for result in results["results"]["bindings"]:
            # Generate a unique variable name for each node
            node_var = f"n{node_counter}"
            node_counter += 1

            # Prepare the Cypher query for the node
            uri = result["id"]["value"]
            label = result["label"]["value"]
            node_type = result["type"]["value"]
            node_query = f"""
            MERGE ({node_var}:Resource:{version} {{uri: '{uri}'}})
            SET {node_var}.label = '{label}',
                {node_var}.type = '{node_type}'
            """

            if "definition" in result:
                definition = result["definition"]["value"].replace('"', '\\"')
                node_query += f", {node_var}.definition = '{definition}'"

            if "deprecationDate" in result:
                deprecation_date = result["deprecationDate"]["value"]
                node_query += f", {node_var}.deprecationDate = '{deprecation_date}'"

            batch.append(node_query)

            if "parentId" in result:
                parent_id = result["parentId"]["value"]
                parent_var = f"p{node_counter}"  # Generate a unique variable name for the parent node
                parent_query = f"""
                WITH {node_var}
                MATCH ({parent_var}:Resource:{version} {{uri: '{parent_id}'}})
                MERGE ({node_var})-[:SUBCLASS_OF]->({parent_var})
                """
                batch.append(parent_query)

            # If the batch reaches the batch_size, execute the batch
            if len(batch) >= batch_size:
                session.write_transaction(run_batch_query, batch)
                batch.clear()

        # Run the remaining queries in the batch
        if batch:
            session.write_transaction(run_batch_query, batch)


def run_batch_query(tx, batch):
    # Join the batch of queries into one large Cypher query
    query = "\n".join(batch)
    tx.run(query)


def update_db():
    endpoint_url = "http://190.92.134.58:8890/sparql"
    neo4j_uri = "bolt://localhost:7687"  # Neo4j URI
    neo4j_user = "neo4j"  # Neo4j username
    neo4j_password = "my_password"  # Neo4j password
    version = "v2"  # Version label
    batch_size = 10000
    offset = 0
    total_triples = 0

    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    # Start timing
    start_time = time.time()

    while True:
        # Fetch data from the SPARQL endpoint
        results = execute_sparql_query(endpoint_url, offset, batch_size)

        # If no results are returned, break the loop
        if not results["results"]["bindings"]:
            break

        # Insert the results directly into the Neo4j database in batches
        insert_results_into_neo4j(driver, results, version, batch_size=100)

        # Increment the offset for the next batch
        offset += batch_size

        # Update the total triples count
        total_triples += len(results["results"]["bindings"])
        print(
            f"Inserted {len(results['results']['bindings'])} triples. Total so far: {total_triples}."
        )

    # End timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTotal triples inserted: {total_triples}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

    driver.close()
