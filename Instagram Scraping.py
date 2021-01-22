import pandas as pd
import numpy as np
import requests
from instascrape import *
from selenium import webdriver
from time import sleep
from Credentials import mail, password
from bs4 import BeautifulSoup


def instush_df(dct):
    # Import relevant libraries
    import pandas as pd
    df_lst = []
    for user in dct.keys():
        # Setting driver and entering Instagram
        driver = webdriver.Chrome(r'C:\Users\nirgo\PycharmProjects\Fantasy\Browsers\chromedriver.exe')
        driver.get('https://instagram.com')
        sleep(5)
        # Set mail and password fields
        mail_field = driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
        pass_field = driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
        login = driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div')

        # Fill the field with the mail and password
        mail_field.send_keys(mail)
        pass_field.send_keys(password)

        # Login by clicking
        login.click()
        sleep(5)

        # Continue to the real homepage by dismissing instagram suggestions
        notnow1 = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')
        notnow1.click()
        sleep(5)
        notnow2 = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
        notnow2.click()
        sleep(5)

        # Empty dataframe to append the scraped data
        Posts = pd.DataFrame()

        # session_id = generate_session()
        profile = Profile(dct[user][0])
        profile.scrape(webdriver=driver)
        posts = profile.get_posts(webdriver=driver, scrape=True)
        posts_df = pd.DataFrame([post.to_dict() for post in posts])
        df_lst.append(posts_df)
        driver.close()

    # Change column names
    # Posts = Posts.rename(columns={0: 'name',
    #                               1: 'organization',
    #                               2: 'gender',
    #                               3: 'hebrew_name',
    #                               4: 'timestamp',
    #                               5: 'shortcode',
    #                               6: 'likes_count',
    #                               7: 'comments_count',
    #                               8: 'caption',
    #                               9: 'video',
    #                               10: 'location'})

    return df_lst



lala = instush_df(politicians_dct)
