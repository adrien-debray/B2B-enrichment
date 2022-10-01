import json
import requests
import datetime 
from utils import name_standardization
import config

added_records = 0

######## Clean & Standardize the data to import in Airtable ##########

def namestr(obj, namespace):
    """ Takes the name of a variable and make it a string """ 
    return [name for name in namespace if namespace[name] is obj]

#Recode de names correctly from latin-1 to utf-8
latin_list = ['Ã©','Ã«','Ã¯','Ã®','Ã¼','Ã§','Ã¯','Ã']

def latin_to_utf(name):
    if any(char in name for char in latin_list):
        return (name.encode("latin-1").decode("utf-8"))
    else:
        return name


def data_cleaning(Data, table_exist):
    """Cleans the original data in pandas type and upload it in a local csv file
        Args: 
        • Data: The data to clean
        • table_exist: True if there is already an existing table in Airtable
    
        Return: 
        • clean_data: A clean version of the original data
    
    """

    Data.fillna("", inplace = True)
    # initial number of rercords
    init_rec=len(Data)

    # Write names in right format
    Data['firstName']= Data['firstName'].apply(lambda name: latin_to_utf(name))
    Data['lastName']= Data['lastName'].apply(lambda name: latin_to_utf(name))

     
    #Drop the duplicates 
    Data['fullname']= Data['firstName']+ " " + Data['lastName']
    Data['fullname_lc']= Data['fullname'].apply(lambda name: name_standardization(name, duplicate_check= True))
    Data=Data.drop_duplicates(['fullname_lc'])

    # Do not take records already in airtable
    if table_exist == 'True':
        airtable_list= config.airtable.all()
        all_names = list()
        for a in  airtable_list:
            full_name = (a['fields']['firstName']+" "+ a['fields']['lastName'])
            all_names.append(full_name)

        for index, row in Data.iterrows():
            if row['fullname'] in all_names:
                Data = Data.drop(index)  
    
    Data.drop(['fullname', 'fullname_lc'], axis = 1, inplace = True)

    # Detect wrong rows (ex. no name but adress in the place)
    genders = ['M','F']
    df_wrong_format = Data[~Data['gender'].isin(genders)]
    df_good_format = Data[Data['gender'].isin(genders)]

    df_wrong_format.to_csv(r'./../Data/Staging/wrong_format.csv', sep= ',')
    clean_data=df_good_format.applymap(str)
    clean_data.to_csv(r'./../Data/Staging/clean_data.csv',sep=',')


    # Summary of the data cleaning in a text file 
    cleaned_rec= len(clean_data)
    dropped_rec= init_rec - cleaned_rec
    e = datetime.datetime.now()
    with open(r'./../execution_logs.txt','a') as file:
        file.write("\n \n")
        file.write("Date & time of Data Injestion execution:  %s/%s/%s at %s:%s:%s" % (e.day, e.month, e.year,e.hour, e.minute, e.second) )
        file.write("\n")
        file.write("Number of cleaned records: %s" %(cleaned_rec))
        file.write("\n")
        file.write("Number of dropped records: %s" %(dropped_rec))
    
    return clean_data

########## Integrate new data into airtable ##############

