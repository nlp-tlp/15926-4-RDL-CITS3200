import os

basedir = os.path.abspath(os.path.dirname(__file__))

HISTORY_FILE = os.path.join(basedir, "../db/history.json")
HISTORY_VERSION = 1
DATABASE_STORAGE_DIR = os.path.join(basedir, "../db/storage")

SOURCE_OF_TRUTH = "http://190.92.134.58:8890/sparql"
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
