import pandas as pd

# All keys and variables are xamples and need to be changed by the user of this file

#Airtable account 
api_key= 'keyUkdojqsCXtdpsBD'
base_id= 'appTBDQj3VlZfP9TF'
table_name = 'tblq7DM41SZECqG0v'

#API Google Custom Search
api_key_CS = 'AIzaSyAgFkM8mGFEVvrJruSaO-20CZ9QFmwh8h'

#API SERP API
api_key_SerpAPI = '8f6bea6959b88d7f96aac8fa2e4439a8e6f7765f11f942441c8986d0aabe1234'

# Parameter to use or not LinkedIn url enrichment with SerpApi
# Be careful: Using serp_api comes at a certain cost!
try_serp_api = True


# Input data
input_data= pd.read_csv(r"./../Data/Source/Solvay_1000_alumni.csv", sep = ";") 