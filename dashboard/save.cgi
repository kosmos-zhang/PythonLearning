#!D:\WebTools\Python\python.exe

print 'Content-type: text/html\n'

import cgitb
import MySQLdb

cgitb.enable()

conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
conn.cursorclass = MySQLdb.cursors.DictCursor
curs = conn.cursor()

import cgi, sys
form = cgi.FieldStorage()

def quote(string):
    if string:
        return string.replace("'", "\\'")
    else:
        return string

sender = quote(form.getvalue('sender'))
subject = quote(form.getvalue('subject'))
text = quote(form.getvalue('text'))
reply_to = quote(form.getvalue('reply_to'))

if not (sender and subject and text):
    print 'Please supply sender, subject, and text'
    sys.exit()

if reply_to is not None:
    query = """
        insert into messages(reply_to, sender, subject, text)
        values(%i, '%s', '%s', '%s')""" % (int(reply_to), sender, subject, text)
else:
    query = """
        insert into messages(sender, subject, text)
        values('%s', '%s', '%s')""" % (sender, subject, text)

curs.execute(query)
conn.commit()

print """
<html>
  <head>
    <title>Message Saved</title>
  </head>
  <body>
    <h1>Message Saved</h1>
    <hr />
    <a href='main.cgi'>Back to the main page</a>
  </body>
</html>
"""