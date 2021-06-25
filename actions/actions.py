



import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import SlotSet
class ActionSlotSetter(Action):

    def name(self) -> Text:
        return "action_slot_setter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        buttons = [
            {"payload":'/ok{"intent_button":"faq-portal"}',"title":"Portal"},
            {"payload":'/ok{"intent_button":"faq-visualisation"}',"title":"Visualisation"}
        ]

        dispatcher.utter_message(text="I am there to help you",buttons=buttons)

        return []

class ActionVizFaq(Action):

    def name(self) -> Text:
        return "action_viz_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons = [
            {"payload":'/ok{"intent_button":"faq-portal"}',"title":"Portal"},
            {"payload":'/ok{"intent_button":"faq-visualisation"}',"title":"Visualisation"},
            {"payload":'/ok{"intent_button":"faq-fel"}',"title":"Fellowship"},
            {"payload":'/ok{"intent_button":"faq-train"}',"title":"Training"}
        ]
        
        # dictionary for mapped retrieval intents
        mapped_intent= { "faq-portal" : "Portal",
                        "faq-visualisation":"Visualisation",
                        "faq-fel": "Fellowship",
                        "faq-train":"Training",
                        None: "No-option"}

        # to get a slot value (here --> slot is intent_button)
        print("slots value is ",tracker.slots['intent_button']) 
        if tracker.slots['intent_button'] ==None:
            slot_value_clicked = mapped_intent[tracker.slots['intent_button']]
        else:
            slot_value_clicked = tracker.slots['intent_button']

        # to get intent of user message
        _intent=tracker.latest_message['intent'].get('name')
        print("Intent of user message ",_intent)

        print(tracker.latest_message['text']) # to get user typed message 

        # actual retrieval intent found
        intent_found = json.dumps(tracker.latest_message['response_selector'][_intent]['ranking'][0]['intent_response_key'], indent=4)
        print("retrieval we found ",intent_found)

        
        # print(mapped_intent[tracker.slots['intent_button']],_intent[:-3])

        if _intent[:-3] == slot_value_clicked[0] :
            """ if intent found is same as faq-visualisation or faq-portal or any other category
            -3 tells we have left - and batch number 
            ex from faq-visualisation-b0 we took faq-visualisation """


        #used eval to remove quotes around the string
            intent_found = f'utter_{eval(intent_found)}'
            
            dispatcher.utter_message(response = intent_found) # use response for defining intent name
      

           
        elif slot_value_clicked == 'No-option':
             dispatcher.utter_message(text = "Please select any option first",buttons=buttons )
            #  dispatcher.utter_message(text = f"Do you want to ask question from {mapped_intent[slot_value_clicked[0]]} otherwise select options from"
            #  ,buttons=buttons)
        else:
            dispatcher.utter_message(text = f"Do you want to ask question from {mapped_intent[ _intent[:-3]]} , If yes please select an options from below"
            ,buttons=buttons)

        return []

# class ActionPortalFaq(Action):

#     def name(self) -> Text:
#         return "action_portal_faq"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # to get a slot value (here --> slot is intent_button)
#         print("slots value is ",tracker.slots['intent_button']) 
#         slot_value_clicked = tracker.slots['intent_button']

#         # to get intent of user message
#         _intent=tracker.latest_message['intent'].get('name')
#         print("Intent of user message ",_intent)

#         print(tracker.latest_message['text']) # to get user typed message 

#         # actual retrieval intent found
#         intent_found = json.dumps(tracker.latest_message['response_selector'][_intent]['ranking'][0]['intent_response_key'], indent=4)
#         print("retrieval we found ",intent_found)

#         if _intent == 'portal':

#         #used eval to remove quotes around the string
#             intent_found = f'utter_{eval(intent_found)}'
            
#             dispatcher.utter_message(response = intent_found) # use response for defining intent name
#         else:
#              dispatcher.utter_message(text = f"Please select your questions from {slot_value_clicked}")

#         return []