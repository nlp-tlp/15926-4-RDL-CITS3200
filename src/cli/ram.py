import psutil
import os

# Function to get current memory usage
def get_memory_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss  # Resident Set Size: the actual memory in use

# Example usage
if __name__ == "__main__":
    # Get memory usage in bytes
    memory_usage_before = get_memory_usage()

    # Perform your operations (e.g., load a large Turtle file into RAM)
    from rdflib import Graph
    g = Graph()
    g.parse("graph.ttl", format="turtle")

    # Get memory usage after loading the data
    memory_usage_after = get_memory_usage()

    # Print memory usage in megabytes
    print(f"Memory usage before loading data: {memory_usage_before / (1024 ** 2):.2f} MB")
    print(f"Memory usage after loading data: {memory_usage_after / (1024 ** 2):.2f} MB")
    print(f"Memory increase: {(memory_usage_after - memory_usage_before) / (1024 ** 2):.2f} MB")
