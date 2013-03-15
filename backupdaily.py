import os
import re
import datetime
import time

yesterday=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d")
yesterdayepoch=time.mktime(time.strptime(yesterday,"%Y%m%d"))
days8=(datetime.datetime.now()-datetime.timedelta(days=8)).strftime("%Y%m%d")

os.system('rm /backup/localdaily/'+days8+'.zip')
os.system('rm /backup/clientdaily/'+days8+'.zip')

localdirs=['/files/py','/files/django','/var/www','/etc/apache2/vhosts.d']
clientdirs=['/files/clientdjango','/var/www/client','/etc/apache2/vhosts.d']

def local():
	for dir in localdirs:
		if dir=="/etc/apache2/vhosts.d":
			file="/etc/apache2/vhosts.d/vhost.conf"
			if os.stat(file).st_mtime>yesterdayepoch:
				os.system('zip -g /backup/localdaily/'+yesterday+'.zip /etc/apache2/vhosts.d/vhost.conf')
		else:
			for a,b,c in os.walk(dir):
				for file in c:
					if not re.search("client",a+"/"+file):
						if os.stat(a+"/"+file).st_mtime>yesterdayepoch:
							os.system('zip -g /backup/localdaily/'+yesterday+'.zip '+a+'/'+file)

def client():
	for dir in clientdirs:
		if dir=="/etc/apache2/vhosts.d":
			for a,b,c in os.walk(dir):
				for file in c:
					if re.search("client",file):
						if os.stat(a+"/"+file).st_mtime>yesterdayepoch:
							os.system('zip -g /backup/clientdaily/'+yesterday+'.zip '+a+'/'+file)
		else:
			for a,b,c in os.walk(dir):
				for file in c:
					if os.stat(a+"/"+file).st_mtime>yesterdayepoch:
						os.system('zip -g /backup/clientdaily/'+yesterday+'.zip '+a+'/'+file)


local()
#client()

files=['/backup/localdaily/'+yesterday+'.zip','/backup/clientdaily/'+yesterday+'.zip']
for item in files:
	try:
		openfile=open(item)
		openfile.close()
	except:
		os.system('echo "" > '+item)
