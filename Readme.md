GISA Travel log
===============

GISA Travel log is an small automation tool that emails the students 
confirmation about their filled in details announcing their
time and date of arrival. It uses [Gdata API](http://code.google.com/apis/gdata/docs/directory.html) to read and extract
the data from [Google Docs](http://docs.google.com). 

It reads the data provided within 'skeleton.txt' and then attempts
to modify the data appropriately to generated personalized e-mails
for every new student.

It also persistently stores the number of students mailed till 
date so as to ensure that every time the script is ran, only
the newly added entries are sent confirmation e-mails.

Getting way too tired of simply copy-pasting stuff can have 
its own share of terrible outcomes. (:

	Usage: ./sendMailTo.py -u <email@gmail.com> -p <password>

Link to the my designed website:

	http://gsa.buffalo.edu/gisa/new