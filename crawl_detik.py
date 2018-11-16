# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 09:39:22 2018

@author: bobby.christian
"""

#detik.com

import bs4 as bs
import urllib.request
import time
import datetime

from bs4 import BeautifulSoup
import requests

import time
from datetime import datetime

from elasticsearch import Elasticsearch
import elastic_configuration as els
from concurrent.futures import ThreadPoolExecutor

from nlp_local import predictPolarity
from nlp_local import predictMood
from nlp_local import predictAspect
from nlp_local import predictIntensity
from nlp_local import entity_analysis

from DataPreprocessing import stemmer
from DataPreprocessing import stopword
from DataPreprocessing import _lookup_words
from DataPreprocessing import cleanSentences
from DataPreprocessing import cleaning_berita

import os

# os.chdir("/home/oracle/u01/crawl_medsos")

link_urls = []
pool = ThreadPoolExecutor(max_workers=10)

elastic_url = "192.168.83.133"
elastic_port = 9200

def searchdetik(katakunci, count):
    querya = "https://www.detik.com/search/searchnews?query="
    queryb = katakunci
    queryc = "&sortby=time&page="
    return str(querya)+str(queryb)+str(queryc)+str(count+1)

halaman = 10
berita = 9

def scrapping_detik(halaman, berita, katakunci):
    for count in range(halaman) :
        try : 
            now = datetime.now()
            # driver = webdriver.Chrome().get(searchdetik(katakunci))
            queryf = urllib.request.urlopen(searchdetik(katakunci, count))
            soup = bs.BeautifulSoup(queryf,'lxml')
            
            i = 0
            j = 0
            k = 0
            dummy3 = []
            dummy4 = []
            dummy5 = []
            dummy6 = []
            dummy7 = []
            
            waktu = now.strftime("%d-%m-%Y %H:%M")
            
            print(waktu)
            
            #Looping Supaya bisa tampilkan judul
            while i < berita :
                for title in soup.find('h2'):
                    dummy = soup.select('h2.title')[i].text.strip()
                    for links in soup.find_all('article'):
                        linker = links.a.get('href')
                        dummy3.append(linker)
                        time.sleep(0.5)             
                    print("Link : \n",dummy3[i])
                time.sleep(0.5)
                print("Judul : \n",dummy)
                i+=1
                      
                dummy4.clear()
                dummy6.clear()
                dummy7.clear()
                queryg = urllib.request.urlopen(str(dummy3[i]))
                chickensoup = bs.BeautifulSoup(queryg,'lxml')
                for title2 in chickensoup.find_all('div',{"class":"detail_wrap"}) :
                    for cari in title2.find_all('table',{"class":"linksisip"}) :
                        cari.decompose() 
                    for cari2 in title2.find_all('center'):
                        cari2.decompose()    
                    for cari3 in title2.find_all('div',{"class":"detail_tag"}):
                        cari3.decompose()
                    for cari4 in title2.find_all('strong') : 
                        cari4.decompose()
                    for cari5 in title2.find_all('div',{"class":"news_tag"}) :
                        cari5.decompose()
                    for cari6 in title2.find_all('script'):
                        cari6.decompose()
                    for cari7 in title2.find_all('div',{"class":"boxlr mt15"}):
                        cari7.decompose()
                    for cari8 in title2.find_all('p'):
                        cari8.decompose()
                    for cari9 in title2.find_all('style'):
                        cari9.decompose()
                    for cari10 in title2.find_all('div',{"class":"term_ugc mb20"}):
                        cari10.decompose()
                                   
                    dummy4.append(title2.text)
                    dummy5 = "\n".join(dummy4) #untuk menggabungkan berita dari tiap paragraf
                
                time.sleep(0.5)
                
                # urls = dummy3.split("/")
                # id_berita = urls[4]
                # print("ID berita : {}".format(id_berita))
                
                for waktuberita in chickensoup.find('div',{"class":"date"}) : 
                    dummy6.append(waktuberita)
                    print("\nHari/Tanggal dan Waktu : ",waktuberita)
                    
                for author in chickensoup.find('div',{"class" : "author"}) : 
                    dummy7.append(author)
                    print("Pengarang : ", author)
                print("\nIsi Berita :",dummy5)
                # Judul Berita : dummy
                # linkberita : dummy3
                # haritanggal : waktuberita
                # pengarang = author
                # isiberita : dummy5
                text = _lookup_words(dummy5)
                text = stemmer.stem(text)
                text = stopword.remove(text)
                polarity, polarity_score = predictPolarity(cleanSentences((text)))
                mood, mood_score = predictMood((text))
                aspect, aspect_score = predictAspect(cleanSentences((text)))
                intensity_score = predictIntensity(cleanSentences((text)))
                # Ada baiknya entity analysis jangan membuang stopwords, dikarenakan ada nama-nama perusahaan
                # yang riskan apabila kata-katanya dibuang
                person, company, eventNegatif, country, city, lat_city, long_city = entity_analysis(dummy5)
        
                es = Elasticsearch([{'host': elastic_url, 'port': elastic_port}])         
                es.index(index='sentiment-index-news',
                            doc_type="news-type",
                            body={  
                                    "Author" : author,
                                    # "ID Berita" : id_berita,
                                    "Judul Berita" : dummy,
                                    "Tanggal Berita" : waktuberita,
                                    "Isi Berita" : dummy5,
                                    "Urls" : dummy3,
                                    "Keyword" : katakunci,
                                    'News Source' : "Detik",
                                    'Datetime' : datetime.utcnow(),
                                    'Polarity' : polarity,
                                    'Polarity Score' : polarity_score,
                                    'Mood' : mood,
                                    'Mood Score' : mood_score,
                                    'Aspect' : aspect,
                                    'Aspect Score' : aspect_score,
                                    'Intensity Score' : intensity_score,
                                    'Person' : person,
                                    'Company' : company,
                                    'Event Negatif' : eventNegatif,
                                    'Country' : country,
                                    'City' : city,
                                    'Lattitude' : lat_city,
                                    'Longitude' : long_city
                                        #"created_at" : tweet["created_at"].encode("ascii",errors="replace").decode("utf8")
                                        })
    
            time.sleep(1)
            
            #while k < baca :
            #    linkberita = dummy3[k]
            #    judul = dummy[k]
            #    haritanggal = waktuberita
            #    pengarang = author
            #    isiberita = dummy5[k]
    
    
        except Exception as e:
            print(e)

scrapping_detik(halaman, berita, "jokowi")
    


