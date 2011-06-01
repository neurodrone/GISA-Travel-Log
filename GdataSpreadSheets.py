#!/usr/bin/python
#
# Codefile: GdataSpreadsheets.py
# Author: vaibhav@bhembre
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

class SpreadSheetOps:
	def __init__(self, email, passwd):
		self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
		self.gd_client.email = email
		self.gd_client.password = passwd
		self.gd_client.source = 'GISA-travel_log-1'
		self.curr_key = ''
		self.curr_wksht_id = ''
		self.gd_client.ProgrammaticLogin()
	
	def getContentsList(self, spname, val):
		feed = self.gd_client.GetSpreadsheetsFeed()
		ip = self.getFeedId(feed, spname)
		if (ip < 0): 
			print 'Spreadsheet named \'' + spname + '\' doesn\'t exist. Please try again.\nExiting.'
			sys.exit(2)
		id_parts = feed.entry[ip].id.text.split('/')
		self.curr_key = id_parts[len(id_parts)-1]
		feed = self.gd_client.GetWorksheetsFeed(self.curr_key)
		id_parts = feed.entry[0].id.text.split('/')
		self.curr_wksht_id = id_parts[len(id_parts)-1]
		feed = self.gd_client.GetListFeed(self.curr_key, self.curr_wksht_id)
		
		for i, entry in enumerate(feed.entry):
			if isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
				if (i == val):
					return entry.custom
		return {}
		
	def PrintListSpreadsheets(self):
		### Get the list of spreadsheets attached to the given account and print them.
		feed = self.gd_client.GetSpreadsheetsFeed()
		self.Printfeed(feed)
		_name = raw_input('\nSelect: ')
		ip = self.getFeedId(feed, _name)
		if (ip < 0): 
			print 'Spreadsheet named \'' + _name + '\' doesn\'t exist. Please try again.\nExiting.'
			sys.exit(2)
		id_parts = feed.entry[ip].id.text.split('/')
		self.curr_key = id_parts[len(id_parts)-1]
		self.PrintListWorksheets()
	
	def PrintListWorksheets(self):
		### Get the list of worksheets present within the selected Spreadsheet
		feed = self.gd_client.GetWorksheetsFeed(self.curr_key)
		self.Printfeed(feed)
		ip = raw_input('\nSelect: ')
		id_parts = feed.entry[string.atoi(ip)].id.text.split('/')
		self.curr_wksht_id = id_parts[len(id_parts)-1]
		self.PrintList()
		
	def PrintList(self):
		### Print list
		feed = self.gd_client.GetListFeed(self.curr_key, self.curr_wksht_id)
		self.Printfeed(feed)
		
		
	def Printfeed(self, feed):
		for i, entry in enumerate(feed.entry):
			if isinstance(feed, gdata.spreadsheet.SpreadsheetsCellsFeed):
				print 'Cell feed: %s %s\n' % (entry.title.text, entry.content.text)
			elif isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
				print 'List feed: %s %s %s' % (i, entry.title.text, entry.content.text)
				print 'Contents:'
				for key in entry.custom:
						print '%s: %s' % (key, entry.custom[key].text)
				print '\n',
			else:
				print 'Generic: %s %s\n' % (i, entry.title.text)
				
	def getFeedId(self, feed, name):
		for i, entry in enumerate(feed.entry):
			if (entry.title.text == name):
				return i;
		return -1;

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "", ['user=', 'pwd='])
	except getopt.error, msg:
		print 'Incorrect format\n'
		print './GdataSpreadSheets.py --user <username> --pwd <password>'
		sys.exit(2)
	
	user = ''
	passwd = ''
	for o, a in opts:
		if o == "--user":
			user = a
		elif o == "--pwd":
			passwd = a
	
	if user == '' or passwd == '':
		print './GdataSpreadSheets.py --user=<username> --pwd=<password>'
		sys.exit(2)
	
	sampleWorksheet = SpreadSheetOps(user, passwd)
	for inp in range(1,20):
		contentsList = sampleWorksheet.getContentsList('GISA - Travel Log for UB Fall 2011', inp)
		if not contentsList:
			print 'No records found for ' + str(inp)
		else:
			print 'Contents:'
			for key in contentsList:
				print '%s: %s' % (key, contentsList[key].text)
	#sampleWorksheet.PrintListSpreadsheets()

if __name__ == '__main__':
	main()
	
			