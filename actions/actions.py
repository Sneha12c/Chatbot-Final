# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import webbrowser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher, Action
import webbrowser
from rasa_sdk.interfaces import Action
from rasa_sdk.events import SlotSet ,EventType
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher , Action
from rasa_sdk.types import DomainDict
from mysql_connectivity import DataUpdate
import spacy
import openai
from dotenv import load_dotenv
load_dotenv()
import os

class ActionTellName(Action):

    def name(self) -> Text:
        return "action_tell_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = tracker.get_slot("name")
        message = " Hi {}! , what is your mobile number ? ".format(name)
        print (message)
        dispatcher.utter_message(text=message)
        return []

class ActionTellName(Action):

    def name(self) -> Text:
        return "action_tell_number"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        number = tracker.get_slot("number")
      #  - text : " Hi {name}! , what is your mobile number 📱 ? "
        message = " Yeah , Your mobile number   is {} . Thanks for giving information ".format(number)
        print (message)
        dispatcher.utter_message(text=message)
        return []


class ValidateHealthForm(FormValidationAction):

  def name(self) -> Text:
      return "validate_health_form"

  async def required_slots(
    self,
    slots_mapped_in_domain: List[Text],
    dispatcher: "CollectingDispatcher",
    tracker: "Tracker",
    domain: "DomainDict"
  ) -> List[Text]:
    if tracker.get_slot("confirm_exercise") == True:
      return ["confirm_exercise", "exercise", "sleep", "diet", "stress", "goal"]
    else:
      return ["confirm_exercise", "sleep", "diet", "stress", "goal"]

class DisplaywebAction(Action):
    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
          nlp = spacy.load("en_core_web_md")
          user_input = tracker.latest_message.get("text")
          doc = nlp(user_input)
          openai.api_key=os.getenv('api')
          completions=openai.Completion.create(engine='text-davinci-002',prompt=user_input,max_tokens=1500)
          message=completions.choices[0].text
          answer=message
          print(answer)
          dispatcher.utter_message(answer)
          DataUpdate(user_input,answer)
          print(user_input)
          return[]

        except:
          dispatcher.utter_message("Can't display the information right now!")


class ActionOpenVideo(Action):
    def name(self) -> Text:
        return "action_open_video"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Replace "video_link" with the name of the slot that contains the video link.
        # video_link = tracker.get_slot("video_link")
        
        # You can replace the following command with the appropriate command for your OS/browser.
        # This example uses the webbrowser module in Python to open the video link in the default browser.
        video_link="https://www.youtube.com/watch?v=s4156vWGbYM"
        webbrowser.open(video_link)

        # Let the user know that the video link has been opened.
        dispatcher.utter_message("Here is your video!")
        
        # Return an event to set the "video_link_opened" slot to "True".
        return []



