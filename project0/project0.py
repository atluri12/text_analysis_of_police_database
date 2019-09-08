import PyPDF2
import tempfile
import urllib.request
import re
import sqlite3
from sqlite3 import Error
import random

def dataDownload(url):
        #Function to download the bytes data from the url given and store in a temporary file
        rawData = urllib.request.urlopen(url).read()
        tempFile = tempfile.TemporaryFile()
        tempFile.write(rawData)
        return tempFile

def dataExtract(tempFile):
        #Function to extract the data from pdf file and parse the data into the form of rows
	pageData = PyPDF2.PdfFileReader(tempFile).getPage(0).extractText()
	pageData = re.sub(' \n', ' ', pageData)
	pageData = pageData.split(';')
	del pageData[len(pageData)-1]
	pageData[0] = pageData[0].split('\n')
	pageData[0] = pageData[0][12:]
	pageData[0] = "\n".join(pageData[0])
	for i in range(len(pageData)):
		pageData[i] = pageData[i].strip().split('\n')
		if(pageData[i][6] != 'HOMELESS'):
			address = ', '.join(pageData[i][6:10])
			pageData[i][6:10] = [address]
	return pageData

def dbCreate():
        #Function to create a database and a table arrests within the database
	try:
		database = 'normanpd.db'
		dbase = sqlite3.connect(database)
		point = dbase.cursor()
		dropQuery = 'DROP TABLE IF EXISTS arrests;'
		createQuery = 'CREATE TABLE IF NOT EXISTS arrests (arrest_time TEXT, case_number TEXT, arrest_location TEXT, offense TEXT, arrestee_name TEXT, arrestee_birthday TEXT, arrestee_address TEXT, status TEXT, officer TEXT);'
		point.execute(dropQuery)
		point.execute(createQuery)
		dbase.commit()
		return database
	except Error as err:
		print(err)

def dbInsert(db, incidents):
        #Function to insert the rows into the table created in the database
	dbase = sqlite3.connect(db)
	point = dbase.cursor()
	insertQuery = 'INSERT INTO arrests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'
	for i in range(len(incidents)):
		point.execute(insertQuery, incidents[i])
	dbase.commit()

def dbStatus(db):
        #Function to print one random row from the database
	dbase = sqlite3.connect(db)
	point = dbase.cursor()
	point.execute('SELECT COUNT(*) FROM arrests;')
	count = point.fetchone()
	itemCount = random.randint(0, count[0]-1)
	point.execute('SELECT * FROM arrests;')
	items = point.fetchall()
	randomItem = "\u00FE".join(items[itemCount])
	print(randomItem)
	return randomItem
