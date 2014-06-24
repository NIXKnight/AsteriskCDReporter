#!/usr/bin/env python
#
# AsteriskCDReporter v0.1
#
# Copyright (c) 2014 Saad Ali (NIXKnight)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import HTML
import time
import datetime
import MySQLdb
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

table = []
records = ""

def appendtable(count):
  global records
  global table
  callerid = str(records[count][0])
  calltime = str(records[count][1])
  sourcext = str(records[count][2])
  destinationxt = str(records[count][3])
  disposition = str(records[count][4])
  duration = str(records[count][5])
  row = [callerid, calltime, sourcext, destinationxt, disposition, duration]
  table.append(row)

def processcdr():
  global records
  date = time.strftime("%Y-%m-%d")
  timeformat = "%H:%i:%S"
  print "\nConnecting to database....\n\n"
  db = MySQLdb.connect(host="localhost", port=3306, user="ADD DATABASE USER HERE", passwd="ADD PASSWORD HERE", db="ADD DATABASE NAME HERE")
  cursor = db.cursor()
  cursor.execute("SELECT clid AS 'Caller ID',calldate AS 'Call Time',src AS 'Source',dst AS 'Destination',disposition AS 'Disposition',duration AS 'Duration' FROM asteriskcdrdb.cdr WHERE calldate = DATE_FORMAT(calldate, '%s %s')" % (date,timeformat))
  records = cursor.fetchall()
  recordscount = len(records)
  for count in range(recordscount):
    if len(records[count][2])|len(records[count][3]) == 4:
      appendtable(count)
    elif len(records[count][2])|len(records[count][3]) == 8:
      appendtable(count)
    elif len(records[count][2])|len(records[count][3]) == 9:
      appendtable(count)
    elif len(records[count][2])|len(records[count][3]) == 10:
      appendtable(count)
    elif len(records[count][2])|len(records[count][3]) == 11:
      appendtable(count)
  print "Disconnecting database....\n\n"
  db.close()

def sendemail():
  global table
  if table:
    html = HTML.table(table,header_row=['Caller ID', 'Call Time', 'Source', 'Destination', 'Disposition', 'Duration (Seconds)'])
    with open('email.html', 'w') as em:
      em.write(html)
    fromaddr = "ADD FROM ADDRESS HERE"
    toaddr = "ADD TO ADDRESS HERE"
    bcc = ['ADD BCC ADDRESS HERE']
    message = MIMEMultipart()
    message['From'] = "ADD FROM ADDRESS HERE"
    message['To'] = "ADD TO ADDRESS HERE"
    message['BCC'] = "ADD BCC ADDRESS HERE"
    message['Subject'] = "PBX Outbound/Inbound Call Report"
    email = file('email.html')
    attachment = MIMEText(email.read(),'html')
    message.attach(attachment)
    server = smtplib.SMTP('ADD SMTP SERVER HERE', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("ADD LOGIN ADDRESS HERE", "ADD PASSWORD HERE")
    text = message.as_string()
    print "sending email....\n\n"
    toaddrs = [toaddr] + bcc
    server.sendmail(fromaddr, toaddrs, text)

if __name__ == '__main__':
  processcdr()
  sendemail()
