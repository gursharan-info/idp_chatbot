


from typing import Any, Text, Dict, List
import urllib.request, json
import os
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# from gensim.models import KeyedVectors
from spellcheck import correction , master_dic_dataset_name,entity_mapper, dict_of_domain_ids, dataset_name_in_api, datset_name_and_ds_api_name
import numpy as np
# from gensim import models
import time
from textblob import TextBlob
from sklearn.metrics.pairwise import cosine_similarity
import sys

dic_of_similarity = {}

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
        
        dispatcher.utter_message(text="You can provide your feedback to us in this [Feedback Form](https://forms.gle/Fk1TxTzAteigKFG87)")
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
        # print('tracker latest message', tracker.latest_message['response_selector'])
        # print(' ')
        # print('---', tracker.latest_message['response_selector'].keys())
        # print('   ')
        # print("retrieval we found (i.e intent response key ) ",intent_found)

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
            # print('intent before adding the utter', intent_found)
            # print('----', eval(intent_found))
            intent_found = f'utter_{eval(intent_found)}'
            print('after adding utter we found -- ', intent_found)
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
    

class ActionLanguageDetector(Action):

    def name(self) -> Text:
        return "action_language_detector"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        # to get intent of user message
        _intent=tracker.latest_message['intent'].get('name')
        print("Intent of user message predicted by Rasa ",_intent)

        text = tracker.latest_message['text'] # to get user typed message
        lang = TextBlob(text)
        lang = lang.detect_language()
        print("Language of user message is ",lang)
        if lang == _intent[-2:]:
            # print(lang,_intent[-2:])
            # dispatcher.utter_message(f"Your message is in {lang}")
            ls_of_lang_intent = []
            intent_found = json.dumps(tracker.latest_message['intent_ranking'], indent=4)
            for lang_finder_iter in tracker.latest_message['intent_ranking']:
                print(lang_finder_iter)
                if lang_finder_iter['name'][-2:] == lang:
                    ls_of_lang_intent.append(lang_finder_iter)
            print("\n","ls_of_lang_intent",ls_of_lang_intent)
            # print("retrieval we found (i.e intent response key ) ",intent_found)

            # sorting needed to get the highest confidence intent
            intent_found = ls_of_lang_intent[0]['name']
            intent_found = 'utter_'+str(intent_found)
            print('after adding utter we found -- ', intent_found)
            dispatcher.utter_message(response=intent_found)
        return [SlotSet('language', lang)]


class ActionLanguageDetectorRetrieval(Action):

    def name(self) -> Text:
        return "action_language_detector_retrieval"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print('Language detector for Retrieval')
        # to get intent of user message
        _intent=tracker.latest_message['intent'].get('name')
        print("Intent of user message predicted by Rasa ",_intent)

        text = tracker.latest_message['text'] # to get user typed message
        lang = TextBlob(text)
        lang = lang.detect_language()
        print("Language of user message is ",lang)
        if lang == _intent[-2:]:
            # print(lang,_intent[-2:])
            # dispatcher.utter_message(f"Your message is in {lang}")
            ls_of_lang_intent = []
            intent_found = json.dumps(tracker.latest_message['response_selector'][_intent]['ranking'], indent=4)
            print(intent_found)
            intent_found = json.loads(intent_found)
            for lang_finder_iter in intent_found:
                print(lang_finder_iter['intent_response_key'])
                if lang_finder_iter['intent_response_key'].split('/',1)[0][-2:] == lang:
                    ls_of_lang_intent.append(lang_finder_iter)
            print("\n","ls_of_lang_intent",ls_of_lang_intent)
            
        #     # sorting needed to get the highest confidence intent
        print("retrieval we found (i.e intent response key ) ",ls_of_lang_intent[0]['intent_response_key'])
        intent_found = ls_of_lang_intent[0]['intent_response_key']

        intent_found = 'utter_'+str(intent_found)
        print('after adding utter we found -- ', intent_found)
        dispatcher.utter_message(response=intent_found)
        return [SlotSet('language', lang)]


