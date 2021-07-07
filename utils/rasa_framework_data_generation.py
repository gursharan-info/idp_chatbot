'''
this script will generate retrieval intents and then make nlu and domain files
'''
import sys
from utils.semi_automation_insertion import *

if __name__ == "__main__":
    gsheetid = '1luFRpbX9a0DIwJ0vNIyVglcKb8TcyNaBHXFj-4TLYAc'
    sheet_name = 'sheet1'
    gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, sheet_name)
    df = pd.read_csv(gsheet_url)
    list_of_ques = list(df['question']) 