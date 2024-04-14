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

        data = response.json()["results"]["bindings"]
        if data:
            return data[0]["description"]["value"]

        return None

    def query_course_event_topics(self, event, eventNumber, courseSubject, courseNumber):

        # we only have lecture content right now
        lecture_variants = ["lecture", "lec"]
        if event.lower() not in lecture_variants:
            return None

        query = f"""
            SELECT ?topicName ?topic ?resource
            WHERE 
            {{
            ?course rdf:type vivo:Course .
            ?course focu:courseSubject "{courseSubject.upper()}" .
            ?course focu:courseNumber "{courseNumber}" .
            ?event rdf:type focu:Lecture ;
                        focu:lectureBelongsTo ?course ;
                        focu:lectureNumber {eventNumber} ;
                        focu:hasContent ?resource .
            ?topic focu:provenance ?resource .
            ?topic focu:topicName ?topicName ;
            }}
            ORDER BY ?topicName
        """
        response = self.make_query(query)
        if response == None:
            return None

        return response.json()["results"]["bindings"]

    def query_covers_topic(self, topic_name):

        query = f"""
            SELECT ?course ?event (COUNT(?topic) AS ?count)
            WHERE 
            {{
            ?course rdf:type vivo:Course .
            ?event focu:lectureBelongsTo ?course ;
                    focu:hasContent ?resource .
            ?topic focu:provenance ?resource .
            ?topic focu:topicName ?topicName ;
            filter contains(lcase(?topicName), "{topic_name.lower()}")
            }}
            GROUP BY ?course ?event
            ORDER BY DESC(?count)
        """
        response = self.make_query(query)
        if response == None:
            return None
        return response.json()["results"]["bindings"]
    
    def query_courses_offered_by(self, uni_name):

        query = f"""
            SELECT ?course ?name 
            WHERE 
            {{
                ?course rdf:type vivo:Course .
                ?course vivo:offeredBy ?uni .
                ?uni rdfs:label ?uni_name .  
                ?course focu:courseName ?name .
                filter contains(lcase(?uni_name), "{uni_name.lower()}")
            }}
        """
        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        courses = [f"{row['course']['value']}, {row['name']['value']}" for row in response]
        response_msg = "Here's what I found:\n" + "\n".join(courses)

        return response_msg
    
    def query_courses_covering_topic(self, topic_name):

        query = f"""
            SELECT DISTINCT ?course 
            WHERE 
            {{
                ?topic rdf:type focu:Topic .
                ?topic focu:provenance ?resource .
                ?topic focu:topicName ?topicName .
                ?event focu:hasContent ?resource .
                ?event focu:lectureBelongsTo ?course .
                filter contains(lcase(?topicName), "{topic_name.lower()}")
            }}
        """
        response = self.make_query(query)        
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        topics = [f"{row['course']['value']}" for row in response]
        response_msg = f"I found {topic_name} discussed here:\n" + "\n".join(topics)

        return response_msg


if __name__ == "__main__":
    qm = QueryManager()
    print(qm.query_courses_offered_by("concordia"))
