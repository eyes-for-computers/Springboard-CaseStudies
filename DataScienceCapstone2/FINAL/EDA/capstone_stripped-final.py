#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Merging columns in many excel files to a standar format

# Many staff have created their own excel sheets to show similiar
# information. This script will find the standar name targets in
# each sheet and put them into a single standard format.


# In[2]:


import matplotlib.pyplot as plt
import requests
import pandas as pd
from fuzzywuzzy import fuzz, process
import Levenshtein
import os
import glob

import pandas_profiling
from pandas_profiling.utils.cache import cache_file


# In[3]:


# Function to read in all excel files in a folder and creates a single dataframe
# Output is the full df and the column names that have been extracted

def read_all_excel_cwd():

    extracted_df = pd.DataFrame()
    test = pd.DataFrame()
    x=0
    test = pd.concat([extracted_df, test])

    path = os.getcwd()
    excel_files = glob.glob(os.path.join(path, "*.xlsx"))
    print(excel_files)
    
    for file in excel_files:
        print(len(excel_files))
        x += 1
        print('finished ', x, ' files')
        df = pd.concat(pd.read_excel(file, sheet_name=None), ignore_index=True)
        print(df.keys())
        extracted_df = extracted_df.append(df)

    extracted_df.columns = map(str.lower, extracted_df.columns)
    extracted_cols = extracted_df.columns 
    extracted_df = extracted_df.set_index('date')
    
    print('should be df next')
      
    return extracted_df, extracted_cols

# An extention on this would have it read in each file one by one to a dictionary 


# In[4]:


extracted_df, extracted_cols = read_all_excel_cwd()


# In[5]:


extracted_df.head()


# In[6]:


# Creating a list of target behaviors that are being searched for

bx_list = ['aggression', 'elope', 'non-compliance', 'sib', 'protesting'  ] #'agg','repeated' #'date'


# In[7]:


# Function takes in the target bx list and the column names that have been extracted
# and returns  match_df of the target bx, the matched column from the extracted_df and
# the fuzz.partial_ratio of the match

def fuzz_match(bx_list,extracted_cols):

    matches = []
    match_df = pd.DataFrame()

    
    for bx in bx_list:
        print('working on: ', bx)
    
        for item in extracted_cols:
           
            fuzz_pr = fuzz.partial_ratio(item, bx)
        
            df_res = pd.DataFrame(data={'bx': bx, 'original_col_name' : item, 'fuzz_pr':fuzz_pr}, index=[i for i in range(len(extracted_df))] )
            match_df = match_df.append(df_res)

    return match_df

match_df = fuzz_match(bx_list,extracted_cols)
print('done')


# In[16]:


# Create df for each target bx match against the extracted_cols and joins them together in all_matches

agg_matches = match_df.loc[(match_df.bx.str.contains('aggression')) & (match_df.fuzz_pr > 80)].drop_duplicates(subset ="original_col_name", keep ='first', inplace = False)

elope_matches = match_df.loc[(match_df.bx.str.contains('elope')) & (match_df.fuzz_pr > 65)].drop_duplicates(subset ="original_col_name", keep ='first', inplace = False)

noncomp_matches = match_df.loc[(match_df.bx.str.contains('non-compliance')) & (match_df.fuzz_pr > 90)].drop_duplicates(subset ="original_col_name", keep ='first', inplace = False)

protest_matches = match_df.loc[(match_df.bx.str.contains('protest')) & (match_df.fuzz_pr > 70)].drop_duplicates(subset ="original_col_name", keep ='first', inplace = False)

sib_matches = match_df.loc[(match_df.bx.str.contains('sib')) & (match_df.fuzz_pr > 80)].drop_duplicates(subset ="original_col_name", keep ='first', inplace = False)

#date_matches = match_df.loc[(match_df.bx.str.contains('date')) & (match_df.fuzz_pr > 85)].drop_duplicates(subset ="original_col_name", keep ='first', inplace = False)


all_matches = pd.concat([agg_matches, elope_matches, noncomp_matches, protest_matches, sib_matches])

print('done')




# Visually inspecting samples of the match_df by bx and fuzz_pr to determine a better match threshold


#thresh 80
#agg_matches_styled = match_df.loc[(match_df.bx.str.contains('aggression')) & (match_df.fuzz_pr > 50) & (match_df.fuzz_pr <= 100) ].groupby('fuzz_pr', sort=True).sample(10).style.background_gradient(subset='fuzz_pr',cmap='summer_r')

#thresh 65
#elope_matches_styled = match_df.loc[(match_df.bx.str.contains('elope')) & (match_df.fuzz_pr > 50) & (match_df.fuzz_pr <= 100) ].groupby('fuzz_pr', sort=True).sample(10).style.background_gradient(subset='fuzz_pr',cmap='summer_r')

#thresh 90
#noncomp_matches_styled = match_df.loc[(match_df.bx.str.contains('nc')) & (match_df.fuzz_pr > 50) & (match_df.fuzz_pr <= 100) ].groupby('fuzz_pr', sort=True).sample(10).style.background_gradient(subset='fuzz_pr',cmap='summer_r')

# thresh = 80
#date_matches_styled = match_df.loc[(match_df.bx.str.contains('date')) & (match_df.fuzz_pr > 50) & (match_df.fuzz_pr <= 100) ].groupby('fuzz_pr', sort=True).sample(10).style.background_gradient(subset='fuzz_pr',cmap='summer_r')

# thresh=70
#protest_matches_styled = match_df.loc[(match_df.bx.str.contains('protest')) & (match_df.fuzz_pr > 50) & (match_df.fuzz_pr <= 100) ].groupby('fuzz_pr', sort=True).sample(10).style.background_gradient(subset='fuzz_pr',cmap='summer_r')

#profile_report = match_df.profile_report(explorative=True, html={'style': {'full_width': True}})
#profile_report

#put the thresholds in a dictionary to access later
fuzz_thresh = { 'date_matches' : 80, 'agg_matches' : 70, 'elope_matches': 65, 'noncomp_matches' : 90, 'sib_matches' : 80} #'date_matches' : 80,


# In[17]:


all_matches


# In[18]:


# Function takes in df of all matching bx and column names and returns the master_df
# containing of the extracted columns data put into the target column names 


#make dictionary using extracted_df[old col name].to_dict()
def add_to_master_df(all_matches):
    
    master_df = pd.DataFrame()
    
    master_df = extracted_df[all_matches['original_col_name'].tolist()]
    master_df.columns = all_matches.bx.tolist()
    master_df.head()
    
    return master_df


# In[19]:


master_df = add_to_master_df(all_matches)


# In[20]:


master_df.to_excel('master_df.xlsx')


# In[ ]:





# In[ ]:




