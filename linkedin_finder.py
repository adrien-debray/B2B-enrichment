import config
from apiclient.discovery import build
import time
from serpapi import GoogleSearch
from utils import name_standardization, url_picker


def method1(table):
    """ Search for the LinkedIn URL of the records if those are not found yet by combining the 'google_api_with_job', 'google_api_without_job' and 'serp_api' methods.
         
        Args: 
        • table: the Airtable to update

        Return:
        • A,B,C,D,d1,d2: Info about which method found the LinkedIn URL
    """
    A,B,C,D1, D2= 0, 0, 0, 0, 0
    # sample_list= table.all(formula="({LinkedIn 1}='')")
    list=table.all()
    sample_list = list[0:935] 
    # Google custom search API
    resource = build("customsearch","v1", developerKey= config.api_key_CS).cse() 

    for rec in sample_list:

        time.sleep(1.2)

        full_name= (rec['fields']['firstName']+" "+ rec['fields']['lastName'])
        fn_without_accent, ln_without_accent = name_standardization(full_name, duplicate_check= False)
        ID = (rec['id'])
        print('------', full_name,'------')
        
        
        # Method 1: Extract urls found with the use of google custom search api and the job position and 
        # Update the table if an url match is found
        try:  
            print('try with method 1')
            job_column= (rec['fields']['Job'])
            job = job_column.split('-')[0]   
            results= resource.list(q= full_name + " "+ job + "LinkedIn",gl="be", cx='71f0cde660f0d38e9').execute()
            state, first_link = url_picker(table, results,fn_without_accent,ln_without_accent,ID, True, False)
            if state == True:
                print('URL found with job position')
                B=B+1
                continue     
            if state == False and first_link != None:
                table.update(ID,{'LinkedIn 1':first_link})
                print('URL found with job position_ext')
                B=B+1
                continue

        except (IndexError,KeyError, TypeError): 
            try:    
                job_column= (rec['fields']['Job'])
                job = job_column.split(' ')[0] # Looking to a more general job position
                results= resource.list(q= full_name +" "+ job + "LinkedIn",gl ="be", cx='71f0cde660f0d38e9').execute()
                state, first_link = url_picker(table, results, fn_without_accent,ln_without_accent,ID, True, False)
                if state == True:
                    print('URL found with job position_ext')
                    B=B+1
                    continue
                if state == False and first_link != None:
                    table.update(ID,{'LinkedIn 1':first_link})
                    print('URL found with job position_ext')
                    B=B+1
                    continue

            except (IndexError, KeyError,TypeError):
                pass


        # Method 2: Extract urls found with the use of google custom search api and the Solvay keyword and 
        # Update the table if an url match is found
        try:
            print('Try with method 2') 
            results= resource.list(q= full_name +" Solvay"+ " LinkedIn",gl ="be", cx='71f0cde660f0d38e9').execute()
            state, first_link = url_picker(table, results,fn_without_accent,ln_without_accent,ID, False, False)
            if state == True:
                print("URL found with Solvay keyword")
                C=C+1
                continue
            if state == False and first_link != None:
                table.update(ID,{'LinkedIn 1':first_link})
                print("URL found with Solvay keyword")
                C=C+1
                continue
        except (IndexError,KeyError,TypeError):
            pass


        # Method 3: Extract urls found with the use of SerpApi 
        # Update the table if an url match is found
        if config.try_serp_api == True:
            try:
                
                job_column= (rec['fields']['Job'])
                job = job_column.split('-')[0]
                params = {
                "api_key": config.api_key_SerpAPI, 
                "engine": "google",
                "q": full_name + " "+job + "LinkedIn",
                "google_domain": "google.com",
                "gl": "be",
                "hl": "en",
                "location_requested": "Belgium",
                "location_used":"Belgium",
                "filter": "0"}

                search = GoogleSearch(params)
                results = search.get_dict()
                state, first_link = url_picker(table, results,fn_without_accent,ln_without_accent,ID, True, True)
                if state == True:
                    print('URL found with SerApi')
                    D1 = D1 +1
                    continue
                if state == False and first_link != None:
                    table.update(ID,{'LinkedIn 1':first_link})
                    print('URL found with SerApi')
                    D1 = D1 + 1
                    continue
            except (IndexError,KeyError): 
                # A More general google search  
                try:   
                    job_column= (rec['fields']['Job'])
                    job = job_column.split(' ')[0]

                    params = {
                        "api_key": config.api_key_SerpAPI,
                        "engine": "google",
                        "q": full_name + " "+job + " LinkedIn",
                        "google_domain": "google.com",
                        "gl": "be",
                        "hl": "en",
                        "location_requested": "Belgium",
                        "location_used":"Belgium",
                        "filter": "0"
                    }
                    search = GoogleSearch(params)
                    results = search.get_dict()
                    state, first_link = url_picker(table, results,fn_without_accent,ln_without_accent,ID, True, True)
                    if state == True:
                        print('URL found with SerApi')
                        D1 = D1 +1
                        continue
                    if state == False and first_link != None:
                        table.update(ID,{'LinkedIn 1':first_link})
                        D1 = D1+1
                        continue
                except (IndexError,KeyError,TypeError):
                    try:
                        params = {
                            "api_key": config.api_key_SerpAPI,
                            "engine": "google",
                            "q": full_name + "Solvay LinkedIn",
                            "google_domain": "google.com",
                            "gl": "be",
                            "hl": "en",
                            "location_requested": "Belgium",
                            "location_used":"Belgium",
                            "filter": "0"
                        }
                        search = GoogleSearch(params)
                        results = search.get_dict()
                        state, first_link = url_picker(table, results,fn_without_accent,ln_without_accent,ID, False, True)
                        if state == True:
                            print('URL found with SerApi')
                            D2 = D2 +1 
                            continue
                        if state == False and first_link != None:
                            print('URL found with SerApi')
                            table.update(ID,{'LinkedIn 1':first_link})
                            D2 = D2 +1
                            continue
                        
                    except (IndexError,KeyError,TypeError):
                        pass

        # print('URL not found')
        A = A+1
    return A,B,C,D1,D2