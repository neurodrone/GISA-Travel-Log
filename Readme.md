GISA Travel log
===============

GISA Travel log is an small automation tool that emails the students 
confirmation about their filled in details announcing their
time and date of arrival. It uses Gdata API to read and extract
the data from Google Docs. 

It reads the data provided within 'skeleton.txt' and then attempts
to modify the data appropriately to generated personalized e-mails
for every new student.

It also persistently stores the number of students mailed till 
date so as to ensure that every time the script is ran, only
the newly added entries are sent confirmation e-mails.

Getting way too tired of simply copy-pasting stuff and pressing
'send' can have its own share of terrible outcomes. (: