import os
import re
import datetime
import time

yesterday=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d")
yesterdayepoch=time.mktime(time.strptime(yesterday,"%Y%m%d"))
days29=(datetime.datetime.now()-datetime.timedelta(days=29)).strftime("%Y%m%d")

os.system('rm /backup/localweekly/'+days29+'.zip')
os.system('rm /backup/clientweekly/'+days29+'.zip')

localdirs=['/files/py','/files/django','/var/www','/etc/apache2/vhosts.d']
clientdirs=['/files/clientdjango','/var/www','/etc/apache2/vhosts.d']

def local():
	for dir in localdirs:
		if dir=="/etc/apache2/vhosts.d":
			file="/etc/apache2/vhosts.d/vhost.conf"
			os.system('zip -g /backup/localweekly/'+yesterday+'.zip /etc/apache2/vhosts.d/vhost.conf')
		elif dir=="/var/www":
			for a,b,c in os.walk(dir):
				for file in c:
					if not re.search("client",a+"/"+file):
						os.system('zip -g /backup/localweekly/'+yesterday+'.zip '+a+'/'+file)
		else:
			for a,b,c in os.walk(dir):
				for file in c:
					os.system('zip -g /backup/localweekly/'+yesterday+'.zip '+a+'/'+file)


def client():
	for dir in clientdirs:
		if dir=="/etc/apache2/vhosts.d":
			for a,b,c in os.walk(dir):
				for file in c:
					if re.search("client",file):
						os.system('zip -g /backup/clientweekly/'+yesterday+'.zip '+a+'/'+file)
                elif dir=="/var/www":
			for a,b,c in os.walk(dir):
				for file in c:
					if re.search("client",a+"/"+file):
						os.system('zip -g /backup/clientweekly/'+yesterday+'.zip '+a+'/'+file)
		else:
			for a,b,c in os.walk(dir):
				for file in c:
					os.system('zip -g /backup/clientweekly/'+yesterday+'.zip '+a+'/'+file)


local()
client()

