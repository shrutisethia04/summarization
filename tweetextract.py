from twython import Twython, TwythonError
import datetime
import time
import pytz
import csv
import MySQLdb
import string




def res(key):
	searchtag='#'+key
	tablename=key
	ACCESS_TOKEN = '1029938216-1EAmYAlJTuI4LUamgQsHTNxJLEAXGLrffjm21dP'
	ACCESS_SECRET = 'WZ5kfMKF4HICYpjuv9rBk7Z6xQLeyOuYyYfRMFIZCcfGj'
	CONSUMER_KEY = '4uZOSMCSCGeZC3IubtiwUBR3y'
	CONSUMER_SECRET = '15tSkR0BkJKuRICWYUxmA9djMRpi8ChnNdBnpZDcVvJ71whPwq'

	db= MySQLdb.connect("localhost","root","shruti","osm")
	cursor = db.cursor()

	twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

	#searchtag = '#uspresidentialelection'
	#tablename = 'uspresidentialelection'

	lasttweetid=0
	sinceId=None
	maxTweets=100000
	max_id = -1L
	tweetCount = 0
	slang_dictionary = {}
	twt_set=set()

	#------------------------- creating table for the given hashtag---------------------------------------------
	#cursor.execute('DROP TABLE IF EXISTS '+tablename+';' )
	cursor.execute('select 1 from '+tablename+' limit 1;')
	db.commit()
	try:
		res=cursor.fetchall()
		
	except Exception, e:
		cursor.execute('create table '+tablename+' (sno int auto_increment primary key, tweet varchar(400), tweettime datetime, hashtag varchar(60), retweet int, ctweet varchar(400), hyd_tfidf decimal, cluster_no int, cluster_tf_idf decimal); ')
		db.commit()

		#-------------------------- collecting tweets --------------------------------------------------------------
		while  tweetCount < maxTweets:
			try:
				if (max_id <= 0):
					if (not sinceId):
					       # new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
						search_results = twitter.search(q=searchtag,lang='en' ,count=1000)
					else:
						search_results = twitter.search(q=searchtag,lang='en' ,count=1000,since_id=sinceId)
				else:
					if (not sinceId):
						search_results = twitter.search(q=searchtag,lang='en' ,count=1000,max_id=str(max_id - 1))
					else:
						search_results = twitter.search(q=searchtag,lang='en' ,count=1000,max_id=str(max_id - 1),since_id=sinceId)
				if not search_results:
					print("No more tweets found")
					break
				tweetCount = tweetCount+ len(search_results)
		
			except TwythonError as e:
				break
			for tweet in search_results['statuses']:
				for i in tweet['text']:
					for j in i:
						if ord(j)>128:
							tweet['text']=tweet['text'].replace(j,'') #removing chars with invalid ascii value
				orig_tweet = tweet['text']
				print tweet['text']
				tweettime=tweet['created_at']
				ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				lasttweetid=tweet['id']
				print tweettime
				fav= tweet['favorited']
				t=tweet['entities']
				hashtag=''
				for tags in t['hashtags']:
					h = tags['text']
					print "#########",h
					for i in h:
						if ord(i)>128:
							h= h.replace(i,'')
					hashtag=h+';'+hashtag
				rt_cnt=tweet['retweet_count']
				'''is_rtd=tweet['retweeted']
				user_arr=tweet['user']
				user_id=user_arr['id_str']
				user_foll=user_arr['followers_count']
				user_friend=user_arr['friends_count']
				user_handle= user_arr['screen_name']
				for i in user_handle:
					if ord(i)>128:
						user_handle = user_handle.replace(i,'')'''

				comp_tweet=(orig_tweet)
				for i in comp_tweet:
					if ord(i)>128:
						comp_tweet= comp_tweet.replace(i,'')
				print "$$$$$$",str(comp_tweet)
				comp_tweet=comp_tweet.replace('"',"")

			#---------------------------------  adding data to DB - --------------------------------------------------
				try:
					#cursor.execute('insert into %s (tweet,retweet,hashtag,tweettime) values (%s,%s,%s,%s)',(str(tablename),str(comp_tweet),str(rt_cnt),str(hashtag),str(ts)) )
					cursor.execute('insert into '+ str(tablename)+' (tweet,retweet,hashtag,tweettime) values ( "'+str(comp_tweet)+ '" , ' +`rt_cnt`+' , "'+str(hashtag)+ '" , "' + str(ts) +'");')
					db.commit()
				except (MySQLdb.Error, MySQLdb.Warning) as e:
					print e
				max_id = tweet['id']

	db.close()
	return 1
