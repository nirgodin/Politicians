import pandas as pd
import numpy as np
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class KnessetWebsiteScraper:

    def __init__(self):

        self.current_knesset_number = 24
        self.main_website = 'https://main.knesset.gov.il/'
        self.historic_knesset_members_page = 'https://main.knesset.gov.il/mk/Pages/Previous.aspx?pg=mkpknessethist'
        self.females_page_xpath = '/html/body/form/div[5]/div/div[1]/div/span/div[2]/table/tbody/tr[1]/td/div/div/div' \
                                  '/div/div[1]/table/tbody/tr/td/div/div/div[1]/div[1]/div[6]'

    @staticmethod
    def open_driver():
        chrome_options = Options()
        chrome_options.experimental_options
        chrome_options.addArguments("disable-blink-features=AutomationControlled")
        # chrome_options.setExperimentalOption("excludeSwitches", Collections.singletonList("enable-automation"))
        chrome_options.setExperimentalOption("useAutomationExtension", False)

        return webdriver.Chrome(executable_path=r'Browsers\chromedriver.exe',
                                options=chrome_options)

    @staticmethod
    def enter_webpage(webpage: str) -> None:
        driver = KnessetWebsiteScraper.open_driver()
        sleep(2)
        driver.get(webpage)
        sleep(2)

    def female_member_scraper(self, knesset_number: int, xapth_ordinal_num: int) -> str:
        """ Scrapes the name of a female parliament member,
            given the number of the knesset and her ordinal number on the web page """

        # Enter the website page
        KnessetWebsiteScraper.enter_webpage(self.historic_knesset_members_page)
        females_page_button = driver.find_element_by_xpath(self.females_page_xpath)
        females_page_button.click()
        sleep(3)

        name_xpath = f'/html/body/form/div[5]/div/div[1]/div/span/div[2]/table/tbody/tr[1]/td/div/div/div/div/div[1]' \
                     f'/table/tbody/tr/td/div/div/div[2]/div[3]/div/div/div[{xapth_ordinal_num}]/div[2]/a'

        name = driver.find_element_by_xpath(name_xpath).text

        return name

    # def female_members_list(self) -> list:
    #     """ Returns a list of all female knesset members to this day """
    #
    #     female_members_list = []
    #
    #     for knesset in range(1, self.current_knesset_number + 1):
    #
    #         while (True):


mk = KnessetWebsiteScraper()

mk.enter_webpage(mk.main_website)
sleep(3)
mk.female_member_scraper(1, 1)
