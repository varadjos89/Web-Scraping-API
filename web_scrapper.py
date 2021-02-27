import requests
import csv
from bs4 import BeautifulSoup
import re
import pandas as pd

URL = 'https://aspe.hhs.gov/poverty-guidelines'
page = requests.get(URL)


soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='content')


## Returns all the tables within html page
table_elems = results.find_all('table', class_='footable')


first_column_arr = []
second_collumn_arr = []

## Accessing rows data by applying regex, to remove unnecessary data 
for tr in soup.find_all('tr'):
    tds = tr.find_all('td')
    if len(tds) == 2:
        first_column_arr.append(str(tds[0]).replace('<td>','').replace('</td>',''))
        second_collumn_arr.append(str(tds[1]).replace('<td>','').replace('</td>','').replace('$','').replace(',',''))
        
## Store dict as a dataframe
dictionary_frame = {"PERSONS IN FAMILY/HOUSEHOLD" : first_column_arr,
                    "POVERT GUIDLINES($)" : second_collumn_arr}
household_df = pd.DataFrame(dictionary_frame)

## Divide the data frame into 3 different data frames
STATES_48_DF = household_df[:8]
ALASKA_DF = household_df[8:16]
HAWAII_DF = household_df[16:32]

## Exports them as CSV files
STATES_48_DF.to_csv('Others.csv', index = False)
ALASKA_DF.to_csv('Alaska.csv', index = False)
HAWAII_DF.to_csv('Hawaii.csv', index = False)

