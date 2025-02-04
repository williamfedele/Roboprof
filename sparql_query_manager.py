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
            SELECT ?topicName ?resource
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
            LIMIT 10
        """
        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None
        
        topics = [f"{row['topicName']['value']} which can be found at {row['resource']['value']}." for row in response]
        response_message = "Here's what I found:\n" + "\n".join(topics)

        return response_message

    def query_covers_topic(self, topic_name):

        query = f"""
            SELECT ?subject ?number ?lecNumber (COUNT(?topic) AS ?count)
            WHERE 
            {{
            ?course rdf:type vivo:Course .
            ?course focu:courseSubject ?subject .
            ?course focu:courseNumber ?number .
            ?event focu:lectureBelongsTo ?course ;
                    focu:lectureNumber ?lecNumber ;
                    focu:hasContent ?resource .
            ?topic focu:provenance ?resource .
            ?topic focu:topicName ?topicName ;
            filter contains(lcase(?topicName), "{topic_name}")
            }}
            GROUP BY ?subject ?number ?lecNumber
            ORDER BY DESC(?count)
        """
        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        topics = [f"{row['subject']['value']} {row['number']['value']} covers that topic in lecture {row['lecNumber']['value']}. It appears {row['count']['value']} time(s)." for row in response]
        response_msg = "Here's what I found:\n" + "\n".join(topics)

        return response_msg
    
    def query_courses_offered_by(self, uni_name):

        query = f"""
            SELECT ?subject ?number ?name
            WHERE 
            {{
                ?course rdf:type vivo:Course .
                ?course vivo:offeredBy ?uni .
                ?uni rdfs:label ?uni_name .  
                ?course focu:courseName ?name .
    			?course focu:courseSubject ?subject .
    			?course focu:courseNumber ?number .
                filter contains(lcase(?uni_name), "{uni_name.lower()}")
            }}
            LIMIT 50
        """
        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        courses = [f"{row['subject']['value']} {row['number']['value']}: {row['name']['value']}" for row in response]
        response_msg = f"These are the courses offered by {uni_name}:\n" + "\n".join(courses)

        return response_msg
    
    def query_courses_covering_topic(self, topic_name):

        query = f"""
            SELECT DISTINCT ?course ?subject ?number ?name 
            WHERE 
            {{
                ?topic rdf:type focu:Topic .
                ?topic focu:provenance ?resource .
                ?topic focu:topicName ?topicName .
                ?event focu:hasContent ?resource .
                ?event focu:lectureBelongsTo ?course .
    			?course focu:courseSubject ?subject .
    			?course focu:courseNumber ?number .
    			?course focu:courseName ?name .
                filter contains(lcase(?topicName), "{topic_name.lower()}")
            }}
        """
        response = self.make_query(query)        
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        topics = [f"{row['subject']['value']} {row['number']['value']}: {row['name']['value']}" for row in response]
        response_msg = f"I found {topic_name} discussed here:\n" + "\n".join(topics)

        return response_msg
    
    def query_courses_in_subject_offered_by(self, uni_name, subject):

        query = f"""
            SELECT ?subject ?number ?name 
            WHERE 
            {{
                ?course rdf:type vivo:Course .
                ?course vivo:offeredBy ?uni .
                ?uni rdfs:label ?uni_name .  
                ?course focu:courseName ?name .
                ?course focu:courseNumber ?number .
    			?course focu:courseSubject ?subject .
                filter contains(lcase(?uni_name), "{uni_name.lower()}") .
    			filter contains(lcase(?subject), "{subject.lower()}")
            }}
            LIMIT 50
        """
        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        courses = [f"{row['subject']['value']} {row['number']['value']}: {row['name']['value']}" for row in response]
        response_msg = f"These are the {subject} courses I found at {uni_name}:\n" + "\n".join(courses)

        return response_msg
    
    def query_materials_for_topic_in_course(self, topic, course_subject, course_number):
        query = f"""
            SELECT ?resource WHERE {{
            ?topic focu:topicName ?topicName .
            ?topic focu:provenance ?resource .
            ?event focu:hasContent ?resource .
            ?event focu:lectureBelongsTo ?course .
            ?course focu:courseSubject "{course_subject.upper()}" .
            ?course focu:courseNumber "{course_number}" .
            filter contains(lcase(?topicName), "{topic}")
            }}
        """
        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        materials = [f"{row['resource']['value']}" for row in response]
        response_msg = f"These are the materials recommended for {topic} in {course_subject} {course_number}:\n" + "\n".join(materials)

        return response_msg

    def query_credit_worth(self, course_subject, course_number):
        query = f"""
            SELECT ?credits 
            WHERE 
            {{
                ?course focu:courseSubject "{course_subject.upper()}" .
                ?course focu:courseNumber "{course_number}" .
                ?course vivo:courseCredits ?credits .
            }}
            LIMIT 1
        """
        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        return f"{course_subject} {course_number} is worth {response[0]['credits']['value']} credits." 

    def query_additional_resources(self, course_subject, course_number):
        query = f"""
            SELECT ?link WHERE {{
                ?course rdf:type vivo:Course .
                ?course focu:courseSubject "{course_subject.upper()}" .
                ?course focu:courseNumber "{course_number}" .
                ?course rdfs:seeAlso ?link
            }}
        """
        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        links = [f"{row['link']['value']}" for row in response]
        response_msg = f"These are the additional resources for {course_subject} {course_number}:\n" + "\n".join(links)

        return response_msg
    
    def query_content_in_lecture(self, event, event_number, course_subject, course_number):

        # we only have lecture content right now
        lecture_variants = ["lecture", "lec"]
        if event.lower() not in lecture_variants:
            return None

        query = f"""
            SELECT ?content ?type WHERE {{
                ?lecture focu:lectureNumber {event_number} .
                ?lecture focu:lectureBelongsTo ?course .
                ?lecture focu:hasContent ?content .
                ?content rdf:type ?type .
                ?course focu:courseSubject "{course_subject.upper()}" .
                ?course focu:courseNumber "{course_number}" .
            }}
        """
        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        content = [f"{row['content']['value']}, {row['type']['value']}" for row in response]
        response_msg = f"This is the content for {course_subject} {course_number}, {event} {event_number}:\n" + "\n".join(content)

        return response_msg

    def query_readings_for_topic_in_course(self, topic, course_subject, course_number):    
        query = f"""
            SELECT ?desc WHERE {{
                ?course focu:courseSubject "{course_subject.upper()}" .
                ?course focu:courseNumber "{course_number}" .
                ?event focu:lectureBelongsTo ?course .
                ?event focu:hasContent ?resource2 .
                ?event focu:hasContent ?resource .
                ?topic focu:provenance ?resource2 .
                ?topic focu:topicName ?topicName .
                ?resource rdf:type focu:Reading .
                ?resource focu:readingDescription ?desc                
                filter contains(lcase(?topicName), "{topic}")
            }}
        """
        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        materials = [f"{row['desc']['value']}" for row in response]
        response_msg = f"These are the readings recommended for {topic} in {course_subject} {course_number}:\n" + "\n".join(materials)

        return response_msg
    
    def query_competencies_for_course_completion(self, course_subject, course_number):
        query = f"""
            SELECT ?topicName WHERE {{
                ?course focu:courseSubject "{course_subject.upper()}" .
                ?course focu:courseNumber "{course_number}" .
                ?lecture focu:lectureBelongsTo ?course .
                ?lecture focu:hasContent ?resource .
                ?topic focu:provenance ?resource .
                ?topic focu:topicName ?topicName .
            }}
            LIMIT 50
        """
        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        competencies = [f"{row['topicName']['value']}" for row in response]
        response_msg = f"These are the competencies acquired for completing {course_subject} {course_number}:\n" + ", ".join(competencies)

        return response_msg
    
    def query_grade_achieved_in_course(self, student, course_subject, course_number):
        query = f"""
            SELECT ?grades WHERE {{
                ?student focu:studentId {student} .
                ?student focu:CompletedCourses ?completed .
                ?completed focu:achievedInCourse ?course .
                ?course focu:courseSubject "{course_subject.upper()}" .
                ?course focu:courseNumber "{course_number}" .
                ?completed focu:achievedGrade ?grades .
                ?completed focu:achievedDate ?date .
            }}
            ORDER BY DESC(?date)
        """

        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        grades = [f"{row['grades']['value']}" for row in response]
        response_msg = f"These are the grades student {student} got in {course_subject} {course_number}: " + ", ".join(grades)

        return response_msg
    
    def query_students_completed_course(self, course_subject, course_number):
        query = f"""
            SELECT DISTINCT ?studentid WHERE {{
                ?student focu:CompletedCourses ?completed .
                ?student focu:studentId ?studentid .
                ?completed focu:achievedInCourse ?course .
                ?course focu:courseSubject "{course_subject.upper()}" .
                ?course focu:courseNumber "{course_number}" .
            }}
        """

        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        students = [f"{row['studentid']['value']}" for row in response]
        response_msg = f"These are the students that completed {course_subject} {course_number}:\n" + "\n".join(students)

        return response_msg
    
    def query_student_transcript(self, student):
        query = f"""
            SELECT ?subject ?number ?grade ?date WHERE {{
                ?student focu:studentId {student} .
                ?student focu:CompletedCourses ?completed .
                ?completed focu:achievedInCourse ?course .
                ?course focu:courseSubject ?subject .
                ?course focu:courseNumber ?number .
                ?completed focu:achievedGrade ?grade .
                ?completed focu:achievedDate ?date .
            }}
            ORDER BY ?course DESC(?date)
        """

        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        students = [f"In {row['subject']['value']} {row['number']['value']}, a {row['grade']['value']} was achieved on {row['date']['value']}." for row in response]
        response_msg = f"This is the transcript for student {student}:\n" + "\n".join(students)

        return response_msg
    
    def query_course_count(self):
        query = f"""
            SELECT (COUNT(*) as ?TotalCourses) WHERE {{
                ?course rdf:type vivo:Course  
            }}
        """

        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        response_msg = f"There are {response[0]['TotalCourses']['value']} courses in the graph."

        return response_msg
    
    def query_total_triples(self):
        query = f"""
            SELECT (COUNT(*) as ?NumTriples) WHERE {{
                ?s ?p ?o  
            }}
        """

        response = self.make_query(query)
        if response == None:
            return None
        
        response = response.json()["results"]["bindings"]
        if not response:
            return None

        response_msg = f"There are {response[0]['NumTriples']['value']} triples in the graph."

        return response_msg


if __name__ == "__main__":
    qm = QueryManager()
    print(qm.query_additional_resources("comp", "442"))
