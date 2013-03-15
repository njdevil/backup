# Version 3.0.2
# Linux Backup System
# ©2013 Modular Programming Systems Inc
# released as GPL 3

import MySQLdb
import MySQLdb.cursors
import os
import sys
import datetime
import time

DB_NAME='...'
DB_HOST='...'
DB_USER='...'
DB_PASS='...'
#keep backups for this long, delete on next day
DAILY_STORE_TERM= 7
WEEKLY_STORE_TERM= 28
LOCAL_INCLUDE=['/var/www',
            '/etc/apache2/vhosts.d']  #example locations
LOCAL_EXCLUDE=['/admin/media',
            '/media']
CLIENT_INCLUDE=['/var/www/client']
CLIENT_EXCLUDE=[]

def backup(name,dates,term):
    location=name["location"]
    dirs=directory_exclude(name["dir_include"],name["dir_exclude"])
    remove_old(location,dates,term)

    for dir in dirs:
        for file in os.listdir(dir):
            if term=="daily":
                file_date_check(location,dir+"/"+file,dates)
            else:
                os.system('zip -g /backup/'+location+term+'/'+dates["yesterday"]+'.zip "'+dir+'/'+file+'"')
    file_exists(location,term,dates["yesterday"])

def directory_exclude(dir_include,dir_exclude):
    dirlist=[]
    gooddirs=[]
    for dir in dir_include:
        for a,b,c in os.walk(dir):
            dirlist.append(a)
    dirlist=list(set(dirlist))
    dirlist.sort()
    for dir in dirlist:
        i=0
        for baddir in dir_exclude:
            if baddir in dir:
                i=1
        if i==0:
            gooddirs.append(dir)
    return gooddirs

def file_date_check(location,file,dates):
    if os.stat(file).st_mtime > dates["yesterdayepoch"]:
        os.system('zip -g /backup/'+location+'daily/'+dates["yesterday"]+'.zip "'+file+'"')

def file_exists(location,term,date):
    if not os.path.isfile('/backup/'+location+term+'/'+date+'/.zip'):
        os.system('echo "" > /backup/'+location+term+'/'+date+'/.zip')

def mysqlbackup(dates):
    dbconn = MySQLdb.connect(db=DB_NAME, host=DB_HOST, user=DB_USER, passwd=DB_PASS, cursorclass=MySQLdb.cursors.DictCursor)

    dbquery=dbconn.cursor()
    dbquery.execute('show databases')
    db=dbquery.fetchall()

    remove_old('mysql',dates)

    for database in db:
        database=database["Database"]
        os.system('mysqldump -u '+DB_USER+' -p'+DB_PASS+' '+database+' > /backup/mysql/'+dates["yesterday"]+'/'+database+'.sql')

def remove_old(location,dates,term=None):
    if location=="mysql":
        os.system('rm -rf /backup/mysql/'+dates["weeklyterm"])
        os.system('mkdir /backup/mysql/'+dates["yesterday"])
    else:
        if term=="daily":
            os.system('rm /backup/'+location+term+'/'+dates["dailyterm"]+'.zip')
        else:
            os.system('rm /backup/'+location+term+'/'+dates["weeklyterm"]+'.zip')


if __name__=="__main__":
    try:
        term=sys.argv[1]
    except:
        print "python backupmaster.py <daily|weekly>\n\n"
        raise

    dates={}
    dates["yesterday"]=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d")
    dates["yesterdayepoch"]=time.mktime(time.strptime(dates["yesterday"],"%Y%m%d"))
    dates["dailyterm"]=(datetime.datetime.now()-datetime.timedelta(days=(DAILY_STORE_TERM+1))).strftime("%Y%m%d")
    dates["weeklyterm"]=(datetime.datetime.now()-datetime.timedelta(days=(WEEKLY_STORE_TERM+1))).strftime("%Y%m%d")

    local={"location": "local", "dir_include": LOCAL_INCLUDE, "dir_exclude": LOCAL_EXCLUDE}
    client={"location": "client", "dir_include": CLIENT_INCLUDE, "dir_exclude": CLIENT_EXCLUDE}

    for name in [local,client]:
        backup(name,dates,term)

    if term=="weekly":
        mysqlbackup(dates)
