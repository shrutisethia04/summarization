import MySQLdb
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import string ,re
import math
import operator
import csv

db= MySQLdb.connect("localhost","root","it-03@CC","osm")
cursor = db.cursor()

slang_dictionary = {}

cursor.execute("select sno, tweet from twitter;") # ctweet has punctuations,stopwords,hyperlinks removed
db.commit()
tweetset=cursor.fetchall()

for tweet in tweetset:
	comp_tweet = tweet[1]
	# lowercase
	comp_tweet = comp_tweet.lower()
	# remove links
	comp_tweet = re.sub(r"(?:\@|https?\://)\S+", "", comp_tweet)
	

	# punctuation
	exclude = set(string.punctuation)
	comp_tweet = ''.join(ch for ch in comp_tweet if ch not in exclude)

	# remove slangs
	csvfile= open('Slang_Dictionary.csv','r')
	reader = csv.reader(csvfile)
	for row in reader :
		slang_dictionary[str(row[0])]= str(row[1])
	for wr in comp_tweet:
		if wr in slang_dictionary:
			comp_tweet = re.sub(r'\b'+wr+r'\b', slang_dictionary[wr],comp_tweet)
	comp_tweet=comp_tweet.replace("'","")
	comp_tweet=comp_tweet.replace('\"',"")
	comp_tweet=comp_tweet.replace('"',"")
	comp_tweet=comp_tweet.replace('rt',"")
	comp_tweet=comp_tweet.replace('RT',"")
	comp_tweet = re.sub(' +',' ',comp_tweet).strip()
	cursor.execute("update twitter set ctweet=%s where sno=%s;",(comp_tweet, tweet[0])) # ctweet has punctuations,stopwords,hyperlinks removed
	db.commit()