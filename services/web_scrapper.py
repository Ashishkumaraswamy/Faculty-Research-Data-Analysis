from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import logging
import os

logger = logging.getLogger("web_scrapper")

chrome_options = Options()
# set headless mode
chrome_options.add_argument('--headless')

# Constants
WEBSITE_URL = "https://psgtech.edu/fac_publications.php"
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
REQUEST_COOKIES = {'PHPSESSID': 'av4fkss9aj8jofen333ote5pd5'}
FACULTY_DATA = []


# Request Configurations

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass


CWD = os.path.abspath('.')
PARENT_DIR = os.path.dirname(CWD)
DATA_FOLDER = "Research_Area_Analysis_AMCS/data"


def store_csv(df, name):
    df.to_csv(CWD.replace(
        '\\', '/')+'/data/{}.csv'.format(name), index=False, header=True)


def extract_journal_description(url):
    url = "https://scholar.google.co.in"+url
    try:
        logger.info(
            "print here Page source of {} and scrapping the google scholar data".format(url))
        driver = webdriver.Chrome(
            'Research_Area_Analysis_AMCS\chromedriver_win32\chromedriver.exe', options=chrome_options)
        # navigate to a website
        driver.get(url)
        element = driver.find_element(By.CLASS_NAME, 'gsh_csp')
        return element.text
    except Exception as e:
        logger.error(
            'Google Scholar Research scrapping failed\n {}'.format(e))
        return


def extract_faculty_research_information(url):
    global FACULTY_DATA
    google_scholar_data = {}
    try:
        logger.info(
            "Requesting Page source of {} and scrapping the google scholar data".format(url))
        page = requests.get(url, headers=REQUEST_HEADERS)
        soup = BeautifulSoup(page.content, 'lxml')
        name = soup.find('div', id="gsc_prf_in")
        faculty_name = name.text
        cited_by_table = soup.find_all('table', id="gsc_rsb_st")[
            0].find('tbody').find_all('tr')
        cited_by = []
        for tr in cited_by_table:
            cited_by.append(tr.find_all('td')[1].text)
        citation_all, h_index, i10_index = cited_by
        title_definition_elements = soup.find_all('td', class_="gsc_a_t")
        journal_titles = []
        journal_description = []
        for elements in title_definition_elements:
            a = elements.find('a', href=True)
            print("***", a['href'])
            journal_titles.append(elements.find('a').text)
            journal_description.append(extract_journal_description(a['href']))
        google_scholar_data = create_google_scholar_record(
            faculty_name, citation_all, h_index, i10_index, journal_titles, journal_description)
        FACULTY_DATA.append(google_scholar_data)
    except Exception as e:
        logger.error(
            'Google Scholar Research scrapping failed\n {}'.format(e))
        return


def create_google_scholar_record(faculty_name, citation_all, h_index, i10_index, journal_titles, journal_description):
    google_scholar_data = {}
    google_scholar_data['Name'] = faculty_name
    google_scholar_data['Citations_All'] = citation_all
    google_scholar_data['H-Index_All'] = h_index
    google_scholar_data['i10-Index_All'] = i10_index
    google_scholar_data['Journals'] = journal_titles
    google_scholar_data['Journal Description'] = journal_description
    google_scholar_data['No. of Journals'] = len(journal_titles)
    print("\n**************************\n")
    print(google_scholar_data)
    return google_scholar_data


def scrape_research_website(url):
    global FACULTY_DATA
    FACULTY_DATA = []
    logger.info(
        "Requesting from page source {} and scraping to extract the faulty research data".format(url))
    page = requests.get(url, verify=False,
                        headers=REQUEST_HEADERS, cookies=REQUEST_COOKIES)
    soup = BeautifulSoup(page.content, "html.parser")
    google_scholar_links = soup.select('td[data-title="google"]')
    for tags in google_scholar_links:
        a = tags.find('a', href=True)
        if a:
            extract_faculty_research_information(a['href'])


def create_faculty_research_data():
    global FACULTY_DATA
    df = pd.DataFrame(FACULTY_DATA)
    df = df.explode(['Journals', 'Journal Description'])
    return df


# df = pd.read_csv(CWD.replace(
#     '\\', '/')+'/data/{}.csv'.format('faculty_research'))
scrape_research_website(WEBSITE_URL)
faculty_research_data = create_faculty_research_data()
store_csv(faculty_research_data, "faculty_research")
