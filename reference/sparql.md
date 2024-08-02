# Using sparql queries to get RDF data

Some common sparql queries used for the CITS3200 ISO RDL visualisation project.

## Things of note

-   Currently, the sparql [endpoint](https://data.15926.org/sparql) only returns the first 10,000 lines of output, and the limit cannot be set to be higher. Some of the data might be excluded because of this limit.

## Queries

### Get class-parentClass-metatype, within the rdl endpoint

Out of only the entries in http://data.15926.org/rdl
So excluding those with URIs like:

-   http://data.15926.org/dm/PossibleIndividual
    (PossibleIndividual) or
-   https://data.15926.org/commodity/RDS575729 (2 ETHOXY ETHANOL)

Note: The name '**metatype**' used here is the type of the class, but only if it is a Class of Class (basically a metaclass). Here is the list of [Class of Classes](https://data.15926.org/rdl/RDS2226564).

Other **named graphs** can be found in the [404 response](https://data.15926.org/abcd) when a bad query is sent.

```
PREFIX meta: <http://data.15926.org/meta/>
SELECT ?id ?label ?parentId ?parentLabel ?metatypeId ?metatypeLabel
{graph <http://data.15926.org/rdl>{
    ?id rdfs:label ?label.
    FILTER (NOT EXISTS {?id meta:valDeprecationDate ?_})

    ?id rdfs:subClassOf ?parentId.
    ?parentId rdfs:label ?parentLabel.
    FILTER (NOT EXISTS {?parentId meta:valDeprecationDate ?_})

    {graph ?metatype{?id rdf:type ?metatypeId}}
    ?metatypeId rdfs:label ?metatypeLabel.
}}
ORDER BY ASC(?label)
```

### Get class-parentClass-metatype, within all available data

Like the above query, but uses all named graphs available to the endpoint instead of just rdl.

```
PREFIX meta: <http://data.15926.org/meta/>
SELECT ?id ?label ?parentId ?parentLabel ?metatypeId ?metatypeLabel
WHERE {
    ?id rdfs:label ?label.
    FILTER (NOT EXISTS {?id meta:valDeprecationDate ?_})

    ?id rdfs:subClassOf ?parentId.
    ?parentId rdfs:label ?parentLabel.
    FILTER (NOT EXISTS {?parentId meta:valDeprecationDate ?_})

    {graph ?metatype{?id rdf:type ?metatypeId}}
    ?metatypeId rdfs:label ?metatypeLabel.
}
ORDER BY ASC(?label)
```

### Search for label

Search for a specific entry using its label, and output it's URI. Searches in all named graphs available to the endpoint.
Replace "YourLabelHere" with the label string you want to search for.

```
SELECT ?id
WHERE {
    ?id rdfs:label ?label.
    FILTER (str(?label) = "YourLabelHere")
}
```
