#!D:\WebTools\Python\python.exe

print 'Content-type: text/html\n'

import cgitb
import MySQLdb

cgitb.enable()

conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8')
conn.cursorclass = MySQLdb.cursors.DictCursor
curs = conn.cursor()

print """
<html>
  <head>
    <title>The FooBar Bulletin Board</title>
  </head>
  <body>
    <h1>The FooBar Bulletin Board</h1>
    """

curs.execute('select * from messages')
rows = curs.fetchall()

toplevel = []
children = {}

for row in rows:
    parent_id = row['reply_to']
    if parent_id is None:
        toplevel.append(row)
    else:
        children.setdefault(parent_id, []).append(row)

def format(row):
    print '<p><a href="view.cgi?id=%(id)i">%(subject)s</a></p>' % row
    try: kids = children[row['id']]
    except KeyError: pass
    else:
        print '<blockquote>'
        for kid in kids:
            format(kid)
        print '</blockquote>'

print '<p>'
for row in toplevel:
    format(row)
print """
    </p>
    <hr />
    <p><a href='edit.cgi'>Post message</a></p>
  </body>
</html>
"""