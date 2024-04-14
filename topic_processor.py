from tika import parser
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("entityfishing")


def process(file):

    raw = parser.from_file(file)
    text = raw["content"]

    doc = nlp(text)

    # filter to only organizations (ORG), locations (GPE), people (PERSON)
    # must have a wikidata link
    named_entities = {
        (ent.text.strip(), ent._.url_wikidata) for ent in doc.ents if ent.label_ in ["ORG"] and ent._.url_wikidata
    }

    return named_entities
