# Imports
from rdflib import Literal, URIRef, BNode


def sanitise_literal(value):
    value = value.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return value


def test_new_database(graph):
    """
    Runs a series of tests on the RDFLib graph to ensure the integrity and correctness
    of the data that has been imported. This includes tests for graph length, namespace
    validity, unique subjects, and SPARQL query execution.
    """
    try:
        test_length(graph)
        test_predicate_namespace(graph)
        test_unique_subject_identifiers(graph)
        test_blank_nodes(graph)
        test_literal_values(graph)
        test_sparql_query(graph)
        test_included_graphs(graph)
        test_core_nodes(graph)

    except Exception as e:
        # Re-raise the issue so that the database controller can handle it
        raise


def test_length(graph):
    """
    Asserts that the graph is not empty and that it contains at least 100 triples.
    This ensures that a substantial amount of data has been downloaded.
    """
    assert len(graph) > 0, "The graph is empty. No tripples were inserted."
    assert (
        len(graph) > 100
    ), "Database is not correctly downloaded, its length is less than 100."


def test_predicate_namespace(graph):
    """
    Ensures that all predicates (the second element in RDF triples) are valid IRIs
    by asserting that they start with either 'http://' or 'https://'.
    """
    for subj, pred, obj in graph:
        assert pred.startswith("http://") or pred.startswith(
            "https://"
        ), f"Invalid predicate IRI: {pred}"


def test_unique_subject_identifiers(graph):
    """
    Collects all unique subjects in the graph and asserts that there is at least one unique subject.
    This test ensures that the data contains distinct resources.
    """
    subjects = set()
    for subj, _, _ in graph:
        subjects.add(subj)

    assert len(subjects) > 0, "No unique subjects found in the graph."


def test_blank_nodes(graph):
    """
    Checks that there are no blank nodes (anonymous nodes) in the subject or object positions
    of any triples in the graph. This ensures that all subjects and objects are fully identified by IRIs.
    """
    for subj, _, obj in graph:
        assert not isinstance(subj, BNode), f"Blank node found in subject: {subj}"
        if isinstance(obj, BNode):
            assert False, f"Blank node found in object: {obj}"


def test_literal_values(graph):
    """
    Ensures that all literal values (objects in the triples that are literals) are sanitized.
    This removes control characters such as newlines, carriage returns, and tabs.
    """
    for subj, pred, obj in graph:
        if isinstance(obj, Literal):
            sanitized_value = sanitise_literal(str(obj))
            assert str(obj) == sanitized_value, f"Invalid literal value: {obj}"


def test_sparql_query(graph):
    """
    Executes a SPARQL query on the graph to check for the presence of triples where the
    subject starts with one of the expected namespaces (rdl, dm, lci). The test
    asserts that at least one result is returned.
    """
    test_query = """
    SELECT ?s ?p ?o
    WHERE {
        ?s ?p ?o .
        FILTER (
            STRSTARTS(STR(?s), "http://data.15926.org/rdl/") ||
            STRSTARTS(STR(?s), "http://data.15926.org/dm/") ||
            STRSTARTS(STR(?s), "http://data.15926.org/lci/")
        )
    } LIMIT 1
    """

    query_result = graph.query(test_query)
    assert (
        len(query_result) > 0
    ), "SPARQL query returned no results for the specified namespaces."


def test_included_graphs(graph):
    """
    Ensures that subjects from each of the expected namespaces (/rdl/, /dm/, /lci/)
    are present in the graph. It asserts that there is at least one subject from each namespace.
    """
    namespaces = [
        "http://data.15926.org/rdl/",
        "http://data.15926.org/dm/",
        "http://data.15926.org/lci/",
    ]
    # DONT TEST FOR `/coco` as thats purely for further types and doesnt have nodes in it

    # Check if there are any subjects from each namespace
    for ns in namespaces:
        found = False
        for subj, _, _ in graph:
            if isinstance(subj, URIRef) and str(subj).startswith(ns):
                found = True
                break
        assert found, f"No subjects found in graph for namespace: {ns}"


def test_core_nodes(graph):
    """
    Asserts that the core node ('Thing' in the 'dm' namespace) is present in the graph.
    This ensures that essential entities from the source data are included.
    """
    thing_uri = URIRef("http://data.15926.org/dm/Thing")

    # Check if there is any triple where 'Thing' is the subject
    assert any(
        graph.triples((thing_uri, None, None))
    ), "The 'Thing' node is missing from the graph."
