import csv
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD
import os


# TODO: figure out what to use instead of example
EXAMPLE = Namespace("http://example.org/")
WIKIDATA = Namespace("http://www.wikidata.org/entity/")

def build_graph():
    g = Graph()
    g.bind("foaf", FOAF)

    # TODO : Build university graph


# building a course : needs to look like this :
# focudata:COMP474
#   a focu:Course ;
#   rdfs:label "Course"@en ;
#   focu:courseName "Intelligent Systems" ;
#   focu:courseSubject "COMP" ;
#   focu:courseNumber "474"^^xsd:integer ;
#   focu:courseCredits "4"^^xsd:integer ;
#   focu:courseDescription "Description of the course" ;
#   focu:courseOutlineLink "Outline link" .
    # Build Courses graph
    with open("data/CATALOG.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            course_key = row["Key"]

            # TODO: find a better namespace that FOAF for name of an object
            g.add((URIRef(EXAMPLE[course_key]), FOAF.name, Literal(row["Title"], datatype=XSD.string)))
            # ... add more properties

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    g.serialize(destination="output/ntriples.ttl", format="ntriples")
    g.serialize(destination="output/turtles.ttl", format="turtle")