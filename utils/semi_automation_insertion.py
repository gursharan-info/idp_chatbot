import pandas as pd


def create_rasa_files(path, create_files_path, nlu_file_name, domain_file_name):
    
    #NLU FILE
    NLU_FILE_CREATION = True
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
    DOMAIN_FILE_CREATION = True
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
    path = '/home/bavalpreet/IDP/nlu_sample_format_for_conversion.csv'
    create_files_path = '/home/bavalpreet/IDP/semiautomation/'
    domain_file_name = '\domain'
    nlu_file_name = '\nlu'
    create_rasa_files(path, create_files_path, nlu_file_name, domain_file_name)