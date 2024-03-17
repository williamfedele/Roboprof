import os
from rdflib import Graph, RDF, RDFS, Literal, URIRef
from course_builder import build_courses
from content_builder import build_content
from academic_builder import build_universities, build_students, build_grades
from constants import FOCU, FOCUDATA, VIVO


def build_graph():
    g_model = Graph()
    g_model.parse("model.ttl")
    g_model.bind("focu", FOCU)
    g_model.bind("focudata", FOCUDATA)
    g_model.bind("vivo", VIVO)

    g_universities = build_universities()
    g_students = build_students()
    g_courses = build_courses()
    g_lectures = build_content()
    g_grades = build_grades()

    g_final = g_model + g_universities + g_courses + g_lectures + g_students + g_grades

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    g_final.serialize(destination="output/ntriples.nt", format="ntriples")
    g_final.serialize(destination="output/turtles.ttl", format="turtle")
