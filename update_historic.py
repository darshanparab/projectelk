import MySQLdb
import csv
import sys
from datetime import datetime

dbserver='localhost'
dbuser='root'
dbpass='p@55w0rd'
dbname='VM'
errorfile='historic_error.log'

db = MySQLdb.connect(dbserver,dbuser,dbpass,dbname)
cursor = db.cursor()
with open('parsed.csv','r') as csvfile:
	reader=csv.reader(csvfile,delimiter=',',quotechar='"')
	for rec in reader:
		query='insert into historic values("'+rec[0]+'","'+rec[1]+'","'+rec[2]+'","'+rec[3]+'","'+rec[4]+'","'+rec[5]+'","'+rec[6]+'","'+rec[7]+'","'+rec[8]+'")'
		cursor.execute(query)
try:
	db.commit()
except:
	db.rollback()
	etype,evalue,etraceb=sys.exec_info()
	ferr.write(datetime.now()+' '+evalue)

db.close()
csvfile.close()
