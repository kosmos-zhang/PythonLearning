#!/usr/local/bin/python
#--
# oldfiles.py:  A script to list all the files in a directory tree
#   in descending order by file size, with full pathname.
#--

import sys
import os
import pathinfo
import stat

class Old(pathinfo.PathInfo):
    """Container for a PathInfo object, and a path
    """
    def __cmp__ ( self, other ):
        compare  =  - cmp ( self.status[stat.ST_MTIME],
                            other.status[stat.ST_MTIME] )
        if compare != 0:
            return compare
        else:
            return cmp ( self.path, other.path )

    def __str__ ( self ):
        return "%s %10s %s" % ( self.modTime(), self.size, self.path )

#--
# Procedures for oldfiles.py
#--

# - - -   V i s i t o r   - - -

def Visitor ( arg, dirName, nameList ):
    info = Old ( dirName )
    files.append ( info )   # Append directory entry
#--
# Append entries for all included names that are not themselves
# directories
#--
    for fileName in nameList:
        info = Old ( os.path.join ( dirName, fileName ) )
        if info.isFile():
            files.append ( info )


# - - -   p i g f i l e s . p y   - -   m a i n   - - -

files = []      # List of Old objects, one per dir. or file

try:
    root = sys.argv[1]  # First command line argument = directory name
except:
    root = "."          # Default is current directory

#--
# Build a list of Old objects for all directories and files
#--

os.path.walk ( root, Visitor, None )

files.sort()        # Sort using builtin cmp() method

for old in files:
    print old
