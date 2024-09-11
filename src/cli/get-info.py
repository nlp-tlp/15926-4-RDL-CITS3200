import json
import csv
import random
from io import StringIO
from SPARQLWrapper import SPARQLWrapper, CSV


# Function to get hierarchical data from GraphDB
def fetch_hierarchical_data_from_graphdb(
    graphdb_endpoint_url, graph_uri, limit=10000, offset=0
):
    sparql = SPARQLWrapper(graphdb_endpoint_url)

    query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX meta: <http://data.15926.org/meta/>

        SELECT DISTINCT ?id ?label ?parentId
        WHERE {{
            GRAPH <{graph_uri}> {{
                ?id rdf:type ?type.
                ?id rdfs:label ?label.
                OPTIONAL {{ ?id rdfs:subClassOf ?parentId . }}
                FILTER NOT EXISTS {{ ?id meta:valDeprecationDate ?deprecationDate }}
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


# Build a dictionary of nodes and edges from the SPARQL CSV results, adding random x and y coordinates
def build_nodes_and_edges(results_csv, existing_node_ids):
    csv_reader = csv.DictReader(StringIO(results_csv))
    nodes = []
    edges = []

    for row in csv_reader:
        node_id = row["id"]
        label = row["label"]
        parent_id = row.get("parentId")

        # Ensure node ID is unique before adding
        if node_id not in existing_node_ids:
            existing_node_ids.add(node_id)  # Mark this node as added
            # Add the node to the nodes list
            nodes.append(
                {
                    "id": node_id,
                    "name": label,
                    # 'x': random.uniform(-1000, 1000),  # Random x coordinate
                    # 'y': random.uniform(-1000, 1000),  # Random y coordinate
                }
            )

        # Add the edge if the parent ID exists
        if parent_id:
            edges.append({"source": node_id, "target": parent_id})

    return nodes, edges


# Fetch and process data in batches from GraphDB
def get_hierarchical_data_from_graphdb(graphdb_endpoint_url, graph_uri):
    batch_size = 10000
    offset = 0
    all_nodes = []
    all_edges = []
    existing_node_ids = set()  # To keep track of already added node IDs

    # Fetch all data in batches
    while True:
        # Fetch data from GraphDB
        results_csv = fetch_hierarchical_data_from_graphdb(
            graphdb_endpoint_url, graph_uri, limit=batch_size, offset=offset
        )

        # Check if there are no more results
        if results_csv.count("\n") <= 1:  # Only header or no results
            break

        # Parse nodes and edges from CSV data
        nodes, edges = build_nodes_and_edges(results_csv, existing_node_ids)

        # Add nodes and edges to the complete list
        all_nodes.extend(nodes)
        all_edges.extend(edges)

        # Increase the offset to fetch the next batch
        offset += batch_size

    return all_nodes, all_edges


# Save nodes and edges to a JSON file in the desired format
def save_graph_data_to_file(nodes, edges, file_path):
    data = {"nodes": nodes, "edges": edges}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Example usage
graphdb_endpoint_url = (
    "http://localhost:7200/repositories/deployment"  # GraphDB repository
)
graph_uri = "http://iso15926vis.org/graph/proper"

# Fetch hierarchical data
all_nodes, all_edges = get_hierarchical_data_from_graphdb(
    graphdb_endpoint_url, graph_uri
)

# Save the hierarchical data to a JSON file in the desired format
save_graph_data_to_file(all_nodes, all_edges, "data3-nodep-noxy.json")

print("Data saved to hierarchical_data.json")
