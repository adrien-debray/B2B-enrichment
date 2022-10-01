
import unidecode
import unidecode
import urllib.parse

def name_standardization(name, duplicate_check):
    """ Standardize the name of the person to find a match between the name and the linkedin http address

    Args:
        name: the full name of the person
        duplicate_check: True if the goal of the function is to check for name duplicates in the dataset, false otherwise
    
    Returns:
        fn: the first name in lowercase letters
        fn_without_accent: the first name with any accents removed
        ln: the last name in lowercase letters
        ln_without_accent: the last name with any accents removed
    """
    fn= name.split(' ')[0].lower()
    fn_without_accent=unidecode.unidecode(fn)
    ln= name.split(' ')[1].lower()  # to correct  -> take [1:]
    ln_without_accent=unidecode.unidecode(ln)
    if duplicate_check== False:
        return fn_without_accent, ln_without_accent
    if duplicate_check == True:
        return (fn_without_accent +' '+ ln_without_accent)

def url_picker(table, links,fn_without_accent,ln_without_accent,ID, with_job, Serp_api):
    """ 
        Args: 
        • table: The Airtable to update
        • links: The http links to analyse
        • fn_without_accent, ln_without_accent: the first and last name in standardized format
        • ID: The row ID where to update the table
        • with_job: True if a job position is given for that row ID
        • Serp_api: True if the links are given using the SerAPi tool
    
        Return: 
        • state: True if the table an url has been picked to update the table
        • first_link: the first http adress given in the links 

    """
    i=0
    # print('-')
    state=False
    first_link = None
    while i<7:    
        if Serp_api == False:
            url1=links["items"][i]['link']
        else:
            url1=links["organic_results"][i]['link']
        # print(url1)
        url=urllib.parse.unquote_plus(url1)
        url_woa= unidecode.unidecode(url)

        if i == 0 and with_job ==  True:
            if ((fn_without_accent or ln_without_accent) in url_woa) and ("linkedin" in url_woa):
                first_link = url1
        
        if i == 0 and with_job ==  False:
            fn_ln1 = (fn_without_accent + ln_without_accent[0])
            # print(fn_ln1)
            if ((fn_ln1) in url_woa) and ("linkedin" in url_woa):
                first_link = url1

        if (fn_without_accent in url_woa) and (ln_without_accent in url_woa) and ("linkedin" in url_woa):  
            table.update(ID,{'LinkedIn 1':url1}) 
            state=True
            break
        else:
            i=i+1
    return state, first_link

