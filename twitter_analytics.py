# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 19:03:49 2017

@author: Darshil
"""
import requests
import os
import zipfile
import openpyxl
import sqlite3
import glob
import getpass
import requests
import csv
import string
import pandas as pd
import numpy as np
import shutil
import json

#Fetching the data from the web hosted twitter file
url="http://kevincrook.com/utd/tweets.json"
r1=requests.get(url)
#Storing the data into Temporary txt file

twitter_file=open("twitter_file.json","wb")
twitter_file.write(r1.content)
twitter_file.close()

#Loading the JSON data into python object
with open('twitter_file.json') as data_file:    
    data = json.load(data_file)

#Removing the temporary created file
os.remove('twitter_file.json')

#Total Number of events in twitter file
total_events=len(data)

#Total Number of tweets in twitter file
count=0
for i in data:
    try:
        i["text"]
        count=count+1
    except KeyError:
        continue
    
#Total tweets and tweet content 
d2={'lang':None}
d3={'text':None}
index2=np.arange(1,count,1);
lang_df= pd.DataFrame(d2,index2);
tweet_df=pd.DataFrame(d3,index2);

count_2=1;
for i in data:
    try:
        i["text"]
        lang_df.loc[count_2,'lang']=i['lang']
        tweet_df.loc[count_2,'text']=i['text'].encode('utf-8')
        #tweet_df.loc[count_2,'text']=tweet_df.loc[count_2,'text'].decode('utf-8')
        count_2=count_2+1
    except KeyError:
        continue
    
lang_df_grouped=pd.Series.to_frame(lang_df.groupby(['lang']).size())
lang_df_grouped.reset_index(inplace=True)
lang_df_grouped_sorted=lang_df_grouped.sort_values([0],ascending=False)

#Opening the file and putting the intital values 
with open('twitter_analytics.txt', 'w') as f:
    print(total_events, file=f)
    print(count,file=f)

#Opening the tweets analytics into the file in append mode
lang_df_grouped_sorted.to_csv('twitter_analytics.txt',sep=',',encoding='utf-8',header=False,index=False,mode ='a')
#Opening the tweets file and putting the tweets into it after encodeing it with the utf-8 encoding system
with open('tweets.txt', 'w',encoding='utf-8') as f:
    for i in range(1,count+1):
        print(tweet_df.loc[i,'text'],file=f)
#tweet_df.to_csv('tweets.txt',sep=',',encoding='utf-8',header=False,index=False,mode='w')
