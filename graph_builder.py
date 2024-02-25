import csv
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, RDFS
import os
import pandas as pd

FOCU = Namespace("http://focu.io/schema#")
FOCUDATA = Namespace("http://focu.io/data#")

df_courses = pd.read_csv("data/CATALOG.csv")
# NOTE: we are completely ignoring the rows that don't have a course code or course number
df_courses = df_courses.dropna(subset=["Course code", "Course number"])
df_course_components = pd.read_csv("data/CU_SR_OPEN_DATA_CATALOG.csv", encoding="utf-16")


def build_graph():
    g_model = Graph()
    g_model.parse("model.ttl")

    g = Graph()
    g.bind("focu", FOCU)
    g.bind("focudata", FOCUDATA)

    # Build Courses graph
    for index, row in df_courses.iterrows():
        # NOTE: we're using the key as the URI. could be more interesting to use
        # the code+number (so COMP474) since that's also unique
        course_uri = FOCUDATA[row["Key"]]
        code = row["Course code"].strip()
        number = row["Course number"].strip()

        title = row["Title"]
        description = row["Description"]
        credits = None

        # NOTE: this could be optimized by merging the two dataframes at init
        course_component = df_course_components[
            (df_course_components["Subject"] == code) & (df_course_components["Catalog"] == number)
        ]["Class Units"]
        if not course_component.empty:
            credits = course_component.iloc[0]

        g.add((course_uri, RDF.type, FOCU.Course))
        # g.add((course_uri, RDFS.label, Literal("Course", lang="en"))) # TODO: do we need this?
        g.add((course_uri, FOCU.courseName, Literal(title)))
        g.add((course_uri, FOCU.courseSubject, Literal(code)))
        g.add((course_uri, FOCU.courseNumber, Literal((number))))
        if credits:
            g.add((course_uri, FOCU.courseCredits, Literal(credits, datatype=XSD.float)))
        g.add((course_uri, FOCU.courseDescription, Literal(description)))

    g_final = g_model + g

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    g_final.serialize(destination="output/ntriples.ttl", format="ntriples")
    g_final.serialize(destination="output/turtles.ttl", format="turtle")