def airtable_upload(table, upload_data, typecast = False, api_key = None, base_id = None, record_id = None):
    """Sends dictionary data to Airtable to add or update a record in a given table. 
        Returns new or updated record in dictionary format.
    
    Keyword arguments:
    • table: set to table name
        ◦ see: https://support.airtable.com/hc/en-us/articles/360021333094#table
    • upload_data: a dictionary of fields and corresponding values to upload in format {field : value}
        ◦ example: {"Fruit" : "Apple", "Quantity" : 20}
    • typecast: if set to true, Airtable will attempt "best-effort automatic data conversion from string values"
        • see: "Create Records" or "Update Records" in API Documentation, available at https://airtable.com/api for specific base
    • api_key: retrievable at https://airtable.com/account
        ◦ looks like "key●●●●●●●●●●●●●●"
    • base_id: retrievable at https://airtable.com/api for specific base
        ◦ looks like "app●●●●●●●●●●●●●●"
    • record_id: when included function will update specified record will be rather than creating a new record
        ◦ looks like "rec●●●●●●●●●●●●●●"
        """
    
    # Authorization Credentials
    if api_key == None:
        print("Enter Airtable API key. \n  *Find under Airtable Account Overview: https://airtable.com/account")
        api_key = input()
        
    headers = {"Authorization" : "Bearer {}".format(config.api_key),  #"Authorization" : "Bearer keyUkdojqsCXtysCB"
               'Content-Type': 'application/json'}
    
    validate_airtable_kwargs(api_key, "API key", "key")

    # Locate Base
    if base_id == None:
        print("Enter Airtable Base ID. \n  *Find under Airtable API Documentation: https://airtable.com/api for specific base]")
        base_id = input()
        
    url = 'https://api.airtable.com/v0/{}/'.format(base_id)
    path = url + table
    validate_airtable_kwargs(base_id, "Base ID", "app")
    
    # Validate Record ID
    if record_id != None:
        validate_airtable_kwargs(record_id, "Record ID", "rec")
    
    # Validate upload_data
    if type(upload_data) != dict:
        print("❌ Error: `upload_data` is not a dictonary.")
        return

    # Create New Record
    if record_id == None:
        global added_records
        added_records +=1
        upload_dict = {"records": [{"fields" : upload_data}], "typecast" : typecast}
        upload_json = json.dumps(upload_dict)
        #print("upload json", upload_json)
        #print(path)
        response = requests.post(path, data=upload_json, headers=headers)
        airtable_response = response.json()
        
    # Update Record
    if record_id != None:
        path = "{}/{}".format(path, record_id)
        upload_dict = {"fields" : upload_data, "typecast" : True}
        upload_json = json.dumps(upload_dict)
        response = requests.patch(path, data=upload_json, headers=headers)
        airtable_response = response.json()
    
    # Identify Errors
    if 'error' in airtable_response:
        identify_errors(airtable_response)

    
    # Diagnositic of every execution of airtable_upload 
    with open(r'./../execution_logs.txt','a') as file:
        file.write("\n")
        file.write("Number of new records: %s" %(added_records))

        
    return (airtable_response)


def upload_pandas_dataframe(pandas_dataframe, table ,api_key , base_id):
    """Uploads a Pandas dataframe to Airtable. If Pandas index values are Airtable Record IDs, will attempt to update 
        record. Otherwise, will create new records."""
    pandas_dicts = pandas_dataframe.to_dict(orient="index")
    # panas_dict:  A huge dict where the key is the record id & the value is a dict of all the values associated to a lead
    for pandas_dict in pandas_dicts:
        record_id = pandas_dict
        if validate_airtable_kwargs(str(record_id), "Record ID", "rec", print_messages=False) is False: #is false means that there is not this record ID yet
            record_id = None
        upload_data = pandas_dicts[pandas_dict]

        x = airtable_upload(table, upload_data, api_key=api_key, base_id=base_id, record_id=record_id)
    return x 

# Troubleshooting Functions
def validate_airtable_kwargs(kwarg, kwarg_name, prefix, char_length=17, print_messages=True):
    """Designed for use with airtable_download() and airtable_upload() functions.
        Checks `api_key`, `base_id` and `record_id` arguments to see if they conform to the expected Airtable API format.
      """
    valid_status = True
    if len(kwarg) != char_length:
        if print_messages is True:
            print("⚠️ Caution: {} not standard length. Make sure API key is {} characters long.".format(kwarg_name, char_length))
        valid_status = False
    if kwarg.startswith(prefix) is False:
        if print_messages is True:
            print("⚠️ Caution: {} doesn't start with `{}`.".format(kwarg_name, prefix))
        valid_status = False
    return valid_status


def identify_errors(airtable_response):
    """Designed for use with airtable_download() and airtable_upload() functions.
        Prints error responses from the Airtable API in an easy-to-read format.
        """
    if 'error' in airtable_response:
        try:
            print('❌ {} error: "{}"'.format(airtable_response['error']['type'], airtable_response['error']['message']))
        except:
            print("❌ Error: {}".format(airtable_response['error']))
    return



