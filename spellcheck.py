# Levenshtein distance https://www.youtube.com/watch?v=MiqoA-yF-0M

# or  https://medium.com/@ethannam/understanding-the-levenshtein-distance-equation-for-beginners-c4285a5604f0

# source http://norvig.com/spell-correct.html

# instead of big.txt we will will have a text file that contains all our glosaary

import re


from collections import Counter

entity_mapper = {'granularity':'Granularity','methodology':'Methodology'
            ,'frequency':'Frequency',
            'dataset_name':'Dataset Name','source_name':'Source Name'
            ,'last_updated_date':'Last Updated date','source_link': 'Source Link',
            'data_extraction_page':'Data Extraction Page','date_of_retrievals':' Retrieval Date',
            'source_name_det':'Source Name Det'}

dataset_name_in_api = ["rural_wages", "cpi", "rbi_credit", "debt_invest", "rbi_deposit", "plfs", "social_education", "nrega", "nrga_emp", "non_agri", "fis", "input_noncrop", "nrlm", "sas", "agcensus_crop", "agcensus_noncrop", "agcensus_c", "agcensus_nc", "agmarknet", "nhb", "apy", "coc", "fertiliser_sales", "subsidy", "input_composite", "input_crop", "nfsm", "procurement", "pds", "shc_fund", "shc_nutrient", "stock", "depth", "groundwater", "rainfall", "soil", "temperature", "pmfby", "msp", "pm_kissan", "pmksy", "antyodaya", "secc", "census_household", "census"]

