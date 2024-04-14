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

sys.path.append(
    "../"
)  # needed since sparql_api is in the parent directory. we can move sparql_api here as an alternative
from sparql_query_manager import QueryManager

# part 2 query 2
class ActionAboutCourse(Action):
    def name(self):
        return "action_about_course"

    def run(self, dispatcher, tracker, domain):
        course_name = tracker.get_slot("course")

        if len(course_name.split(" ")) != 2 or course_name == "unknown":
            dispatcher.utter_message(text="Sorry, I don't recognize that course.")
            return []

        subject = course_name.split(" ")[0].upper()
        number = course_name.split(" ")[1]

        qm = QueryManager()
        description = qm.query_about_course(subject, number)

        if description is None:
            dispatcher.utter_message(text="Sorry, I don't recognize that course.")
            return []

        dispatcher.utter_message(text=f"Here's what I know: {description}")
        return []


# part 2 query 3
class ActionEventTopics(Action):
    def name(self):
        return "action_event_topics"

    def run(self, dispatcher, tracker, domain):
        event = tracker.get_slot("event")
        course = tracker.get_slot("course")

        # expecting event = 'Lecture 2', course = 'COMP 474'
        if len(event.split(" ")) != 2 or len(course.split(" ")) != 2 or event == "unknown" or course == "unknown":
            dispatcher.utter_message(text="Please specify the course event you are interested in.")
            return []

        event_type = event.split(" ")[0]
        event_num = int(event.split(" ")[1])
        course_subject = course.split(" ")[0]
        course_number = course.split(" ")[1]

        qm = QueryManager()
        response = qm.query_course_event_topics(event_type, event_num, course_subject, course_number)

        if response is None:
            dispatcher.utter_message(text=f"No topics found for {event} in {course}.")
            return []

        # TODO move to query manager
        if response:
            topics = [
                f"{row['topicName']['value']}, {row['topic']['value']}, {row['resource']['value']}" for row in response
            ]
            response_message = "Here's what I found:\n" + "\n".join(topics)
        else:
            response_message = f"No topics found for {event} in {course}."

        dispatcher.utter_message(text=response_message)
        return []


# part 2 query 3
class ActionCoversTopic(Action):
    def name(self):
        return "action_covers_topic"

    def run(self, dispatcher, tracker, domain):
        topic_name = tracker.get_slot("topic")

        if topic_name == "unknown":
            dispatcher.utter_message(text="Sorry, I don't recognize that topic.")
            return []

        qm = QueryManager()
        response = qm.query_covers_topic(topic_name)

        if response is None:
            dispatcher.utter_message(text="Sorry, I don't recognize that topic.")
            return []

        # TODO move to query manager
        topics = [f"{row['course']['value']}, {row['event']['value']}" for row in response]
        response_msg = "Here's what I found:\n" + "\n".join(topics)

        dispatcher.utter_message(text=response_msg)
        return []


# part 1 query 1
class ActionCoursesOfferedBy(Action):
    def name(self):
        return "action_courses_offered_by"

    def run(self, dispatcher, tracker, domain):
        uni_name = tracker.get_slot("university")

        if uni_name == "unknown":
            dispatcher.utter_message(text="Sorry, I don't recognize that university.")
            return []

        qm = QueryManager()
        response = qm.query_courses_offered_by(uni_name)

        if response is None:
            dispatcher.utter_message(text="Sorry, I don't recognize that university.")
            return []

        dispatcher.utter_message(text=response)
        return []


# part 1 query 2
class ActionCoversTopic(Action):
    def name(self):
        return "action_courses_covering_topic"

    def run(self, dispatcher, tracker, domain):
        topic_name = tracker.get_slot("topic")

        if topic_name == "unknown":
            dispatcher.utter_message(text="Sorry, I don't recognize that topic.")
            return []

        qm = QueryManager()
        response = qm.query_courses_covering_topic(topic_name)

        if response is None:
            dispatcher.utter_message(text="Sorry, I don't recognize that topic.")
            return []

        dispatcher.utter_message(text=response)
        return []

# part 1 query 4
class ActionCoursesOfferedBy(Action):
    def name(self):
        return "action_courses_in_subject_offered_by"

    def run(self, dispatcher, tracker, domain):
        uni_name = tracker.get_slot("university")
        subject = tracker.get_slot("subject")

        if uni_name == "unknown" or subject == "unknown":
            dispatcher.utter_message(text="Sorry, I don't understand.")
            return []

        qm = QueryManager()
        print(uni_name)
        print(subject)
        response = qm.query_courses_in_subject_offered_by(uni_name, subject)

        if response is None:
            dispatcher.utter_message(text="Sorry, I couldn't find anything for that.")
            return []

        dispatcher.utter_message(text=response)
        return []