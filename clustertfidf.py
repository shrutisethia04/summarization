from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import MySQLdb 
import math
import cosim

db= MySQLdb.connect("localhost","root","shruti","osm")
cursor = db.cursor()

_stopwords = set(stopwords.words('english') + list(punctuation))
def _compute_frequencies( word_sent):
		""" 
		Compute the frequency of each of word.
		Input: 
		word_sent, a list of sentences already tokenized.
		Output: 
		freq, a dictionary where freq[w] is the frequency of w.
		"""
		freq = defaultdict(int)
		for s in word_sent:
			for word in s:
				if word not in _stopwords:
					freq[word] += 1
				# frequencies normalization and fitering
		return freq


def begin(hashtag):
	tablename=hashtag
	cluster_size=5
	cursor.execute('select TIMESTAMPDIFF(second, max(tweettime), min(tweettime)) from '+ tablename )
	db.commit()
	max_min=cursor.fetchall()
	timegap=abs(max_min[0][0] / cluster_size)
	#print max_min[0][0]
	#print timegap
	cluster_array=[]
	cluster_dis=[]
	word_dis={}
	arr_dict=[]
	all_cluster_dic={}
	tweet_cluster_array=[]

	tweet_sno={}

	no_of_tweets_cluster= {}
	for i in range(1,cluster_size+1):
		#print i
		#cursor.execute('Select ctweet,sno from twitter_duplicate where tweettime between DATE_ADD( (select min(tweettime) from twitter_duplicate),INTERVAL '+str(timegap*(i-1))+' SECOND) and  DATE_ADD( (select min(tweettime) from twitter_duplicate),INTERVAL '+str(timegap*i)+' SECOND) ;')
		cursor.execute('Select ctweet,sno from '+tablename+' where tweettime between DATE_ADD( (select min(tweettime) from '+tablename+'),INTERVAL '+str(timegap*(i-1))+' SECOND) and  DATE_ADD( (select min(tweettime) from '+tablename+'),INTERVAL '+str(timegap*i)+' SECOND) ;')
		#print 'Select ctweet,sno from twitter_duplicate where tweettime between DATE_ADD( (select min(tweettime) from twitter_duplicate),INTERVAL '+str(timegap*(i-1))+' SECOND) and  DATE_ADD( (select min(tweettime) from twitter_duplicate),INTERVAL '+str(timegap*i)+' SECOND) ;'
		row=cursor.fetchall()
		cluster_dis.append(row)	
		tweettext=''
		count=0
		cluster_tweets={}
		for tweet in row:
			tweettext = tweet[0] +'. '+tweettext	
			cursor.execute('UPDATE '+tablename+' set cluster_no='+str(i)+' where sno= '+str(tweet[1]))
			cluster_tweets[int(tweet[1])]= tweet[0]
			count= count+1
		no_of_tweets_cluster[i]= count
		tweet_sno[i]= cluster_tweets
		#print tweettext
		sents = sent_tokenize(tweettext)
		tweet_cluster_array.append(sents)
		word_sent = [word_tokenize(s) for s in sents]
		cluster_array.append(word_sent)
		#print word_sent
		tweet_dict={}

		#calculating no of times word appears in cluster
		num_word=0.0 #no. of words in the cluster
		for tweet in word_sent:		
			for word in tweet:
				num_word=num_word+1
			
				if word in tweet_dict :
					tweet_dict[word]=tweet_dict[word]+1
				else:
					tweet_dict[word]=1.0
		#print num_word

			
		# calculating term frequency of word in cluster
		for word in tweet_dict:
			tf_word=tweet_dict[word]/num_word
			#print word, tf_word
			tweet_dict[word]=tf_word
		
		# print tweet_dict

		# arr_dict contains term frequency of words in each cluster
		arr_dict.append(tweet_dict)

	#for i in tweet_sno:
	#	t= tweet_sno[i]
	#	print "cluster no",i
	#	for j in t:
	#		print j,t[j]
	#	print "\n \n"

	#print tweet_sno
	#print no_of_tweets_cluster
	#calculating no. of documents a word appears in. Stored in all_cluster_dic
	for cluster in arr_dict:
		for word in cluster:
			if word in all_cluster_dic:
				all_cluster_dic[word]= all_cluster_dic[word]+1
			else:
				all_cluster_dic[word]=1.0

	idf={}
	for i in all_cluster_dic:
		idf[i]=math.log(1+cluster_size/all_cluster_dic[i])
		#print  i,idf[i]

	tf_idf_all=[]
	for dict1 in arr_dict:
		tf_idf={}
		for word in dict1:
			tf_idf[word]=dict1[word]*idf[word]
		#print tf_idf
		#print "\n \n"
		tf_idf_all.append(tf_idf)

	
	# for i in tf_idf_all:
		# for j in i:
			# print i[j]
		# print "\n \n"

	#print tf_idf_all
	scores=[]
	update_query= "UPDATE "+tablename+" SET cluster_tf_idf= CASE sno "
	sno_array= "("
	for i in tweet_sno:
		cluster= tweet_sno[i]
		for tweet_no in cluster:
			tokenized_tweet= word_tokenize(cluster[tweet_no])
			#print tokenized_tweet
			tf_idf= tf_idf_all[i-1]
			score= 0.0
			for word in tokenized_tweet:
				if word in tf_idf:
					score = score + tf_idf[word]
		
			update_query+= " WHEN "+str(tweet_no)+" THEN "+str(round(score,8))
			sno_array+= str(tweet_no)
			sno_array+= ","
			#cursor.execute("UPDATE twitter_duplicate set cluster_tf_idf= "+str(round(score,8))+" where sno= "+str(tweet_no))
			#db.commit()
	#sno_array.strip(',')
	sno_array= sno_array[:-1]

	sno_array+=")"

	update_query+= " END WHERE sno in "+sno_array
	cursor.execute(update_query)	
	'''region 1'''

	# -------------- selecting top tweets ---------------------
	output=[]
	for i in range(1, cluster_size+1):
		print "\n\n\n-------------------------- Cluster Number ",i, "-------------------------------------------- "
		#print len(scores[i-1])
		top_per= no_of_tweets_cluster[i]*0.1
		topno=min(15, top_per)
		#print " \n Top 10% percent of tweets: ", top_per
		#print "No. of tweets chosen: ", topno
		cursor.execute("Select distinct tweet,cluster_tf_idf from "+tablename+" where cluster_no= "+str(i)+" ORDER BY cluster_tf_idf DESC LIMIT "+str(int(topno)))
		db.commit()
		toptweets=cursor.fetchall()
		j=1
		kl=1
		tweetct=int(topno)
		#arr of size 25 with initial value 0
		bool_arr=[0] * 25
		ocluster={}
		for x in range(tweetct):
			if bool_arr[x] == 0:
				bool_arr[x] = 1;
				ocluster[kl]=toptweets[x][0]
				print ocluster[kl]
				kl=kl+1
				if kl==21:
					break
				for z in range(x+1, tweetct):
					if cosim.cosine_similarity(toptweets[x][0],toptweets[z][0]) > 0.8 :
						bool_arr[z]=1	

		output.append(ocluster)
	return output
	#--------------------------------------------------------------

	'''
	for i in range(0,cluster_size):
		score_array=[]
		tf_idf=tf_idf_all[i]
		for tweet in word_sent:
			tweetscore=0.0
			for word in tweet:
				tweetscore=tweetscore+tf_idf[word]
			score_array.append(tweetscore)
		scores.append(score_array)

	for i in scores:
		print i
		print "\n"


	'''

	#print all_cluster_dic['elections']




	'''

	region 1: 

	cluster_no= 1
	sno = 1
	for cluster in cluster_array:
		tf_idf= tf_idf_all[cluster_no-1]
		for i in range(i, len())


	cluster_no=1
	sno= 1
	for cluster in cluster_array:
		if cluster_no==3:
			break
		cluster_score= []
		print "cluster #", cluster_no
		for tweet in cluster:
			score=0.0		
			tf_idf= tf_idf_all[cluster_no-1]
			if sno==170 or sno==172 or sno==173:
				print "##tweet is##", tweet
			for word in tweet:
				if word in tf_idf:
					score = score+ tf_idf[word]
					if sno==170 or sno==172 or sno==173:
						print word, tf_idf[word]
			cluster_score.append(score)
			#print cluster_no
			#cursor.execute("UPDATE twitter_duplicate set cluster_tf_idf="+str(round(score,8)) +" where sno="+str(sno) )
			#db.commit()
			sno= sno+1
		cluster_score.sort()
		scores.append(cluster_score)
		cluster_no= cluster_no+1

	'''
