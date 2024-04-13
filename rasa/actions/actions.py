# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sys
sys.path.append('../') # needed since sparql_api is in the parent directory. we can move sparql_api here as an alternative
from sparql_api import make_query


class ActionAboutCourse(Action):
    def name(self):
        return "action_about_course"
    def run(self, dispatcher, tracker, domain):
        course_name = tracker.get_slot('course')
        if len(course_name.split(' ')) != 2 or not course_name:
            dispatcher.utter_message(text="Sorry, I don't recognize that course.")
            return []
        
        subject = course_name.split(' ')[0].upper()
        number = course_name.split(' ')[1]
        query = f"SELECT ?description WHERE {{ ?course focu:courseSubject '{subject}' . ?course focu:courseNumber '{number}' . ?course focu:courseDescription ?description }} LIMIT 1"

        response = make_query(query)
        if response is None:
            dispatcher.utter_message(text="Sorry, I don't recognize that course.")
            return []
        
        description = response.json()['results']['bindings'][0]['description']['value']

        dispatcher.utter_message(text=f"Here's what I know: {description}")
        return []
