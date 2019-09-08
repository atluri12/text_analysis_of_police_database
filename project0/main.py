import argparse

import random

import project0

def main(url):
	#Download Data
        tempFile = project0.dataDownload(url)

        #Extract Data
        incidents = project0.dataExtract(tempFile)

	#Create Database
        db = project0.dbCreate()

	#Insert Data
        project0.dbInsert(db, incidents)

	#Print Status
        item = project0.dbStatus(db)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--arrests", type = str, required = True, help = "The arrest summary url.")

	args = parser.parse_args()
	if args.arrests:
		main(args.arrests)

