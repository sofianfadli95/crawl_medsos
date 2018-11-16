# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 10:09:43 2018

@author: CS
"""

from nltk.tokenize import word_tokenize

import io

# Path dimana kita meletakkan seluruh codingan yg kita buat
OUR_PATH = "."

# Angka menunjukkan seberapa besar tingkat positif maupun negatif dari kata-kata tersebut
# Inisialisasi dataset untuk penilaian polarity 
neg_words = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/polarity/neg.txt', encoding="utf8"))
neg_words_2 = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/polarity/neg_2.txt', encoding="utf8"))
neg_words_3 = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/polarity/neg_3.txt', encoding="utf8"))

pos_words = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/polarity/pos.txt', encoding="utf8"))
pos_words_2 = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/polarity/pos_2.txt', encoding="utf8"))
pos_words_3 = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/polarity/pos_3.txt', encoding="utf8"))

# Inisialisasi dataset untuk penilaian mood 
pos_mood = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/mood/happy.txt', encoding="utf8"))
pos_mood_2 = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/mood/happy_2.txt', encoding="utf8"))

neg_mood = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/mood/sad.txt', encoding="utf8"))
neg_mood_2 = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/mood/sad_2.txt', encoding="utf8"))

# Inisialisasi dataset untuk penilaian aspect 
pos_aspect = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/aspect/pos.txt', encoding="utf8"))
pos_aspect_2 = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/aspect/pos_2.txt', encoding="utf8"))

neg_aspect = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/aspect/neg.txt', encoding="utf8"))
neg_aspect_2 = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/aspect/neg_2.txt', encoding="utf8"))

# Inisialisasi dataset untuk penilaian aspect
intensity = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/intensity/intensity.txt', encoding="utf8"))
intensity_2 = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/intensity/intensity_2.txt', encoding="utf8"))
intensity_3 = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/intensity/intensity_3.txt', encoding="utf8"))

b_company = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/dictionary_entity/company.txt', encoding="utf8"))
b_person = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/dictionary_entity/person.txt', encoding="utf8"))

kata_negasi = {"tidak","bukan","kurang","belum","jangan"}

# Tambahan entity person dari Stanly
for line in io.open(OUR_PATH + '/Dataset/dictionary_entity/person_stanly.txt', encoding="utf8"):
    b_person.add(line.strip().lower())
    
# Tambahan entity perusahaan dari Stanly 
for line in io.open(OUR_PATH + '/Dataset/dictionary_entity/perusahaan.txt', encoding="utf8"):
    b_company.add(line.strip().lower())

list_event_negatif = set(line.strip().lower() for line in io.open(OUR_PATH + '/Dataset/dictionary_entity/eventNegatif.txt', encoding="utf8"))

# Inisialisasi data city beserta dengan koordinat lokasinya
with io.open(OUR_PATH + "/Dataset/Location2.txt", 'r', encoding="utf-8", errors = 'ignore') as f:
    list_city = []
    loc_dict = {}
    for line in f:
        items = line.split("\t")
        key, values1, values2 = items[0].lower() , items[1], items[2]
        loc_dict[key.lower()] = { "lattitude" : values1.replace("\n",""), "longitude" : values2.replace("\n","") }
        list_city.append(key)
    list_city = set(list_city)

# Inisialisasi data country beserta dengan nama ibukotanya
with io.open(OUR_PATH + "/Dataset/dictionary_entity/country.txt", 'r', encoding="utf-8", errors = 'ignore') as f:
    list_country = []
    for line in f:
        items = line.split("\t")
        key = items[0].lower()
        list_country.append(key.replace("\n",""))
    list_country = set(list_country)

def create_ngrams(data):
    """
    Function ini apabila dipanggil akan membuat ngrams level 1, 2, dan 3
    """
    ngrams_2 = []
    ngrams_3 = []
    
    words = word_tokenize(data.lower())
    # Membuat n-gram level 2
    for i in range(len(words)-2):
        gram = " ".join(words[i:i+2])
        ngrams_2.append(gram)
        
    for i in range(len(words)-3):
        gram = " ".join(words[i:i+3])
        ngrams_3.append(gram)
    
    return words, ngrams_2, ngrams_3

def scoring_words(pos_score, neg_score, n_pos, n_neg, words, score, dict_neg, dict_pos):
    """
    Ini adalah function untuk menscoring suatu kalimat berdasarkan kata-katanya
    Aturan penilaian scoring :
    +1 : Apabila kata-katanya sedikit positif
    +3 : Apabila kata-katanya positif
    +5 : Apabila kata-katanya sangat positif
    -1 : Apabila kata-katanya sedikit negatif
    -3 : Apabila kata-katanya negatif
    -5 : Apabila kata-katanya sangat negatif
    Data yang diinputkan berupa kumpulan kata-kata atau frase yang disimpan dalam file text
    
    """
    for i in range(len(words)):
        if words[i] in dict_neg:
            if (i != 0):
                # Mengecek apakah ada kata negasi
                if words[i-1] in kata_negasi:
                    pos_score += score
                    n_pos += 1
                else:
                    neg_score += score
                    n_neg += 1
        elif words[i] in dict_pos:
            if (i != 0):
                # Mengecek apakah ada kata negasi
                if words[i-1] in kata_negasi:
                    neg_score += score
                    n_neg += 1
                else:
                    pos_score += score
                    n_pos += 1
    return pos_score, neg_score, n_pos, n_neg

def scoring_ngrams(pos_score, neg_score, n_pos, n_neg, ngrams, score, dict_neg, dict_pos):
    """
    Ini adalah function untuk menscoring suatu kalimat berdasarkan kata-katanya
    Aturan penilaian scoring :
    +1 : Apabila kata-katanya sedikit positif
    +3 : Apabila kata-katanya positif
    +5 : Apabila kata-katanya sangat positif
    -1 : Apabila kata-katanya sedikit negatif
    -3 : Apabila kata-katanya negatif
    -5 : Apabila kata-katanya sangat negatif
    Data yang diinputkan berupa kumpulan kata-kata atau frase yang disimpan dalam file text
    
    """
    # Cek per 2 kata
    for i in range(len(ngrams)):
        # Cek apakah ada frase atau idiom
        # negatif level 1 di element ngrams_2
        if ngrams[i] in dict_neg:
            if (i != 0):
                # Mengecek apakah ada kata negasi
                for word in kata_negasi:
                    if word in ngrams[i-1]:
                        pos_score += score
                        n_pos += 1
                    else:
                        neg_score += score
                        n_neg += 1
        # Cek apakah ada frase atau idiom
        # positif level 1 di element ngrams_2
        elif ngrams[i] in dict_pos:
            if (i != 0):
                # Mengecek apakah ada kata negasi
                for word in kata_negasi:
                    if word in ngrams[i-1]:
                        neg_score += 1
                        n_neg += 1
                    else:
                        pos_score += 1
                        n_pos += 1
    return pos_score, neg_score, n_pos, n_neg
    
    
def predictPolarity(data):
    # Inisialisasi variabel utk menampung score positif dan negatif
    pos_score = 0
    neg_score = 0
    # Inisialisasi jumlah kata positif dan negatif yg terdeteksi
    n_pos = 0
    n_neg = 0
    # Inisialisasi bobot nilai pembagi utk scoring
    final_score = 0
    words, ngrams_2, ngrams_3 = create_ngrams(data)
    
    # Cek kata per kata
    # Cek apakah ada kata-kata negatif / positif level 1
    # Level 1 kita berikan nilai score sebesar 1
    pos_score, neg_score, n_pos, n_neg = scoring_words(pos_score, neg_score, n_pos, n_neg, words, score=1, dict_neg=neg_words, dict_pos=pos_words)
    # Cek apakah ada kata-kata negatif / positif level 2
    # Level 2 kita berikan nilai score sebesar 3
    pos_score, neg_score, n_pos, n_neg = scoring_words(pos_score, neg_score, n_pos, n_neg, words, score=3, dict_neg=neg_words_2, dict_pos=pos_words_2)
    # Cek apakah ada kata-kata negatif / positif level 3
    # Level 2 kita berikan nilai score sebesar 5
    pos_score, neg_score, n_pos, n_neg = scoring_words(pos_score, neg_score, n_pos, n_neg, words, score=5, dict_neg=neg_words_3, dict_pos=pos_words_3)
    
    # Cek menggunakan n-grams
    # Cek apakah ada kata-kata negatif / positif level 1
    # Level 1 kita berikan nilai score sebesar 1
    pos_score, neg_score, n_pos, n_neg = scoring_ngrams(pos_score, neg_score, n_pos, n_neg, ngrams_2, score=1, dict_neg=neg_words, dict_pos=pos_words)
    # Cek apakah ada kata-kata negatif / positif level 2
    # Level 2 kita berikan nilai score sebesar 3
    pos_score, neg_score, n_pos, n_neg = scoring_ngrams(pos_score, neg_score, n_pos, n_neg, ngrams_2, score=3, dict_neg=neg_words_2, dict_pos=pos_words_2)
    # Cek apakah ada kata-kata negatif / positif level 3
    # Level 2 kita berikan nilai score sebesar 5
    pos_score, neg_score, n_pos, n_neg = scoring_ngrams(pos_score, neg_score, n_pos, n_neg, ngrams_2, score=5, dict_neg=neg_words_3, dict_pos=pos_words_3)
            
    if neg_score > pos_score:
        polarity = "negatif"
        final_score = n_neg
    elif pos_score > neg_score:
        polarity = "positif"
        final_score = n_pos
    else:
        polarity = "netral"
    
    # Menghitung score polarity
    if (final_score) != 0 :
        polarity_score = ((pos_score - neg_score) / (final_score * 5)) * 3
    else:
        polarity_score = 0
    return polarity, polarity_score

def predictMood(data):
    pos_score = 0
    neg_score = 0
    n_pos = 0
    n_neg = 0
    final_score = 0
    words, ngrams_2, ngrams_3 = create_ngrams(data)

    # Cek kata per kata
    # Cek apakah ada kata-kata mood sedih / senang level 1
    # Level 1 kita berikan nilai score sebesar 1
    pos_score, neg_score, n_pos, n_neg = scoring_words(pos_score, neg_score, n_pos, n_neg, words, score=1, dict_neg=neg_mood, dict_pos=pos_mood)
    # Cek apakah ada kata-kata mood sedih / senang level 2
    # Level 2 kita berikan nilai score sebesar 3
    pos_score, neg_score, n_pos, n_neg = scoring_words(pos_score, neg_score, n_pos, n_neg, words, score=3, dict_neg=neg_mood_2, dict_pos=pos_mood_2)
    
    # Cek menggunakan n-grams
    # Cek apakah ada kata-kata mood sedih / senang level 1
    # Level 1 kita berikan nilai score sebesar 1
    pos_score, neg_score, n_pos, n_neg = scoring_ngrams(pos_score, neg_score, n_pos,  n_neg, ngrams_2, score=1, dict_neg=neg_mood, dict_pos=pos_mood)
    # Cek apakah ada kata-kata mood sedih / senang level 2
    # Level 2 kita berikan nilai score sebesar 3
    pos_score, neg_score, n_pos, n_neg = scoring_ngrams(pos_score, neg_score, n_pos, n_neg, ngrams_2, score=3, dict_neg=neg_mood_2, dict_pos=pos_mood_2)
            
    if neg_score > pos_score:
        mood = "sad"
        final_score = n_neg
    elif pos_score > neg_score:
        mood = "happy"
        final_score = n_pos
    else:
        mood = "netral"
        
    if (final_score) != 0 :
        mood_score = ((pos_score - neg_score) / (final_score * 3)) * 3
    else:
        mood_score = 0
    return mood, mood_score

def predictAspect(data):
    pos_score = 0
    neg_score = 0
    n_pos = 0
    n_neg = 0
    final_score = 0
    words, ngrams_2, ngrams_3 = create_ngrams(data)

    # Cek kata per kata
    # Cek apakah ada kata-kata aspect positif / negatif level 1
    # Level 1 kita berikan nilai score sebesar 1
    pos_score, neg_score, n_pos, n_neg = scoring_words(pos_score, neg_score, n_pos, n_neg, words, score=1, dict_neg=neg_aspect, dict_pos=pos_aspect)
    # Cek apakah ada kata-kata aspect positif / negatif level 2
    # Level 2 kita berikan nilai score sebesar 3
    pos_score, neg_score, n_pos, n_neg = scoring_words(pos_score, neg_score, n_pos, n_neg, words, score=3, dict_neg=neg_aspect_2, dict_pos=pos_aspect_2)
    
    # Cek menggunakan n-grams
    # Cek apakah ada kata-kata aspect positif / negatif level 1
    # Level 1 kita berikan nilai score sebesar 1
    pos_score, neg_score, n_pos, n_neg = scoring_ngrams(pos_score, neg_score, n_pos,  n_neg, ngrams_2, score=1, dict_neg=neg_aspect, dict_pos=pos_aspect)
    # Cek apakah ada kata-kata aspect positif / negatif level 2
    # Level 2 kita berikan nilai score sebesar 3
    pos_score, neg_score, n_pos, n_neg = scoring_ngrams(pos_score, neg_score, n_pos, n_neg, ngrams_2, score=3, dict_neg=neg_aspect_2, dict_pos=pos_aspect_2)
            
    if neg_score > pos_score:
        aspect = "negatif"
        final_score = n_neg
    elif pos_score > neg_score:
        aspect = "positif"
        final_score = n_pos
    else:
        aspect = "netral"
        
    if (final_score) != 0 :
        aspect_score = ((pos_score - neg_score) / (final_score * 3)) * 3
    else:
        aspect_score = 0
    return aspect, aspect_score

def predictIntensity(data):
    intensity_score = 0
    n_intensity = 0
    final_score = 0
    words, ngrams_2, ngrams_3 = create_ngrams(data)

    # Cek kata per kata
    for i in range(len(words)):
        if words[i] in intensity:
            intensity_score += 1
            n_intensity += 1
                    
        elif words[i] in intensity_2:
            intensity_score += 2
            n_intensity += 1
                
        elif words[i] in intensity_3:
            intensity_score += 3
            n_intensity += 1

    # Cek per 2 kata
    for i in range(len(ngrams_2)):
        if ngrams_2[i] in intensity:
            intensity_score += 1
            n_intensity += 1
                    
        elif ngrams_2[i] in intensity_2:
            intensity_score += 2
            n_intensity += 1
                
        elif ngrams_2[i] in intensity_3:
            intensity_score += 3
            n_intensity += 1
        
    if (final_score) != 0 :
        intensity_score = ((intensity_score) / (final_score * 3)) * 3
    else:
        intensity_score = 0
    return intensity_score

def entity_analysis(data):
    try:
        person = []
        company = []
        eventNegatif = []
        country = []
        location = []
        lat_city = []
        long_city = []
        
        words, ngrams_2, ngrams_3 = create_ngrams(data)
            
        # Check apakah ada Entity Person dalam kalimat
        # Step 1 - check kata per kata
        for element in words:
            # Jika element ada di dictionary person
            if element in b_person:
                print("Person : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array person
                if element not in person:
                    person.append(element)
        
        # Step 2 - check per dua kata
        for element in ngrams_2:
            # Jika element ada di dictionary person
            if element in b_person:
                print("Person : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array person
                if element not in person:
                    person.append(element)
        
        # Step 3 - Check per tiga kata
        for element in ngrams_3:
            # Jika element ada di dictionary person
            if element in b_person:
                print("Person : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array person
                if element not in person:
                    person.append(element)
                                
        # Check apakah ada Entity Company dalam kalimat
        # Step 1 - check kata per kata
        for element in words:
            # Jika element ada di dictionary company
            if element in b_company:
                print("Company : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in company:
                    company.append(element)
        
        # Step 2 - check per dua kata
        for element in ngrams_2:
            # Jika element ada di dictionary company
            if element in b_company:
                print("Company : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in company:
                    company.append(element)
                    
        # Step 3 - Check per tiga kata
        for element in ngrams_3:
            # Jika element ada di dictionary company
            if element in b_company:
                print("Company : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in company:
                    company.append(element)
                                
        # Check apakah ada Entity Country dalam kalimat
        # Step 1 - check kata per kata
        for element in words:
            # Jika element ada di dictionary list_country
            if element in list_country:
                print("Country : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in country:
                    country.append(element)
        
        # Step 2 - check per dua kata
        for element in ngrams_2:
            # Jika element ada di dictionary list_country
            if element in list_country:
                print("Country : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in country:
                    country.append(element)
        
        # Step 3 - Check per tiga kata
        for element in ngrams_3:
            # Jika element ada di dictionary list_country
            if element in list_country:
                print("Country : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in country:
                    country.append(element)
                            
        # Check apakah ada Entity Event Negatif dalam kalimat
        # Step 1 - check kata per kata
        for element in words:
            # Jika element ada di dictionary event_negatif
            if element in list_event_negatif:
                print("Event Negatif : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in eventNegatif:
                    eventNegatif.append(element)
        
        # Step 2 - check per dua kata
        for element in ngrams_2:
            # Jika element ada di dictionary event_negatif
            if element in list_event_negatif:
                print("Event Negatif : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in eventNegatif:
                    eventNegatif.append(element)
        
        # Step 3 - Check per tiga kata
        for element in ngrams_3:
            # Jika element ada di dictionary event_negatif
            if element in list_event_negatif:
                print("Event Negatif : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in eventNegatif:
                    eventNegatif.append(element)
            
        # Check apakah ada Entity Location dalam kalimat
        # Step 1 - check kata per kata
        for element in words:
            # Jika element ada di dictionary list_city
            if element in list_city:
                print("Location : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in location:
                    location.append(element)
        
        # Step 2 - check per dua kata
        for element in ngrams_2:
            # Jika element ada di dictionary list_city
            if element in list_city:
                print("Location : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in location:
                    location.append(element)
        
        # Step 3 - Check per tiga kata
        for element in ngrams_3:
            # Jika element ada di dictionary list_city
            if element in list_city:
                print("Location : {}".format(element))
                # Check terlebih dahulu apakah element sudah
                # terdapat di array company
                if element not in location:
                    location.append(element)
                    
        # Mapping location ke lattitude dan longitudenya
        for w in location:
            if w in loc_dict.keys():
                lat_city.append(loc_dict[w]["lattitude"])
                long_city.append(loc_dict[w]["longitude"])
            # Jika tidak ada, maka buang kata tersebut
            else:
                location.remove(w)
        
        return person, company, eventNegatif, country, location, lat_city, long_city
    except Exception as e:
        print(e)
        raise
