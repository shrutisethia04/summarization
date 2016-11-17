from twython import Twython, TwythonError
import datetime
import time
import pytz
import time
import csv
import MySQLdb
import re,string

ACCESS_TOKEN = '209973347-gVZSvi8vozsgApO5DG7FshcX4FjFanIs4CYTTgys'
ACCESS_SECRET = 'TxR80g0abSs2RPIUxhzYLGWanOGzl6QaOlsoOBA0Ft1Yj'
CONSUMER_KEY = '1aD1nSK3lZXLHCW3dxm2BIhi9'
CONSUMER_SECRET = 'smXOuQ3Yr23Va49VXLnsjQhFWBTMy0hj0gvdTj9ETiDJAgSh0Y'

db= MySQLdb.connect("localhost","root","it-03@CC","osm")
cursor = db.cursor()
count=1
twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
word = '#IAmWithModi'
lasttweetid=0
sinceId=None
maxTweets=10000
max_id = -1L
tweetCount = 0
slang_dictionary = {}
twt_set=set()
#cursor.execute('delete from twitter')
#db.commit()
cursor.execute('alter table iamwithmodi auto_increment=1')
db.commit()
while  tweetCount < maxTweets:
	try:
		
		if (max_id <= 0):
			if (not sinceId):
			       # new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
				search_results = twitter.search(q=word,lang='en' ,count=1000)
			else:
				search_results = twitter.search(q=word,lang='en' ,count=1000,since_id=sinceId)
		else:
			if (not sinceId):
				search_results = twitter.search(q=word,lang='en' ,count=1000,max_id=str(max_id - 1))
			else:
				search_results = twitter.search(q=word,lang='en' ,count=1000,max_id=str(max_id - 1),since_id=sinceId)
		if not search_results:
			print("No more tweets found")
			break
		tweetCount += len(search_results)
		
	except TwythonError as e:
		print e
		time.sleep(120)
		
			#print search_results
	for tweet in search_results['statuses']:

		for i in tweet['text']:
			if ord(i)>128:
				tweet['text']=tweet['text'].replace(i,'')
		orig_tweet = tweet['text']
		print tweet['text']
		#if tweet['text'] not in twt_set:
		#	twt_set = set(tweet['text'])
	# -------------------------- cleaning ---------------
		# lowercase
		tweet['text'] = tweet['text'].lower()
		# remove links
		tweet['text'] = re.sub(r"(?:\@|https?\://)\S+", "", tweet['text'])
		

		# punctuation
		exclude = set(string.punctuation)
		tweet['text'] = ''.join(ch for ch in tweet['text'] if ch not in exclude)
	
		# remove slangs
		csvfile= open('Slang_Dictionary.csv','r')
		reader = csv.reader(csvfile)
		for row in reader :
			slang_dictionary[str(row[0])]= str(row[1])
		for wr in tweet['text']:
			if wr in slang_dictionary:
				tweet['text'] = re.sub(r'\b'+wr+r'\b', slang_dictionary[wr],tweet['text'])
	# ----------------------------------------------------

		
		#mydate=tweet['created_at'] 
		#tweettime = datetime.datetime.strptime('%a %b %d %H:%M:%S +0000 %Y")
		
		tweettime=tweet['created_at']
		ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
		lasttweetid=tweet['id']
		print tweettime
		fav= tweet['favorited']
		t=tweet['entities']
		hashtag=''
		for tags in t['hashtags']:
			h= tweet['text']
			for i in h:
				if ord(i)>128:
					h= h.replace(i,'')
			hashtag+=(h)


		comp_tweet=(orig_tweet)

		for i in comp_tweet:
			if ord(i)>128:
				comp_tweet= comp_tweet.replace(i,'')
		
		comp_tweet=comp_tweet.replace("'","")
		comp_tweet=comp_tweet.replace('\"',"")
		comp_tweet=comp_tweet.replace('"',"")
		comp_tweet=comp_tweet.replace('rt',"")
		comp_tweet=comp_tweet.replace('RT',"")
		comp_tweet = re.sub(' +',' ',comp_tweet)
	

		rt_cnt=tweet['retweet_count']
		is_rtd=tweet['retweeted']

		user_arr=tweet['user']
		user_id=user_arr['id_str']
		user_foll=user_arr['followers_count']
		user_friend=user_arr['friends_count']
		user_handle= user_arr['screen_name']
		for i in user_handle:
			if ord(i)>128:
				user_handle= user_handle.replace(i,'')
	
				#query= 
		try:
			#cursor.execute('insert into  values ('+`count`+',"'+comp_tweet+'",'+`rt_cnt`+',"'+`hashtag`+'")')
			cursor.execute('insert into iamwithmodi (tweet,retweet,hashtag,tweettime,ctweet) values ("'+comp_tweet+'",'+`rt_cnt`+',"IAmWithModi","'+ts+'","'+tweet['text']+'")')

			db.commit()
			#datetime.strptime('Thu Apr 23 13:38:19 +0000 2009','%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
			count=count+1
		except (MySQLdb.Error, MySQLdb.Warning) as e:
			print e
		#lasttweet = search_results[1]
		max_id = tweet['id']

db.close()
	# print 'Tweet from @%s Date: %s %s' % (tweet['user']['screen_name'].encode('utf-8'),tweet['created_at'],tweet['retweet_count'])
    # print tweet['text'].encode('utf-8'), '\n'
