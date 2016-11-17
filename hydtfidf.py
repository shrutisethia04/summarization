#------------------hybrid tf-idf---------------

import MySQLdb
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import string ,re
import math
import operator

_stopwords = stopwords.words('english')
_stopwords.extend(string.punctuation)
_stopwords.append("rt") 

db= MySQLdb.connect("localhost","root","it-03@CC","osm")
cursor = db.cursor()

cursor.execute("select sno,ctweet from twitter;") # ctweet has punctuations,stopwords,hyperlinks removed
db.commit()
tweetset=cursor.fetchall()

#----------Term Frequency ----------
def _compute_frequencies(word_sent):
		""" 
		Compute the frequency of each of word.
		Input: word_sent, a list of sentences already tokenized.
		Output: freq, a dictionary where freq[w] is the frequency of w.
		"""
		freq = defaultdict(int)
		for s in word_sent:
			for word in s:
				if word not in _stopwords:
					freq[word] += 1
				# frequencies normalization and fitering
		return freq


def term_freq(word_dict , no_of_word):
	tf = defaultdict(float)
	for item in word_dict:
		tf[item[0]]= float(item[1])/float(no_of_word)
	return tf

def inverse_freq(tweetset, word_dict):
	cursor.execute("select count(*) from twitter;") # ctweet has punctuations,stopwords,hyperlinks removed
	db.commit()
	tweetno=cursor.fetchall()
	totdoc= tweetno[0] # total #docs=tot #tweets
	print totdoc[0]
	idf = defaultdict(float)
	for word in word_dict :
		idf[word[0]]=0
		#print word

	#print word_dict[0][0]
	for word in word_dict :
		for tweet in tweetset:
			#print word[0]+ " : "+tweet[1]
			if word[0] in tweet[1]:
				idf[word[0]]=idf[word[0]]+1

	for key, value in idf.iteritems():
		'''if value==0:
			print key
		else:'''
		val =  math.log(1 + totdoc[0]/value)
		idf[key]=val
		
	return idf

#-----------------------------------MAIN -------------------------------------------------

#------------------Making document of all tweets to calcuate tf ----------------------
tweettext=''
for tweet in tweetset:
	#print tweet[1]
	tweetq = re.sub(' +',' ',tweet[1])
	#print tweetq
	tweettext = tweetq+' . '+tweettext

#print tweettext

sents = sent_tokenize(tweettext)

word_sent = [word_tokenize(s) for s in sents]
#print word_sent

_freq = _compute_frequencies(word_sent)	
#print _freq
#-----------sorting the words acc to frequency ---------------
sorted_x = sorted(_freq.items(), key=operator.itemgetter(1))

'''for key, value in sorted_x.iteritems():
	print key+":"+str(value)
'''
# --- calculating #total words -----
total_words=0
for item in sorted_x:
	#print item[0]+':'+str(item[1])
	total_words=total_words+item[1]

# --- calculating #tf of all words -----
_tf = term_freq(sorted_x , total_words)
'''for key, value in _tf.iteritems():
	print key+":"+str(value)
print "\n\n\n"'''

# --- calculating #idf of all words -----
_idf = inverse_freq(tweetset, sorted_x)
'''for key, value in _idf.iteritems():
	print str(key)+":"+str(value)
print "\n\n\n"'''

# --- calculating #tfidf of all words -----
_tfidf = defaultdict(float)
'''for key,value in sorted_x:	
	_tfidf[key]=_tf[key]*_idf[key]
	print key,_tfidf[key],_tf[key],_idf[key]'''

# --- ranking of all tweets on tfidf score -----
for tweet in tweetset:
	sum=0
	#print tweet[1]
	words= tweet[1].split()
	#print words
	for word in words:
		#print word
		sum=sum+_tfidf[word]
		#print word,_tfidf[word]
	'''try:
		cursor.execute("update twitter set hyd_tfidf=%s where sno=%s",(sum,tweet[0]))
		db.commit()
	except:
		print "error"
	'''

cursor.execute("select distinct tweet, hyd_tfidf from twitter order by hyd_tfidf desc limit 20;")	
db.commit()
toptweets=cursor.fetchall();
i=1
for toptweet in toptweets:
	print i,toptweet[0]
	i=i+1

#-----------check which log -------------
#print math.log(2,2)
