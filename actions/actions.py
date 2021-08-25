



import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import SlotSet

import urllib.request

master_dic_dataset_name = {
        'agricultural data' : 'agcensus_crop',
        'agricluture' : 'agcensus_crop', 
        'agri data' : 'agcensus_crop',
        'agricuture data':'agcensus_crop',
        'agriculture':'agcensus_crop',
        'agriculture census': 'agcensus_crop',
        'agcensus':'agcensus_crop',
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
         'sales regarding fertlisers':'fertiliser_sales',
         'rbi_deposit':'rbi_deposit',
         'deposits of rbi':'rbi_deposit',
         'rbi-deposit':'rbi_deposit',
         'deposits by rbi':'rbi_deposit',
         'investments of rbi':'rbi_deposit',
         'investments by rbi':'rbi_deposit',
         'mnrega employment':'nrga_emp',
         'credit by bank':'rbi_credit',
         'Soil':'soil'
         ,'soil':'soil',
         'pmfby':'pmfby'
         }

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
            dispatcher.utter_message(text="Hi!! Welcome to India Data Portal. How can I help you??",buttons=buttons)


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
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Feedback",
                        # "subtitle": "feedback form",
                        "image_url": "data:image/png;base64,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",
                        "buttons": [ 
                            {
                            "title": "Click here",
                            "url": "https://docs.google.com/forms/d/e/1FAIpQLSe4ZbIwB0BmX1_wEXUlL0Ywl_dt7US-Ipa_YLU2mDtjkqfPjg/viewform",
                            "type": "web_url"
                            }
                        ]
                    }
                ]
                }
        }
        dispatcher.utter_message(attachment=message)
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
    

        global transformed_dataset_name
    
        transformed_dataset_name =0
        global master_dic_dataset_name
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
 
                    # print(f"{data['dataset_name']} ---> {data['dataset_id']}")
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
                        dispatcher.utter_message(text = f'Can you write few lines about the doubts you have related to {temp_dataset_name}')
                        

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
                dataset_name_ = tracker.slots['dataset_name']

                # calling global dictionary
                global master_dic_dataset_name

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
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

                # calling global dictionary
                global master_dic_dataset_name

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]

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



class ActionMethodology(Action):

    def name(self) -> Text:
        return "action_about_data_methodology"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            print("\n",tracker.get_intent_of_latest_message())

            print("\n","Now slots value in Methodology is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
  
                global master_dic_dataset_name
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in Methodology {extracted_ls_entity}")


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
                                print("yes i am in methodology")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity

                                
                                if entity_iter in p.keys():
                                    # if entity is present in p then print the value of that entity
                                    # print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Methodology of a Dataset
                                                                        say it like :- What was the methodolgy adopted to make Rainfall Data""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Methodology of a Dataset
                                                                        say it like :- What was the methodolgy adopted to make Rainfall Data""")

            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")

class ActionFrequency(Action):

    def name(self) -> Text:
        return "action_about_data_frequency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            print("\n",tracker.get_intent_of_latest_message())

            print("\n","Now slots value in frequency is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']

                 # calling global dictionary
                global master_dic_dataset_name

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in frequency {extracted_ls_entity}")


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
                                print("yes i am in frequency")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity

                                
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    # print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Frequqncy of about Dataset updation
                                                                        say it like :- How often Rainfall Data is updated""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Frequqncy of about Dataset updation
                                                                        say it like :- How often Rainfall Data is updated""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")


class ActionLastDateUpdated(Action):

    def name(self) -> Text:
        return "action_about_data_data_last_updated"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            # print("\n",tracker.get_intent_of_latest_message())

            print("\n","Now slots value in Last date Updated is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']

                # calling global dictionary
                global master_dic_dataset_name

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]


                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in frequency {extracted_ls_entity}")


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
                        

                        if len(extracted_ls_entity) >=1:
                            # iterating through all entites other than dataset_name
                            for entity_iter in extracted_ls_entity:
                                print("yes i am in Last Date Updated")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity

                                
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    # print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Last Date updated for a Dataset 
                                                                        say it like :- When was this last date updated""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Last Date updated for a Dataset 
                                                                        say it like :- When was this last date updated""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")
