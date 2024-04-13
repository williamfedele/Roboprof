from sparql_fuseki_manager import FusekiManager
from constants import FUSEKI_BASE_URL, DATASET_NAME

class QueryManager:
    def __init__(self):
        self.fuseki_manager = FusekiManager()
        self.prefixes = """
        PREFIX vivo: <http://vivoweb.org/ontology/core#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX focu: <http://focu.io/schema#>
        """

    def make_query(self, query):
        print("Querying...")
        return self.fuseki_manager.query(query, self.prefixes)




    def example_query(self):
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
        return self.make_query(query)

if __name__ == "__main__":
    fm = FusekiManager()
    qm = QueryManager(fm)
    print(qm.example_query().text)
