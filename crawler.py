# -*- coding: utf-8 -*-
"""
Created on 7/19/17
Author: Jihoon Kim
"""


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()


print("Select your web-driver path: ")
driver = webdriver.Chrome(file_path)
driver.implicitly_wait(3)

lang = int(input("Choose the language: \n 1. English \n 2. Korean"))

if lang == 1:
    webadr = "https://www.tripadvisor.co.uk/Attractions"
elif lang == 2:
    webadr = "https://www.tripadvisor.co.kr/Attractions"
else:
    raise ValueError("Wrong input.")

print("Type the sites you want to crawl: (type 'quit' to end)")
sites = []
while True:
    site = input()
    if site == 'quit':
        break
    sites.append(site)

for site in range(len(sites)):
    # access trip advisor page
    driver.get(webadr)

    print("========================================")
    # Test Case
    driver.find_element_by_class_name("typeahead_input").clear()
    driver.find_element_by_class_name("typeahead_input").send_keys(sites[site])
    driver.find_element_by_id("SUBMIT_THINGS_TO_DO").click()
    time.sleep(3)

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
        time.sleep(3)
        latest_review_id = driver.find_element_by_xpath("//div[@class='reviewSelector']").get_attribute("id")
        id_num = latest_review_id.split('_')[1]
        target_path_for_more_button = "#" + "review_" + id_num
        selector = target_path_for_more_button + " > div > div.ui_column.is-9 > div > div.wrap > \
        div.prw_rup.prw_reviews_text_summary_hsx > div > p > span"
        time.sleep(3)
        try:
            driver.find_element_by_css_selector(selector).click()
        except:
            pass
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        titles.extend([title.text for title in soup.find_all("span", {"class": "noQuotes"})])
        reviews.extend([review.text for review in soup.find_all("p", {"class": "partial_entry"})][:])
        len_this_page = len([title.text for title in soup.find_all("span", {"class": "noQuotes"})])

        for num_rate in range(len_this_page):
            if lang == 2:
                ratings.append(int(soup.find_all("div", {"class": "rating reviewItemInline"})[num_rate+2].find('span')\
                                   .get("class")[1][-2:-1]))
            else:
                ratings.append(int(soup.find_all("div", {"class": "rating reviewItemInline"})[num_rate].find('span') \
                                   .get("class")[1][-2:-1]))
            dates.append(soup.find_all("span", {"class": "ratingDate relativeDate"})[num_rate].get('title'))
        if i < last_page - 1:
            driver.find_element_by_xpath("//*[@id=\"taplc_location_reviews_list_0\"]/div[22]/div/span[2]").click()
        time.sleep(3)
    print("Crawling Completed: ", sites[site])
    print("========================================")
    ta_df = pd.DataFrame({'title': titles, 'review': reviews, 'rating': ratings, 'dates': dates})
    ta_df.to_csv('./data/' + sites[site] + '.csv', encoding='utf-8')
