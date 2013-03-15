import MySQLdb
import MySQLdb.cursors
import os
import datetime

dbconn = MySQLdb.connect(db='...', host='...', user='...', passwd='...', cursorclass=MySQLdb.cursors.DictCursor)

dbquery=dbconn.cursor()
dbquery.execute('show databases')
db=dbquery.fetchall()


yesterday=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d")
days29=(datetime.datetime.now()-datetime.timedelta(days=29)).strftime("%Y%m%d")

os.system('rm -rf /backup/mysql/'+days29)
os.system('mkdir /backup/mysql/'+yesterday)

for database in db:
	database=database["Database"]
	print database
	os.system('mysqldump -u ... -p... '+database+' > /backup/mysql/'+yesterday+'/'+database+'.sql')
