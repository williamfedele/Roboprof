import os
from rdflib import Graph, RDF, RDFS, Literal, URIRef
from course_builder import build_courses
from lecture_builder import build_lectures
from constants import FOCU, FOCUDATA, VIVO


def build_graph():
    g_model = Graph()
    g_model.parse("model.ttl")
    g_model.bind("focu", FOCU)
    g_model.bind("focudata", FOCUDATA)
    g_model.bind("vivo", VIVO)

    g_model.add((FOCUDATA.Concordia, RDF.type, VIVO.University))
    g_model.add((FOCUDATA.Concordia, RDFS.label, Literal("Concordia University")))
    g_model.add((FOCUDATA.Concordia, RDFS.seeAlso, URIRef("http://dbpedia.org/resource/Concordia_University")))

    g_courses = build_courses()
    g_lectures = build_lectures()

    g_final = g_model + g_courses + g_lectures

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    g_final.serialize(destination="output/ntriples.nt", format="ntriples")
    g_final.serialize(destination="output/turtles.ttl", format="turtle")
