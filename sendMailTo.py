#!/usr/bin/python
#
# Codefile: sendMailTo.py
# Author: vaibhav@bhembre.com
#
# The purpose of this script is to mail the respective students ranging between a
# given interval (x, y) asking them to confirm their details which they have filled
# in the online form.
# The interval will be specified, inclusively, by two row numbers of the corresponding 
# worksheet arranged in an ascending order.

__author__ = 'vaibhav@bhembre.com (Vaibhav Bhembre)'

import smtplib
import getopt, sys
import string
from GdataSpreadSheets import SpreadSheetOps


subject = 'GISA - Travel Log Update - Fall 2011' #Change the subject to suit the year. 
docname = 'GISA - Travel Log for UB Fall 2011'	#Change the spreadsheet name if you want to.

def getUserPass():
	try:
		optlist, args = getopt.getopt(sys.argv[1:], "u:p:")
	except getopt.GetoptError, err:
		print 'Usage: ./sendMailTo.py -u <email@gmail.com> -p <password>'
		sys.exit(2)
	email = ''
	passwd = ''
	for i, a in optlist:
		if (i == '-u'):
			email = a
		elif (i == '-p'):
			passwd = a
	if (email == '' or passwd == ''):
		print 'Usage: ./sendMailTo.py -u <email@gmail.com> -p <password>'
		sys.exit(2)
		
	return (email, passwd)

def sendmail(to, subject, msg):
	user, passwd = getUserPass()
	smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo()
	smtpserver.login(user, passwd)
	header = 'To:' + ','.join(to) + '\nFrom:' + user + '\nSubject:' + subject + '\n\n'
	finmsg = header + msg + '\n'
	
	smtpserver.sendmail(user, to, finmsg)
	print 'Sent message to ' + ','.join(to) + '!'
	smtpserver.close()
	
def buildMessage(file, contentsList):
	f = open(file, 'r')
	finstr = f.read()
		
	strDear = 'Dear'
	strHomeAddress = 'Home Address in India:'
	strContactInd = 'Contact No. in India:'
	strContactUS = 'Contact No. in USA:'
	strTimeofArr = 'Time of Arrival:'
	strDateofArr = 'Date of Arrival:'
	strFlight = 'Flight name:'
	strEmail = 'E-mail:'
	finstr = string.replace(finstr, strDear, strDear + ' ' + contentsList["fullname"].text + ',')
	finstr = string.replace(finstr, strHomeAddress, wrapStr(strHomeAddress) + '\n' + str(contentsList["homeaddressindia"].text))
	finstr = string.replace(finstr, strContactInd, wrapStr(strContactInd) + ' ' + str(contentsList["contactno.india"].text))
	finstr = string.replace(finstr, strContactUS, wrapStr(strContactUS) + ' ' + str(contentsList["contactno.usa"].text))
	finstr = string.replace(finstr, strTimeofArr, wrapStr(strTimeofArr) + ' ' + contentsList["timeofarrival"].text + ' hours.')
	finstr = string.replace(finstr, strDateofArr, wrapStr(strDateofArr) + ' ' + contentsList["dateofarrival"].text + ' [mm/dd/yy]')
	finstr = string.replace(finstr, strFlight, wrapStr(strFlight) + ' ' + contentsList["flightnameno."].text)
	finstr = string.replace(finstr, strEmail, wrapStr(strEmail) + ' ' + contentsList["emailveryimportant"].text)
	
	f.close()
	return finstr

def wrapStr(strname):
	return '' + strname + '--   '

def main():
	f = open('mailedtillnowcount.txt', 'r+')
	user, passwd = getUserPass()
	sampleWorksheet = SpreadSheetOps(user, passwd)
	
	inp = string.atoi(f.readline())
	f.close()
	while(1):
		to = []
		contentsList = sampleWorksheet.getContentsList(docname, inp)
		if not contentsList:
			print 'No records found for No. ' + str(inp)
			print 'Exiting.'
			break
		msg = buildMessage('skeleton.txt', contentsList)
		to.append(contentsList["emailveryimportant"].text)
		sendmail(to, subject, msg)
		inp += 1
	f = open('mailedtillnowcount.txt', 'w')
	f.write(str(inp))
	f.close()
	

if __name__ == '__main__':
	main()