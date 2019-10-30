import requests
import urllib.request
from urllib.request import Request, urlopen
import urllib.request
from bs4 import BeautifulSoup
import re
import datetime
from time import time, mktime


req = Request('https://names.mongabay.com/male_names_alpha.htm', headers={'User-Agent': 'Mozilla/5.0'})
name_boy_webpage = urlopen(req).read()
soup_name_boy = BeautifulSoup(name_boy_webpage ,'html.parser')
all_name_boys = soup_name_boy.find('table',attrs={'id':'myTable'}).find_all('tr')[1:]
list_name_all_boy = []
for all_name_boy in all_name_boys:
    name_all = all_name_boy.find('td').get_text()
    list_name_all_boy.append(name_all)
print(list_name_all_boy)