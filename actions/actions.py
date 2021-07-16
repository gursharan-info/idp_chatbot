



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
            {"payload":'/ok{"intent_button":"faq-visualisation"}',"title":"Visualisation"},
            {"payload":'/ok{"intent_button":"faq-fel"}',"title":"Fellowship"},
            {"payload":'/ok{"intent_button":"faq-train"}',"title":"Training"},
             {"payload":'/ok{"intent_button":"faq-dataset"}',"title":"Dataset"}
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
            {"payload":'/ok{"intent_button":"faq-train"}',"title":"Training"},
            {"payload":'/ok{"intent_button":"faq-dataset"}',"title":"Dataset"}
        ]
        
        # dictionary for mapped retrieval intents
        mapped_intent= { "faq-portal" : "Portal",
                        "faq-visualisation":"Visualisation",
                        "faq-fel": "Fellowship",
                        "faq-train":"Training",
                        "faq-dataset":"Dataset",
                        None: "No-option"}

        # to get a slot value (here --> slot is intent_button)
        print("\n","slots value is ",tracker.slots['intent_button']) 
        if tracker.slots['intent_button'] ==None:
            slot_value_clicked = mapped_intent[tracker.slots['intent_button']]
        else:
            slot_value_clicked = tracker.slots['intent_button']

        # to get intent of user message
        _intent=tracker.latest_message['intent'].get('name')
        print("Intent of user message ",_intent)

        print(tracker.latest_message['text']) # to get user typed message 

        intent_found = json.dumps(tracker.latest_message['response_selector'][_intent]['ranking'][0]['intent_response_key'], indent=4)
        print("retrieval we found ",intent_found)

        # confidence of retrieval intent we found
        retrieval_intent_confidence = tracker.latest_message['response_selector'][_intent]['response']['confidence']*100
        
        print(f"retrieval_intent_confidence we found was {retrieval_intent_confidence}")

        if _intent[:-3] == slot_value_clicked[0] :
            """ if intent found is same as faq-visualisation or faq-portal or any other category
            -3 tells we have left - and batch number 
            ex from faq-visualisation-b0 we took faq-visualisation """


        #used eval to remove quotes around the string
            intent_found = f'utter_{eval(intent_found)}'
            
            dispatcher.utter_message(response = intent_found) # use response for defining intent name
      

           
        elif slot_value_clicked == 'No-option':
             dispatcher.utter_message(text = "Please select any option first",buttons=buttons )
        else:

            # if retrieval_intent_confidence > 90:
            intent_found = f'utter_{eval(intent_found)}'
            
            dispatcher.utter_message(response = intent_found)

            dispatcher.utter_message(text = f"Seems like you want to ask question from {mapped_intent[ _intent[:-3]]} ok now you can ask question from {mapped_intent[ _intent[:-3]]}")
            
            tracker.slots['intent_button'] = _intent[:-3]
            
            print(f"Now slot value is {tracker.slots['intent_button']}","\n")
            
            # else: # if confidence is less than 90 percent
            #     dispatcher.utter_message(text = f"Do you want to ask question from {mapped_intent[ _intent[:-3]]} , If yes please select an options from below"
            #     ,buttons=buttons)

        return [SlotSet(key = "intent_button", value= _intent[:-3])] # setting slot values
