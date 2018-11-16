# Media Social Crawler

This program is created to crawling data from social media sources, likes Twitter, Instagram, Facebook, and News.
The crawler that available nows is for Twitter and News. This program is running on CENTOS environment. 
And make sure you have elasticsearch and kibana installed on your system because the data that has been crawled will be stored in elasticsearch.

And now, for running the program, using this command :

`python scrapping_data.py`

![alt text](images/start_crawler.png "Logo Title Text 1")

Now, open your IP address which your program is located :

![alt text](images/web_crawler.PNG "Logo Title Text 2")

Now, for adding keyword for crawling :
1. Fill form with the keyword that you want added 
2. Next, choose one for available source

![alt text](images/add_keyword.PNG "Logo Title Text 3")

3. After that, click "Add_Keyword"
4. And the keyword is successfully adding to your crawler

![alt text](images/add_keyword02.PNG "Logo Title Text 4")

Now, to start crawling program :
1. Choose one for available source (example : Twitter)
2. Click "Start_Twitter"
![alt text](images/start_web02.PNG "Logo Title Text 5")
3. After that, you can check in the console that crawler program is running
![alt text](images/result-01.PNG "Logo Title Text 6")
4. You can check too on your kibana data that has entered
![alt text](images/kibana.PNG "Logo Title Text 7")