from facebook_scraper import *
from requests.exceptions import HTTPError
import pandas as pd
import numpy as np
from Code.Dictionaries import fb_politicians_dct

# Initialize empty list to which we'll append posts dataframes of each politician
df_lst = []

# Iterate through the politicians dictionary and create for each of them a seperate posts dataframe
for p in fb_politicians_dct.keys():

    # Initialize empty dataframe
    pst_df = pd.DataFrame()

    # Append each post's data points to the post dataframe as row
    try:
        for post in get_posts(fb_politicians_dct[p][0], pages=50):
            pst_df = pst_df.append(pd.Series(post), ignore_index=True)
    except HTTPError:
        pass

    # Insert a name column with the politician name
    pst_df.insert(0, 'name', p)

    # Append the final dataframe to the dataframes list
    df_lst.append(pst_df)

# Concateante the different dataframes stored in the df_lst to one big dataframe
Politicians = pd.concat(df_lst)

Politicians.to_csv(r'Data/Facebook/Facebook.csv', index=False) # encoding='utf-8-sig'

gen_lst = []
for p in fb_politicians_dct.keys():
    gen_lst.append(fb_politicians_dct[p][2])

gen_dct = dict(zip(list(fb_politicians_dct.keys()), gen_lst))

Politicians['gender'] = Politicians['name'].map(gen_dct)

pst_df = pd.DataFrame()
for post in get_posts('אבישי-בן-חיים-100044619060813', pages=1):
    pst_df = pst_df.append(pd.Series(post), ignore_index=True)

