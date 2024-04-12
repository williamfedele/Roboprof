import requests
from constants import FUSEKI_BASE_URL


def make_query(query):
    rows = requests.get(FUSEKI_BASE_URL, params={'query': query})
    return rows


# this is just an example. TODO: remove
def query2():
    
    # paste query here
    query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX vivo: <http://vivoweb.org/ontology/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX focu: <http://focu.io/schema#>

SELECT ?course ?event ?count
WHERE 
{
  ?course rdf:type vivo:Course .
  ?lecture focu:lectureBelongsTo ?course ;
           focu:hasContent ?event .
  ?topic focu:provenance ?event ;
	rdfs:seeAlso <https://www.wikidata.org/wiki/Q1367488> .
  ?event ?mentionid ?topic .
  ?mentionid focu:mentionCount ?count .
} 
ORDER BY DESC(?count)
        """

    rows = make_query(query)

    return rows


if __name__ == "__main__":
    print(query2().text)