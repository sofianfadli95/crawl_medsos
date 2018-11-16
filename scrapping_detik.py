# -*- coding: utf-8 -*-
"""
Created on Tue May  1 14:40:17 2018

@author: sofyan.fadli

Ini adalah program untuk scrapping berita dari website detik.com
Kita dapat memasukkan search query sesuai dengan topik yg kita inginkan

"""

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

os.chdir("/home/oracle/u01/crawl_medsos")

# Step 1 - Mendapatkan semua alamat urls yang ingin kita scrapping
# Simpan url yg didapatkan ke dlm array link_urls

link_urls = []
pool = ThreadPoolExecutor(max_workers=10)

elastic_url = "127.0.0.1"
elastic_port = 9200

def scrap_detik_isi(element,query):
    # Result berfungsi utk menampung isi berita sementara apabila isi beritanya berbentuk list
    result = []
    # Print alamat url yg didapatkan
    print(element)
    urls = element
    urls = urls.split("/")
                        
    try:
        # Mengirim request ke link yg kita tuju
        source = requests.get(element).text
        time.sleep(3)
        # Scrapping dgn menggunakan BeautifulSoup
        soup = BeautifulSoup(source, 'lxml')
        author = soup.find('div', class_='author')
        if not author:
            author = soup.find('span', class_='author')
        # Mendapatkan nama author dari berita
        author = author.text
        print("Author : {}".format(author))
        # Mendapatkan id dari berita
        id_berita = urls[4]
        print("ID berita : {}".format(id_berita))
        # Mendapatkan judul dari berita
        judul = soup.find('div', class_='jdl').h1.text
        print("Judul : {}".format(judul))
        tanggal = soup.find('div', class_='date')
        if not tanggal:
            tanggal = soup.find('span', class_='date')
        # Mendapatkan tanggal dari berita
        tanggal = tanggal.text
        print("Tanggal : {}".format(tanggal))
        isi_berita = soup.find('div', class_='detail_text')
        text = isi_berita.text
        # isi_berita_2 = isi_berita.find_all("p")
        """
        for element3 in isi_berita_2:
            result.append(element3.text)
                    
        text_ori = "\n".join(result)
        """
        text = cleaning_berita(text)
        text = _lookup_words(text)
        text = stemmer.stem(text)
        text = stopword.remove(text)
                    
        polarity, polarity_score = predictPolarity(cleanSentences((text)))
        mood, mood_score = predictMood((text))
        aspect, aspect_score = predictAspect(cleanSentences((text)))
        intensity_score = predictIntensity(cleanSentences((text)))
        # Ada baiknya entity analysis jangan membuang stopwords, dikarenakan ada nama-nama perusahaan
        # yang riskan apabila kata-katanya dibuang
        person, company, eventNegatif, country, city, lat_city, long_city = entity_analysis(isi_berita.text)

        es = Elasticsearch([{'host': elastic_url, 'port': elastic_port}])         
        es.index(index='sentiment-index-news',
                    doc_type="news-type",
                    body={  
                            "Author" : author,
                            "ID Berita" : id_berita,
                            "Judul Berita" : judul,
                            "Tanggal Berita" : tanggal,
                            "Isi Berita" : "\n".join(result),
                            "Urls" : element,
                            "Keyword" : query,
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
    except Exception as e:
        print(e)

# Function ini berfungsi utk mengambil seluruh url yang muncul pada saat dilakukan pencarian
# Variabel query adalah keyword yang digunakan utk melakukan pencarian berita        
def scrap_detik_url(query):
    # query = set(line.strip().lower() for line in io.open(OUR_PATH + '/keyword/query_politik.txt'))
    try:
            source = requests.get("https://www.detik.com/search/searchall?query={}".format(query)).text
            time.sleep(5)
            soup = BeautifulSoup(source, 'lxml')
            
            for article in soup.find_all("article"):
                #print(article.prettify())
                try:
                    judul = article.h2.text
                    print("Title : {}".format(judul))
                except Exception as e:
                    judul = None
                #print(judul)
            
                try:
                    link = article.a['href']
                    print("Link : {}".format(link))
                    link_urls.append(link)
                except Exception as e:
                    link = None
                #print(link)
                print()
                print("Link berita berhasil ditambahkan...")
            
            # Ini untuk scrapping ke halaman selanjutnya
            for i in range(2,10):
                
                source = requests.get("https://www.detik.com/search/searchall?query={}&sortby=time&page={}".format(query,i)).text
                time.sleep(5)
                soup = BeautifulSoup(source, 'lxml')
                
                for article in soup.find_all("article"):
                    #print(article.prettify())
                    try:
                        judul = article.h2.text
                        print("Title : {}".format(judul))
                    except Exception as e:
                        judul = None
                    #print(judul)
                
                    try:
                        link = article.a['href']
                        print("Link : {}".format(link))
                        link_urls.append(link)
                    except Exception as e:
                        link = None
                    #print(link)
                    print()
                    print("Link berita berhasil ditambahkan...")
            
            # Step 2 - Setelah kita mendapatkan alamat-alamat url yg akan kita scrapping
            # Selanjutnya kita men-generate masing-masing url utk kita scrapping
            
            for element in link_urls:
            #Works if the file is in the same folder, 
            # Otherwise include the full path
                pool.submit(scrap_detik_isi,element,query)
                try:
                    link_urls.remove(element)
                except Exception as e:
                    print(e)
                print("Link berita berhasil di-scrapping...")
    except ConnectionError:
        print(5)
        raise

# scrap_detik_url("jokowi")

