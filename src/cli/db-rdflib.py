import time
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal


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


# Store the SPARQL query results into the RDF graph.
def store_results_to_graph(graph, results):
    for result in results["results"]["bindings"]:
        s = URIRef(result["id"]["value"])
        p_label = URIRef("http://www.w3.org/2000/01/rdf-schema#label")
        p_type = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
        graph.add((s, p_label, Literal(result["label"]["value"])))
        graph.add((s, p_type, URIRef(result["type"]["value"])))

        if "definition" in result:
            p_definition = URIRef("http://www.w3.org/2004/02/skos/core#definition")
            graph.add((s, p_definition, Literal(result["definition"]["value"])))

        if "deprecationDate" in result:
            p_deprecationDate = URIRef("http://data.15926.org/meta/valDeprecationDate")
            graph.add(
                (s, p_deprecationDate, Literal(result["deprecationDate"]["value"]))
            )

        if "parentId" in result:
            p_parentId = URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf")
            graph.add((s, p_parentId, URIRef(result["parentId"]["value"])))


# Save the RDF graph to a file in the specified format.
def save_graph_to_file(graph, file_path, format="turtle"):
    with open(file_path, "w") as f:
        f.write(graph.serialize(format=format))
    print(f"\nGraph serialised to '{file_path}'.")


def main():
    endpoint_url = "http://190.92.134.58:8890/sparql"
    turtle_file_path = "graph.ttl"
    batch_size = 5
    offset = 0
    total_triples = 0

    # Start timing
    start_time = time.time()

    # Create an RDF graph
    g = Graph()

    while True:
        # Fetch data from SPARQL endpoint
        results = execute_sparql_query(endpoint_url, offset, batch_size)

        print("RESULTS\n\n")
        print(results)
        print("results2\n\n")
        print(results["results"])
        print("bingings\n\n")
        print(results["results"]["bindings"])

        # If no results are returned, break the loop
        if not results["results"]["bindings"]:
            break

        # Store the results in the graph
        store_results_to_graph(g, results)

        # Increment the offset for the next batch
        offset += batch_size

        # Update the total triples count
        total_triples += len(results["results"]["bindings"])
        print(
            f"Fetched {len(results['results']['bindings'])} triples. Total so far: {total_triples}."
        )

    # Save the RDF graph to a file
    save_graph_to_file(g, turtle_file_path, format="turtle")

    # End timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTotal triples in graph: {len(g)}")
    print(f"Time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
