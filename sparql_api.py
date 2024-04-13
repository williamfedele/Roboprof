import requests
from constants import FUSEKI_BASE_URL

headers = """
    PREFIX vivo: <http://vivoweb.org/ontology/core#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX focu: <http://focu.io/schema#>
    """
    


def make_query(query):
    rows = requests.get(FUSEKI_BASE_URL, params={'query': headers + query})
    return rows

# this is just an example. TODO: remove
def query2():
    
    # paste query here
    query = """
SELECT ?course ?event (COUNT(?topic) AS ?count)
WHERE 
{
  ?course rdf:type vivo:Course .
  ?event focu:lectureBelongsTo ?course ;
           focu:hasContent ?resource .
  ?topic focu:provenance ?resource .
  ?topic focu:topicName ?topicName ;
         rdfs:seeAlso <https://www.wikidata.org/wiki/Q326342> .
} 
GROUP BY ?course ?event
ORDER BY DESC(?count)
        """

    rows = make_query(query)

    return rows


if __name__ == "__main__":
    print(query2().text)