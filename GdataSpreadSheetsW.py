#!/usr/bin/env python
#
# Codefile: GdataSpreadsheetsW.py
# Author: vaibhav@bhembre.com
#
# Description: Print a set of worksheets present within a desired spreadsheet. Provide 
# a function to output the entire contents of a particular row, the number of which
# is accepted as in input to it.


__author__ = 'vaibhav@bhembre.com (Vaibhav Bhembre)'

try:
	from xml.etree import ElementTree	
except ImportError:
	from elementtree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import getopt, sys
import string
from GdataSpreadSheets import SpreadSheetOps

todocName = 'GISA - Students from India'
fromdocName = 'GISA - Travel Log for UB Fall 2011'

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "u:p:n:", "")
	except getopt.error, msg:
		print 'Incorrect format.'
		usage()
		sys.exit(2)


	val = 0
	user = passwd = ''
	
	for o, a in opts:
		if o == '-u':
			user = a
		elif o == '-p':
			passwd = a
		elif o == '-n':
			val = a

	if (user == '' or passwd == ''):
		print "Incomplete input."
		usage()
		sys.exit(2)
	
	mywksht = SpreadSheetOps(user, passwd)
	currRow = string.atoi(val) - 2
	contentsList = mywksht.getContentsList(fromdocName, currRow)
	results = {}
	if not contentsList:
		print "No records found for Row: " + str(currRow)
	else:
		print "Contents:"
		for key in contentsList:
			print "%s %s." % (key, contentsList[key].text)	
			results[key] = contentsList[key].text
		print "Initiating insertion..."
		new_wksht = SpreadSheetOps(user, passwd)
		mywksht.ListInsertAction(todocName, results)

def usage():
	print "python " + sys.argv[0] + " -u <user@email> -p <password> [-n <row-no.>]"

if __name__ == '__main__':
	main()
