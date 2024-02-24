import csv
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
import os


def build_graph():
    g = Graph()

    # define namespace
    ns = URIRef("http://concordia.org/courses/")

    with open("data/CATALOG.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            course_uri = ns + row["Key"]

            # Add triples using the course URI
            g.add((course_uri, FOAF.name, Literal(row["Title"], datatype=XSD.string)))
            # ... add more properties

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    g.serialize(destination="output/graph.ttl", format="ntriples")
