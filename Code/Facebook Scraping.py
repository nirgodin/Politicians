from facebook_scraper import *
import pandas as pd
import numpy as np

politicians_dct = {'Bennett': 'NaftaliBennett',
                   'Netanyahu': 'Netanyahu'}

# Initialize empty list to which we'll append posts dataframes of each politician
df_lst = []

# Iterate through the politicians dictionary and create for each of them a seperate posts dataframe
for p in politicians_dct.keys():

    # Initialize empty dataframe
    pst_df = pd.DataFrame()

    # Append each post's data points to the post dataframe as row
    for post in get_posts(politicians_dct[p], pages=20):
        pst_df = pst_df.append(pd.Series(post), ignore_index=True)

    # Insert a name column with the politician name
    pst_df.insert(0, 'name', p)

    # Append the final dataframe to the dataframes list
    df_lst.append(pst_df)

# Concateante the different dataframes stored in the df_lst to one big dataframe
Politicians = pd.concat(df_lst)
