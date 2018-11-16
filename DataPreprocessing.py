# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:03:12 2018

@author: sofyan.fadli
"""

"""

Codingan ini berisi fungsi yang digunakan untuk melakukan
data preprocessing...

"""

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

import re

import io

# Path dimana kita meletakkan seluruh codingan yg kita buat
OUR_PATH = "."

# Inisialisasi fungsi Stemmer bahasa Indonesia
# Stemmer untuk membuang semua imbuhan dan mendapatkan kata dasarnya
factory_stem = StemmerFactory()
stemmer = factory_stem.create_stemmer()

more_stopword = []
factory_stop = StopWordRemoverFactory()

for line in io.open(OUR_PATH + '/Dataset/stopwords/stopwords.txt', 'r', encoding="utf8"):
    more_stopword.append(line.strip().lower())
    
stopwords = factory_stop.get_stop_words()

# Tambahkan Stopword Baru
data = factory_stop.get_stop_words()+more_stopword
stopword = factory_stop.create_stop_word_remover()

lookup_dict = {}
# Dictionary utk lemmatize
with open(OUR_PATH + "/Dataset/formalizationDict.txt", 'r', encoding="utf8") as f:
    for line in f:
        items = line.split()
        key, values = items[0], items[1:]
        lookup_dict[key] = ' '.join(values)

# Fungsi untuk menimpa kata-kata yang salah / alay dengan kata
# yang terdapat pada formalizationDict
# Contoh : gpp => tidak apa-apa
#          egp => emang saya pikirin
def _lookup_words(input_text):
    words = input_text.split() 
    new_words = []
    new_text = ""
    for word in words:
        if word.lower() in lookup_dict:
            word = lookup_dict[word.lower()]
        new_words.append(word)
        new_text = " ".join(new_words) 
    return new_text

# Removes punctuation, parentheses, question marks, etc., and leaves only alphanumeric characters
strip_special_chars = re.compile("[^A-Za-z ]+")
def cleanSentences(string):
    string = string.lower().replace("<br />", " ")
    return re.sub(strip_special_chars, " ", string.lower())

# print(stemmer.stem("menindaklanjuti"))
def cleaning_berita(sent):
    sent = sent.replace("googletag.cmd.push(function() { googletag.display('div-gpt-ad-1523548302020-0'); });","")
    sent = sent.replace("<!--// <![CDATA[","")
    sent = sent.replace("OA_show('newstag');","")
    sent = sent.replace("// ]]> -->","")
    sent = sent.replace("<!--// <![CDATA[","")
    sent = sent.replace("OA_show('hiddenquiz');","")
    sent = sent.replace("// ]]> -->","")
    sent = sent.split('-')
    sent = "-".join(sent[1:])
    sent = sent.replace('\r', '')
    sent = sent.replace('\n', '')
    sent = sent.replace('\t', '')
    sent = sent.replace('\\n', '')
    sent = sent.replace('\\r', '')
    sent = sent.replace('\\t', '')
    return sent
