# self-containedAsset: B2B-Enrichment V1

## Intro

This page is a large documentation of the B2B-enrichment project.   

The structure is as follows:

In [section 1](https://www.notion.so/self-containedAsset-B2B-Enrichment-V1-8561c8834bcd4267a8993c2e849f1eb5), the context of the project is described, and the goals are stated. 

[Section 2](https://www.notion.so/self-containedAsset-B2B-Enrichment-V1-8561c8834bcd4267a8993c2e849f1eb5) explains the main deliverables. The automated workflow and the results on the Solvay Alumni Dataset are shown. The automated workflow was divided into 3 phases. Phases 0 and 1 are finished; a full documentation of the tools and methods explored and the choices’ explanation for these phases is documented in the A[ppendix](https://www.notion.so/self-containedAsset-B2B-Enrichment-V1-8561c8834bcd4267a8993c2e849f1eb5). Phase 2 is not finished but some tools and ideas are already explored, these are documented in the [Appendix](https://www.notion.so/self-containedAsset-B2B-Enrichment-V1-8561c8834bcd4267a8993c2e849f1eb5).

[Section 3](https://www.notion.so/self-containedAsset-B2B-Enrichment-V1-8561c8834bcd4267a8993c2e849f1eb5) explains in a step-by-step process how to use the B2B-Enrichment tool.

[Section 4](https://www.notion.so/self-containedAsset-B2B-Enrichment-V1-8561c8834bcd4267a8993c2e849f1eb5) explains the python scripts and the methods created in more detail.

## 1. Problem Description

In B2B marketing, it is easy to gather structured information about Belgian companies. The reason is we have unique company numbers (also used as VAT ID) for both head offices but also "exploitation units" and subsidiaries.

A lot of financial, social, and organizational information is available for free at the "banque carrefour des entreprises".

However, information about a company does not always help us identify the decision makers in those companies.

That's why we are looking for a similar type of **unique ID that could allow us to automatically update our information on decision makers with publicly available information.**

The next phase is to monitor the enriched database and flag for job changes within the company or company changes

## 2. The B2B-Enrichment workflow

The B2B-Enrichment tool is a semi-automated workflow that finds the **unique LinkedIn URL** of individuals based on imperfect information with only a few manual actions to take.

The deployment of the tool is divided into 3 different phases. 

- Phase 0: Finding a suitable place to store the data for enrichment and perform operations
- Phase 1: Develop a workflow that finds the LinkedIn URL of persons from imperfect or incomplete information
- Phase 2: based on the identified URL, enrich a database with all the other publicly available information
- Phase 3: Monitor the information about people through their LinkedIn profile and flag for job changes or company changes.

[Sans titre](https://www.notion.so/a6991c1c52ca4382bba9bd988677f93a)

The **B2B-Enrichment V1 tool** automates phase 0 and phase 1 but not yet phase 2. Suggestions and ideas for Phase 2 are given in the [Appendix.](https://www.notion.so/self-containedAsset-B2B-Enrichment-V1-8561c8834bcd4267a8993c2e849f1eb5)

The workflow works as a data pipeline automated through Python scripts. 
The scripts take a CSV file as input. 

Once executed:

If there is **already a table** with the same column names in Airtable, the CSV file will be cleaned and added into Airtable automatically. All the records in Airtable without a LinkedIn URL yet to their name will be extracted and enriched with their personal LinkedIn URL when one is found.

If there is **no existing table** yet with the correct column names. The CSV file is only cleaned during the execution. The clean data has then to be added manually in a new Airtable. Once this is done, a second execution of the script will extract the records without LinkedIn URL out of the table and enrich them.

![Data Pipeline summary](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/09cb30a9-afd1-4794-9a6b-1b2270ec9fe9/Untitled.png)

Data Pipeline summary

### 30k Solvay Alumni Dataset

- A CSV file containing info about ± 30k Solvay Alumni.
- **Columns**:
    
    [ID, firstName, lastName, originalFirstName, originalLastName, Language(s), gender, Birthdate, email, Email erroremail2, mobilePhone, address, zipcode, city, Country, Address error, Membership status, Solvay education 1, Solvay promotion 1, Solvay education 2, Solvay promotion 2, Solvay education 3, Solvay promotion 3, Solvay education 4, Solvay promotion 4, Categories, LinkedIn, Job, Professional email, roleNumber, EXED ID, Past Memberships, Deceased, deceasedDate]
    
- Performance on 4500 records:

![Google (job poistion), Google (”Solvay”), SerpAPI (job position), SerpAPI (”Solvay”) are the methods used in the sript to retrieve the LinkedIn URL’s. # Found is the number of Linked URL’s found with each method and “%” is the percentage compared to the total number of records.](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0a7d5d67-a241-4ccd-a2e3-666203de9153/Untitled.png)

Google (job poistion), Google (”Solvay”), SerpAPI (job position), SerpAPI (”Solvay”) are the methods used in the sript to retrieve the LinkedIn URL’s. # Found is the number of Linked URL’s found with each method and “%” is the percentage compared to the total number of records.

## 3. How to use the tool?

This asset provides an end-to-end pipeline written in Python that finds the LinkedIn URL of persons by performing only a few manual actions.

Steps needed to run the asset:

1. **Download the scripts** from the GitHub repository on your local machine.
    
    See [Getting started with Python](https://www.notion.so/Getting-started-with-Python-5fe473bdd4814a23940da1ffb6ba5b19) 
    
    Build your file structure as follows around the GitHub repository:
    
    - 📁 B2B Enrichment
        - 📁Data
            - 📁Source
                
                “*The data sources to enrich”*
                
            - 📁Staging
                
                “*The script will store at this place the clean data and wrong formatted data when executed”*
                
        - 📁GitHub Repository
        
        📄execution_logs (.txt file)
        
2. Set up the working environment
    1. Install anaconda/miniconda python version 3.6+
    2. Create the self-contained Conda environment. Open anaconda prompt, go to the project root directory and enter the command:
        
        pip install -r requirements.txt
        
3. **Connect to the different tools** used to take their API keys and check that enough credits are available to perform your task. 
    - **Airtable**: Ask Julien Theys for Agilytics’ account
        
        [Airtable | Everyone's app platform](https://www.airtable.com/)
        
    
    - **Google Custom search engine**: Use your own search engine on your Google account.
        
        [](https://programmablesearchengine.google.com/cse/all)
        
    - **SerpApi**: Ask Julien Theys for Agilytics’ account
        
        [SerpApi: Google Search API](https://serpapi.com/)
        

1. **To modify in the scripts**
    1. Create a **config.py** file with all the necessary paths, variables & keys:
        
        
        | Variable name(s) | Description |
        | --- | --- |
        | api_key, base_id,table_name | Airtable keys of the API, the base and the table in which you want to enrich your data |
        | api_key_CS | API key of Google Custom Search Engine |
        | api_key_SerpAPI | A key of SerpApi |
        | try_serp_api  | True / False: Is a boolean that tells if you use SerpAPI in the enrichment process |
        | input_data | the directory of the data to enrich |
    2. In the [**main.py](http://main.py)**  modify the arguments of the `upload_pandas_dataframe` function according to the specific table you want to enrich.
2. Execute the **main.py** script. A command line will open and ask for a boolean input.
    1. Type `False` if no table is already created in Airtable with the correct column names to enrich your data. 
    You have to **create & configure your table manually:**
        1. Click on the ➕ icon and select “Quick import from” > “CSV file” 
        2. Import the cleaned CSV file saved at “*./Data/Staging/cleaned_data”* into a new table and select the following options
            
            ![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5358a4e1-ba3d-4f4f-b5a4-9edd5f046539/image-20220819-145703.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5358a4e1-ba3d-4f4f-b5a4-9edd5f046539/image-20220819-145703.png)
            
        3. **Manually** add a new column labelled “LinkedIn 1” and make sure the primary field is called “ID”
        4. Re-execute the script and type `True` as Boolean input.
    2. Type `True` if there is already an existing table with the correct column names. The script will upload the new data and enrich it automatically in Airtable.

## 4. Python code explanation

### The scripts

- [main.py](http://main.py) : The main script calls the functions in charge of the data cleaning, ingestion and enrichment. All these functions are created in other scripts
- data_ingestion.py : Contains the functions used for the cleaning of the list of persons and for the automatic upload of the records not in Airtable yet into Airtable.
- linkedin_finder.py :  Contains 1 function that is the main method used to enrich every single record with a LinkedIn URL if one has been found.
- [utils.py](http://utils.py) : Contains additional functions used in linkedin_finder.py and data_ingestion.py.
- config_template.py : Contains all the keys and variables necessary to assign to start executing the script. The current keys are examples.

### The methods used

- **`data_cleaning`**
    1. Writes the names in the right format (Latin format → utf-8 format)
    2. Drop the duplicates (= 2 times the same person in the dataset).  Rewrites the names in a standardized format, lowercase letters without accents, and compares them (ex. *Frédéric* = *frederic*).
    3. Remove people that are already in the Airtable.
    4. Check by looking at the gender whether the record is correctly written (ex. If gender = “Togo”, the record is removed from the cleaned data and added to the “wrong formatted” data.
    5. Save the clean and wrong formatted data in a CSV file
    6. Write a summary of the cleaning procedure in a text file (Number of cleaned and dropped records).
    
- **`upload_pandas_dataframe`**
    1. Make a dictionary from clean records
    2. For every element of dictionary, create a new record in Airtable if this was not present yet.
    
- **`url_finder`**
    1. Take all the records of the table where no LinkedIn URL is found yet and make a list of them
    2. For every record on the list:
        1. Extract the first and last names with lowercase letters and without accents (fn_woa & ln_woa) with the `name_standardization` function.
        2. Try **Method 1**
            1. Makes a Google search using the full name of the record and its job position when possible and extracts all the HTTP addresses given by this search. 
            2. Try to find a match between one of HTTP addresses and fn_woa and ln_woa with the `url_picker` function and write the match into the Airtable.
        3. Try **Method 2** if no URL is found with Method 1
            1. Makes a Google search using the full name of the record and the “Solvay” keyword and extracts all the HTTP addresses given by this search.
            2. Try to find a match between one of HTTP addresses and fn_woa and ln_woa with the `url_picker` function and write the match into the airtable.
        4. Try **Method 3** if no URL is found with Method 1 and Method 2
            1.  Repeat the process done in Method 1 and 2 (first searching using the job position, searching with “Solvay keyword” otherwise) but using SerApi as API connection to the Google Search engine in place of Google search API.
    3. Return the number of LinkedIn URLs found by each method and the number of URLs not found.
- **`name_standardization`**
    1. Create a first and last name without accents and in lowercase letters based on the full name of the person
    2. Returns the full name without accents and in lowercase letters if the goal is to find duplicated in the dataset. Returns the first and last name separately if the goal is to find the LinkedIn URL.
- **`url_picker`**
    1. Take the HTTP addresses extracted by the Google search API or SerpApi.
    2. Go through all the HTTP addresses. If fn_woa, ln_woa and “linkedin” are in the address, select this URL as the LinkedIn URL of the record.
    3. If no HTTP address matches the criteria, look for the first URL given by the search and seek for less stringent criteria.
    4. Returns “True” to `url_finder` when a LinkedIn URL has been found. 

 

![Summary of the url_finder method that uses the url_picker and the name_standardization functions to find the LinkedIn url of the records and add it into Airtable.](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c5e14043-8285-4f95-a687-69da05804f65/Untitled.png)

Summary of the url_finder method that uses the url_picker and the name_standardization functions to find the LinkedIn url of the records and add it into Airtable.

## 5. Limitations

- **Flexibility of the algorithm**
    - Looks to the content of the HTTP address to detect if a LinkedIn URL might be the one of the individuals. If the format of these HTTP addresses changes, the performance of the algorithm will decrease.
    - The Google Search query is designed to target people from Solvay Alumni Dataset. Enriching other datasets requires changing the queries made in the scripts
- **Treatment of FP identifications:** The B2B-enrichment asset does not treat false LinkedIn URLs yet. A suggestion is made in the [Appendix](https://www.notion.so/self-containedAsset-B2B-Enrichment-V1-8561c8834bcd4267a8993c2e849f1eb5) to detect them, but this comes at a certain cost.
- **Correctness of the data**: 
When a profile is created on LinkedIn, a public version of the profile is published to the LinkedIn member directory. Search engines like Google and Yahoo periodically review this member directory for new and updated public profile information to show in their search results. This indexes the LinkedIn profiles and makes them searchable on the web. **This means LinkedIn public profiles are not always up to date**

## 6. Future Suggestions

**For a more robust search algorithm**

- More in depth LinkedIn URL vs full name matching.
Ex. “*Maxime Khamnei*”, search for “*mkhamnei”* in the HTTP address
- Double-checking with another Solvay alumni Database extracted from a LinkedIn search ($$$)

**Similar projects around leads enrichment**

- Creation of a tool that proposes LinkedIn profiles similar to a target profile. 
Ex. I want to find people with a similar profile (years of experience, previous job positions, education & skills) of the one of “Olivier van Overstraeten”.

# Appendix

The Appendix documents all the tools and methods explored for each different phase. The goal of this documentation is to see if some tools can be useful to use or not. The reasoning why specific tools are chosen is detailed in Phase 0 and 1. For Phase 2, because no choice has been made yet, some suggestions are proposed for enrichment.

The goal of this documentation is mainly to facilitate the takeover of the project by a next person but also to document the different tools in case they might be used for another project. 

## Phase 0: Data Storage

For the storage of the data, the choice is made to use a spreadsheet and not a static database as SQL. This allows simple online data manipulation from the user interface if needed.

### Documentation on tools & methods

 📁 **[Airtable](https://www.airtable.com/)** ✅

- Available Plans
    
    [Sans titre](https://www.notion.so/fbadb5f347314366b898c6bdbedc2476)
    
- Features
    
    ➖ No possibility to add new/rename columns in Airtable from the python script
    
    ➕ Connectivity & non-static: Is available online
    
    ➕ Allows relational databases (not possible with Google sheets)
    
    ➕ Available interface for statistics
    
    ➕ Possible to add automations (ex. triggers created when new records are added)
    

📁 **[Rows.com](https://rows.com/)** ❌

“A spreadsheet with built in functions to do API calls on websites integrated with [rows.com](http://rows.com) 

Possible API connections:

- LinkedIn: Get profile information from the LinkedIn URL
- [Fullcontact](https://www.fullcontact.com/): Persons enrichment based on emial address.
- …

### **Choice explanation**

Airtable is chosen as the storage place over [rows.com](http://rows.com) as it is less expensive, more flexible and more suited to the specific task of LinkedIn url enrichment.

## Phase 1: LinkedIn URL enrichment

To add the LinkedIn URL to the records of persons, several tools and methods are investigated. The idea is to find a combination of methods that are able to find as many correct LinkedIn URLs as possible. 

There are 2 main ways to extract an online LinkedIn address. The first one by **scraping** through the web or by extracting information from an **API call** directly. Scraping is free but is a difficult and long process, while API calls are often more expensive but also more effective. 

### Documentation on tools & methods

*Scraping tools* 🎣
*Api tools* 📑

🎣 **[Phantombuster](https://phantombuster.com/)** ❌

“A tool to automate data extraction based on ‘phantoms’ that extract info from web pages”

- Features:
    
    ➕ Can be integrated in other products with the PhB API
    
    ➕ Opportunity to set up manual and automatic launches of the phantom
    
    ➕ Opportunity to combine different types of phantoms to create an automated workflow. 
         (ex. *LinkedIn URL finder* phantom + *email finder* phantom)
    
- Phantoms:
    - **LinkedIn profile URL finder**: Finds the LinkedIn URL based on the full name & region of search
        - Limitations: Unlimited searches possible since this is done with a search engine and not LinkedIn
        - Inputs: The URL of a spreadsheet, a CSV file or simply a full name and the target market area (ex. French Belgium).
        - Outputs: CSV/ JSON file with the LinkedIn URLs
        - Tests: 6/8 profiles successfully found, 2/8 took a wrong LinkedIn profile.
        - Python Notebook template to enrich Airtable with the use of the *PhantomBuster LinkedIn profile URL finder:*
            
            [PhantomBuster.ipynb](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5e3d2f8e-f12b-4dfa-8380-b70cf554545d/PhantomBuster.ipynb)
            
- Pricing

|  | Starter | Pro | Team |
| --- | --- | --- | --- |
| Price | $59/ month | $139/month | $399/month |
| Execution time | 20h/month | 80h/month | 300h/month |
| # of phantoms | 5 | 15 | 50 |

🎣 **Manual scraping on Google search engine** ❌ 

“Serp Scraping” 

The goal is to scrape directly on the search result pages of browsers like Google or Firefox and find LinkedIn URLs we are interested in.

- **Pros and cons:**
    
    ➕ Free and flexible: You can choose exactly what you query in the browser
    
    ➖ Hard and long process: difficult to find the right URLs by simple scraping on a Chrome     browser.
    
    ➖ Not reliable over time: If the layout of a webpage changes, the scraping tool will not work anymore
    
    ➖ Scraping limits: most browsers set a scraping limit over which your IP address and your     account can be blocked.
    
    ➖ Bad test results: 44 true positives, 18 False positives, 7 Not found 
    
- **Future idea:** Connect to your google or Firefox account with the *selenium* package so that the browser can give you more precise results of your searches. This method was tried in the Google SERP scraping.ipynb notebook, but Google doesn’t allow an automated script to connect to an account.
- **Python Notebook template:**

[Google SERP scraping.ipynb](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6896732c-8a58-462b-98fe-0ea37cbedfd3/Google_SERP_scraping.ipynb)

📑 **[Google Custom Search API](https://developers.google.com/custom-search/v1/overview)** ✅

Connects to your Google programmable search engine and get the results of the search through an API call.

- **Pricing:**
    - 100 queries free/day
    - 5$/1000 queries after that
- **Pros and cons:**
    
    ➕ Scalable: You pay exactly for the number of queries you want to do in your search engine
    
    ➕ Reliable: As you connect directly to the data through the API and not the layout of the site, a change in that will not influence the process.
    
    ➕ Lot of possibilities of different queries to write in the engine.
    
    ➖ Low control over the results the search engine gives. This might not be adapted to our searches.
    
- **Tests:**
Different queries in the google search engine are tried. The results are shown in the table below. The “Query” **column explains which information was used in the Google search engine. 
For example: [full name, job position, “LinkedIn”] for JQueryulien Theys writes [Julien Theys Managing Partner Agilytic LinkedIn] in the Google search engine.
    
    
    | Query | query example | True Positives | False Positives | Not Found |
    | --- | --- | --- | --- | --- |
    | full name, job position, “LinkedIn” | “Julien Theys managing partner Agilytic” | 55/80 | 0/80 | 25/80 |
    | full name, “Solvay”, “LinkedIn” | “Julien Theys Solvay LinkedIn” | 53/80 | 2/80 | 25/80 |
    | full name, “LinkedIn” | “Julien Theys LinkedIn” | 61/80 | 15/80 | 4/80 |
    
    *Example. For the query in the search engine specifying the full name of the record, its job position and the “LinkedIn” keyword, the correct LinkedIn URL was found for 55 out of the 80 records.*
    
    - True Positive (TP): The LinkedIn URL is successfully found.
    - False Positive (FP): The LinkedIn URL is found but is not the one of the recordsDeveloper we are searching for.
    - Not Found (NF): No LinkedIn URL is found for that specific record.
    **

📑 **[SerpApi](https://serpapi.com/)** ✅

“A real time API to access google search results”

- **Pricing:**
    
    
    |  | Developper | Production |
    | --- | --- | --- |
    | Price | $50/ month | $130/month |
    | Searches | 5000/month | 15 000/month |
- **Pros and cons:**
    
    ➕ Precise and reliable
    
    ➖ Expensive
    
- **Tests:**
    
    The query written for the SerpApi search takes the full name, the job position and the “LinkedIn keyword” into account. 
    The results are the following:
    
    - TP: 28/30
    - FP: 1/30
    - NF: 1/30

### **Choice explanation**

**Summary of the methods tested on the Solvay Dataset**

|  | Method 1 | Method 2 | Method 3 | Method 4 | Method 5 | Method 6 | Method 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tool used | Google Custom search | Google Custom search | Google Custom search | SERP scraping | SERP scraping | Serp API | PhantomBuster |
| Search Query  | Full name, Job, “LinekdIn” | Full name, “Solvay”, “LinkedIn” | Full name, “LinkedIn” | Full name, Job, “LinkedIn” | Full name, “Solvay”, “LinkedIn” | Full name, Job, LinkedIn | Full name, region (ex. French Belgium) |
| Results | TP: 55
FP: 0
NF: 25 | TP: 53
FP: 2
NF: 25 | TP: 61
FP: 15
NF: 4 | TP: 44
FP: 18
NF: 7 | TP: 53
FP: 23
NF: 5 | TP: 28
FP: 1
NF: 1 | TP: 6
FP: 2 |
| Price  | $$ | $$ | $$ | $ | $ | $$$ | $$$ |

*Explanation: The results indicates the amount of LinkedIn profile urls found that correspond to the profile of the individual (TP), the amount of LinkedIn profile urls found that corresponds to someone else profile (FP) and the amount of records for which no LinkedIn profile url is found (NF)*

The goal during phase 1 is to retrieve as much LinkedIn profiles as possible but to ensure a very high precision. The precision is the amount of correct LinkedIn profiles out of all the URLs found [TP/(FP+TP)]. A high precision can be achieved through different stages of enrichment. Each stage uses a different method in function of the difficulty to find the personal LinkedIn URL of a person.

1. In the first stage, we want to have a method that finds the LinkedIn profile of individuals for which it is easy to find their LinkedIn profile but that do not find any wrong profile (FP). For that **method 1** is chosen as the number of FP is 0.
2. In the next stages we want to find the remaining LinkedIn profiles, the one the one not found by the first method. We thus progressively uses less severe method that are able to find LinkedIn profile of individuals that are harder to find. It is important to not have too many FP in the results url, thus we stop the enrichment once we feel adding other methods will detect a lot of FP’s compare to TP’s. Thus **method 2** and **method 6** are chosen as additional methods. 

Other criterias takeninto account are:

- Scalability: The possibility to extend the solution to larger datasets
- Reliability over time: Scraping methods are jot reliable over time as they depend of the site layout

Note that the price is not really taken into account as the budget available for enrichment is way bigger than the cost of the enrichment.

**Results on the test dataset by staging Method 1, Method 2 and Method 6 on 80 records**

|  | Method 1 | Method 1 + 2 | Method 1 + 2 + 6 |
| --- | --- | --- | --- |
| Number of urls found | 55/80 | 70/80 | 79/80 |
| Precision  | 55/55 | 69/70 | 76/79 |

Combining method 1, 2 and 6 cumulatively gives a total precision of 76/79 on this dataset. This means that out of the 80 records, 79 LinkedIn profiles where found and 76 out of this 79 where the specific profile of that person we searched for.

Staging several methods on top of another lowers the precision a bit compared to using only 1 method, but more LinkedIn addresses are found.

![Illustration of the performance of the test dataset](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e8f0b08c-594b-41db-922b-ef9aaf34034e/Untitled.png)

Illustration of the performance of the test dataset

## Phase 2 & 3: Further data enrichment & monitoring

The goal of this phase is to extract information out of the LinkedIn profile of the individuals found during phase 1. The informations of interest are the company the individual is working in and their job position. These whole databases of individuals can thus be monitored as the informations extracted in phase 2 allow to flag for job changes within the company or company changes. 

Additionally the email of these individuals is also an important as this provide another way to connect the persons besides through their LinkedIn profile.

### Documentation on tools & methods

🎣 [**Iscraper.io**](https://iscraper.io/)

A tool you can connect to with an API and that does scrape on LinkedIn for you. Allows to extract information out of LinkedIn profiles such as company and current job position.

Possibility to be **used for FP (false profile) identification**. 
Example In Solvay dataset: You scrape through all the LinkedIn urls and check whether “Solvay Business School” is part of their educational background.

- **Pricing:**
    - 0.006$ per request → 180$ to enrich the full Solvay Alumni dataset
- **Pros and cons:**
    
    ➕ Unlimited: Don’t need to fill in your LinkedIn profile to scrape.
    
    ➕ Reliable information: Don’t uses a database but scrapes directly through the profiles. 
    
- **Python Notebook template:** 
Python code that check whether “Solvay” is stated in one of the formation of the individuals.
    
    [Iscraper_Nubela.ipynb](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/842a2976-163a-4432-9e4c-fa9c6bab1630/Iscraper_Nubela.ipynb)
    

🎣 **[Evaboot](https://evaboot.com/)**

A LinkedIn sales navigator scraper that allows you to extract several LinkedIn profiles at once from a search in Sales Navigator. It has an additional option that allows to find the email of the profile extracted

Can be used for “inverse enrichment: You start from a huge database by scraping all the LinkedIn profiles you might be interested in and check if one of these profiles matches with the individual you want to find a LinkedIn profile for.

ex. You extract all the people on LinkedIn with “Solvay” in their formation and use this database to find matches with the Solvay Alumni from which you want to find the LinkedIn profile.

- **Pricing**
    
    
    | Number of leads | Extract only | Extract + email |
    | --- | --- | --- |
    | 1k  | 17 € | 35 € |
    | 5k  | 63 € | 117 € |
    | 20k  | 117 € | 236 € |
    | 50k | 227 € | 454 € |
    | 100k | 363 € | 818 € |
- **Pros and cons**
    
    ➕ Becomes cheap with larger databases
    
    ➕ Lots of info about extraction (url, job title & description, company, location, …)
    

🎣 **[](https://evaboot.com/)[Nubela/ Proxycurl](https://nubela.co/proxycurl/)**

Connect to the sites API to extract information about LinkedIn profiles from their database

- Pricing: 0,01$/ request
- **pros and cons:**
    
    ➖ reliability: You are scraping on a database and not in LinkedIn directly which means the data is not always up to date.
    

📩 [**Dropcontact**](https://www.dropcontact.com/fr)

- **Description**
    - **Enrich** your leads data: Email finder with 98% confidence, LinkedIn profile finder, …
    - **Boost** the data: Email verification, Merge duplicates, Standardize the information, …
    - **Clean** the data: ex. Name order correction
- **Pros ans cons**
    
    ➕ Possibility of interation with Hubspot
    
    ➕ RGDP compliant
    
- **Pricing:**
    
    
    | # enrichments/mont | 1k  | 8k | 20k | 40k |
    | --- | --- | --- | --- | --- |
    | Price  | 29 € | 75 € | 179 € | 349 € |

🎣 **[Phantombuster](https://phantombuster.com/)** ❌

“A tool to automate data extraction based on ‘phantoms’ that extract info from web pages”

- Features:
    
    ➕ Can be intergated in other products with the PhB API
    
    ➕ Possibility to setup manual and automatic launches of the phantom
    
    ➕ Possibility to combine different types of phantoms to create a automated workflow. 
         (ex. *LinkedIn url finder* phantom + *email finder* phantom)
    
- Phantoms:
    - **LinkedIn Search Export**: Finds sevral LinkedIn URLs based on a search
        - Limitiations: Max 100 pages/ 1000 results per day over 5 launches minimum in the day, otherwise LinkedIn might block your account.
    - **LinkedIn profile scraper**: Get all the info on a LinkedIn profile based on the LinkedIn URL
        - Limitations: +- 80 LinkedIn profile scraping/day per account
        - See [good practices](https://phantombuster.com/blog/guides/linkedin-automation-rate-limits-2021-edition-5pFlkXZFjtku79DltwBF0M) when scraping on LinkedIn
    - **Professional Email finder:** Reconstruct an intelligent email address based on LinkedIn full name and company name and verifies it once the email is created
        - 35% - 65% succes rate
        - 500 credits/month
        - Possibility to use for further Data Enrichment
- Pricing
    
    
    |  | Starter | Pro | Team |
    | --- | --- | --- | --- |
    | Price | $59/ month | $139/month | $399/month |
    | Execution time | 20h/month | 80h/month | 300h/month |
    | # of phantoms | 5 | 15 | 50 |

### Suggestions

Regarding the prices and performances, Iscraper seems the most suited tool to scrape information out of the LinkedIn profiles of individuals. scraping once in a while over all the profiles also allows to flag for changes in job position or company. 

In certain cases (as for the Solvay Alumni dataset), I scraper would also allow to detect LinkedIn profiles that do not correspond to the person it is attached to in our database. 

## Summary of the tools and for what they can be used

|  | LI-URL finder | LinkedIn profile scraping | Other data enrichment |
| --- | --- | --- | --- |
| PhantomBuster | x | x | x |
| Google search API | x |  |  |
| SerpAPI | x |  |  |
| Serp scraping | x |  |  |
| Iscraper |  | x |  |
| Evaboot |  | x |  |
| Nubela |  | x |  |
| Dropcontact |  |  | x |

### Questions Julien

Comment continuer ASAP?

1. Finir enrichissement URL et le pousser dans la DB de prod
2. Finir enrichissement des autres donées
3. Monitoring
