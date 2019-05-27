import requests
import urllib.request
from urllib.request import Request, urlopen


# 
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
collections = db['profile']

def get_name_boy():
    req = Request('https://names.mongabay.com/male_names_alpha.htm', headers={'User-Agent': 'Mozilla/5.0'})
    name_boy_webpage = urlopen(req).read()
    soup_name_boy = BeautifulSoup(name_boy_webpage ,'html.parser')
    all_name_boys = soup_name_boy.find('table',attrs={'id':'myTable'}).find_all('tr')[1:]
    list_name_all_boy = []
    for all_name_boy in all_name_boys:
        name_all = all_name_boy.find('td').get_text()
        list_name_all_boy.append(name_all)
    return list_name_all_boy
# print(get_name_boy())

def get_name_girl():
    req = Request('https://names.mongabay.com/female_names_alpha.htm', headers={'User-Agent': 'Mozilla/5.0'})
    name_girl_webpage = urlopen(req).read()
    soup_name_girl = BeautifulSoup(name_girl_webpage ,'html.parser')
    all_name_girls = soup_name_girl.find('table',attrs={'id':'myTable'}).find_all('tr')[1:]
    list_name_all_girl = []
    for all_name_girl in all_name_girls:
        name_all = all_name_girl.find('td').get_text()
        list_name_all_girl.append(name_all)
    return list_name_all_girl
# print(get_name_girl())

def get_surname():
    link_alls = ['','1','2','5','8','12','16']
    list_all_surname = []
    for link_all in link_alls:
        req = Request(f'https://names.mongabay.com/most_common_surnames{link_all}.htm', headers={'User-Agent': 'Mozilla/5.0'})
        surname_webpage = urlopen(req).read()
        surname = BeautifulSoup(surname_webpage ,'html.parser')
        all_surnames = surname.find('table',attrs={'id':'myTable'}).find_all('tr')[1:]
        for all_surname in all_surnames:
            surname_all = all_surname.find('td').get_text()
            list_all_surname.append(surname_all)
    return list_all_surname
# print(get_surname())
# print(len(get_surname()))

def get_photo():
    list_name_category = ['girl','boy','people']
    list_all_photo = []
    for page in list_name_category:
        req = Request(f'https://pixabay.com/images/search/{page}/', headers={'User-Agent': 'Mozilla/5.0'})
        r = urlopen(req).read()
        soup = BeautifulSoup(r ,'html.parser')
        all_page = soup.find('form',attrs={'class':'add_search_params pure-form hide-xs hide-sm hide-md'}).get_text().split('/ ')[1]
        print('all page = ',all_page)
        # print('---------------')
        for element in range(1,int(all_page)):
            req = Request(f'https://pixabay.com/images/search/people/?pagi={element}', headers={'User-Agent': 'Mozilla/5.0'})
            print('this is page:',element)
            r = urlopen(req).read()
            soup = BeautifulSoup(r ,'html.parser')
            all_photos = soup.find_all('div',attrs={'class':'item'})
            for all_photo in all_photos:
                try:
                    photo = all_photo.find('img').get('src')
                    if photo != '/static/img/blank.gif':
                        list_all_photo.append(photo)
                except:
                    print('error')
    return list_all_photo
# print(get_photo())
# print(len(get_photo()))

def email_password():
    list_name_girl = get_name_girl()
    list_name_boy = get_name_boy()
    list_surname = get_surname()
    list_photo = get_photo()
    all_name = list_name_girl + list_name_boy + list_name_girl + list_name_boy + list_name_girl + list_name_boy + list_name_girl + list_name_boy
    for element in range(0,len(list_photo)):
        email = f'{all_name[element].lower()}.{list_surname[element].lower()}@gmail.com'
        password = f'S9/{all_name[element].lower()}{list_surname[element].lower()}'
        print(email)
        print(password)
        dict_profile = {
            'name':all_name[element],
            'surname':list_surname[element],
            'email':email,
            'password':password,
            'photo':list_photo[element]
        }
        try:
            allData = {'MacthID':email,'api': dict_profile}
            query = {"MacthID":email}
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
print(email_password())



