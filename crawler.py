# -*- coding: utf-8 -*-
"""
Created on 7/19/17
Author: Jihoon Kim
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome('chromedriver/chromedriver')
driver.implicitly_wait(3)

# access trip advisor page
driver.get("https://www.tripadvisor.co.kr/")
# access things to do page
driver.find_element_by_id("global-nav-attractions").click()

sites = ['김광석']

# Test Case
driver.find_element_by_class_name("typeahead_input").send_keys(sites[0])
driver.find_element_by_id("SUBMIT_THINGS_TO_DO").click()
time.sleep(2)


# extract last page
print("Crawling Starts on: " + sites[0])
soup = BeautifulSoup(driver.page_source, "html.parser")
last_page_att = soup.find("span", {"class": "pageNum last taLnk "})
last_page = int(last_page_att.get("data-page-number"))
print("Number of Pages: ", last_page)

# containers
titles = []
reviews = []
ratings = []

for i in range(last_page):

    print("Crawling Process: %s / %s" % (i + 1, last_page))
    # Extract Latest Review
    time.sleep(2)
    latest_review_id = driver.find_element_by_xpath("//div[@class='reviewSelector']").get_attribute("id")
    id_num = latest_review_id.split('_')[1]
    target_path_for_more_button = "\"" + "review_" + id_num + "\""
    xpath_more = "//*[@id=" + target_path_for_more_button + "]/div/div[2]/div/div[1]/div[3]/div/p/span"
    time.sleep(2)
    driver.find_element_by_xpath(xpath_more).click()
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    titles.extend([title.text for title in soup.find_all("span", {"class": "noQuotes"})])
    reviews.extend([review.text for review in soup.find_all("p", {"class": "partial_entry"})][2:])

    len_this_page = len([title.text for title in soup.find_all("span", {"class": "noQuotes"})])

    for num_rate in range(len_this_page):
        ratings.append(int(soup.find_all("div", {"class": "rating reviewItemInline"})[num_rate+2].find('span').get("class")[1][-2:-1]))
    time.sleep(2)

    if i < last_page - 1:
        driver.find_element_by_xpath("//*[@id=\"taplc_location_reviews_list_0\"]/div[22]/div/span[2]").click()

    print("========================================")

ta_df = pd.DataFrame({'Title': titles, 'Review': reviews, 'Rating': ratings})
