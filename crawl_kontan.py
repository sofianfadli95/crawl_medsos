# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 09:39:22 2018

@author: bobby.christian
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


def searching(katakunci,loop):
    querya = "https://search.kontan.co.id/main/cari_news/"
    queryb = katakunci
    queryc = "/"
    queryd = "/#content_news"
    return str(querya)+str(queryb)+str(queryc)+str(loop)+str(queryd)

halaman = 7    #jumlah halaman yang mau dibuka
data = 20      #jumlah berita per halaman, default = 20
berita = 20     #jumlah berita yang mau dibaca

def scrap_kontan(halaman,data,katakunci):
    for counting in range(halaman): #looping jumlah page berita, untuk range(6) maka dari 0 - 5
        try : 
            now = datetime.datetime.now()
            loop = (counting)*20
            if loop == 0 :
                loop = ""
                queryh = urllib.request.urlopen(searching(katakunci,loop))
                souping = bs.BeautifulSoup(queryh,'lxml')
                waktus = now.strftime("%d-%m-%Y %H:%M")
                k = 0
                dummy8 = []
                dummy11 = []
                dummy12 = []
                
                print(waktus)
                while k < data : #jumlah berita dalam 1 halaman page ada 20
                    dummy7 = souping.select('h1')[k].text.strip()
                    #time.sleep(0.5)
                    for links in souping.find_all(class_ = "linkto-orange hrf-gede mar-r-5"): #mengambil link berita
                        linker = links.a.get('href')
                        dummy8.append(linker) #menyimpan link berita
        
                    dummy11.clear()
                    queryi = urllib.request.urlopen(str("https:" + dummy8[k]))
                    lambsoup = bs.BeautifulSoup(queryi,'lxml') 
            
                    for title4 in lambsoup.find('div',{"class":"tmpt-desk-kon"}).find_all("p") :
                        dummy11.append(title4.text)
                        dummy12 = "\n".join(dummy11)
            
                    waktuberita = lambsoup.find('div',{"class":" fs14 ff-opensans font-gray"}) 
                    author = lambsoup.find('div',{"class":"fs13 font-gray ff-knowledge-l"}) 
                    
                    print("Link Berita : ", dummy8[k])
                    print("Judul Berita : ",dummy7)
                    print("\nHari/Tanggal dan Waktu : ",waktuberita.text)
                    print("Pengarang : ", author.text)
                    print("\nIsi Berita :","\n",dummy12)
            
                    k+=1
                    time.sleep(0.5)
        
        #judul berita = dummy7
        #link berita = dummy8
        #haritanggal = waktuberita
        #pengarang = author
        #isiberita = dummy12
        
        except Exception as e : 
            print(e)
        
time.sleep(0.1)
scrap_kontan(halaman,data,katakunci)
"""


