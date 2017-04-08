import MySQLdb
import csv
from datetime import datetime
import sys

# variable declaration
dbserver='localhost'
dbname='VM'
dbuser='root'
dbpass='p@55w0rd'
nessusfile='parsed.csv'
errorfile='VMDB_error.log'

#Open database connection
db=MySQLdb.connect(dbserver,dbuser,dbpass,dbname)
cursor=db.cursor()
ferr=open(errorfile,'w')

#Function to insert values to database
def insert(record):
	query='insert into live values("'+record[0]+'","'+record[1]+'","'+record[2]+'","'+record[3]+'","'+record[4]+'","'+record[5]+'","'+record[6]+'","'+record[7]+'","'+record[8]+'")'
	cursor.execute(query)
	try:
		db.commit()
	except:
		db.rollback()
		etype, evalue, etraceb =sys.exec_info()
		error.write(datetime.now()+' '+record[4]+' Plugin ID:'+record[0]+' '+evalue+'.\n')

#Function to update values to database
def update(record):
	query='select * from live where plugin ="'+record[0]+'" and ip_addr="'+record[4]+'"'
	cursor.execute(query)
	data=cursor.fetchall()
	if data:
		if data[0][8]<datetime.strptime(record[8],'%Y-%m-%d %H:%M:%S'): #Update existing record
			query='delete from live where plugin="'+record[0]+'" and ip_addr="'+record[4]+'"'
			cursor.execute(query)
			try:
				db.commit()
			except:
				db.rollback()
				etype, evalue, etraceb = sys.exec_info()
				error.write(datetime.now()+' '+record[4]+' Plugin ID:'+record[0]+' '+evalue+'\n')
			insert(record)
	else:
		insert(record) #Insert new plugin record
	data=None

#Get unique IP Addresses from db
cursor.execute('select distinct ip_addr from live')
data=cursor.fetchall()
IPs=[]
for IP in data:
	IPs.append(IP[0])
data=None

#check if IP address is already present in records
with open(nessusfile,'r') as scanresults:
	reader=csv.reader(scanresults,delimiter=',',quotechar='"')
	for rec in reader:
		if rec[4] in IPs:
			update(rec)
		else:
			insert(rec) #insert new IP record
db.close()
scanresults.close()
ferr.close()
