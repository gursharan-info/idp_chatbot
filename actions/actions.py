



import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import SlotSet

import urllib.request

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

            

        if tracker.slots['intent_button'] == None:
            print("\n","slots value is ",tracker.slots['intent_button']) 
            dispatcher.utter_message(text="I am there to help you",buttons=buttons)


        else:
            print("\n","Now slots value is ",tracker.slots['intent_button'])  
        
            dispatcher.utter_message(text="Yes you are good to go")

        return []

class ActionFeedback(Action):

    def name(self) -> Text:
        return "action_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Please give your feedback")
        dispatcher.utter_message(text="[feedback](https://forms.gle/Fk1TxTzAteigKFG87)")
        
        
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
        print("Intent of user message predicted by Rasa ",_intent)

        print(tracker.latest_message['text']) # to get user typed message 

        intent_found = json.dumps(tracker.latest_message['response_selector'][_intent]['ranking'][0]['intent_response_key'], indent=4)
        print("retrieval we found (i.e intent response key ) ",intent_found)

        # confidence of retrieval intent we found
        retrieval_intent_confidence = tracker.latest_message['response_selector'][_intent]['response']['confidence']*100
        
        print(f"retrieval_intent_confidence we found was {retrieval_intent_confidence}")
        if str(tracker.latest_message['text']) == str('https://forms.gle/Fk1TxTzAteigKFG87'):
            dispatcher.utter_message(text='You can fill and submit the Google form')

        elif _intent[:-3] == slot_value_clicked[0] :
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

            dispatcher.utter_message(text = f"Seems like you want to ask question from {mapped_intent[ _intent[:-3]]} If yes you are good to go with that  but if you want to ask question from any other category please select a button",buttons=buttons)
            
            tracker.slots['intent_button'] = _intent[:-3]

            
            print(f"Now slot value is {tracker.slots['intent_button']}","\n")
            


        return [SlotSet(key = "intent_button", value= [str(_intent[:-3])] ) ] # setting slot values
    


class ActionDatasetName(Action):

    def name(self) -> Text:
        return "action_about_data_dataset_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # print(tracker.latest_message['text']) # to get user typed message 

        ls_entity =tracker.latest_message['entities'] # to get entities from user message

        print(ls_entity)

        # initilize the dataset name
        dataset_name = 0

        # spellcheck the user extracted_dataset_name
        extracted_dataset_name = 0

        for i in range(len(ls_entity)):
            if ls_entity[i]['entity'] == 'dataset_name':

                # name of dataset extracted from RASA
                temp_dataset_name = ls_entity[i]['value']

                # name of dataset we get after extraction
                extracted_dataset_name = ls_entity[i]['value']
                print(extracted_dataset_name)
                break
    
        # dictionary  conating all possible name that can be given to a dataset name
        master_dic_dataset_name = {
        'agricultural data' : 'agcensus_crop',
        'agricluture' : 'agcensus_crop', 
        'agri data' : 'agcensus_crop',
        'agricuture data':'agcensus_crop',
        'agriculture':'agcensus_crop',
        'rainfall':'rainfall',
        'rain data':'rainfall',
        'rainfall data':'rainfall',
        'agricultural census':'agcensus_crop',
        'rain figures':'rainfall',
        'sales of fertiliser':'fertiliser_sales',
        'sales of fertilisers':'fertiliser_sales',
        'fertiliser sales':'fertiliser_sales',
        'fertilizer sales data':'fertiliser_sales',
        'fertilizers sales data':'fertiliser_sales',
         'sales regarding fertlisers':'fertiliser_sales',}

        global transformed_dataset_name
    
        transformed_dataset_name =0
        if extracted_dataset_name in master_dic_dataset_name.keys():
            

            transformed_dataset_name = master_dic_dataset_name[extracted_dataset_name]

        
        print(f"after tranformation ---> {transformed_dataset_name}")


        if transformed_dataset_name !=0 :
     
            # by defualt dataset name value will be given to slot if that was extratced from user message
            print("\n","Now slots value is ",tracker.slots['dataset_name'])  

            extracted_ls_entity = []
            for i in range(len(ls_entity)):
                extracted_ls_entity.append(ls_entity[i]['entity'])

            extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
            print(f"Entites we extracted {extracted_ls_entity}")


            dict_of_mapped_data_with_id = {}
            with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                data = json.loads(url.read().decode())
                temp_data  = json.dumps(data, indent=4, sort_keys=True)
                temp_data = json.loads(temp_data)

                for i in range(len(temp_data)):
                    data = temp_data[i]
 
                    print(f"{data['dataset_name']} ---> {data['dataset_id']}")
                    dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']
  

                # if transformed_dataset_name is present in our data we got from json file
                if transformed_dataset_name in dict_of_mapped_data_with_id.keys():
                    
                    # extract id for that dataset name
                    extracted_id = dict_of_mapped_data_with_id[transformed_dataset_name]

                    for i in range(len(temp_data)):
                            data = temp_data[i]
                            if data['dataset_id']==extracted_id:
                                p = json.dumps(data)
                                p = json.loads(p)
                                
                    

                    if len(extracted_ls_entity) >=1:
                        # iterating through all entites other than dataset_name
                        for entity_iter in extracted_ls_entity:

                            # check if entity present in extracted_ls_entity is also present in p ( data in db)
                            # spellcheck the entity
                            if entity_iter in p.keys():
                                # if entity is present in p then print the value of that entity
                                print(f"{entity_iter} ----> {p[entity_iter]}")
                                dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                            
                            else:
                                dispatcher.utter_message(text = 'Sorry but can you pls say it again')
                                # return [SlotSet('dataset_name', dataset_name)]
                    
                    else:
                        dispatcher.utter_message(text = f'Yes you can start with {temp_dataset_name}')
                        

            print(f"Returning value of {transformed_dataset_name}")
            return [SlotSet('dataset_name', transformed_dataset_name)]
        
        # if dataset_name is not present in our data we got from json file
        else:
            dispatcher.utter_message(text = """Can You Please rephrase your question about which dataset
             you want ask """)
        
