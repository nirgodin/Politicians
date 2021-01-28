import pandas as pd
import numpy as np
import requests
from instascrape import *
from selenium import webdriver
from time import sleep
from Code.Credentials import mail, password
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

    return df_lst

# Import relevant libraries
import pandas as pd
# from Instagram Dictionaries import politicians_dct

df_lst = []
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
for user in list(politicians_dct.keys())[0:10]:
    for attempt in range(0,10):
        try:
            # Empty dataframe to append the scraped data
            # Posts = pd.DataFrame()

            # session_id = generate_session()
            profile = Profile(politicians_dct[user][0])
            profile.scrape(webdriver=driver)
            posts = profile.get_posts(webdriver=driver, scrape=True)
            posts_df = pd.DataFrame([post.to_dict() for post in posts])
            df_lst.append(posts_df)
        except ValueError:
            pass
        except IndexError:
            sleep(600)
            continue
        else:
            print('we failed all the attempts - deal with the consequences.')


lala = instush_df(politicians_dct)

type()
