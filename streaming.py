from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import MySQLdb

db= MySQLdb.connect("localhost","root","it-01@CC","osm")
cursor = db.cursor()

#Variables that contains the user credentials to access Twitter API 
access_token = '209973347-gVZSvi8vozsgApO5DG7FshcX4FjFanIs4CYTTgys'
access_token_secret ='TxR80g0abSs2RPIUxhzYLGWanOGzl6QaOlsoOBA0Ft1Yj'
consumer_key = '1aD1nSK3lZXLHCW3dxm2BIhi9'
consumer_secret ='smXOuQ3Yr23Va49VXLnsjQhFWBTMy0hj0gvdTj9ETiDJAgSh0Y'


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        #with open('fetched_tweets.txt','a') as tf:
         #   tf.write(data)
        #print data
        d = json.loads(data)
        orig_tweet = str(d['text'])
        tweettext = str(d['retweeted_status']['text'])
        tweetcnt = str(d['retweeted_status']['retweet_count'])
        hashes = ''
        #print d['retweeted_status']['favorite_count']
        for y in d['entities']['hashtags']:
            hashes = y+','+hashes 
        tweettime = d['created_at']
        cursor.execute('insert into %s values (tweet,retweet,hashtag,tweettime) values (%s,%s,%s,%s)',%(tablename,tweettext,tweetcnt,hashes,tweettime))
        db.commit()
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    tablename = 'stream_'+hashtag
    cursor.execute('create table %s (sno int auto_increment primary key, tweet varchar(400), tweettime datetime, hashtag varchar(60), retweet int, ctweet varchar(400) );',%(tablename))
    db.commit()    

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['iamwithmodi'])
