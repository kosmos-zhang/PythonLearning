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
id=form.getvalue('id')

print """
<html>
  <head>
    <title>View Message</title>
  </head>
  <body>
    <h1>View Message</h1>
    """

try: id=int(id)
except:
    print 'Invalid message ID'
    sys.exit()

curs.execute('select * from messages where id=%i' % id)
rows = curs.fetchall()

if not rows:
    print 'Unknown message ID'
    sys.exit()

row = rows[0]

print """
    <p>
      <b>Subjects:</b>%(subject)s<br/>
      <b>Sender:</b>%(sender)s<br/>
      <pre>%(text)s</pre>
    </p>
    <hr />
    <a href='main.cgi'>Back to the main page</a>
     | <a href='edit.cgi?reply_to=%(id)s'>Reply</a>
  </body>
</html>
""" % row