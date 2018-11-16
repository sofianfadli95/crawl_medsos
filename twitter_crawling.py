import requests
from requests_oauthlib import OAuth1
# import json
import twitter_credentials

# from urllib.parse import urlparse
#from kafka import KafkaProducer

import time
from datetime import datetime
from elasticsearch import Elasticsearch
import elastic_configuration as els

from nlp_local import predictPolarity
from nlp_local import predictMood
from nlp_local import predictAspect
from nlp_local import predictIntensity
from nlp_local import entity_analysis

from DataPreprocessing import stemmer
from DataPreprocessing import stopword
from DataPreprocessing import _lookup_words
from DataPreprocessing import cleanSentences

import preprocessor as p

# Path dimana kita meletakkan seluruh codingan yg kita buat
OUR_PATH = "."

#import logging
#logging.basicConfig(level=logging.DEBUG)

#Endpoints
url_rest = "https://api.twitter.com/1.1/search/tweets.json"
url_streaming = "https://stream.twitter.com/1.1/statuses/sample.json"

# create instance of elasticsearch
# es = Elasticsearch([{'host': '192.168.9.62', 'port': 9200}])

csv_head = ['Post ID','Screen Name', 'ID', "sentence", "Sentiment"]
params = {
'app_key': twitter_credentials.ckey,
'app_secret': twitter_credentials.csecret,
'oauth_token': twitter_credentials.atoken,
'oauth_token_secret':twitter_credentials.asecret
}

elastic_url = els.elastic_url
elastic_port = els.elastic_port

def get_tweets(querry, max_id = 0, post = {}):
    try:
            url_rest = "https://api.twitter.com/1.1/search/tweets.json"
            params = {'q' : querry, 'count' : 10, 'lang' : 'id', 'max_id': max_id}
            auth = OAuth1(twitter_credentials.ckey,twitter_credentials.csecret,twitter_credentials.atoken,twitter_credentials.asecret)
            result = requests.get(url_rest,params=params,auth=auth)
            for tweet in result.json()['statuses']:
                text = tweet['text'].encode("ascii",errors="replace").decode("utf8")
                text = p.clean(text)
                text = text.replace('\r', ' ')
                text = text.replace('\n', ' ')
                text = text.replace('\t', ' ')
                text = text.replace('\\n', ' ')
                text = text.replace('\\r', ' ')
                text_ori = text.replace('\\t', ' ')
                text = _lookup_words(text_ori)
                text = stopword.remove(text)
                text = stemmer.stem(text)
                
                polarity, polarity_score = predictPolarity(cleanSentences(((text))))
                mood, mood_score = predictMood((((text))))
                aspect, aspect_score = predictAspect(cleanSentences(((text))))
                intensity_score = predictIntensity(cleanSentences(((text))))
                person, company, eventNegatif, country, city, lat_city, long_city = entity_analysis(text_ori)
                
                es = Elasticsearch([{u'host': elastic_url, u'port': elastic_port}])
                es.index(index='sentiment-index-twitter',
                doc_type="test-type",
                body={
                        'Post ID' : tweet['id'],
                        'Account': tweet['user']['name'].encode("ascii",errors="replace").decode("utf8"),
                        'ID': tweet['user']['id_str'],
                        'Tweet Date' : tweet['created_at'],
                        'User Location': tweet['user']['location'],
                        'Message': tweet['text'].encode("ascii",errors="replace").decode("utf8"),
			#'Hastag' : tweet['entities']['hashtags']['text'].encode("ascii",errors="replace").decode("utf8"),
			'Hashtags' : [hashtag['text'] for hashtag in tweet['entities']['hashtags']],
                        'Followers' : tweet['user']['followers_count'],
                        #'Timestamp': tweet['timestamp_ms'],
                        #'Datetime' : datetime.now(),
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

                print("This is tweet : ",tweet)
                print("Type of tweet : ",type(tweet))
                #print("This is user_json : ",user_json)
                #print("Type of tweet : ",type(user_json))
                print("\n")
                max_id = tweet['id']
            if('next_results' not in result.json()['search_metadata']):
                print('next_result invalid')
                return post
                time.sleep(20)
            else:
                return get_tweets(querry, max_id,post)
    except KeyError:
        print("KeyError happens...")
        time.sleep(20)

#    return post

#dict_post = get_tweets('jokowi')

"""
while 1:
    connection = sqlite3.connect('./data.db')
    cursor = connection.cursor()
    row = cursor.execute(select_query)
    # query = set(line.strip().lower() for line in io.open(OUR_PATH + '/keyword/query_politik.txt'))
    for element in row:
        try:
            dict_post = get_tweets(element[0])
        except Exception as e:
            print(str(e))
            time.sleep(20)

"""
"""
openfile = open("tweet_all6.txt","a")

try:
    if dict_post :
        openfile.writelines(str(dict_post).encode("ascii",errors="replace").decode("utf8"))
        openfile.writelines('\n')
    openfile.close()
except KeyError:
    openfile.close()
"""

"""
#auth = auth = OAuth1(config.consumer_key,config.consumer_secret,config.access_token,config.access_secret)
#
#q = 'adira AND finance'
#
#params = {'q' : q, 'count' : 200, 'lang' : 'id', 'since_id': '926349041629196288'}
#
#results = requests.get(url_rest,params=params, auth=auth)
#print(len(results.json()))
##print(results.json()['search_metadata'])
##dicti = {}
##dicti = results.json()['search_metadata']['next_results']
##print(dicti)
##print(dicti.find("max_id"))
##min_indx = dicti.find("max_id")+7
##max_indx = dicti.find("&q=")
##print(dicti[min_indx:max_indx])
##print(dicti.find("&q="))
##print(results.json()['statuses'])
#for tweet in results.json()['statuses']:
##    print(tweet['created_at'])
#    with open("tweet_save.csv","a") as csv_open:
#        writer = csv.DictWriter(csv_open, delimiter=',', lineterminator='\n', fieldnames=csv_head)
#        writer.writerow({
#                'Post ID' : tweet['id'],
#                'Screen Name':tweet['user']['name'].encode("ascii",errors="replace").decode("utf8"),
#                'ID':tweet['user']['id_str'],
#                "sentence":tweet['text'].encode("ascii",errors="replace").decode("utf8")
#                })
#    print(tweet['id'])
#    print(tweet['text'].encode("ascii",errors="replace").decode("utf8"))
#    print(tweet['user']['name'])
#    print(tweet['user']['id_str'])
#    print()
#
#stream_results = requests.get(url_streaming, stream=True,auth=auth)
#
#for line in stream_results.iter_lines():
#    try:
#        decoded_line = line.decode('utf-8')
#        print(json.loads(decoded_line)['text'])
#    except:
#         pass
"""
