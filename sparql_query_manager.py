from sparql_fuseki_manager import FusekiManager

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
        return self.fuseki_manager.query(query, self.prefixes)

    def query_about_course(self, subject, number):
        query = f"SELECT ?description WHERE {{ ?course focu:courseSubject '{subject}' . ?course focu:courseNumber '{number}' . ?course focu:courseDescription ?description }} LIMIT 1"
        response = self.make_query(query)
        if response == None:
            return None

        data = response.json()['results']['bindings']
        if data:
            return data[0]['description']['value']
        
        return None


if __name__ == "__main__":
    qm = QueryManager()
    print(qm.query_about_course("COMP", "474"))
