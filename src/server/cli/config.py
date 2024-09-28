HISTORY_FILE = "../../db/history.json"
HISTORY_VERSION = 1
DATABASE_STORAGE_DIR = "../../db/storage/"

SOURCE_OF_TRUTH = "https://data.15926.org/sparql/"
BATCH_SIZE = 10000
LOG_LEVEL = "DEBUG"
SOURCE_QUERY = """
  SELECT DISTINCT ?id ?predicate ?object ?g
  WHERE {
    GRAPH ?g {
      ?id ?predicate ?object .
    }
    FILTER(?g IN (<http://data.15926.org/rdl>, <http://data.15926.org/dm>, <http://data.15926.org/coco>, <http://data.15926.org/lci>))
  }
  """