class ActionDatasetName(Action):

    def name(self) -> Text:
        return "action_about_data_dataset_name"

    def remove_punctuation_mark_from_user_entity(self, user_entity):
        # define punctuation
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        my_str = str(user_entity)
        # remove punctuation from the string
        no_punct = ""
        for ele in my_str:
            if ele in punctuations:
                user_entity = user_entity.replace(ele, " ")

        return user_entity

    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global datset_name_and_ds_api_name
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
                # breaks

        # dictionary  conating all possible name that can be given to a dataset name
    

        global transformed_dataset_name
    
        transformed_dataset_name =0
        global master_dic_dataset_name

        print("extracted dataset mame ",extracted_dataset_name)
        # converting name extracted to lower case
        if type(extracted_dataset_name)!=int:
            extracted_dataset_name = extracted_dataset_name.lower()

            # corrected extracted_dataset_name

            extracted_dataset_name = correction(extracted_dataset_name)

            print(f'after correction {extracted_dataset_name}')
        if  tracker.slots['dataset_name'] and tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                extracted_dataset_name = tracker.slots['dataset_name']
                print('this is the dataset name which is setup as a slot value', extracted_dataset_name)
                extracted_dataset_name = extracted_dataset_name.lower() 
                # calling global dictionary
                global master_dic_dataset_name

                print("Before spell check",extracted_dataset_name)
                # spellcheck the name of dataset
                if extracted_dataset_name not in ['nsso','employment','non-crop','crop','foodgrains']:
                    print("Before spell check inside if",extracted_dataset_name)
                    if extracted_dataset_name in dataset_name_in_api:
                        extracted_dataset_name = extracted_dataset_name
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        extracted_dataset_name = correction(extracted_dataset_name)
                        corrected_extracted_dataset_name = extracted_dataset_name
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # extracted_dataset_name = correction(extracted_dataset_name)
                    # corrected_extracted_dataset_name = extracted_dataset_name
                    print("after spellcheck inside if condition  ",extracted_dataset_name)
                # elif len(ls_entity)>1: # removing that entity where datset name is nsso
                else:
                    print(ls_entity)
                    removable_index = [[j,i['value']] for j,i in enumerate(ls_entity) if i['value'] in  ['NSSO','Employment','Non-Crop','Crop','Foodgrains']]

          
                    print("\n",'printing removable index --',removable_index,"\n")

                    for last_check in removable_index:
                        # there are chance when employemnt and NSSO can come together 
                        # then to remove only NSSO dataset_name we used this last filter

                        print('printing last check --',last_check)

                        bracket_dataset_name = last_check[1]    #i.e crop, non-crop, nsso etc category

                        # iff NSSO found remove that corresponding dictionary from ls_entity
                        if last_check[1]=='NSSO':
                            removable_index = last_check[0]

                            # if not NSSO then remove then EMPLOYMENT entity dictionary from ls_entity
                        else:
                            # continue
                            removable_index = last_check[0]
    
                    
                    print("\n",removable_index,"\n")
                
                    ls_entity.pop(removable_index)
                    print("After Pop",ls_entity)

                    for iter in range(len(ls_entity)):
                        if ls_entity[iter]['entity']=='dataset_name' :
                            
                            # dataset_name_list_countter =  [i for i in range(len(ls_entity)) if ls_entity[i]['entity']=='dataset_name' ]
                            
                            print("word in a bracket",bracket_dataset_name)
                            if bracket_dataset_name=='Crop':

                                print("green")
                                extracted_dataset_name  = ls_entity[iter]['value']
                            
                                if extracted_dataset_name == 'Agricultural Census 2010-11':
                                    actual_extracted_dataset_name = 'Agricultural Census 2010-11 (Crop)'
                                    extracted_dataset_name = 'agcensus_crop'
                                elif extracted_dataset_name == 'Agricultural Census 2015-16':
                                    actual_extracted_dataset_name = 'Agricultural Census 2015-16 (Crop)'
                                    extracted_dataset_name = 'agcensus_c'
                                elif  extracted_dataset_name == 'Input Survey':
                                    actual_extracted_dataset_name = 'Input Survey (Crop)'
                                    extracted_dataset_name = 'input_crop'
                                  
                                else:
                                    actual_extracted_dataset_name = extracted_dataset_name+ '(Crop)'
                                    extracted_dataset_name = extracted_dataset_name
                                
                                break
                                
                            elif  bracket_dataset_name=='Non-Crop' :
                                # second_removable_index = iter
                                print("iter",iter)
                                # ls_entity.pop(second_removable_index)

                                # again we'll have to iterate to get dataset value
                                for iter  in range(len(ls_entity)):
                                    if ls_entity[iter]['entity']=='dataset_name' :
                                        extracted_dataset_name  = ls_entity[iter]['value']

                                # as Non has came now just need to map to correct non option
                                if extracted_dataset_name == 'Agricultural Census 2010-11':
                                    actual_extracted_dataset_name = 'Agricultural Census 2010-11 (Non-Crop)'
                                    extracted_dataset_name = 'agcensus_noncrop'
                                elif extracted_dataset_name == 'Agricultural Census 2015-16':
                                    actual_extracted_dataset_name = 'Agricultural Census 2015-16 (Non-Crop)'
                                    extracted_dataset_name = 'agcensus_nc'
                                elif  extracted_dataset_name == 'Input survey':
                                    actual_extracted_dataset_name = 'Input Survey (Non-Crop)'
                                    extracted_dataset_name == 'input_crop'
                                else:
                                    actual_extracted_dataset_name = extracted_dataset_name+ '(Non-Crop)'
                                    extracted_dataset_name = extracted_dataset_name
                                break

                            else:
                                extracted_dataset_name  = ls_entity[iter]['value']

                        else:
                            continue  
                    print("Before spell check inside else",extracted_dataset_name)
                    if extracted_dataset_name in dataset_name_in_api:
                        extracted_dataset_name = extracted_dataset_name
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        extracted_dataset_name = correction(extracted_dataset_name)
                        corrected_extracted_dataset_name = extracted_dataset_name
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # extracted_dataset_name = correction(extracted_dataset_name)
                    # corrected_extracted_dataset_name = extracted_dataset_name
                    print("after spellcheck inside else condition ",extracted_dataset_name)
               
                if extracted_dataset_name in master_dic_dataset_name.keys():
                    print("IN",extracted_dataset_name)
                    actual_extracted_dataset_name = extracted_dataset_name
                    extracted_dataset_name = master_dic_dataset_name[extracted_dataset_name]
                    
                    print("OUT",extracted_dataset_name)

                    # transformed_dataset_name = master_dic_dataset_name[extracted_dataset_name]

                
                    # print(f"after tranformation ---> {transformed_dataset_name}")
                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entity we extracted in Dataset Name is  {extracted_ls_entity}")

                print(ls_entity)

                # print('before removing datatset name from list - ', extracted_ls_entity)
                # if 'dataset_name' in extracted_ls_entity :
                #     extracted_ls_entity.remove('dataset_name')
                #     print('after removing datatset name from list - ', extracted_ls_entity)


                dict_of_mapped_data_with_id = {}
                with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
                    data = json.loads(url.read().decode())
                    temp_data  = json.dumps(data, indent=4, sort_keys=True)
                    temp_data = json.loads(temp_data)
                    for i in range(len(temp_data)):
                        data = temp_data[i]
                        dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']

                    # if extracted dataset name is present in our data we got from json file
                    if extracted_dataset_name in dict_of_mapped_data_with_id.keys():
                        
                        # extract id for that dataset name
                        extracted_id = dict_of_mapped_data_with_id[extracted_dataset_name]

                        for i in range(len(temp_data)):
                                data = temp_data[i]
                                if data['dataset_id']==extracted_id:
                                    p = json.dumps(data)
                                    p = json.loads(p)
                                    # print(p,'\n')
                        

                        if len(extracted_ls_entity) >=1:
                            # iterating through all entites other than dataset_name
                            for entity_iter in extracted_ls_entity:
                                print("yes i am in Dataset name with entity as ", entity_iter)
                                if entity_iter == 'dataset_name':
                                    # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                    # spellcheck the entity
                                    entity_iter = correction(entity_iter)

                                    if entity_iter in p.keys() and entity_iter in entity_mapper.keys():
                                        new_entity_iter = entity_mapper[entity_iter]
                                        # if entity is present in p then print the value of that entity
                                        # if entity_iter != 'dataset_name':
                                        print(f"{entity_iter} ----> {p[entity_iter]}")
                                        # dispatcher.utter_message(text = f" for {corrected_dataset_name_} {new_entity_iter} is {p[entity_iter]}")
                                        # dispatcher.utter_message(text=f'{new_entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                        if actual_extracted_dataset_name in datset_name_and_ds_api_name.keys():
                                            actual_extracted_dataset_name = datset_name_and_ds_api_name[actual_extracted_dataset_name]
                                        else:
                                            actual_extracted_dataset_name = actual_extracted_dataset_name
                                        dispatcher.utter_message(text = f'You can ask specific questions related to the {actual_extracted_dataset_name} dataset here. For complete details of dataset, you can also visit this link. [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                        return [SlotSet('dataset_name', extracted_dataset_name)]
                                        # elif entity_iter == 'dataset_name':
                                        #     print(f"Returning {dataset_name_}")
                                        #     return [SlotSet('dataset_name', dataset_name_)] 
                                    
                                    else:
                                        dispatcher.utter_message(text = 'Sorry but can you pls tell again  what Dataset you are looking for')
                                        # dispatcher.utter_message(text = """Ex :Like if you want to know Granularity level of a Dataset
                                        #                                     say it like :- What is the Granularity level of Rainfall Data""")
                                else:
                                    continue
                        else:
                            dispatcher.utter_message(text = 'Sorry but what exactly you wanted I could not get that')
                            # dispatcher.utter_message(text = """Ex :Like if you want to know Granularity level of a Dataset
                                                                        # say it like :- What is the Granularity level of Rainfall Data""")

                    else:
                        extracted_id = dict_of_mapped_data_with_id[extracted_dataset_name]
                        if actual_extracted_dataset_name in datset_name_and_ds_api_name.keys():
                            actual_extracted_dataset_name = datset_name_and_ds_api_name[actual_extracted_dataset_name]
                        else:
                            actual_extracted_dataset_name = actual_extracted_dataset_name            
                        dispatcher.utter_message(text = f'You can ask specific questions related to the {actual_extracted_dataset_name} dataset here. For complete details of dataset, you can also visit this link. [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                        return [SlotSet('dataset_name', extracted_dataset_name)]
        else:
            dispatcher.utter_message(text = "Sorry but seems like there is some Misspell in Dataset Name Please try again")


        # if extracted_dataset_name !=0 :
     
        #     # by defualt dataset name value will be given to slot if that was extratced from user message
        #     print("\n","Now slots value is ",tracker.slots['dataset_name'])  

        #     extracted_ls_entity = []
        #     for i in range(len(ls_entity)):
        #         extracted_ls_entity.append(ls_entity[i]['entity'])

        #     extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
        #     print(f"Entites we extracted {extracted_ls_entity}")


        #     dict_of_mapped_data_with_id = {}
        #     with urllib.request.urlopen("https://indiadataportal.com/meta_data_info") as url:
        #         data = json.loads(url.read().decode())
        #         # print(data[0])
        #         temp_data  = json.dumps(data, indent=4, sort_keys=True)
        #         temp_data = json.loads(temp_data)

        #         for i in range(len(temp_data)):
        #             data = temp_data[i]
 
        #             # print(f"{data['dataset_name']} ---> {data['dataset_id']}")
        #             dict_of_mapped_data_with_id[data['dataset_name']] = data['dataset_id']
        #         # print('dict_of_mapped_data_with_id', dict_of_mapped_data_with_id)
  

        #         # if transformed_dataset_name is present in our data we got from json file
        #         if extracted_dataset_name in dict_of_mapped_data_with_id.keys():
                    
        #             # extract id for that dataset name
        #             extracted_id = dict_of_mapped_data_with_id[extracted_dataset_name]

        #             for i in range(len(temp_data)):
        #                     data = temp_data[i]
        #                     if data['dataset_id']==extracted_id:
        #                         p = json.dumps(data)
        #                         p = json.loads(p)
                                
                    

        #             if len(extracted_ls_entity) >=1:
        #                 # iterating through all entites other than dataset_name
        #                 for entity_iter in extracted_ls_entity:

        #                     # check if entity present in extracted_ls_entity is also present in p ( data in db)
                            
        #                     # spellcheck the entity
        #                     entity_iter = correction(entity_iter)
        #                     if entity_iter in p.keys() and entity_iter in entity_mapper:
        #                         entity_iter = entity_mapper[entity_iter]
                                
        #                         # if entity is present in p then print the value of that entity
        #                         print(f"{entity_iter} ----> {p[entity_iter]}")
        #                         dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)")
        #                         return [SlotSet('dataset_name', extracted_dataset_name)]
                            
        #                     else:
        #                         dispatcher.utter_message(text = 'Sorry but can you pls say it again')
        #                         # return [SlotSet('dataset_name', dataset_name)]
                    
        #             else:
        #                 dispatcher.utter_message(text = f'Yes you can start with {temp_dataset_name} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
        #                 return [SlotSet('dataset_name', extracted_dataset_name)]
        #     print(f"Returning value of {extracted_dataset_name}")
        #     return [SlotSet('dataset_name', extracted_dataset_name)]

        # else:
        #     dispatcher.utter_message(text='Sorry but seems like there is some Misspell in Dataset Name')                

        # # print(f"Returning value of {transformed_dataset_name}")
        # # return [SlotSet('dataset_name', temp_dataset_name)]
       

class ActionGranularityLevel(Action):

    def name(self) -> Text:
        return "action_about_data_granularity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global dataset_name_in_api
            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in granular is ",tracker.slots['dataset_name'])
            ls_entity = tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
                print('this is the dataset name which is setup as a slot value------', dataset_name_)
                dataset_name_ = dataset_name_.lower() 
                # calling global dictionary
                global master_dic_dataset_name

                print("Before spell check",dataset_name_)
                # spellcheck the name of dataset
                if dataset_name_ not in ['nsso','employment','non-crop','crop','foodgrains']:
                    print("Before spell check inside if",dataset_name_)
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_
                    print("after spellcheck inside if condition  ",dataset_name_)
                # elif len(ls_entity)>1: # removing that entity where datset name is nsso
                else:
                    print(ls_entity)
                    removable_index = [[j,i['value']] for j,i in enumerate(ls_entity) if i['value'] in  ['NSSO','Employment','Non-Crop','Crop','Foodgrains']]

          
                    print("\n",'printing removable index --',removable_index,"\n")

                    for last_check in removable_index:
                        # there are chance when employemnt and NSSO can come together 
                        # then to remove only NSSO dataset_name we used this last filter

                        print('printing last check --',last_check)

                        bracket_dataset_name = last_check[1]    #i.e crop, non-crop, nsso etc category

                        # iff NSSO found remove that corresponding dictionary from ls_entity
                        if last_check[1]=='NSSO':
                            removable_index = last_check[0]

                            # if not NSSO then remove then EMPLOYMENT entity dictionary from ls_entity
                        else:
                            # continue
                            removable_index = last_check[0]
    
                    
                    print("\n",removable_index,"\n")
                
                    ls_entity.pop(removable_index)
                    print("After Pop",ls_entity)

                    for iter in range(len(ls_entity)):
                        if ls_entity[iter]['entity']=='dataset_name' :
                            
                            # dataset_name_list_countter =  [i for i in range(len(ls_entity)) if ls_entity[i]['entity']=='dataset_name' ]
                            
                            print("word in a bracket",bracket_dataset_name)
                            if bracket_dataset_name=='Crop':

                                print("green")
                                dataset_name_  = ls_entity[iter]['value']
                            
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_crop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_c'
                                elif  dataset_name_ == 'Input Survey':
                                    dataset_name_ = 'input_crop'
                                  
                                else:
                                    dataset_name_ = dataset_name_
                                
                                break
                                
                            elif  bracket_dataset_name=='Non-Crop' :
                                # second_removable_index = iter
                                print("iter",iter)
                                # ls_entity.pop(second_removable_index)

                                # again we'll have to iterate to get dataset value
                                for iter  in range(len(ls_entity)):
                                    if ls_entity[iter]['entity']=='dataset_name' :
                                        dataset_name_  = ls_entity[iter]['value']

                                # as Non has came now just need to map to correct non option
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_noncrop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_nc'
                                elif  dataset_name_ == 'Input survey':
                                    dataset_name_ == 'input_crop'
                                else:
                                    dataset_name_ = dataset_name_
                                break

                            else:
                                dataset_name_  = ls_entity[iter]['value']

                        else:
                            continue  
                    print("Before spell check inside else",dataset_name_)
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_
                    print("after spellcheck inside else condition ",dataset_name_)
                # else:
                #     print("Before spell check inside else condition",dataset_name_)
                #     dataset_name_ = correction(dataset_name_)
                #     print("after spellcheck inside else condition ",dataset_name_)

                  # initializing punctuations string
                punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                
                # Removing punctuations in string
                # Using loop + punctuation string
                for ele in dataset_name_:
                    if ele in punc:
                        dataset_name_ = dataset_name_.replace(ele, " ")

                print("Removed punctuation marks",dataset_name_)


                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
                    print("IN",dataset_name_)
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
                    print("OUT",dataset_name_)

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in granularity is  {extracted_ls_entity}")

                print(ls_entity)

                # print('before removing datatset name from list - ', extracted_ls_entity)
                # if 'dataset_name' in extracted_ls_entity :
                #     extracted_ls_entity.remove('dataset_name')
                #     print('after removing datatset name from list - ', extracted_ls_entity)


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
                                print("yes i am in granularity with entity as ", entity_iter)
                                if entity_iter != 'dataset_name':
                                    # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                    # spellcheck the entity
                                    entity_iter = correction(entity_iter)

                                    if entity_iter in p.keys() and entity_iter in entity_mapper.keys():
                                        new_entity_iter = entity_mapper[entity_iter]
                                        # if entity is present in p then print the value of that entity
                                        # if entity_iter != 'dataset_name':
                                        print(f"{entity_iter} ----> {p[entity_iter]}")
                                        # dispatcher.utter_message(text = f" for {corrected_dataset_name_} {new_entity_iter} is {p[entity_iter]}")
                                        dispatcher.utter_message(text=f'{new_entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                        return [SlotSet('dataset_name', dataset_name_)]
                                        # elif entity_iter == 'dataset_name':
                                        #     print(f"Returning {dataset_name_}")
                                        #     return [SlotSet('dataset_name', dataset_name_)] 
                                    
                                    else:
                                        dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                        dispatcher.utter_message(text = """Ex :Like if you want to know Granularity level of a Dataset
                                                                            say it like :- What is the Granularity level of Rainfall Data""")
                                else:
                                    continue
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Granularity level of a Dataset
                                                                        say it like :- What is the Granularity level of Rainfall Data""")

                    else:
                        dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                        dispatcher.utter_message(text = """Ex :Like if you want to know Granularity level of a Dataset
                                                                        say it like :- What is the Granularity level of Rainfall Data""")

            else:
                dispatcher.utter_message(text = """Right now our datasets have the granularity level of states, districts and blocks. """)



class ActionSourcedata(Action):

    def name(self) -> Text:
        return "action_about_data_source_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global dataset_name_in_api
            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in source name  is ",tracker.slots['dataset_name'])
            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
                dataset_name_ = dataset_name_.lower() 
                # calling global dictionary
                global master_dic_dataset_name

                print("Before spell check",dataset_name_)
                # spellcheck the name of dataset
                if dataset_name_ not in ['nsso','employment','non-crop','crop','foodgrains']:
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_

                else: # removing that entity where datset name is nsso

                    print(ls_entity)
                    removable_index = [[j,i['value']] for j,i in enumerate(ls_entity) if i['value'] in  ['NSSO','Employment','Non-Crop','Crop','Foodgrains']]

          
                    print("\n",removable_index,"\n")

                    for last_check in removable_index:
                        # there are chance when employemnt and NSSO can come together 
                        # then to remove only NSSO dataset_name we used this last filter

                        print(last_check)

                        bracket_dataset_name = last_check[1]

                        # iff NSSO found remove that corresponding dictionary from ls_entity
                        if last_check[1]=='NSSO':
                            removable_index = last_check[0]

                            # if not NSSO then remove then EMPLOYMENT entity dictionary from ls_entity
                        else:
                            removable_index = last_check[0]
    
                    
                    print("\n",removable_index,"\n")
                
                    ls_entity.pop(removable_index)
                    print("After Pop",ls_entity)

                    for iter in range(len(ls_entity)):
                        if ls_entity[iter]['entity']=='dataset_name' :
                            
                            # dataset_name_list_countter =  [i for i in range(len(ls_entity)) if ls_entity[i]['entity']=='dataset_name' ]
                            
                            print("word in a bracket",bracket_dataset_name)
                            if bracket_dataset_name=='Crop':

                                print("green")
                                dataset_name_  = ls_entity[iter]['value']
                            
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_crop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_c'
                                elif  dataset_name_ == 'Input Survey':
                                    dataset_name_ = 'input_crop'
                                  
                                else:
                                    dataset_name_ = dataset_name_
                                
                                break
                                
                            elif  bracket_dataset_name=='Non-Crop' :
                                # second_removable_index = iter
                                print("iter",iter)
                                # ls_entity.pop(second_removable_index)

                                # again we'll have to iterate to get dataset value
                                for iter  in range(len(ls_entity)):
                                    if ls_entity[iter]['entity']=='dataset_name' :
                                        dataset_name_  = ls_entity[iter]['value']

                                # as Non has came now just need to map to correct non option
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_noncrop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_nc'
                                elif  dataset_name_ == 'Input survey':
                                    dataset_name_ == 'input_crop'
                                else:
                                    dataset_name_ = dataset_name_
                                break

                            else:
                                dataset_name_  = ls_entity[iter]['value']

                        else:
                            continue  

                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_
                print("after spellcheck ",dataset_name_)

                  # initializing punctuations string
                punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                
                # Removing punctuations in string
                # Using loop + punctuation string
                for ele in dataset_name_:
                    if ele in punc:
                        dataset_name_ = dataset_name_.replace(ele, " ")

                print("Removed punctuation marks",dataset_name_)


                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
                    print("IN",dataset_name_)
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
                    print("OUT",dataset_name_)

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in source name  is  {extracted_ls_entity}")

                print(ls_entity)

                # print('before removing datatset name from list - ', extracted_ls_entity)
                # if 'dataset_name' in extracted_ls_entity :
                #     extracted_ls_entity.remove('dataset_name')
                #     print('after removing datatset name from list - ', extracted_ls_entity)


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
                                print("yes i am in source with entity iter as", entity_iter)
                                if entity_iter != 'dataset_name':
                                    # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                    # spellcheck the entity
                                    entity_iter = correction(entity_iter)
                                    print("after correction in source",entity_iter)

                                    if entity_iter in p.keys() and entity_iter in entity_mapper.keys():
                                        new_entity_iter = entity_mapper[entity_iter]
                                        # if entity is present in p then print the value of that entity
                                        # if entity_iter != 'dataset_name':
                                        print(f"{entity_iter} ----> {p[entity_iter]}")
                                        # dispatcher.utter_message(text = f" for {corrected_dataset_name_} {new_entity_iter} is {p[entity_iter]}")
                                        dispatcher.utter_message(text=f'{new_entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                        return [SlotSet('dataset_name', dataset_name_)]
                                    # elif entity_iter == 'dataset_name':
                                    #     print(f"Returning {dataset_name_}")
                                    #     return [SlotSet('dataset_name', dataset_name_)] 
                                
                                    else:
                                        dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                        dispatcher.utter_message(text = """Ex :Like if you want to know Source name of a Dataset
                                                                            say it like :- what is source name for this dataset? """)
                                else: 
                                    continue                
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Source name of a Dataset
                                                                        say it like :- what's the source name of Agriculture Wages""")
                    else:
                        dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                        dispatcher.utter_message(text = """Ex :Like if you want to know Source name of a Dataset
                                                                        say it like :- what's the source name of Agriculture Wages""")

            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")



class ActionMethodology(Action):

    def name(self) -> Text:
        return "action_about_data_methodology"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global dataset_name_in_api
            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in methodology is ",tracker.slots['dataset_name'])
            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
                dataset_name_ = dataset_name_.lower() 
                # calling global dictionary
                global master_dic_dataset_name

                print("Before spell check",dataset_name_)
                # spellcheck the name of dataset
                if dataset_name_ not in ['nsso','employment','non-crop','crop','foodgrains']:
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_

                else: # removing that entity where datset name is nsso

                    print(ls_entity)
                    removable_index = [[j,i['value']] for j,i in enumerate(ls_entity) if i['value'] in  ['NSSO','Employment','Non-Crop','Crop','Foodgrains']]

          
                    print("\n",removable_index,"\n")

                    for last_check in removable_index:
                        # there are chance when employemnt and NSSO can come together 
                        # then to remove only NSSO dataset_name we used this last filter

                        print(last_check)

                        bracket_dataset_name = last_check[1]

                        # iff NSSO found remove that corresponding dictionary from ls_entity
                        if last_check[1]=='NSSO':
                            removable_index = last_check[0]

                            # if not NSSO then remove then EMPLOYMENT entity dictionary from ls_entity
                        else:
                            removable_index = last_check[0]
    
                    
                    print("\n",removable_index,"\n")
                
                    ls_entity.pop(removable_index)
                    print("After Pop",ls_entity)

                    for iter in range(len(ls_entity)):
                        if ls_entity[iter]['entity']=='dataset_name' :
                            
                            # dataset_name_list_countter =  [i for i in range(len(ls_entity)) if ls_entity[i]['entity']=='dataset_name' ]
                            
                            print("word in a bracket",bracket_dataset_name)
                            if bracket_dataset_name=='Crop':

                                print("green")
                                dataset_name_  = ls_entity[iter]['value']
                            
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_crop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_c'
                                elif  dataset_name_ == 'Input Survey':
                                    dataset_name_ = 'input_crop'
                                  
                                else:
                                    dataset_name_ = dataset_name_
                                
                                break
                                
                            elif  bracket_dataset_name=='Non-Crop' :
                                # second_removable_index = iter
                                print("iter",iter)
                                # ls_entity.pop(second_removable_index)

                                # again we'll have to iterate to get dataset value
                                for iter  in range(len(ls_entity)):
                                    if ls_entity[iter]['entity']=='dataset_name' :
                                        dataset_name_  = ls_entity[iter]['value']

                                # as Non has came now just need to map to correct non option
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_noncrop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_nc'
                                elif  dataset_name_ == 'Input survey':
                                    dataset_name_ == 'input_crop'
                                else:
                                    dataset_name_ = dataset_name_
                                break

                            else:
                                dataset_name_  = ls_entity[iter]['value']

                        else:
                            continue  

                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_
                print("after spellcheck ",dataset_name_)

                  # initializing punctuations string
                punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                
                # Removing punctuations in string
                # Using loop + punctuation string
                for ele in dataset_name_:
                    if ele in punc:
                        dataset_name_ = dataset_name_.replace(ele, " ")

                print("Removed punctuation marks",dataset_name_)


                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
                    print("IN",dataset_name_)
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
                    print("OUT",dataset_name_)

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in methodology is  {extracted_ls_entity}")

                print(ls_entity)

                # print('before removing datatset name from list - ', extracted_ls_entity)
                # if 'dataset_name' in extracted_ls_entity :
                #     extracted_ls_entity.remove('dataset_name')
                #     print('after removing datatset name from list - ', extracted_ls_entity)


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
                                print("yes i am in methodology with entity iter as ", entity_iter)
                                if entity_iter != 'dataset_name':
                                    # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                    # spellcheck the entity
                                    entity_iter = correction(entity_iter)

                                    if entity_iter in p.keys() and entity_iter in entity_mapper.keys():
                                        new_entity_iter = entity_mapper[entity_iter]
                                        # if entity is present in p then print the value of that entity
                                        print(f"{entity_iter} ----> {p[entity_iter]}")
                                        limited_methodology = p[entity_iter]
                                        # if entity_iter != 'dataset_name':

                                        if limited_methodology!=None:
                                            limited_methodology=limited_methodology[:350]
                                            dispatcher.utter_message(text = f" {new_entity_iter} is {limited_methodology} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)")
                                            return [SlotSet('dataset_name', dataset_name_)]
                                        else:
                                            dispatcher.utter_message(text = f" It will be updated in future for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)")
                                            return [SlotSet('dataset_name', dataset_name_)]
                                        # elif entity_iter == 'dataset_name':
                                        #     print(f"Returning {dataset_name_}")
                                        #     return [SlotSet('dataset_name', dataset_name_)] 
                                    
                                    else:
                                        dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                        dispatcher.utter_message(text = """Ex :Like if you want to know Methodology of a Dataset
                                                                            say it like :- What was the methodolgy adopted to make Rainfall Data""")
                                else:
                                    continue
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Methodology of a Dataset
                                                                        say it like :- What was the methodolgy adopted to make Rainfall Data""")
                    else:
                        dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                        dispatcher.utter_message(text = """Ex :Like if you want to know Methodology of a Dataset
                                                                        say it like :- What was the methodology adopted to make Rainfall Data""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")

class ActionFrequency(Action):

    def name(self) -> Text:
        return "action_about_data_frequency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global dataset_name_in_api
            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in frequency is ",tracker.slots['dataset_name'])
            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
                dataset_name_ = dataset_name_.lower() 
                # calling global dictionary
                global master_dic_dataset_name

                print("Before spell check",dataset_name_)
                # spellcheck the name of dataset
                if dataset_name_ not in ['nsso','employment','non-crop','crop','foodgrains']:
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_

                else: # removing that entity where datset name is nsso

                    print(ls_entity)
                    removable_index = [[j,i['value']] for j,i in enumerate(ls_entity) if i['value'] in  ['NSSO','Employment','Non-Crop','Crop','Foodgrains']]

          
                    print("\n",removable_index,"\n")

                    for last_check in removable_index:
                        # there are chance when employemnt and NSSO can come together 
                        # then to remove only NSSO dataset_name we used this last filter

                        print(last_check)

                        bracket_dataset_name = last_check[1]

                        # iff NSSO found remove that corresponding dictionary from ls_entity
                        if last_check[1]=='NSSO':
                            removable_index = last_check[0]

                            # if not NSSO then remove then EMPLOYMENT entity dictionary from ls_entity
                        else:
                            removable_index = last_check[0]
    
                    
                    print("\n",removable_index,"\n")
                
                    ls_entity.pop(removable_index)
                    print("After Pop",ls_entity)

                    for iter in range(len(ls_entity)):
                        if ls_entity[iter]['entity']=='dataset_name' :
                            
                            # dataset_name_list_countter =  [i for i in range(len(ls_entity)) if ls_entity[i]['entity']=='dataset_name' ]
                            
                            print("word in a bracket",bracket_dataset_name)
                            if bracket_dataset_name=='Crop':

                                print("green")
                                dataset_name_  = ls_entity[iter]['value']
                            
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_crop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_c'
                                elif  dataset_name_ == 'Input Survey':
                                    dataset_name_ = 'input_crop'
                                  
                                else:
                                    dataset_name_ = dataset_name_
                                
                                break
                                
                            elif  bracket_dataset_name=='Non-Crop' :
                                # second_removable_index = iter
                                print("iter",iter)
                                # ls_entity.pop(second_removable_index)

                                # again we'll have to iterate to get dataset value
                                for iter  in range(len(ls_entity)):
                                    if ls_entity[iter]['entity']=='dataset_name' :
                                        dataset_name_  = ls_entity[iter]['value']

                                # as Non has came now just need to map to correct non option
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_noncrop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_nc'
                                elif  dataset_name_ == 'Input survey':
                                    dataset_name_ == 'input_crop'
                                else:
                                    dataset_name_ = dataset_name_
                                break

                            else:
                                dataset_name_  = ls_entity[iter]['value']

                        else:
                            continue  

                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_
                print("after spellcheck ",dataset_name_)

                  # initializing punctuations string
                punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                
                # Removing punctuations in string
                # Using loop + punctuation string
                for ele in dataset_name_:
                    if ele in punc:
                        dataset_name_ = dataset_name_.replace(ele, " ")

                print("Removed punctuation marks",dataset_name_)


                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
                    print("IN",dataset_name_)
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
                    print("OUT",dataset_name_)

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in frequency is  {extracted_ls_entity}")

                print(ls_entity)

                # print('before removing datatset name from list - ', extracted_ls_entity)
                # if 'dataset_name' in extracted_ls_entity :
                #     extracted_ls_entity.remove('dataset_name')
                #     print('after removing datatset name from list - ', extracted_ls_entity)


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
                                print("yes i am in frequency with entity_iter", entity_iter)
                                if entity_iter != 'dataset_name':
                                    # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                    # spellcheck the entity
                                    entity_iter = correction(entity_iter)   

                                    if entity_iter in p.keys() and entity_iter in entity_mapper.keys():
                                        new_entity_iter = entity_mapper[entity_iter]
                                        # if entity is present in p then print the value of that entity
                                        # if entity_iter != 'dataset_name':
                                        print(f"{entity_iter} ----> {p[entity_iter]}")
                                        # dispatcher.utter_message(text = f" for {corrected_dataset_name_} {new_entity_iter} is {p[entity_iter]}")
                                        dispatcher.utter_message(text=f'{new_entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                        return [SlotSet('dataset_name', dataset_name_)]
                                        # elif entity_iter == 'dataset_name':
                                        #     print(f"Returning {dataset_name_}")
                                        #     return [SlotSet('dataset_name', dataset_name_)] 
                                    
                                    else:
                                        dispatcher.utter_message(text = 'Sorry but can you pls tell again what feature you are looking for')
                                        dispatcher.utter_message(text = """Ex :Like if you want to know Frequqncy at which Dataset is updated
                                                                            say it like :- how frequently does the agri wages data get updated?""")
                                else:
                                    continue
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Frequqncy at which Dataset is updated
                                                                        say it like :- how frequently does the agri wages data get updated?""")
                    else:
                        dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                        dispatcher.utter_message(text = """Ex :Like if you want to know Frequqncy at which Dataset is updated
                                                                        say it like :- how frequently does the agri wages data get updated?""")
            else:
                # dispatcher.utter_message(text = "Can you tell which dataset it is")
                dispatcher.utter_message(text = 'India Data Portal has data from various government sources and once the data is uploaded on the source, it is updated on the portal within a short time')
                
class ActionLastDateUpdated(Action):

    def name(self) -> Text:
        return "action_about_data_last_updated_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global dataset_name_in_api
            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in last updated date is ",tracker.slots['dataset_name'])
            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
                dataset_name_ = dataset_name_.lower() 
                # calling global dictionary
                global master_dic_dataset_name

                print("Before spell check",dataset_name_)
                # spellcheck the name of dataset
                if dataset_name_ not in ['nsso','employment','non-crop','crop','foodgrains']:
                    # global dataset_name_in_api
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_

                else: # removing that entity where datset name is nsso

                    print(ls_entity)
                    removable_index = [[j,i['value']] for j,i in enumerate(ls_entity) if i['value'] in  ['NSSO','Employment','Non-Crop','Crop','Foodgrains']]

          
                    print("\n",removable_index,"\n")

                    for last_check in removable_index:
                        # there are chance when employemnt and NSSO can come together 
                        # then to remove only NSSO dataset_name we used this last filter

                        print(last_check)

                        bracket_dataset_name = last_check[1]

                        # iff NSSO found remove that corresponding dictionary from ls_entity
                        if last_check[1]=='NSSO':
                            removable_index = last_check[0]

                            # if not NSSO then remove then EMPLOYMENT entity dictionary from ls_entity
                        else:
                            removable_index = last_check[0]
    
                    
                    print("\n",removable_index,"\n")
                
                    ls_entity.pop(removable_index)
                    print("After Pop",ls_entity)

                    for iter in range(len(ls_entity)):
                        if ls_entity[iter]['entity']=='dataset_name' :
                            
                            # dataset_name_list_countter =  [i for i in range(len(ls_entity)) if ls_entity[i]['entity']=='dataset_name' ]
                            
                            print("word in a bracket",bracket_dataset_name)
                            if bracket_dataset_name=='Crop':

                                print("green")
                                dataset_name_  = ls_entity[iter]['value']
                            
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_crop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_c'
                                elif  dataset_name_ == 'Input Survey':
                                    dataset_name_ = 'input_crop'
                                  
                                else:
                                    dataset_name_ = dataset_name_
                                
                                break
                                
                            elif  bracket_dataset_name=='Non-Crop' :
                                # second_removable_index = iter
                                print("iter",iter)
                                # ls_entity.pop(second_removable_index)

                                # again we'll have to iterate to get dataset value
                                for iter  in range(len(ls_entity)):
                                    if ls_entity[iter]['entity']=='dataset_name' :
                                        dataset_name_  = ls_entity[iter]['value']

                                # as Non has came now just need to map to correct non option
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_noncrop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_nc'
                                elif  dataset_name_ == 'Input survey':
                                    dataset_name_ == 'input_crop'
                                else:
                                    dataset_name_ = dataset_name_
                                break

                            else:
                                dataset_name_  = ls_entity[iter]['value']

                        else:
                            continue  
                    
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print('passed api check')
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print('failed api test')
                print("after spellcheck -------",dataset_name_)

                  # initializing punctuations string
                punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                
                # Removing punctuations in string
                # Using loop + punctuation string
                for ele in dataset_name_:
                    if ele in punc:
                        dataset_name_ = dataset_name_.replace(ele, " ")

                print("Removed punctuation marks",dataset_name_)


                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
                    print("IN",dataset_name_)
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
                    print("OUT",dataset_name_)

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in last updated date is  {extracted_ls_entity}")

                print(ls_entity)

                # print('before removing datatset name from list - ', extracted_ls_entity)
                # if 'dataset_name' in extracted_ls_entity :
                #     extracted_ls_entity.remove('dataset_name')
                #     print('after removing datatset name from list - ', extracted_ls_entity)


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
                                print("yes i am in Last Date Updated with entity_iter - ", entity_iter)
                                if entity_iter != 'dataset_name':
                                    # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                    # spellcheck the entity
                                    entity_iter = correction(entity_iter)

                                    if entity_iter in p.keys() and entity_iter in entity_mapper.keys():
                                        new_entity_iter = entity_mapper[entity_iter]
                                        # if entity is present in p then print the value of that entity
                                        # if entity_iter != 'dataset_name':
                                        print(f"{entity_iter} ----> {p[entity_iter]}")
                                        # dispatcher.utter_message(text = f" for {corrected_dataset_name_} {new_entity_iter} is {p[entity_iter]}")
                                        dispatcher.utter_message(text=f'{new_entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                        return [SlotSet('dataset_name', dataset_name_)]
                                    # elif entity_iter == 'dataset_name':
                                    #     print(f"Returning {dataset_name_}")
                                    #     # dispatcher.utter_message(text=f'{new_entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                    #     return [SlotSet('dataset_name', dataset_name_)]                               
                                    else:
                                        dispatcher.utter_message(text = 'Sorry but can you pls tell again what feature you are looking for')
                                        dispatcher.utter_message(text = """Ex :Like if you want to know Last Date updated for a Dataset 
                                                                        say it like :- when was the last updated data uploaded""")
                                else:
                                    continue
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Last Date updated for a Dataset 
                                                                        say it like :- i'd like to know the last updated date of mgnrega employment""")
                    else:
                        dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                        dispatcher.utter_message(text = """Ex :Like if you want to know Last Date updated for a Dataset 
                                                                        say it like :- i'd like to know the last updated date of mgnrega employment""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")


class ActionSourceLink(Action):

    def name(self) -> Text:
        return "action_about_data_source_link"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global dataset_name_in_api
            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in source link is ",tracker.slots['dataset_name'])
            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
                dataset_name_ = dataset_name_.lower() 
                # calling global dictionary
                global master_dic_dataset_name

                print("Before spell check",dataset_name_)
                # spellcheck the name of dataset
                if dataset_name_ not in ['nsso','employment','non-crop','crop','foodgrains']:
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_

                else: # removing that entity where datset name is nsso

                    print(ls_entity)
                    removable_index = [[j,i['value']] for j,i in enumerate(ls_entity) if i['value'] in  ['NSSO','Employment','Non-Crop','Crop','Foodgrains']]

          
                    print("\n",removable_index,"\n")

                    for last_check in removable_index:
                        # there are chance when employemnt and NSSO can come together 
                        # then to remove only NSSO dataset_name we used this last filter

                        print(last_check)

                        bracket_dataset_name = last_check[1]

                        # iff NSSO found remove that corresponding dictionary from ls_entity
                        if last_check[1]=='NSSO':
                            removable_index = last_check[0]

                            # if not NSSO then remove then EMPLOYMENT entity dictionary from ls_entity
                        else:
                            removable_index = last_check[0]
    
                    
                    print("\n",removable_index,"\n")
                
                    ls_entity.pop(removable_index)
                    print("After Pop",ls_entity)

                    for iter in range(len(ls_entity)):
                        if ls_entity[iter]['entity']=='dataset_name' :
                            
                            # dataset_name_list_countter =  [i for i in range(len(ls_entity)) if ls_entity[i]['entity']=='dataset_name' ]
                            
                            print("word in a bracket",bracket_dataset_name)
                            if bracket_dataset_name=='Crop':

                                print("green")
                                dataset_name_  = ls_entity[iter]['value']
                            
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_crop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_c'
                                elif  dataset_name_ == 'Input Survey':
                                    dataset_name_ = 'input_crop'
                                  
                                else:
                                    dataset_name_ = dataset_name_
                                
                                break
                                
                            elif  bracket_dataset_name=='Non-Crop' :
                                # second_removable_index = iter
                                print("iter",iter)
                                # ls_entity.pop(second_removable_index)

                                # again we'll have to iterate to get dataset value
                                for iter  in range(len(ls_entity)):
                                    if ls_entity[iter]['entity']=='dataset_name' :
                                        dataset_name_  = ls_entity[iter]['value']

                                # as Non has came now just need to map to correct non option
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_noncrop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_nc'
                                elif  dataset_name_ == 'Input survey':
                                    dataset_name_ == 'input_crop'
                                else:
                                    dataset_name_ = dataset_name_
                                break

                            else:
                                dataset_name_  = ls_entity[iter]['value']

                        else:
                            continue  

                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_
                print("after spellcheck ",dataset_name_)

                  # initializing punctuations string
                punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                
                # Removing punctuations in string
                # Using loop + punctuation string
                for ele in dataset_name_:
                    if ele in punc:
                        dataset_name_ = dataset_name_.replace(ele, " ")

                print("Removed punctuation marks",dataset_name_)


                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
                    print("IN",dataset_name_)
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
                    print("OUT",dataset_name_)

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in source link is  {extracted_ls_entity}")

                print(ls_entity)

                # print('before removing datatset name from list - ', extracted_ls_entity)
                # if 'dataset_name' in extracted_ls_entity :
                #     extracted_ls_entity.remove('dataset_name')
                #     print('after removing datatset name from list - ', extracted_ls_entity)


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
                    if dataset_name_ in list(dict_of_mapped_data_with_id.keys()):
                        
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
                                print("yes i am in Source Link with entity iter as ", entity_iter)
                                if entity_iter != 'dataset_name':
                                    # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                    # spellcheck the entity
                                    entity_iter = correction(entity_iter)

                                    if entity_iter in p.keys() and entity_iter in entity_mapper.keys():
                                        new_entity_iter = entity_mapper[entity_iter]
                                        # if entity is present in p then print the value of that entity
                                        # if entity_iter != 'dataset_name':
                                        print(f"{entity_iter} ----> {p[entity_iter]}")
                                        # dispatcher.utter_message(text = f" for {corrected_dataset_name_} {new_entity_iter} is {p[entity_iter]}")
                                        dispatcher.utter_message(text=f'{new_entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                        return [SlotSet('dataset_name', dataset_name_)]
                                        # elif entity_iter == 'dataset_name':
                                        #     print(f"Returning {dataset_name_}")
                                        #     return [SlotSet('dataset_name', dataset_name_)] 
                                    else:
                                        dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                        dispatcher.utter_message(text = """Ex :Like if you want to know Source Link for a Dataset 
                                                                            say it like :- I need a source link for this data""")
                                else:
                                    continue
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Source Link for a Dataset 
                                                                        say it like :- Kindly give me a source link for rural wages dataset""")
                    else:
                        dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                        dispatcher.utter_message(text = """Ex :Like if you want to know Source Link for a Dataset 
                                                                        say it like :- Kindly give me a source link for rural wages dataset""")
            else:
                # dispatcher.utter_message(text = "Can you tell which dataset it is")
                dispatcher.utter_message(text='The source of the data can be found at the bottom of the image that is downloaded which can be accessed through the informations section of the dataset')


class ActionDataExtractionPage(Action):

    def name(self) -> Text:
        return "action_about_data_data_extraction_page"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global dataset_name_in_api
            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in data extraction page is ",tracker.slots['dataset_name'])
            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
                dataset_name_ = dataset_name_.lower() 
                # calling global dictionary
                global master_dic_dataset_name

                print("Before spell check",dataset_name_)
                # spellcheck the name of dataset
                if dataset_name_ not in ['nsso','employment','non-crop','crop','foodgrains']:
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_

                else: # removing that entity where datset name is nsso

                    print(ls_entity)
                    removable_index = [[j,i['value']] for j,i in enumerate(ls_entity) if i['value'] in  ['NSSO','Employment','Non-Crop','Crop','Foodgrains']]

          
                    print("\n",removable_index,"\n")

                    for last_check in removable_index:
                        # there are chance when employemnt and NSSO can come together 
                        # then to remove only NSSO dataset_name we used this last filter

                        print(last_check)

                        bracket_dataset_name = last_check[1]

                        # iff NSSO found remove that corresponding dictionary from ls_entity
                        if last_check[1]=='NSSO':
                            removable_index = last_check[0]

                            # if not NSSO then remove then EMPLOYMENT entity dictionary from ls_entity
                        else:
                            removable_index = last_check[0]
    
                    
                    print("\n",removable_index,"\n")
                
                    ls_entity.pop(removable_index)
                    print("After Pop",ls_entity)

                    for iter in range(len(ls_entity)):
                        if ls_entity[iter]['entity']=='dataset_name' :
                            
                            # dataset_name_list_countter =  [i for i in range(len(ls_entity)) if ls_entity[i]['entity']=='dataset_name' ]
                            
                            print("word in a bracket",bracket_dataset_name)
                            if bracket_dataset_name=='Crop':

                                print("green")
                                dataset_name_  = ls_entity[iter]['value']
                            
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_crop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_c'
                                elif  dataset_name_ == 'Input Survey':
                                    dataset_name_ = 'input_crop'
                                  
                                else:
                                    dataset_name_ = dataset_name_
                                
                                break
                                
                            elif  bracket_dataset_name=='Non-Crop' :
                                # second_removable_index = iter
                                print("iter",iter)
                                # ls_entity.pop(second_removable_index)

                                # again we'll have to iterate to get dataset value
                                for iter  in range(len(ls_entity)):
                                    if ls_entity[iter]['entity']=='dataset_name' :
                                        dataset_name_  = ls_entity[iter]['value']

                                # as Non has came now just need to map to correct non option
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_noncrop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_nc'
                                elif  dataset_name_ == 'Input survey':
                                    dataset_name_ == 'input_crop'
                                else:
                                    dataset_name_ = dataset_name_
                                break

                            else:
                                dataset_name_  = ls_entity[iter]['value']

                        else:
                            continue  

                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_
                print("after spellcheck ",dataset_name_)

                  # initializing punctuations string
                punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                
                # Removing punctuations in string
                # Using loop + punctuation string
                for ele in dataset_name_:
                    if ele in punc:
                        dataset_name_ = dataset_name_.replace(ele, " ")

                print("Removed punctuation marks",dataset_name_)


                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
                    print("IN",dataset_name_)
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
                    print("OUT",dataset_name_)

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in data extraction page is  {extracted_ls_entity}")

                print(ls_entity)

                # print('before removing datatset name from list - ', extracted_ls_entity)
                # if 'dataset_name' in extracted_ls_entity :
                #     extracted_ls_entity.remove('dataset_name')
                #     print('after removing datatset name from list - ', extracted_ls_entity)


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
                                print("yes i am in extarct data with entity iter as ", entity_iter)
                                if entity_iter != 'dataset_name':
                                    # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                    # spellcheck the entity
                                    entity_iter = correction(entity_iter)

                                    if entity_iter in p.keys() and entity_iter in entity_mapper.keys():
                                        new_entity_iter = entity_mapper[entity_iter]
                                        # if entity is present in p then print the value of that entity
                                        # if entity_iter != 'dataset_name':
                                        print(f"{entity_iter} ----> {p[entity_iter]}")
                                        # dispatcher.utter_message(text = f" for {corrected_dataset_name_} {new_entity_iter} is {p[entity_iter]}")
                                        dispatcher.utter_message(text=f'{new_entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                        return [SlotSet('dataset_name', dataset_name_)]
                                        # elif entity_iter == 'dataset_name':
                                        #     print(f"Returning {dataset_name_}")
                                        #     return [SlotSet('dataset_name', dataset_name_)] 
                                    
                                    else:
                                        dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                        dispatcher.utter_message(text = """Ex :Like if you want to get Data extraction page for a Dataset 
                                                                            say it like :- where i can get the extraction page for apy data?""")
                                else:
                                    continue
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to get Data extraction page for a Dataset 
                                                                        say it like :- where i can get the extraction page for apy data?""")
                    else:
                        dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                        dispatcher.utter_message(text = """Ex :Like if you want to get Data extraction page for a Dataset 
                                                                        say it like :- where i can get the extraction page for apy data?""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")

class ActionDetailedSourceName(Action):

    def name(self) -> Text:
        return "action_about_data_source_name_det"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global dataset_name_in_api
            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in source name detailed is ",tracker.slots['dataset_name'])
            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
                dataset_name_ = dataset_name_.lower() 
                # calling global dictionary
                global master_dic_dataset_name

                print("Before spell check",dataset_name_)
                # spellcheck the name of dataset
                if dataset_name_ not in ['nsso','employment','non-crop','crop','foodgrains']:
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_

                else: # removing that entity where datset name is nsso

                    print(ls_entity)
                    removable_index = [[j,i['value']] for j,i in enumerate(ls_entity) if i['value'] in  ['NSSO','Employment','Non-Crop','Crop','Foodgrains']]

          
                    print("\n",removable_index,"\n")

                    for last_check in removable_index:
                        # there are chance when employemnt and NSSO can come together 
                        # then to remove only NSSO dataset_name we used this last filter

                        print(last_check)

                        bracket_dataset_name = last_check[1]

                        # iff NSSO found remove that corresponding dictionary from ls_entity
                        if last_check[1]=='NSSO':
                            removable_index = last_check[0]

                            # if not NSSO then remove then EMPLOYMENT entity dictionary from ls_entity
                        else:
                            removable_index = last_check[0]
    
                    
                    print("\n",removable_index,"\n")
                
                    ls_entity.pop(removable_index)
                    print("After Pop",ls_entity)

                    for iter in range(len(ls_entity)):
                        if ls_entity[iter]['entity']=='dataset_name' :
                            
                            # dataset_name_list_countter =  [i for i in range(len(ls_entity)) if ls_entity[i]['entity']=='dataset_name' ]
                            
                            print("word in a bracket",bracket_dataset_name)
                            if bracket_dataset_name=='Crop':

                                print("green")
                                dataset_name_  = ls_entity[iter]['value']
                            
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_crop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_c'
                                elif  dataset_name_ == 'Input Survey':
                                    dataset_name_ = 'input_crop'
                                  
                                else:
                                    dataset_name_ = dataset_name_
                                
                                break
                                
                            elif  bracket_dataset_name=='Non-Crop' :
                                # second_removable_index = iter
                                print("iter",iter)
                                # ls_entity.pop(second_removable_index)

                                # again we'll have to iterate to get dataset value
                                for iter  in range(len(ls_entity)):
                                    if ls_entity[iter]['entity']=='dataset_name' :
                                        dataset_name_  = ls_entity[iter]['value']

                                # as Non has came now just need to map to correct non option
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_noncrop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_nc'
                                elif  dataset_name_ == 'Input survey':
                                    dataset_name_ == 'input_crop'
                                else:
                                    dataset_name_ = dataset_name_
                                break

                            else:
                                dataset_name_  = ls_entity[iter]['value']

                        else:
                            continue  

                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_
                print("after spellcheck ",dataset_name_)

                  # initializing punctuations string
                punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                
                # Removing punctuations in string
                # Using loop + punctuation string
                for ele in dataset_name_:
                    if ele in punc:
                        dataset_name_ = dataset_name_.replace(ele, " ")

                print("Removed punctuation marks",dataset_name_)


                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
                    print("IN",dataset_name_)
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
                    print("OUT",dataset_name_)

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in source name detailed is  {extracted_ls_entity}")

                print(ls_entity)

                # print('before removing datatset name from list - ', extracted_ls_entity)
                # if 'dataset_name' in extracted_ls_entity :
                #     extracted_ls_entity.remove('dataset_name')
                #     print('after removing datatset name from list - ', extracted_ls_entity)


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
                                print("yes i am in detailed source name with entity_iter as", entity_iter)
                                if entity_iter != 'dataset_name':
                                    # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                    # spellcheck the entity
                                    entity_iter = correction(entity_iter)
                                    print("after correction in detailed source name",entity_iter)

                                    if entity_iter in p.keys() and entity_iter in entity_mapper.keys():
                                        new_entity_iter = entity_mapper[entity_iter]
                                        # if entity is present in p then print the value of that entity
                                        # if entity_iter != 'dataset_name' and new_entity_iter == 'Source Name Det':
                                        if new_entity_iter == 'Source Name Det':
                                            new_entity_iter = 'Detailed source name'
                                            print(f"{entity_iter} ----> {p[entity_iter]}")
                                            # dispatcher.utter_message(text = f" for {corrected_dataset_name_} {new_entity_iter} is {p[entity_iter]}")
                                            dispatcher.utter_message(text=f'{new_entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                            return [SlotSet('dataset_name', dataset_name_)]
                                        else:
                                            print(f"Returning {dataset_name_}")
                                            return [SlotSet('dataset_name', dataset_name_)] 
                                    
                                    else:
                                        dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                        dispatcher.utter_message(text = """Ex :Like if you want to know Detailed Source name of a Dataset
                                                                            say it like :- What is the Source of Rainfall Data""")
                                else:
                                    continue                
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Detailed Source name of a Dataset
                                                                        say it like :- What is the Source of Rainfall Data""")
                    else:
                        dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                        dispatcher.utter_message(text = """Ex :Like if you want to know Detailed Source name of a Dataset
                                                                        say it like :- I want to know the detailed source name for household consumption on eduaction data.""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")

class ActionDateofRetrievals(Action):

    def name(self) -> Text:
        return "action_about_data_date_of_retrievals"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global dataset_name_in_api
            # intent of user message 
            print(tracker.get_intent_of_latest_message())

            print("\n","Now slots value in date of retrievals is ",tracker.slots['dataset_name'])
            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
                dataset_name_ = dataset_name_.lower() 
                # calling global dictionary
                global master_dic_dataset_name

                print("Before spell check",dataset_name_)
                # spellcheck the name of dataset
                if dataset_name_ not in ['nsso','employment','non-crop','crop','foodgrains']:
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_

                else: # removing that entity where datset name is nsso

                    print(ls_entity)
                    removable_index = [[j,i['value']] for j,i in enumerate(ls_entity) if i['value'] in  ['NSSO','Employment','Non-Crop','Crop','Foodgrains']]

          
                    print("\n",removable_index,"\n")

                    for last_check in removable_index:
                        # there are chance when employemnt and NSSO can come together 
                        # then to remove only NSSO dataset_name we used this last filter

                        print(last_check)

                        bracket_dataset_name = last_check[1]

                        # iff NSSO found remove that corresponding dictionary from ls_entity
                        if last_check[1]=='NSSO':
                            removable_index = last_check[0]

                            # if not NSSO then remove then EMPLOYMENT entity dictionary from ls_entity
                        else:
                            removable_index = last_check[0]
    
                    
                    print("\n",removable_index,"\n")
                
                    ls_entity.pop(removable_index)
                    print("After Pop",ls_entity)

                    for iter in range(len(ls_entity)):
                        if ls_entity[iter]['entity']=='dataset_name' :
                            
                            # dataset_name_list_countter =  [i for i in range(len(ls_entity)) if ls_entity[i]['entity']=='dataset_name' ]
                            
                            print("word in a bracket",bracket_dataset_name)
                            if bracket_dataset_name=='Crop':

                                print("green")
                                dataset_name_  = ls_entity[iter]['value']
                            
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_crop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_c'
                                elif  dataset_name_ == 'Input Survey':
                                    dataset_name_ = 'input_crop'
                                  
                                else:
                                    dataset_name_ = dataset_name_
                                
                                break
                                
                            elif  bracket_dataset_name=='Non-Crop' :
                                # second_removable_index = iter
                                print("iter",iter)
                                # ls_entity.pop(second_removable_index)

                                # again we'll have to iterate to get dataset value
                                for iter  in range(len(ls_entity)):
                                    if ls_entity[iter]['entity']=='dataset_name' :
                                        dataset_name_  = ls_entity[iter]['value']

                                # as Non has came now just need to map to correct non option
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_noncrop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_nc'
                                elif  dataset_name_ == 'Input survey':
                                    dataset_name_ == 'input_crop'
                                else:
                                    dataset_name_ = dataset_name_
                                break

                            else:
                                dataset_name_  = ls_entity[iter]['value']

                        else:
                            continue  

                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_
                print("after spellcheck ",dataset_name_)

                  # initializing punctuations string
                punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                
                # Removing punctuations in string
                # Using loop + punctuation string
                for ele in dataset_name_:
                    if ele in punc:
                        dataset_name_ = dataset_name_.replace(ele, " ")

                print("Removed punctuation marks",dataset_name_)


                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
                    print("IN",dataset_name_)
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
                    print("OUT",dataset_name_)

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in date of retrievals is  {extracted_ls_entity}")
                
                # as entity was extracted more than once there fore we are making set of that list
                extracted_ls_entity = list(set(extracted_ls_entity))
                print(f"Entites we extracted in date of retrievals after removing duplicates is  {extracted_ls_entity}")
                print(ls_entity)

                # print('before removing datatset name from list - ', extracted_ls_entity)
                # if 'dataset_name' in extracted_ls_entity :
                #     extracted_ls_entity.remove('dataset_name')
                #     print('after removing datatset name from list - ', extracted_ls_entity)


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
                                print("yes i am in date of retrievals with entity_iter - ", entity_iter)
                                if entity_iter != 'dataset_name':
                                    # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                    # spellcheck the entity
                                    entity_iter = correction(entity_iter)
                                    print("after correction in date of retrievals ",entity_iter)

                                    if entity_iter in p.keys() and entity_iter in entity_mapper.keys():
                                        new_entity_iter = entity_mapper[entity_iter]
                                        # if entity is present in p then print the value of that entity
                                        # if entity_iter != 'dataset_name':
                                        print(f"{entity_iter} ----> {p[entity_iter]}")
                                        # dispatcher.utter_message(text = f" for {corrected_dataset_name_} {new_entity_iter} is {p[entity_iter]}")
                                        dispatcher.utter_message(text=f'{new_entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                        return [SlotSet('dataset_name', dataset_name_)]
                                    # elif entity_iter == 'dataset_name':
                                    #     print(f"Returning {dataset_name_}")
                                    #     return [SlotSet('dataset_name', dataset_name_)] 
                                
                                    else:
                                        dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                        dispatcher.utter_message(text = """Ex :Like if you want to know Date of Retrieval for a Dataset
                                                                            say it like :- Can you provide me the retrieval date for foodgrain stock data""")
                                else:
                                    continue              
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Date of Retrieval for a Dataset
                                                                        say it like :- Can you provide me the retrieval date for foodgrain stock data""")
                    else:
                        dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                        dispatcher.utter_message(text = """Ex :Like if you want to know Date of Retrieval for a Dataset
                                                                        say it like :- Can you provide me the retrieval date for foodgrain stock data""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")
# THIS PART(ActionDomainName) IS BEING HARDCODED AS DISCUSSSED WITH THE GURSHARAN ON 28TH SEPTEMBER 2021
class ActionDomainName(Action):

    def name(self) -> Text:
        return "action_about_data_domain_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            global dataset_name_in_api
            # intent of user message 
            print(tracker.get_intent_of_latest_message())
            global dict_of_domain_ids

            print(dict_of_domain_ids,"DOmain ids")
            print("\n","Now slots value in domain is ",tracker.slots['dataset_name'])
            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']
                dataset_name_ = dataset_name_.lower() 
                # calling global dictionary
                global master_dic_dataset_name

                print("Before spell check",dataset_name_)
                # spellcheck the name of dataset
                if dataset_name_ not in ['nsso','employment','non-crop','crop','foodgrains']:
                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_

                else: # removing that entity where datset name is nsso

                    print(ls_entity)
                    removable_index = [[j,i['value']] for j,i in enumerate(ls_entity) if i['value'] in  ['NSSO','Employment','Non-Crop','Crop','Foodgrains']]

          
                    print("\n",removable_index,"\n")

                    for last_check in removable_index:
                        # there are chance when employemnt and NSSO can come together 
                        # then to remove only NSSO dataset_name we used this last filter

                        print(last_check)

                        bracket_dataset_name = last_check[1]

                        # iff NSSO found remove that corresponding dictionary from ls_entity
                        if last_check[1]=='NSSO':
                            removable_index = last_check[0]

                            # if not NSSO then remove then EMPLOYMENT entity dictionary from ls_entity
                        else:
                            removable_index = last_check[0]
    
                    
                    print("\n",removable_index,"\n")
                
                    ls_entity.pop(removable_index)
                    print("After Pop",ls_entity)

                    for iter in range(len(ls_entity)):
                        if ls_entity[iter]['entity']=='dataset_name' :
                            
                            # dataset_name_list_countter =  [i for i in range(len(ls_entity)) if ls_entity[i]['entity']=='dataset_name' ]
                            
                            print("word in a bracket",bracket_dataset_name)
                            if bracket_dataset_name=='Crop':

                                print("green")
                                dataset_name_  = ls_entity[iter]['value']
                            
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_crop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_c'
                                elif  dataset_name_ == 'Input Survey':
                                    dataset_name_ = 'input_crop'
                                  
                                else:
                                    dataset_name_ = dataset_name_
                                
                                break
                                
                            elif  bracket_dataset_name=='Non-Crop' :
                                # second_removable_index = iter
                                print("iter",iter)
                                # ls_entity.pop(second_removable_index)

                                # again we'll have to iterate to get dataset value
                                for iter  in range(len(ls_entity)):
                                    if ls_entity[iter]['entity']=='dataset_name' :
                                        dataset_name_  = ls_entity[iter]['value']

                                # as Non has came now just need to map to correct non option
                                if dataset_name_ == 'Agricultural Census 2010-11':

                                    dataset_name_ = 'agcensus_noncrop'
                                elif dataset_name_ == 'Agricultural Census 2015-16':
                                    dataset_name_ = 'agcensus_nc'
                                elif  dataset_name_ == 'Input survey':
                                    dataset_name_ == 'input_crop'
                                else:
                                    dataset_name_ = dataset_name_
                                break

                            else:
                                dataset_name_  = ls_entity[iter]['value']

                        else:
                            continue  

                    if dataset_name_ in dataset_name_in_api:
                        dataset_name_ = dataset_name_
                        print("dataset's api name is being setup as a slot value therefore no spellcheck" )
                    else:
                        dataset_name_ = correction(dataset_name_)
                        corrected_dataset_name_ = dataset_name_
                        print("dataset's api name is not setted up as a slot value therefore we will use spellcheck")
                    # dataset_name_ = correction(dataset_name_)
                    # corrected_dataset_name_ = dataset_name_
                print("after spellcheck ",dataset_name_)

                  # initializing punctuations string
                punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                
                # Removing punctuations in string
                # Using loop + punctuation string
                for ele in dataset_name_:
                    if ele in punc:
                        dataset_name_ = dataset_name_.replace(ele, " ")

                print("Removed punctuation marks",dataset_name_)


                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
                    print("IN",dataset_name_)
                    dataset_name_ = master_dic_dataset_name[dataset_name_]
                    print("OUT",dataset_name_)

                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in domain is  {extracted_ls_entity}")
                
                # as entity was extracted more than once there fore we are making set of that list
                extracted_ls_entity = list(set(extracted_ls_entity))
                print(f"Entites we extracted in domain after removing duplicates is  {extracted_ls_entity}")
                print(ls_entity)

                # print('before removing datatset name from list - ', extracted_ls_entity)
                # if 'dataset_name' in extracted_ls_entity :
                #     extracted_ls_entity.remove('dataset_name')
                #     print('after removing datatset name from list - ', extracted_ls_entity)


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
                                print("yes i am in domain with entity_iter - ", entity_iter)
                                if entity_iter != 'dataset_name':
                                    # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                    # spellcheck the entity
                                    entity_iter = correction(entity_iter)
                                    print("after correction in domain ",entity_iter)
                                    for id_for_domain in dict_of_domain_ids.keys():
                                        # print('id for domain mapping', id_for_domain)
                                        if id_for_domain == extracted_id:
                                            dispatcher.utter_message(text = f'{dict_of_domain_ids[id_for_domain]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                            return [SlotSet('dataset_name', dataset_name_)]
                                        # break
                                        else:
                                            continue
                                    # if entity_iter in p.keys() and entity_iter in entity_mapper.keys():
                                    #     new_entity_iter = entity_mapper[entity_iter]
                                    #     # if entity is present in p then print the value of that entity
                                    #     # if entity_iter != 'dataset_name':
                                    #     print(f"{entity_iter} ----> {p[entity_iter]}")
                                    #     # dispatcher.utter_message(text = f" for {corrected_dataset_name_} {new_entity_iter} is {p[entity_iter]}")
                                    #     dispatcher.utter_message(text=f'{new_entity_iter} is {p[entity_iter]} for more [click here](https://indiadataportal.com/visualize?language=English&location=India#?dataset_id={extracted_id}&tab=details-tab)')
                                    # # elif entity_iter == 'dataset_name':
                                    # #     print(f"Returning {dataset_name_}")
                                    # #     return [SlotSet('dataset_name', dataset_name_)] 
                                
                                    # else:
                                    #     dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    #     dispatcher.utter_message(text = """Ex :Like if you want to know Date of Retrieval for a Dataset
                                    #                                       say it like :- Can you provide me the retrieval date for foodgrain stock data""")
                                else:
                                    continue              
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Date of Retrieval for a Dataset
                                                                        say it like :- Can you provide me the retrieval date for foodgrain stock data""")
                    else:
                        dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                        dispatcher.utter_message(text = """Ex :Like if you want to know Date of Retrieval for a Dataset
                                                                        say it like :- Can you provide me the retrieval date for foodgrain stock data""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")


