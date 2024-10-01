from app.controllers import get_root_node
from app.config import Config


def test_database_initialized(sample_graph):
    """
    Test that the RDFLib graph is initialized with expected triples.
    """
    assert sample_graph, "The graph should exist."
    assert len(sample_graph) > 0, "The graph should be initialized with triples."


def test_root_node_set():
    """
    Test configuration is set correctly and the root node is set to 'http://data.15926.org/dm/Thing'
    """
    root_node = get_root_node()

    assert (
        root_node == "http://data.15926.org/dm/Thing"
    ), "'Thing' should be the root of the node in the configuration."


def test_database_config_set():
    """
    Test database configuration is set correctly for history file and storage location.
    """
    # Ensure that the history file is correctly set
    # assert Config.DB_HISTORY_FILE, "History file must be set in configuration."

    # Ensure that the storage directory path is correctly set
    assert (
        Config.DB_STORAGE_DIR
    ), "Database storage directory path must be set in configuration."

    # Ensure ROOT_NODE_URI is properly configured
    assert (
        Config.ROOT_NODE_URI == "http://data.15926.org/dm/Thing"
    ), "ROOT_NODE_URI should be correctly set."
