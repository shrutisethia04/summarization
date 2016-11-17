import MySQLdb

db= MySQLdb.connect("localhost","root","it-03@CC","osm")
cursor = db.cursor()
cursor.execute('select distinct ctweet,retweet from twitter order by retweet desc limit 15')
#cursor.execute('select * from twitter')
db.commit()
i=1
rows = cursor.fetchall()
for r in rows:
	print "#",i," ",r[0], "\n \n"
	i=i+1