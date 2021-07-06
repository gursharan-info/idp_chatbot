import pandas as pd

#FROM CLIENT INPUT TO PARTICULAR FORMAT
def pad_dict_list(dict_list, padel):
    lmax = 0
    for lname in dict_list.keys():
        lmax = max(lmax, len(dict_list[lname]))
    for lname in dict_list.keys():
        ll = len(dict_list[lname])
        if  ll < lmax:
            dict_list[lname] += [padel] * (lmax - ll)
    return dict_list

def preparing_intermediate_output_for_nlu_and_domain_filegeneration(path_to_csv, df):
  intent_list = list(df['intent'].unique())
  dic = {}
  for intent in intent_list:
    variation_list = list(df[df['intent'] == intent]['variations'])
    question_list = list(set(list(df[df['intent'] == intent]['question'])))
    print(question_list)
    dic[intent] = variation_list+question_list
  padel = 'xyz'
  pad_dict_list(dic, padel)
  data = pd.DataFrame(dic)
  df = data.replace(['xyz'],'')
  df.to_csv(path_to_csv)

'''
param: create_files_path - where we want to create the nlu and domain files
param: nlu_file_name
param: domain_file_name
'''
#GENERATING FILES
def create_rasa_files(path, create_files_path, nlu_file_name, domain_file_name, Nlu_file_flag = True, Domain_file_flag = True):
    
    #NLU FILE
    NLU_FILE_CREATION = Nlu_file_flag
    if(NLU_FILE_CREATION):
        df = pd.read_csv(r"{}".format(path))
        file = open(create_files_path+'nlu'+nlu_file_name+'.yml',"w")
        
        intents = list(df.columns)
        for item in intents:
            file.write("- intent: {intent_name}\n".format(intent_name=item))
            file.write("  examples: |"+'\n')
            for sent in df[item]:
                file.write("    - {}\n".format(sent))
        file.close()


    #DOMAIN FILE
    DOMAIN_FILE_CREATION = Domain_file_flag
    if(DOMAIN_FILE_CREATION):
        file = open(create_files_path+domain_file_name+'.yml',"w")
        file.write("intents:\n")
        file.write("responses:\n")
        for intent_name in intents:
            file.write("    utter_{}:\n".format(intent_name))
            file.write('    - text:\n')
        file.write("actions: []\n")
        # for intent_name in intents:
        #     file.write("  - utter_{}\n".format(intent_name))
        file.write('forms: {}\n')
        file.write('e2e_actions: []\n')
        file.close()
    return None

if __name__ == '__main__':
    path_to_csv = ''
    df = pd.read_csv('')
    preparing_intermediate_output_for_nlu_and_domain_filegeneration(path_to_csv)
    
    path = '/home/bavalpreet/IDP/nlu_sample_format_for_conversion.csv'
    create_files_path = '/home/bavalpreet/IDP/generated_data/semiautomation/'
    domain_file_name = '\domain'
    nlu_file_name = '\nlu'
    create_rasa_files(path, create_files_path, nlu_file_name, domain_file_name)