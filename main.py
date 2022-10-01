import datetime 
import config
import data_ingestion
from linkedin_finder import method1  

table_exists = input("Type <True> if there is already an airtable filled in, <False> otherwise: ")

print(config.input_data)
cleaned_data = data_ingestion.data_cleaning(config.input_data, table_exists)

if table_exists == 'True':
    if cleaned_data.empty == False:
        data_ingestion.upload_pandas_dataframe(cleaned_data, config.table_name2 ,config.api_key , config.base_id1)

    # Use the methods to enrich the Airtable DB with the personnal LinkedIn
    A,B,C,D1, D2 = method1(config.airtable)

    e = datetime.datetime.now()
    with open(r'./../execution_logs.txt','a') as file:
        file.write("\n \n")
        file.write("Date & time of URL finder execution:  %s/%s/%s at %s:%s:%s" % (e.day, e.month, e.year,e.hour, e.minute, e.second) )
        file.write("\n")
        file.write("Number LinkedIn URL's not found: %s " %A)
        file.write("\n")
        file.write("Number LinkedIn URL's found with job position: %s " %B)
        file.write("\n")
        file.write("Number LinkedIn URL's found with Solvay keyword: %s " %C)
        file.write("\n")
        file.write("Number LinkedIn URL's found with SerpApi-job position: %s " %D1)
        file.write("\n")
        file.write("Number LinkedIn URL's found with SerpApi-'Solvay': %s " %D2)
