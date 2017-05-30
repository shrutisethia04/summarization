import MySQLdb
db= MySQLdb.connect("localhost","root","snigdha","osm")
cursor = db.cursor()
cursor.execute('select ctweet from punjabelection2017 ;')
db.commit()
tweets = cursor.fetchall()
file= open('punjabelection2017_clean.txt','w')
arr=[]
for tweet in tweets:
	arr.append(tweet[0])
arr= list(set(arr))

for a in arr:
	file.write(a+'\n')