from rdflib import Graph, RDF, RDFS, Literal, URIRef
from rdflib.namespace import XSD
from constants import FOCU, FOCUDATA
from helpers import visible_files_iterator
import topic_processor


"""
Fully automated lecture and lecture content generation.

The content folder contains courses as folders in the format COMP_232 or COMP_474_6741 in the case of cross listed courses.

Each course folder contains lecture folders in the format lecture{i} where 'i' is used to denote the order of the lectures.

Each lecture folder contains some type of content such as:
    slidesXX.pdf
    worksheetXX.pdf
    readingsXX.pdf
    otherXX.pdf

XX values should be distinct for URI usage.

name.txt file contains the name of the lecture on the first line. Ex: Knowledge Graphs
readingsXX.txt should contain one reading per line for each required reading found in the slides
topics.txt contains topics extracted from the lecture slides on each line along with a relevant dbpedia/wikidata link. These topics are automatically linked to the corresponding lecture.

"""


CONTENT_PATH = "./content"


def build_content():
    g = Graph()

    for course in visible_files_iterator(CONTENT_PATH):
        lec_path = f"{CONTENT_PATH}/{course}"
        for lecture in visible_files_iterator(lec_path):
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
            for c in visible_files_iterator(content_path):
                # remove file extensions
                fileName = c.split(".")[0]

                # the lecture name is stored in a name.txt file
                if c == "name.txt":
                    with open(f"{content_path}/name.txt", "r") as file:
                        lec_name = file.readline().strip()
                        g.add((lec_uri, FOCU.lectureName, Literal(lec_name)))
                    continue
                elif "readings" in c.lower():
                    # create multiple reading objects for each line of the readingsXX.txt file
                    with open(f"{content_path}/{c}", "r") as file:
                        for line_num, line in enumerate(file, 1):
                            content_uri = FOCUDATA[f"{course}_{lecture}_{fileName}_{line_num}"]

                            g.add((content_uri, RDF.type, FOCU.Reading))
                            g.add((content_uri, FOCU.readingDescription, Literal(line.strip())))
                            g.add((lec_uri, FOCU.hasContent, content_uri))
                    continue
                elif "slides" in c.lower() or "worksheet" in c.lower():
                    content_uri = FOCUDATA[f"{course}_{lecture}_{fileName}"]
                    content_link = f"{content_path}/{c}"  # relative path to the file
                    g.add((content_uri, FOCU.contentLink, URIRef(content_link)))

                    # generate topics from slides and worksheets using spaCy
                    # get named entities from the document
                    named_entities = topic_processor.process(content_link)
                    for e in named_entities:
                        # entity format: (NAME, WIKIDATA_LINK)

                        topic_name = e[0]
                        topic_dbpedia = e[1]
                        if not topic_name.replace(" ", "").isalnum():
                            continue
                        topic_uri = FOCUDATA[f"T_{topic_name.replace(' ', '_')}"]

                        g.add((topic_uri, RDF.type, FOCU.Topic))
                        g.add((topic_uri, FOCU.topicName, Literal(topic_name)))
                        g.add((topic_uri, RDFS.seeAlso, URIRef(topic_dbpedia.strip())))
                        g.add((topic_uri, FOCU.provenance, content_uri))
                        g.add((content_uri, FOCU.hasTopic, topic_uri))

                    # extract the type of lecture content from the name of the file.
                    type = None
                    if "slides" in c.lower():
                        type = FOCU.Slide
                    elif "worksheet" in c.lower():
                        type = FOCU.Worksheet

                    # finalize this content and connect it to the current lecture
                    g.add((content_uri, RDF.type, type))
                    g.add((lec_uri, FOCU.hasContent, content_uri))
                else:
                    content_uri = FOCUDATA[f"{course}_{lecture}_{fileName}"]
                    content_link = f"{content_path}/{c}"  # relative path to the file
                    g.add((content_uri, FOCU.contentLink, URIRef(content_link)))

                    # finalize content and connect it to the current lecture
                    g.add((content_uri, RDF.type, FOCU.OtherContent))
                    g.add((lec_uri, FOCU.hasContent, content_uri))

    return g


if __name__ == "__main__":
    build_content()
