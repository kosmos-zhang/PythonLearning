#!/usr/local/bin/python
#--
# pigfiles.py:  A script to list all the files in a directory tree
#   in descending order by file size, with full pathname.
#--

import sys
import os
import pathinfo

class Pig(pathinfo.PathInfo):
    """Container for a PathInfo object, and a path
    """
    def __cmp__ ( self, other ):
        compare  =  - cmp ( self.size(), other.size() )
        if compare != 0:
            return compare
        else:
            return cmp ( self.path, other.path )

    def __str__ ( self ):
        return "%s %10s %s" % ( self._modTime(), self.size(), self.path )

#--
# Procedures for pigfiles.py
#--

# - - -   V i s i t o r   - - -

def Visitor ( arg, dirName, nameList ):
    info = Pig ( dirName )
    files.append ( info )   # Append directory entry
#--
# Append entries for all included names that are not themselves
# directories
#--
    for fileName in nameList:
        info = Pig ( os.path.join ( dirName, fileName ) )
        if info.isFile():
            files.append ( info )


# - - -   p i g f i l e s . p y   - -   m a i n   - - -

files = []      # List of Pig objects, one per dir. or file

try:
    root = sys.argv[1]  # First command line argument = directory name
except:
    root = "."          # Default is current directory

#--
# Build a list of Pig objects for all directories and files
#--

os.path.walk ( root, Visitor, None )

files.sort()        # Sort using builtin cmp() method

for pig in files:
    print pig
