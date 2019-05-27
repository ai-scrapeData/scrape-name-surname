import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import datetime
from time import time, mktime

import pymongo
from pymongo import MongoClient
uri = "mongodb://heroku_sgnt6qng:3b864au43jrrv6dqllicsi3mvk@ds261296.mlab.com:61296/heroku_sgnt6qng"
from time import time, mktime
timeStart = time()
client = MongoClient(uri)
db = client["heroku_sgnt6qng"]
collections = db['name_surname']


website_name = 'https://nameberry.com/popular_names/Nameberry'
r_name = urllib.request.urlopen(website_name).read()
soup_name = BeautifulSoup(r_name ,'html.parser')
all_name = soup_name.find_all('a',attrs={'class':'flex-1'})

website_surname = 'https://www.houseofnames.com/top-surnames.html'
r_surname = urllib.request.urlopen(website_surname).read()
soup_surname = BeautifulSoup(r_surname ,'html.parser')
all_surname = soup_surname.find_all('b')
for element in range(0,len(all_surname)):
    sex_type = 'girl'
    surname = all_surname[element].text.split(' ')[0]
    name_girl = all_name[element].get('href').split('/')[2]
    print('----------------------------------------------------------')
    print(f'{name_girl} {surname}')
    print(element)
    print('----------------------------------------------------------')
    dict_profile_girl = {
        'sex_type':sex_type,
        'name':name_girl,
        'surname':surname
    }
    try:
        allData = {'MacthID':element,'api': dict_profile_girl}
        query = {"MacthID":element}
        print(query)
        result = collections.find(query, {'_id': False})
        print(result.count())
        if result.count() == 0:
            print('Not found. inserting')
            collections.insert_one(allData)
        else:
            collections.replace_one(query, allData)
            print('Updated completed!')
    except:
        print('error try catch')
        
for element,element_man in zip(range(0,len(all_surname)),range(1001,2000)):
    sex_type = 'man'
    surname = all_surname[element].text.split(' ')[0]
    name_boy = all_name[element_man].get('href').split('/')[2]
    # print('----------------------------------------------------------')
    # print(f'{name_boy} {surname}')
    # print(element_man)
    # print('----------------------------------------------------------')
    dict_profile_boy = {
        'sex_type':sex_type,
        'name':name_boy,
        'surname':surname
    }
    try:
        allData = {'MacthID':element_man,'api': dict_profile_boy}
        query = {"MacthID":element_man}
        print(query)
        result = collections.find(query, {'_id': False})
        print(result.count())
        if result.count() == 0:
            print('Not found. inserting')
            collections.insert_one(allData)
        else:
            collections.replace_one(query, allData)
            print('Updated completed!')
    except:
        print('error try catch')

