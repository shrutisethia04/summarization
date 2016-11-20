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

tablename = 'twitter'

cursor.execute("select sno, tweet from %s;" % (tablename)) # ctweet has punctuations,stopwords,hyperlinks removed
db.commit()
tweetset=cursor.fetchall()

for tweet in tweetset:
	up_tweet=tweet[1] #tweet original with spaces removed
	up_tweet = re.sub(' +',' ',up_tweet).strip()
	up_tweet = re.sub('&amp;','&',up_tweet)
	up_tweet=up_tweet.replace('\n',"")
	up_weet=up_tweet.replace('\r',"")

	comp_tweet = tweet[1]
	# lowercase
	comp_tweet = comp_tweet.lower()
	# remove links
	comp_tweet = re.sub(r"(?:\@|https?\://)\S+", "", comp_tweet)
	comp_tweet = re.sub('&amp;','&',comp_tweet)
	#incomplete tweet
	comp_tweet = re.sub('htt','',comp_tweet)
	comp_tweet = re.sub('http;','',comp_tweet)
	comp_tweet = re.sub('https;','',comp_tweet)
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
	comp_tweet=comp_tweet.replace('\n',"")
	comp_tweet=comp_tweet.replace('\r',"")
	comp_tweet = re.sub(' +',' ',comp_tweet).strip()

	print tweet[0]
	cursor.execute("""update %s set tweet= "%s", ctweet='%s' where sno=%s;""" % (tablename, up_tweet, comp_tweet , `str(tweet[0])`))
	db.commit()