# -*- coding: utf-8 -*-
"""
Created on 7/19/17
Author: Jihoon Kim
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome('./chromedriver/chromedriver')
driver.implicitly_wait(3)

sites = ['여수 해상케이블카', '서울대공원', '남이섬']

for site in range(len(sites)):
    # access trip advisor page
    driver.get("https://www.tripadvisor.co.kr/Attractions")

    print("========================================")
    # Test Case
    driver.find_element_by_class_name("typeahead_input").clear()
    driver.find_element_by_class_name("typeahead_input").send_keys(sites[site])
    driver.find_element_by_id("SUBMIT_THINGS_TO_DO").click()
    time.sleep(2)

    # extract last page
    print("Crawling Starts on: " + sites[site])
    soup = BeautifulSoup(driver.page_source, "html.parser")
    last_page_att = soup.find("span", {"class": "pageNum last taLnk "})
    last_page = int(last_page_att.get("data-page-number"))
    print("Number of Pages: ", last_page)

    # containers
    titles = []
    reviews = []
    ratings = []
    dates = []

    for i in range(last_page):

        print("Crawling Process: %s / %s" % (i + 1, last_page))
        # Extract Latest Review
        time.sleep(2)
        latest_review_id = driver.find_element_by_xpath("//div[@class='reviewSelector']").get_attribute("id")
        id_num = latest_review_id.split('_')[1]
        target_path_for_more_button = "#" + "review_" + id_num
        selector = target_path_for_more_button + " > div > div.ui_column.is-9 > div > div.wrap > div.prw_rup.prw_reviews_text_summary_hsx > div > p > span"
        time.sleep(3)
        try:
            driver.find_element_by_css_selector(selector).click()
        except:
            pass
        time.sleep(4)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        titles.extend([title.text for title in soup.find_all("span", {"class": "noQuotes"})])
        reviews.extend([review.text for review in soup.find_all("p", {"class": "partial_entry"})][2:])
        len_this_page = len([title.text for title in soup.find_all("span", {"class": "noQuotes"})])

        for num_rate in range(len_this_page):
            ratings.append(int(soup.find_all("div", {"class": "rating reviewItemInline"})[num_rate+2].find('span').get("class")[1][-2:-1]))
            dates.append(soup.find_all("span", {"class": "ratingDate relativeDate"})[num_rate].get('title'))
        if i < last_page - 1:
            driver.find_element_by_xpath("//*[@id=\"taplc_location_reviews_list_0\"]/div[22]/div/span[2]").click()
        time.sleep(2)

    print("========================================")
    ta_df = pd.DataFrame({'title': titles, 'review': reviews, 'rating': ratings, 'dates': dates})
    ta_df.to_csv(sites[site]+'.csv', encoding='utf-8')