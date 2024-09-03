import json

def generate_dag(levels):
    nodes = []
    edges = []
    node_id = 1

    # Increased screen dimensions
    screen_width = 2000  # Increased width
    screen_height = 1200  # Increased height

    # Create the root node
    nodes.append({"id": "Root", "name": "Root", "x": 100, "y": screen_height // 2})

    # Generate nodes and edges level by level
    for level in range(1, levels + 1):
        num_nodes = 2 ** (level - 1)
        print(f"Level {level}: {num_nodes} nodes")
        
        # Adjust vertical and horizontal spacing based on the level
        y_offset = screen_height // (num_nodes + 1) * (1 + (level / levels) * 0.5)
        x_offset = screen_width // (levels + 1) * (1 + (level / levels) * 0.5)
        
        for i in range(num_nodes):
            parent_id = f"Node{level-1}-{(i//2)+1}" if level > 1 else "Root"
            node_id_str = f"Node{level}-{i+1}"
            nodes.append({"id": node_id_str, "name": node_id_str, "x": x_offset * level, "y": (screen_height // 2) + y_offset * (2 * i - num_nodes + 1)})
            edges.append({"source": node_id_str, "target": parent_id})

    # Add some additional edges to create a more complex DAG
    for level in range(2, levels + 1):
        num_nodes = 2 ** (level - 1)
        for i in range(num_nodes):
            if i % 2 == 0:
                source_id = f"Node{level}-{i+1}"
                target_id = f"Node{level-1}-{i//2+1}"
                edges.append({"source": source_id, "target": target_id})

    # Add backward edges to create more complexity
    for level in range(3, levels + 1):
        num_nodes = 2 ** (level - 1)
        for i in range(num_nodes):
            if i % 3 == 0:  # Add backward edges for every third node
                source_id = f"Node{level}-{i+1}"
                target_id = f"Node{level-2}-{i//4+1}"
                edges.append({"source": source_id, "target": target_id})

    print(f"Total number of nodes: {len(nodes)}")
    return {"nodes": nodes, "edges": edges}

def main():
    levels = 6  # Number of levels in the DAG
    dag = generate_dag(levels)

    with open('./src/assets/mockData.json', 'w') as f:
        json.dump(dag, f, indent=2)

if __name__ == "__main__":
    main()