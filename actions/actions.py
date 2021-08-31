



from typing import Any, Text, Dict, List
import urllib.request, json
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from gensim.models import KeyedVectors
from spellcheck import correction , master_dic_dataset_name
import numpy as np
from gensim import models
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
        
        dispatcher.utter_message(attachment="You can provide your feedback to us in this [Feedback Form](https://forms.gle/Fk1TxTzAteigKFG87)")
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

    def remove_punctuation_mark_from_user_entity(self, user_entity):
        # define punctuation
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        my_str = str(user_entity)
        # remove punctuation from the string
        no_punct = ""
        for ele in my_str:
            if ele in punctuations:
                user_entity = user_entity.replace(ele, " ")

        # display the unpunctuated string
        # print(user_entity)
        return user_entity

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        # word_vectors = KeyedVectors.load_word2vec_format("/home/ubuntu/17aug_word2vec_bot/GoogleNews-vectors-negative300.bin",binary=True)
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

        # converting name extracted to lower case
        if type(extracted_dataset_name)!=int:
            extracted_dataset_name = extracted_dataset_name.lower()

            # corrected extracted_dataset_name
            extracted_dataset_name = correction(extracted_dataset_name)

            print(f'after correction {extracted_dataset_name}')

        if extracted_dataset_name in master_dic_dataset_name.keys():
            

            transformed_dataset_name = master_dic_dataset_name[extracted_dataset_name]

        else:
            if extracted_dataset_name != 0:
                # word_vectors = models.KeyedVectors.load_word2vec_format("/home/ubuntu/17aug_word2vec_bot/GoogleNews-vectors-negative300.bin",binary= True, limit = 50000)
                word_vectors = models.KeyedVectors.load("/home/ubuntu/17aug_word2vec_bot/GoogleNews-vectors-negative300.kv",mmap='r')
                extracted_dataset_name = self.remove_punctuation_mark_from_user_entity(extracted_dataset_name)
                print('extracted_dataset_name is', extracted_dataset_name)
                extracted_dataset_name_list = extracted_dataset_name.split(' ')
                try:
                    entity_extracted_vec = []
                    for word in extracted_dataset_name_list:
                        entity_extracted_vec.append(word_vectors[word])

                    entity_extracted_vec_mean = np.mean(np.array(entity_extracted_vec),axis=0).reshape(1, -1)
                    list_of_datasets = list(master_dic_dataset_name.keys())
                    for dataset_iter in list_of_datasets:
                        dataset_iter = self.remove_punctuation_mark_from_user_entity(dataset_iter)
                        list_dataset_iter = dataset_iter.split(' ')
                        # print("dataset we have splited ")
                        list_dataset_iter_vec = []
                        for word in list_dataset_iter:
                            # print("Inside for")
                            if word in word_vectors.vocab:
                                # print("If")
                                list_dataset_iter_vec.append(word_vectors[word])

                        
                        if list_dataset_iter_vec.__len__() > 0:
                            list_dataset_iter_vec_mean = np.mean(np.array(list_dataset_iter_vec),axis=0).reshape(1, -1)
                            
                            #computing similarity
                            sim = cosine_similarity(entity_extracted_vec_mean, list_dataset_iter_vec_mean).item(0)
                            # print(extracted_dataset_name,'-' , dataset_iter,':',sim)
                            
                            #making dic which is containing dataset name and similarity score with extracted entity
                            global dic_of_similarity
                            dic_of_similarity[dataset_iter] = sim
                            
                   
                    print(sorted(dic_of_similarity.items(), key = lambda kv:(kv[1], kv[0])))
                    sorted_dic_of_similarity = sorted(dic_of_similarity.items(), key = lambda kv:(kv[1], kv[0]))
                    
                    #picking the topmost dataset name 
                    most_similar_dataset = list(sorted_dic_of_similarity)[-1][0]
                    transformed_dataset_name = master_dic_dataset_name[most_similar_dataset]
                except:
                    dispatcher.utter_message('Sorry but seems like there is some Misspell in Dataset Name')
            else:
                dispatcher.utter_message(text = "Sorry i coundn't interpret dataset name, please try again with complete name of dataset")
                
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
                            entity_iter = correction(entity_iter)
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
        

