import requests
from bs4 import BeautifulSoup
import csv
import lxml
import feedparser
import pandas as pd
import re
from dateutil.parser import parse
import datetime
our_feeds = {'Tass': 'https://tass.ru/rss/v2.xml',
'Lenta.ru': 'https://lenta.ru/rss/',
'Vedomosty': 'https://www.vedomosti.ru/rss/news'} #пример словаря RSS-лент 
                                                                  #русскоязычных источников

f_all_news = 'allnews.csv' 
f_certain_news = 'certainnews.csv' #пример пути файла
f_today_news = 'today.csv'
f_today_certain_news = 'certaintodaynews.csv'

def check_url(url_feed): #функция получает линк на рсс ленту, возвращает        
# распаршенную ленту с помощью feedpaeser
    return feedparser.parse(url_feed)  
    
def getHeadlines(url_feed): #функция для получения заголовков новости
    headlines = []
    lenta = check_url (url_feed)
    for item_of_news in lenta['items']:
        headlines.append(item_of_news ['title'])
    return headlines
def getLinks(url_feed): #функция для получения ссылки на источник новости
    links = []
    lenta = check_url(url_feed)
    for item_of_news in lenta['items']:
        links.append(item_of_news ['link'])
    return links

def getDates(url_feed): #функция для получения даты публикации новости
    dates = []
    lenta = check_url(url_feed)
    for item_of_news in lenta['items']:
        dates.append(item_of_news ['published'])
    return dates
allheadlines = []
alllinks = []
alldates = []
# Прогоняем наши URL и добавляем их в наши пустые списки
for key,url in our_feeds.items():
    allheadlines.extend( getHeadlines(url) )
      
for key,url in our_feeds.items():
    alllinks.extend( getLinks(url) )
    
for key,url in our_feeds.items():
    alldates.extend( getDates(url) )

def write_all_news(all_news_filepath): #функция для записи всех новостей в .csv, 
# возвращает нам этот датасет
    header = ['Title','Links','Publication Date'] 

    with open(all_news_filepath, 'w', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        writer.writerow(i for i in header) 

        for a,b,c  in zip(allheadlines,
                            alllinks, alldates):
            writer.writerow((a,b,c))


        df = pd.read_csv(all_news_filepath)
            
    return df

def looking_for_certain_news(all_news_filepath, certain_news_filepath, target1): #функция для поиска, а затем записи
                #определенных новостей по таргета,
                #затем возвращает этот датасет
    df = pd.read_csv(all_news_filepath)
    
    result = df.apply(lambda x: x.str.contains(target1, na=False,
                                    flags = re.IGNORECASE, regex=True)).any(axis=1)

    new_df = df[result]
        
    new_df.to_csv(certain_news_filepath
                     ,sep = '\t', encoding='utf-8-sig')
        
    return new_df
def loking_for_today_news(news_filepath, today_news_filepath):
    df = pd.read_csv(news_filepath)
    today_date = datetime.date.today()
    str_date = today_date.strftime("%d %b %Y")
    result = df.apply(lambda x: x.str.contains(str_date,  na=False, 
                                     regex=True)).any(axis=1)
    new_df = df[result]
        
    new_df.to_csv(today_news_filepath
                     ,sep = '\t', encoding='utf-8-sig')
        
    return new_df
    
vector= input('Укажите теги: ')
vector = str(vector.strip())
write_all_news(f_all_news) #все новости
looking_for_certain_news(f_all_news, f_certain_news, vector)
loking_for_today_news(f_all_news, f_today_news)
loking_for_today_news(f_certain_news, f_today_certain_news)

def count(path):
    df = pd.read_csv(path)
    count_= len(df)
    print(count_)
    return(count_)
print('Общее число новостей: ')
count(f_all_news)
print('Число новостей на сегодня: ')
count(f_today_news)
print('Число новостей по тегу ', vector, ': ')
count(f_certain_news)
print('Число новостей по тегу ', vector, 'на сегодня: ')
count(f_today_certain_news)

#count (f_certain_news)
#count(f_today_news)
# name of csv file 





 
    
     