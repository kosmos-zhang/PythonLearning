#!D:\WebTools\Python\python.exe
"""#!/usr/bin/env python"""

print 'Content-type: text/html'

from os.path import join, abspath
import cgi, sys

BASE_DIR = abspath('data')

form = cgi.FieldStorage()
filename = form.getvalue('filename')
if not filename:
    print 'Please enter a file name'
    sys.exit()

text = open(join(BASE_DIR, filename)).read()

print """
<html>
  <head>
    <title>Editing...</title>
  </head>
  <body>
    <form action='save.cgi' method='POST'>
      <b>File:</b> %s <br />
      <input type='hidden' value='%s', name='filename' />
      <b>password:</b><br />
      <input name='password', type='password'/><br />
      <b>Text:</b><br />
      <textarea name='text' rows='20' cols='40'>%s</textarea><br />
      <input type='submit' value='Save' />
    </form>
  </body>
</html>
""" % (filename, filename, text)