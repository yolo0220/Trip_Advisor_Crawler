# -*- coding: utf-8 -*-
"""
Created on 7/19/17
Author: Jihoon Kim
"""

from selenium import webdriver


driver = webdriver.Chrome('/home/jihoon_kim/.ChromeDriver/chromedriver')
driver.implicitly_wait(3)

# access trip advisor page
driver.get("https://www.tripadvisor.co.kr/")
# access things to do page
driver.find_element_by_id("global-nav-attractions").click()

# Test Case for '경복궁'
driver.find_element_by_class_name("typeahead_input").send_keys('경복궁')
driver.find_element_by_id("SUBMIT_THINGS_TO_DO").click()