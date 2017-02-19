from __future__ import division
from flask import app,Flask
from flask import render_template, request,redirect,url_for
from flask import request

app=Flask(__name__)

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
	keyword=request.form["keyword"]
	print keyword
	try:
		
		import tweetextract
		result=tweetextract.res(keyword)
		#print result
		import tweetclean
		s=tweetclean.tweet_clean(keyword)
		#print s
		return redirect(url_for('hydtfidf',hashtag=keyword))
	except Exception, e:
		return(str(e))
	
@app.route('/hydtfidf/<hashtag>')	
def hydtfidf(hashtag):
	try:
		import hydtfidf
		print hashtag
		summary=hydtfidf.begin(hashtag)
		return render_template("index.html", hashtag=hashtag , summary=summary)	
	except Exception, e:
		return(str(e))

@app.route('/temptfidf/<hashtag>')
def temptfidf(hashtag):
	try:
		import clustertfidf
		summary=clustertfidf.begin(hashtag)
		return render_template("index1.html",hashtag=hashtag , summary=summary)
	except Exception, e:
		return(str(e))


@app.route('/retweet/<hashtag>')
def retweet(hashtag):
	try:
		import retweetcount
		summary=retweetcount.begin(hashtag)
		return render_template("index2.html",hashtag=hashtag , summary=summary)	
	except Exception, e:
		return(str(e))
if __name__ == "__main__":
	app.run(debug=True)
