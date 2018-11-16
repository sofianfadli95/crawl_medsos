# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 09:16:51 2018

@author: sofyan.fadli
"""

from flask import Flask, render_template, request, redirect, flash
import sqlite3
from threading import Thread
from twitter_crawling import get_tweets
from scrapping_detik import scrap_detik_url
# from crawl_detik import scrapping_detik

keyword_twitter = []
keyword_fb = []
keyword_insta = []
keyword_news = []
news_url = []

app = Flask(__name__)
app.secret_key = 'development key'

stop_run_twitter = False
stop_run_news = False
insta_condition = "Not Active"
fb_condition = "Not Active"
twitter_condition = "Not Active"
news_condition = "Not Active"

querry = []

# elastic_url = "127.0.0.1" 
# elastic_port = 9200

def twitter_crawl(x):
    global stop_run_twitter
    while not stop_run_twitter:
        get_tweets(x)

def manual_run_twitter(x):
    t = Thread( target = twitter_crawl, args = (x,) )
    t.start()
    return "Processing Twitter crawler"

def news_crawl(x):
    global stop_run_news
    while not stop_run_news:
        scrap_detik_url(x)

def manual_run_news(x):
    t = Thread( target = news_crawl, args = (x,) )
    t.start()
    return "Processing Twitter crawler"

# Function utk mengambil element dari table
def get_row_from_table(table):
    result = []
    select_query = "SELECT * FROM {}".format(table)
    connection = sqlite3.connect('./data.db')
    cursor = connection.cursor()
    rows = cursor.execute(select_query)
    for element in rows:
        result.append(element)
    return result

@app.route('/', methods = ['POST','GET'])
def submit():
    global stop_run_twitter, stop_run_news, querry, elastic_url, elastic_port, insta_condition, fb_condition, twitter_condition, news_condition
    # Jika user melakukan request 'POST'
    if request.method == 'POST':
        # Jika tombol 'Add' yang ditekan
        if request.form['submit'] == 'Add_Keyword':
            connection = sqlite3.connect('./data.db')
            cursor = connection.cursor()
            keyword = request.form['keyword']
            print("Your keyword is '" + keyword + "'")
            print("Type your keyword is '" + str(type(keyword)) + "'")
            
            # Query utk menambahkan element ke table database
            try:
                sources = request.form['sources']
                insert_query = "INSERT INTO keywords_{} VALUES (?)".format(sources)
                cursor.execute(insert_query, (keyword.strip(),))
                connection.commit()
                flash("You were successfully added '{}' keyword to your '{}' crawler".format(keyword.strip(), sources), "notif")
            except KeyError:
                flash("You haven't selected the available source. Please choose one", "error")
                
            # Send back to the home page
            keyword_twitter = get_row_from_table("keywords_twitter")
            keyword_fb = get_row_from_table("keywords_facebook")
            keyword_insta = get_row_from_table("keywords_instagram")
            keyword_news = get_row_from_table("keywords_news")
            news_url = get_row_from_table("news_url")
            return render_template('index.html', row_twitter = set(keyword_twitter), row_fb = set(keyword_fb), 
                                   row_insta = set(keyword_insta), row_news = set(keyword_news), table_news = set(news_url),
                                   news_condition = news_condition, insta_condition = insta_condition, 
                                   twitter_condition = twitter_condition, fb_condition = fb_condition)
        
        elif request.form['submit'] == 'Update_Elastic':
            elastic_url = request.form['elastic_url']
            elastic_port = request.form['elastic_port']
            if elastic_url == "":
                flash("Please enter the elasticsearch's url", "error")
            elif elastic_port == "":
                flash("Please enter the elasticsearch's port", "error")
            else:
                file  = open("elastic_configuration.py", "w")
                file.write("elastic_url = \"" + elastic_url + "\" ")
                file.write("\n")
                file.write("elastic_port = " + elastic_port)
                file.close()
                flash("You were successfully added new configuration setting to your elasticsearch", "notif")
                
            # Send back to the home page
            keyword_twitter = get_row_from_table("keywords_twitter")
            keyword_fb = get_row_from_table("keywords_facebook")
            keyword_insta = get_row_from_table("keywords_instagram")
            keyword_news = get_row_from_table("keywords_news")
            news_url = get_row_from_table("news_url")
            return render_template('index.html', row_twitter = set(keyword_twitter), row_fb = set(keyword_fb), 
                                       row_insta = set(keyword_insta), row_news = set(keyword_news), table_news = set(news_url),
                                       news_condition = news_condition, insta_condition = insta_condition, 
                                       twitter_condition = twitter_condition, fb_condition = fb_condition)
                
        elif request.form['submit'] == 'Update_Twitter':
            ckey_twitter = request.form['ckey_twitter']
            csecret_twitter = request.form['csecret_twitter']
            atoken_twitter = request.form['atoken_twitter']
            asecret_twitter = request.form['asecret_twitter']
            
            if ckey_twitter == "":
                flash("Please enter the consumer key", "error")
            elif csecret_twitter == "":
                flash("Please enter the consumer secret", "error")
            elif atoken_twitter == "":
                flash("Please enter the access token", "error")
            elif asecret_twitter == "":
                flash("Please enter the access secret", "error")
            else:
                file  = open("twitter_credentials.py", "w")
                file.write("ckey = \"" + ckey_twitter + "\" ")
                file.write("\n")
                file.write("csecret = \"" + csecret_twitter + "\" ")
                file.write("\n")
                file.write("atoken = \"" + atoken_twitter + "\" ")
                file.write("\n")
                file.write("asecret = \"" + asecret_twitter + "\" ")
                file.write("\n")
                file.close()
                flash("You were successfully added new configuration setting to your 'twitter' crawler", "notif")

            # Send back to the home page
            keyword_twitter = get_row_from_table("keywords_twitter")
            keyword_fb = get_row_from_table("keywords_facebook")
            keyword_insta = get_row_from_table("keywords_instagram")
            keyword_news = get_row_from_table("keywords_news")
            news_url = get_row_from_table("news_url")
            return render_template('index.html', row_twitter = set(keyword_twitter), row_fb = set(keyword_fb), 
                                       row_insta = set(keyword_insta), row_news = set(keyword_news), table_news = set(news_url),
                                       news_condition = news_condition, insta_condition = insta_condition, 
                                       twitter_condition = twitter_condition, fb_condition = fb_condition)
            
        # Jika tombol 'Delete' yang ditekan
        elif request.form['submit'] == 'Delete_Keyword':
            try:
                connection = sqlite3.connect('./data.db')
                cursor = connection.cursor()
                keyword = request.form['keyword']
                print("Your keyword is '" + keyword + "'")
                print("Type your keyword is '" + str(type(keyword)) + "'")
                sources = request.form['sources']
                print("Your sources are '" + str(sources) + "'")
                print("Type your sources are '" + str(type(sources)) + "'")
                
                delete_query = "DELETE FROM keywords_{} WHERE keyword=?;".format(sources)
                cursor.execute(delete_query, (keyword.strip(),))
                connection.commit()
                flash("You were successfully deleted '{}' keyword to your '{}' crawler".format(keyword.strip(), sources), "notif")
            except KeyError:
                flash("You haven't selected the available source. Please choose one", "error")
                
            keyword_twitter = get_row_from_table("keywords_twitter")
            keyword_fb = get_row_from_table("keywords_facebook")
            keyword_insta = get_row_from_table("keywords_instagram")
            keyword_news = get_row_from_table("keywords_news")
            news_url = get_row_from_table("news_url")
            return render_template('index.html', row_twitter = set(keyword_twitter), row_fb = set(keyword_fb), 
                                   row_insta = set(keyword_insta), row_news = set(keyword_news), table_news = set(news_url),
                                   news_condition = news_condition, insta_condition = insta_condition, 
                                   twitter_condition = twitter_condition, fb_condition = fb_condition)
        
        # Jika tombol 'Start_Twitter' ditekan
        elif request.form['submit'] == 'Start_Twitter':
            twitter_condition = "Active"
            stop_run_twitter = False
            keyword_twitter = get_row_from_table("keywords_twitter")
            querry = set(keyword_twitter)
            for element in querry:
                manual_run_twitter(element)
            print("Application Twitter crawler running...")
            flash("You were successfully started 'twitter' crawler", "notif")
            # Send back to the home page
            keyword_fb = get_row_from_table("keywords_facebook")
            keyword_insta = get_row_from_table("keywords_instagram")
            keyword_news = get_row_from_table("keywords_news")
            news_url = get_row_from_table("news_url")
            return render_template('index.html', row_twitter = set(keyword_twitter), row_fb = set(keyword_fb), 
                                   row_insta = set(keyword_insta), row_news = set(keyword_news), table_news = set(news_url),
                                   news_condition = news_condition, insta_condition = insta_condition, 
                                   twitter_condition = twitter_condition, fb_condition = fb_condition)
        
        # Jika tombol 'Stop_Twitter' ditekan
        elif request.form['submit'] == 'Stop_Twitter':
            twitter_condition = "Not Active"
            stop_run_twitter = True
            print("Application Twitter crawler stopped...")
            flash("You were successfully stopped 'twitter' crawler", "notif")
            
            # Send back to the home page
            keyword_twitter = get_row_from_table("keywords_twitter")
            keyword_fb = get_row_from_table("keywords_facebook")
            keyword_insta = get_row_from_table("keywords_instagram")
            keyword_news = get_row_from_table("keywords_news")
            news_url = get_row_from_table("news_url")
            return render_template('index.html', row_twitter = set(keyword_twitter), row_fb = set(keyword_fb), 
                                   row_insta = set(keyword_insta), row_news = set(keyword_news), table_news = set(news_url),
                                   news_condition = news_condition, insta_condition = insta_condition, 
                                   twitter_condition = twitter_condition, fb_condition = fb_condition)
        
        # Jika tombol 'Start_News' ditekan
        elif request.form['submit'] == 'Start_News':
            news_condition = "Active"
            stop_run_news = False
            keyword_news = get_row_from_table("keywords_news")
            querry = set(keyword_news)
            for element in querry:
                manual_run_news(element)
            print("Application News crawler running...")
            flash("You were successfully started 'news' crawler", "notif")
            
            # Send back to the home page
            keyword_fb = get_row_from_table("keywords_facebook")
            keyword_insta = get_row_from_table("keywords_instagram")
            keyword_twitter = get_row_from_table("keywords_twitter")
            news_url = get_row_from_table("news_url")
            return render_template('index.html', row_twitter = set(keyword_twitter), row_fb = set(keyword_fb), 
                                   row_insta = set(keyword_insta), row_news = set(keyword_news), table_news = set(news_url),
                                   news_condition = news_condition, insta_condition = insta_condition, 
                                   twitter_condition = twitter_condition, fb_condition = fb_condition)
        
        # Jika tombol 'Stop_News' ditekan
        elif request.form['submit'] == 'Stop_News':
            news_condition = "Not Active"
            stop_run_news = True
            print("Application News crawler stopped...")
            flash("You were successfully stopped 'news' crawler", "notif")
            
            # Send back to the home page
            keyword_twitter = get_row_from_table("keywords_twitter")
            keyword_fb = get_row_from_table("keywords_facebook")
            keyword_insta = get_row_from_table("keywords_instagram")
            keyword_news = get_row_from_table("keywords_news")
            news_url = get_row_from_table("news_url")
            return render_template('index.html', row_twitter = set(keyword_twitter), row_fb = set(keyword_fb), 
                                   row_insta = set(keyword_insta), row_news = set(keyword_news), table_news = set(news_url),
                                   news_condition = news_condition, insta_condition = insta_condition, 
                                   twitter_condition = twitter_condition, fb_condition = fb_condition)
    
    # Jika user melakukan request 'GET'
    elif request.method == 'GET':
        keyword_twitter = get_row_from_table("keywords_twitter")
        keyword_fb = get_row_from_table("keywords_facebook")
        keyword_insta = get_row_from_table("keywords_instagram")
        keyword_news = get_row_from_table("keywords_news")
        news_url = get_row_from_table("news_url")
        return render_template('index.html', row_twitter = set(keyword_twitter), row_fb = set(keyword_fb), 
                               row_insta = set(keyword_insta), row_news = set(keyword_news), table_news = set(news_url), 
                               news_condition = news_condition, insta_condition = insta_condition, 
                                   twitter_condition = twitter_condition, fb_condition = fb_condition)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)