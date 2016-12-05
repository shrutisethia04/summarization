import MySQLdb


def begin(hashtag):
	tablename=hashtag
	db= MySQLdb.connect("localhost","root","shruti","osm")
	cursor = db.cursor()
	cursor.execute('select distinct tweet,retweet from '+tablename+' order by retweet desc limit 20')
	#cursor.execute('select * from twitter')
	db.commit()
	i=1
	output={}
	rows = cursor.fetchall()
	for r in rows:
		#print "#",i," ",r[0], "\n \n"
		output[i]=r[0]
		i=i+1
	return output