dict_of_domain_ids = {1: 'Food and Agriculture', 2: 'Food and Agriculture', 3: 'Socio Economic', 4: 'Food and Agriculture', 5: 'Food and Agriculture', 6: 'Food and Agriculture', 7: 'General', 8: 'Government Schemes', 9: 'General', 10: 'Financial Inclusion', 11: 'Food and Agriculture', 12: 'Economy, Financial Inclusion', 13: 'Economy,  Rural Development', 14: 'Financial Inclusion, Food and Agriculture', 15: 'Food and Agriculture', 16: 'Food and Agriculture', 17: 'Economy, Financial Inclusion', 18: 'Socio Economic', 19: 'Economy', 20: 'Economy, Financial Inclusion', 21: 'General', 22: 'General', 23: 'Rural Development, Socio Economic', 24: 'Economy, National Sample Survey (NSSO)', 25: 'Economy, National Sample Survey (NSSO)', 26: 'Economy, Financial Inclusion, National Sample Survey (NSSO)', 27: 'Economy, Financial Inclusion, National Sample Survey (NSSO)', 28: 'Rural Development, Socio Economic', 29: 'Government Schemes', 30: 'Government Schemes', 31: 'Government Schemes', 32: 'Food and Agriculture, Government Schemes', 33: 'Food and Agriculture, Government Schemes', 34: 'Food and Agriculture', 35: 'Food and Agriculture', 36: 'Food and Agriculture', 37: 'Food and Agriculture, Government Schemes', 38: 'Food and Agriculture', 39: 'Financial Inclusion, National Sample Survey (NSSO)', 40: 'Food and Agriculture, Government Schemes', 41: 'Food and Agriculture', 42: 'Economy,  Rural Development', 43: 'Financial Inclusion', 44: 'Food and Agriculture, Government Schemes', 45: 'General'}
master_dic_dataset_name = {'agriculture wages': 'rural_wages',
 'agricultur wages': 'rural_wages', 'agri wages': 'rural_wages',
  'rural wages': 'rural_wages', 'consumer price index': 'cpi',
   'consumer price index and inflation': 'cpi', 'cpi and inflation': 'cpi',
    'cpi': 'cpi', 'consumre price index and inflation': 'cpi', 
    'consumer price index and inflation cpi': 'cpi', 
    'Consumer Price Index and Inflation':'cpi',
    'credit by bank': 'rbi_credit', 'credet by bank': 'rbi_credit', 
    'credts by bank': 'rbi_credit', 'bank credit': 'rbi_credit',
    'rbi credits': 'rbi_credit', 'credit bie bank': 'rbi_credit',
    'debt and investnent data by nsso': 'debt_invest',
    'debt investment': 'debt_invest', 
    'debtt and investment': 'debt_invest',
    'debt and investment nsso': 'debt_invest', 'nsso debt and investment': 'debt_invest', 
    'nsso dataset on debt and investment': 'debt_invest', 
    'nsso dataset regarding debt and investment': 'debt_invest', 
    'debt and investment': 'debt_invest', 'nsso data for debt and investmnet': 'debt_invest', 
    'debt and investment data by nsso': 'debt_invest', 
    'Debt and Investment':'debt_invest',
    'deposist with bank': 'rbi_deposit',
     'deposits by bank': 'rbi_deposit', 'nsso employmenet': 'plfs', 'nsso data for employment': 'plfs',

     'employment':'plfs', 
     'employment under national sample survey': 'plfs', 
     'Employment':'plfs',
     'plfs': 'plfs', 
     'employment by nssso': 'plfs', 'employment data by nsso': 'plfs', 
     'employment nsso': 'plfs', 'nsso dataset of employment': 'plfs', 
     'household consumption on education': 'social_education', 
     'Household Consumption on Education':'social_education',
     'household consumption on education by nsso': 'social_education', 
     'nsso household consumption on edu': 'social_education',
    'household consumption on education nsso': 'social_education', 
    'mgnrega dataset of agriculture investments': 'nrega',
    'mgnrega agriculture investments': 'nrega',
    'agriculture investments':'nrega',
    'agriculture investments by mgnrega': 'nrega', 
    'mgnrega employment': 'nrga_emp',
    'employment under the mgnrega': 'nrga_emp', 'employment data by mgnrega': 'nrga_emp',
    'mgnrega-employment':'nrga_emp','MGNREGA':'nrga_emp',
          'unincorporated non agriculture enterprises excluding construction nsso': 'non_agri', 
          'Unincorporated Non-Agriculture Enterprises Excluding Construction':'non_agri',
          'unincorporated non agri enterprises excluding construction': 'non_agri',
          'unincorporated non-agriculture enterprises excluding construction nsso':'non_agri',
           'unincorporated non agriculture enterprises excluding construction by nsso': 'non_agri', 
           'unincorporated non agriculture enterprises excluding construction': 'non_agri',

           'Unincorporated Non Agriculture Enterprises Excluding Construction':'non_agri',
            'nabard financial inclusion survey': 'fis', 'financial inclusion survey': 'fis', 
            'nabard financial inclusion findings': 'fis', 'financial inclusion survey nabard': 'fis',
             'financial inclusion survey by nabard': 'fis', 'nabard':'fis',
             'input survey for non crop': 'input_noncrop', 
             'input survey non crop': 'input_noncrop',
             'Input survey':'input_noncrop',
             'non crop input survey': 'input_noncrop',
              'nrlm shgs': 'nrlm', 'self help groups': 'nrlm', 
             'nrlm self help groups shgs': 'nrlm','shgs':'nrlm',
             'nrlm self help groups':'nrlm',
              'situation assessment of agri household ': 'sas', 
             'situation assessment of agricultural household nsso': 'sas',
             'Situation Assessment of Agricultural household':'sas',
              'situation assessment of agricultural household by nsso': 'sas', 
              'situation assessment of agricultural household': 'sas',

            'agricultural census 2010-11 crop': 'agcensus_crop', 
            'agricultural census 2010 11 crop': 'agcensus_crop',
            'agriculture census 2010 2011 crop':'agcensus_crop',
            'agcensus crop':'agcensus_crop',
            'agriculture census 2010 2011 crop': 'agcensus_crop',
            'agricultural census 2010-2011 crop':'agcensus_crop',
            'agricultural census 2010 2011 crop':'agcensus_crop',
            'agriculture census 2010-2011 crop' : 'agcensus_crop',


            'agri census 2010-11 non-crop': 'agcensus_noncrop',
            'agri census 2010 11 non-crop': 'agcensus_noncrop',
            'agri census 2010 11 non crop': 'agcensus_noncrop',
            'agricultural census 2010-11 non crop': 'agcensus_noncrop', 
            'agri census 2010-2011 non-crop':'agcensus_noncrop',
            'agriculture census 2010-11 non crop':'agcensus_noncrop',
            'agcensus noncrop':'agcensus_noncrop',
            'agriculture census 2010 11 non crop':'agcensus_noncrop',




            'agricultural census 2015 16 crop': 'agcensus_c', 
            'agri census 2015 16 crop': 'agcensus_c',
            'agriculture census 2015 2016 crop': 'agcensus_c','agcensus c':'agcensus_c',

            'agri census 2015 16 non crop': 'agcensus_nc', 
            'agricultural census 2015 16 non crop': 'agcensus_nc',
            'Agricultural Census 2015 2016':'agcensus_nc',
                'agcensus nc':'agcensus_nc',

             'agricultural census 2015-16 non crop': 'agcensus_nc', 
             
             'agri marketing': 'agmarknet',
             'agmarknet':'agmarknet',
              'agricultural marketing agmarknet': 'agmarknet', 'agricultural marketing': 'agmarknet', 
              'area production statistics': 'nhb', 'area prod stats': 'nhb','nhb':'nhb',
               'area production statistics nhb': 'nhb',
               'area production yield apy': 'apy', 'apy': 'apy', 'area production yeild': 'apy', 'area production yeild apy': 'apy', 'area prod yield': 'apy', 'cost of cultivation': 'coc', 'cost of cultivation coc': 'coc', 
               'cultivation expenses': 'coc','coc':'coc',
                'fertilizers sales': 'fertiliser_sales', 'fertiliser sales': 'fertiliser_sales', 'fertilizer sales ': 'fertiliser_sales', 'sales of fertiliser': 'fertiliser_sales',
                'sales of fertilisers': 'fertiliser_sales', 'food and fertiliser subsidies': 'subsidy', 'food and fertiliser subsidy': 'subsidy',
            'food and compost subsidies': 'subsidy', 'food and fertilizer': 'subsidy', 'subsidy for food and fertilisers': 'subsidy', 
            'crop and fertiliser subsidy': 'subsidy', 'crop composite input survey': 'input_composite',
            'crop composite':'input_composite', 'input survey crop composite': 'input_composite', 
            'crop Input Survey': 'input_crop', 'input survey crop': 'input_crop',
            'input crop':'input_crop',
             'national food security mission nfsm spending': 'nfsm',
             'nfsm': 'nfsm', 
             'national food security mission': 'nfsm', 
             'national food security mission spending': 'nfsm','spending':'nfsm',
              'foodgrains procurement': 'procurement', 'procurement of foodgrains': 'procurement', 
              'Procurement of':'procurement',
              
              'public distribution system': 'pds', 'public distribution system pds': 'pds', 'pds': 'pds',
             'soil health card - funding status': 'shc_fund', 
             'funding status':'shc_fund','shc - funding status': 'shc_fund', 
             'shc  funding status':'shc_fund',
             'funding status shc': 'shc_fund',
             'funding status soil health card':'shc_fund',
              'soil health card funding status': 'shc_fund', 'shc nutrent status': 'shc_nutrient', 
             'soil health card - nutrient status': 'shc_nutrient', 'nutrient status':'shc_nutrient',
             'nutrient status soil':'shc_nutrient',
             'shc - nutrent status': 'shc_nutrient',
             'soil health card nutrient status':'shc_nutrient',
              'stock of foodgrains': 'stock', 'foodgrain stock': 'stock',
              'Stock':'stock',
               'depth to water level': 'depth', 'depth of water level': 'depth', 'groundwater extraction stages': 'groundwater', 'groundwater-extraction stages': 'groundwater', 'groundwater-stages of extraction': 'groundwater', 'groundwater - stages of extraction':'groundwater',
             'stages of groundwater extraction': 'groundwater'
             ,'stages of extraction':'groundwater','groundwater stages of extraction': 'groundwater', 'rainfall': 'rainfall', 'soil': 'soil', 'temperature': 'temperature', 'crop insurance pradhan mantri fasal bima yojana pmfby': 'pmfby', 'crop insurance': 'pmfby', 'pradhan mantri fasal bima yojana': 'pmfby', 'pmfby': 'pmfby', 'minimum support price msp': 'msp', 'minimum support price': 'msp', 'msp': 'msp', 
             'pm kisan': 'pm_kissan','pradhan mantri kisan':   'pm_kissan','pradhan mantri kisan yojana':'pm_kissan',         
             
              'pradhan mantri krishi sinchai yojana pmksy': 'pmksy', 'pradhan mantri krishi sinchai yojana': 'pmksy', 'pmksy': 'pmksy', 'antodaya mission': 'antyodaya', 'mission antodaya': 'antyodaya', 'socio economic caste census secc': 'secc', 'socio economic caste census': 'secc', 'secc': 'secc', 'household amenities census': 'census_household', 'household amenities': 'census_household', 'census household amenities': 'census_household', 'census pca demography': 'census',
 'pca demography census': 'census', 'pca demography': 'census'}
template_names_variations =['granularity','source_name','methodology','frequency','last_updated_date'
                        'source_link','data_extraction_page','source_name_det','date_of_retrievals']
def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(list(master_dic_dataset_name.keys()) + template_names_variations)

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    #Most probable spelling correction for word.

    # key : key function where the iterables are passed and comparsion is performed
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]

    # Deletes words one by one
    deletes    = [L + R[1:]               for L, R in splits if R]

    # transposes are done on first and second place
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))