class ActionGranularityLevel(Action):

    def name(self) -> Text:
        return "action_about_data_granularity"

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
                # spellcheck the name of dataset
                dataset_name_ = correction(dataset_name_)
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
                                entity_iter = correction(entity_iter)

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
        return "action_about_data_source_name"

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
                # spellcheck the name of dataset
                dataset_name_ = correction(dataset_name_)
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
                                entity_iter = correction(entity_iter)
                                print("after correction in source",entity_iter)
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Granularity level of a Dataset
                                                                        say it like :- What is the Granularity level of Rainfall Data""")
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

                # spellcheck the name of dataset
                dataset_name_ = correction(dataset_name_)
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
                                entity_iter = correction(entity_iter)
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
                
                # spellcheck the name of dataset
                dataset_name_ = correction(dataset_name_)

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
                                entity_iter = correction(entity_iter)                                
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
        return "action_about_data_last_updated_date"

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


                # spellcheck the name of dataset
                dataset_name_ = correction(dataset_name_)

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
                                entity_iter = correction(entity_iter)
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


class ActionSourceLink(Action):

    def name(self) -> Text:
        return "action_about_data_source_link"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            # print("\n",tracker.get_intent_of_latest_message())

            print("\n","Now slots value in Source Link is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']

                # calling global dictionary
                global master_dic_dataset_name

                # spellcheck the name of dataset
                dataset_name_ = correction(dataset_name_)

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]


                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in source link {extracted_ls_entity}")


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
                                print("yes i am in Source Link")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity
                                entity_iter = correction(entity_iter)
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    # print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Source Link for a Dataset 
                                                                        say it like :- What was the source for the dataset""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Source Link for a Dataset 
                                                                        say it like :- What was the source for the dataset""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")


class ActionDataExtractionPage(Action):

    def name(self) -> Text:
        return "action_about_data_data_extraction_page"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            # print("\n",tracker.get_intent_of_latest_message())

            print("\n","Now slots value in Extraction page is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']

                # calling global dictionary
                global master_dic_dataset_name

                # spellcheck the name of dataset
                dataset_name_ = correction(dataset_name_)

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]


                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in Extraction page {extracted_ls_entity}")


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
                                print("yes i am in extarct data")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity
                                entity_iter = correction(entity_iter)
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    # print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know Source Link for a Dataset 
                                                                        say it like :- What was the source for the dataset""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know Source Link for a Dataset 
                                                                        say it like :- What was the source for the dataset""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")


class ActionAboutData(Action):

    def name(self) -> Text:
        return "action_about_data_about_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # intent of user message 
            # print("\n",tracker.get_intent_of_latest_message())

            print("\n","Now slots value in about data is ",tracker.slots['dataset_name'])

            ls_entity =tracker.latest_message['entities'] # to get entities from user message
            if  tracker.slots['dataset_name'] and  tracker.slots['dataset_name']!=None:
                # name of datset from slot we had
                dataset_name_ = tracker.slots['dataset_name']

                # calling global dictionary
                global master_dic_dataset_name

                # spellcheck the name of dataset
                dataset_name_ = correction(dataset_name_)

                # if dataset name that is extracted from user message is present in our data we got from json file
                if dataset_name_ in master_dic_dataset_name.keys():
        
                    dataset_name_ = master_dic_dataset_name[dataset_name_]


                extracted_ls_entity = []
                for i in range(len(ls_entity)):
                    extracted_ls_entity.append(ls_entity[i]['entity'])
                # extracted_ls_entity = list(filter(lambda x:x!='dataset_name', extracted_ls_entity))
                print(f"Entites we extracted in about data {extracted_ls_entity}")


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
                                print("yes i am in about data Link")
                                # check if entity present in extracted_ls_entity is also present in p ( data in db)
                                # spellcheck the entity
                                entity_iter = correction(entity_iter)
                                if entity_iter in p.keys():

                                    # if entity is present in p then print the value of that entity
                                    # print(f"{entity_iter} ----> {p[entity_iter]}")
                                    dispatcher.utter_message(text = f"{entity_iter} is {p[entity_iter]}")
                                
                                else:
                                    dispatcher.utter_message(text = 'Sorry but can you pls tell again  what feature you are looking for')
                                    dispatcher.utter_message(text = """Ex :Like if you want to know about a Dataset 
                                                                        say it like :- can you tell me about soil data""")
                        
                        else:
                            dispatcher.utter_message(text = f'Sorry but what exactly you wanted I could not get that')
                            dispatcher.utter_message(text = """Ex :Like if you want to know about a Dataset 
                                                                        say it like :- can you tell me about soil data""")
            else:
                dispatcher.utter_message(text = "Can you tell which dataset it is")
