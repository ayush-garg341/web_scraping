import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import requests

driver = webdriver.Chrome(r'C:\Users\shivam\Downloads\chromedriver.exe')
driver.get('https://www.naukri.com')
driver.find_element_by_xpath('//*[@id="qsbClick"]/span[1]').click()
SearchBar = driver.find_element_by_xpath('//*[@id="skill"]/div[1]/div[2]/input')
filename = r"E:\pdftotext\xml_data.csv"
file = open(filename, encoding = 'ISO-8859-1')
reader = csv.reader(file)
query = 'ASP.NET, C#, SQL2012, jQuery, MVC, Window Phone'
SearchBar.send_keys(query)
driver.find_element_by_xpath('//*[@id="qsbFormBtn"]').click()
print(driver.current_url)
'''for rows in reader:
	query = rows[2]
	if len(query)!=0:
		SearchBar.send_keys(query)
		driver.find_element_by_xpath('//*[@id="qsbFormBtn"]').click()
		print(driver.current_url)
		time.sleep(5)'''