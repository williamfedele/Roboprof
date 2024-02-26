from rdflib import Graph, Namespace, RDF, Literal
from rdflib.namespace import XSD
import os


"""
Fully automated lecture and lecture content generation.

The content folder contains courses as folders in the format COMP_232 or COMP_474_6741 in the case of cross listed courses.

Each course folder contains lecture folders in the format lecture{i} where 'i' is used to denote the order of the lectures.

Each lecture folder contains some type of content such as:
    slidesXX.pdf
    worksheetXX.pdf
    readingXX.pdf
    otherXX.pdf

XX values should be distinct for URI usage.

name.txt file contains the name of the lecture on the first line. Ex: Knowledge Graphs
"""


CONTENT_PATH = "./content"

FOCU = Namespace("http://focu.io/schema#")
FOCUDATA = Namespace("http://focu.io/data#")


def build_lectures():

    g = Graph()
    g.bind("focu", FOCU)
    g.bind("focudata", FOCUDATA)

    courses = os.listdir(CONTENT_PATH)
    for course in courses:

        lec_path = f"{CONTENT_PATH}/{course}"
        lectures = os.listdir(lec_path)

        for lecture in lectures:
            lec_uri = FOCUDATA[f"{course}_{lecture}"]

            # cross listed courses should be stored as COMP_474_6741
            # extract each individual course id so we can assign a lecture to both sections:
            code = course.split("_")[0]
            numbers = course.split("_")[1:]
            for number in numbers:
                g.add((lec_uri, FOCU.lectureBelongsTo, FOCUDATA[f"{code}_{number}"]))

            g.add((lec_uri, RDF.type, FOCU.Lecture))

            # extract the lecture number
            lec_num = lecture[len("lecture") :]
            g.add((lec_uri, FOCU.lectureNumber, Literal(lec_num, datatype=XSD.integer)))

            content_path = f"{CONTENT_PATH}/{course}/{lecture}"
            content = os.listdir(content_path)
            for c in content:

                # the lecture name is stored in a name.txt file
                if c == "name.txt":
                    with open(f"{content_path}/name.txt", "r") as file:
                        lec_name = file.readline().strip()
                        g.add((lec_uri, FOCU.lectureName, Literal(lec_name)))
                    continue

                # remove file extensions
                fileName = c.split(".")[0]
                content_uri = FOCUDATA[f"{course}_{lecture}_{fileName}"]

                g.add((content_uri, FOCU.contentLink, FOCUDATA[f"{course}_{lecture}_{c}"]))

                # extract the type of lecture content from the name of the file.
                type = None
                if "slides" in c.lower():
                    type = FOCU.Slide
                elif "worksheet" in c.lower():
                    type = FOCU.Worksheet
                elif "reading" in c.lower():
                    type = FOCU.Reading
                else:
                    type = FOCU.OtherContent

                # finalize content and connect it to the current lecture
                g.add((content_uri, RDF.type, type))
                g.add((lec_uri, FOCU.hasContent, content_uri))

    g.serialize(destination="output/lectures.ttl", format="turtle")
    return g


if __name__ == "__main__":
    build_lectures()
