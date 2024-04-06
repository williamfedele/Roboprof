from rdflib import Graph, Literal, RDF, RDFS, URIRef
from rdflib.namespace import XSD, FOAF
import pandas as pd
from constants import FOCU, FOCUDATA, VIVO


def build_universities():
    g = Graph()
    df_universities = pd.read_csv("data/universities.csv", names=["UniversityName", "DBpediaLink"], skiprows=1)
    for index, row in df_universities.iterrows():
        uni_uri = FOCUDATA[f"{row['UniversityName'].replace(' ', '_')}"]
        uni_name = row["UniversityName"]
        dbpedia = row["DBpediaLink"]
        g.add((uni_uri, RDF.type, VIVO.University))
        g.add((uni_uri, RDFS.label, Literal(uni_name)))
        g.add((uni_uri, RDFS.seeAlso, URIRef(dbpedia)))
    return g


def build_students():
    g = Graph()
    df_students = pd.read_csv("data/students.csv", names=["SID", "FirstName", "LastName", "Age", "Email"], skiprows=1)
    for index, row in df_students.iterrows():
        uri = FOCUDATA[f"{row['SID']}"]
        g.add((uri, RDF.type, VIVO.Student))
        g.add((uri, FOCU.studentId, Literal(row["SID"])))
        g.add((uri, FOAF.firstName, Literal(row["FirstName"])))
        g.add((uri, FOAF.lastName, Literal(row["LastName"])))
        g.add((uri, FOAF.age, Literal(row["Age"])))
        g.add((uri, FOAF.mbox, Literal(row["Email"])))
    return g


def build_grades():
    g = Graph()
    df_grades = pd.read_csv("data/grades.csv", names=["SID", "Course", "Grade", "Date"], skiprows=1)
    for index, row in df_grades.iterrows():
        student_uri = FOCUDATA[f"{row['SID']}"]
        course_uri = FOCUDATA[f"{row['Course']}"]
        completion_uri = FOCUDATA[f"{row['SID']}_{row['Course']}_{row['Date']}"]

        # new completion
        g.add((completion_uri, RDF.type, FOCU.CourseCompleted))
        g.add((completion_uri, FOCU.achievedGrade, Literal(row["Grade"])))
        g.add((completion_uri, FOCU.achievedByStudent, student_uri))
        g.add((completion_uri, FOCU.achievedInCourse, course_uri))
        g.add((completion_uri, FOCU.achievedDate, Literal(row["Date"], datatype=XSD.date)))
        # add to the students list of completed courses
        g.add((student_uri, FOCU.CompletedCourses, completion_uri))
    return g
