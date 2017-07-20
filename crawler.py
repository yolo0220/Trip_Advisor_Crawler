# -*- coding: utf-8 -*-
"""
Created on 7/19/17
Author: Jihoon Kim
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome('chromedriver/chromedriver')
driver.implicitly_wait(3)

# access trip advisor page
driver.get("https://www.tripadvisor.co.kr/")
# access things to do page
driver.find_element_by_id("global-nav-attractions").click()


# Test Case for '경복궁'
driver.find_element_by_class_name("typeahead_input").send_keys('경복궁')
driver.find_element_by_id("SUBMIT_THINGS_TO_DO").click()

# Extract Latest Review
latest_review_id = driver.find_element_by_xpath("//div[@class='reviewSelector']").get_attribute("id")
id_num = latest_review_id.split('_')[1]
target_path_for_more_button = "\"" + "review_" + id_num + "\""
xpath_more = "//*[@id=" + target_path_for_more_button + "]/div/div[2]/div/div[1]/div[3]/div/p/span"
driver.find_element_by_xpath(xpath_more).click()
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
titles = [title.text for title in soup.find_all("span", {"class": "noQuotes"})]
reviews = [review.text for review in soup.find_all("p", {"class": "partial_entry"})][2:]
ratings = []
for i in range(len(titles)):
    rating.append(int(soup.find_all("div", {"class": "rating reviewItemInline"})[i+2].find('span').get("class")[1][-2:]))