class ActionGranularityLevel(Action):

    def name(self) -> Text:
        return "action_about_data_granularity_level"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in granular is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_granular = tracker.slots['dataset_name']
                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in gran {extracted_ls_entity}")


                dict_of_mapped_data_with_id = {}
                with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                    data = json.loads(url.read().decode())
                    temp_data  = json.dumps(data, indent=4, sort_keys=True)
                    temp_data = json.loads(temp_data)
                    for i in range(len(temp_data)):
                        data = temp_data[i]
                        dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']

                    # if extracted dataset name is present in our data we got from json file
                    if dataset_name_granular in dict_of_mapped_data_with_id.keys():
                        
                        # extract id for that dataset name
                        extracted_id = dict_of_mapped_data_with_id[dataset_name_granular]

                        for i in range(len(temp_data)):
                                data = temp_data[i]
                                if data['dataset_id']==extracted_id:
                                    p = json.dumps(data)
                                    p = json.loads(p)
                                    # print(p,'\n')
                        

                        if len(extracted_ls_entity) >=1:
                            # iterating through all entites other than dataset_name
                            for entity_iter in extracted_ls_entity:
                                print("yes i am ")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Granularity level of a Dataset
                                                                        say it like :- What is the Granularity level of Rainfall Data""")
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Granularity level of a Dataset
                                                                        say it like :- What is the Granularity level of Rainfall Data""")
                                

            else:
                dispatcher.utter_message(text = """Can you specify the Dataset Name completely and
                what's your query reagrding it """)


class ActionSourcedata(Action):

    def name(self) -> Text:
        return "action_about_data_source_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in source is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in source {extracted_ls_entity}")


                dict_of_mapped_data_with_id = {}
                with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                    data = json.loads(url.read().decode())
                    temp_data  = json.dumps(data, indent=4, sort_keys=True)
                    temp_data = json.loads(temp_data)
                    for i in range(len(temp_data)):
                        data = temp_data[i]
                        # print(f"{data['dataset_name']} ---- > {data['dataset_id']} " )
                        dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']

                    # if extracted dataset name is present in our data we got from json file
                    if dataset_name_ in dict_of_mapped_data_with_id.keys():
                        
                        # extract id for that dataset name
                        extracted_id = dict_of_mapped_data_with_id[dataset_name_]

                        for i in range(len(temp_data)):
                                data = temp_data[i]
                                if data['dataset_id']==extracted_id:
                                    p = json.dumps(data)
                                    p = json.loads(p)
                                    # print(p,'\n')
                        

                        if len(extracted_ls_entity) >=1:
                            # iterating through all entites other than dataset_name
                            for entity_iter in extracted_ls_entity:
                                print("yes i am in source")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity

                                
                                if entity_iter in p.keys():
                                    # if entity is present in p then print the value of that entity
                                    print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Source of a Dataset
                                                                        say it like :- What is the Source of Rainfall Data""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Source of a Dataset
                                                                        say it like :- What is the Source of Rainfall Data""")

            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")
