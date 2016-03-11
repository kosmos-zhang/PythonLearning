#!/usr/local/bin/python
#--
"""pinemerge.py  $Revision: 1.7 $  $Date: 1997/09/30 23:09:17 $

Author:
    John W. Shipman (john@nmt.edu), New Mexico Tech
    Computer Center, Socorro, NM 87801.  This program is in the
    public domain.

Purpose:

    Merges two or more Pine address books.

    Command line arguments:

        pinemerge file1 file2 ...

    A merged address book is written to stdout.  Errors may be
    written to stderr.

    For any address that whose nickname is in multiple files but
    is not the same in all other fields, the first-named file
    wins, and information about the winners and losers is written
    to stderr.

References:
    The Pine address book format is document at the Pine
    Information Center, http://www.washington.edu/pine/.  Refer
    to the ``Technical Notes'' page, more specifically:

        http://www.washington.edu/pine/tech-notes/low-level.html#addrbook

    This software includes intended functions for Cleanroom
    verification.  For more information on this methodology,
    see http://www.nmt.edu/~shipman/soft/clean/.
"""

import sys, string, types


# - - - - -   C l a s s   A d d r B o o k   - - - - -

class AddrBook:
    """Address book object

        Each instance represents one complete Pine address book.

        Exports:
            AddrBook ( fileName )
                [ if fileName is None ->
                    return a new, empty AddrBook object
                  if fileName is a string ->
                    if fileName names a readable, valid Pine address
                    book ->
                      return a new AddrBook object representing
                      the entries from that file
                    else ->
                      <stderr>  :=  error message(s)
                      raise IOError
                ]
            .insert ( a )
                [ if a is an Address object ->
                    if there is no entry for a's nickname in self ->
                      self  :=  self with a added
                    else ->
                      raise ValueError
                ]
            .write ( outFile )
                [ if outFile is a writeable file ->
                    outFile  +:=  self in Pine address book format,
                                  with entries in ascending order
                                  by (full name+nickname)
                ]
            .nickMap ==
              a dictionary mapping each nickname to the corresponding
              Address object
    """

# - - -   _ _ i n i t _ _   - - -

    def __init__ ( self, fileName=None ):
        """Constructor function for AddrBook
        """
        #-- 1 --
        self.nickMap  =  { }

        #-- 2 --
        #-[ if fileName is None -> I
        #   else ->
        #     if fileName names a readable, valid Pine address book ->
        #       self.nickMap  :=  entries mapping each nickname to the
        #                         corresponding Address object
        #     else ->
        #       sys.stderr  +:=  error message
        #       raise IOError
        #-]
        if fileName is not None:
            self.__readFile ( fileName )


# - - -   i n s e r t   - - -

    def insert ( self, address ):
        if self.nickMap.has_key ( address.nickname ):
            raise ValueError
        else:
            self.nickMap[address.nickname]  =  address


# - - -   w r i t e   - - -

    def write ( self, outFile ):
        #-- 1 --
        #-[ L  :=  a list of all the Address objects in self
        #-]
        L = self.nickMap.values ( )

        #-- 2 --
        #-[ L  :=  L, sorted by (fullName+nickname)
        #-]
        L.sort()

        #-- 3 --
        #-[ outFile  +:=  the elements of L as rendered by their str() methods
        #-]
        for a in L:
            outFile.write ( str ( a ) + "\n" )


# - - -   _ _ r e a d F i l e   - - -

    def __readFile ( self, fileName ):
        """Function to read a Pine address book.
            [ if fileName is a string ->
                if fileName names a readable, valid Pine address book ->
                  self.nickMap  :=  entries mapping each nickname to the
                                    corresponding Address object
                else ->
                  sys.stderr  +:=  error message
                  raise IOError
            ]
        """
        #-- 1 --
        #-[ if fileName can be opened for reading ->
        #     inFile  :=  fileName opened for reading
        #   else ->
        #     sys.stderr  +:=  error message
        #     raise IOError
        #-]
        try:
            inFile  =  open ( fileName, "r" )
        except:
            sys.stderr.write ( "Can't open file `" + fileName +
                               "' for reading.\n" )
            raise IOError, "Can't open Pine address book."

        #-- 2 --
        #-[ L  :=  a list of the lines in file inFile, with line
        #          terminators intact, and continuation lines
        #          (those that start with one or more spaces)
        #          attached to previous lines
        #-]
        L  =  self.__unfoldInput ( inFile )

        #-- 3 --
        #-[ if L represents a valid Pine address book as a list
        #   of lines ->
        #     self.nickMap  +:=  entries mapping each nickname from L
        #                        to the corresponding Address object
        #   else ->
        #     sys.stderr  +:=  error message(s)
        #     raise IOError
        #-]
        self.__processList ( L )

        #-- 4 --
        inFile.close ( )
        return self

# - - -   _ _ u n f o l d I n p u t   - - -

    def __unfoldInput ( self, inFile ):
        """Reads and ``unfolds'' input.
            [ if inFile is a readable file object ->
                return the contents of that file as a list of lines,
                with continuation lines (those that start with one or
                more spaces) reassembled to make one long line for
                each entry
            ]
        """
        #-- 1 --
        #-[ foldedList  :=  the lines of inFile represented as a list
        #                   of strings with their line terminators intact
        #-]
        foldedList  =  inFile.readlines ( )

        #-- 2 --
        result  =  []

        #-- 3 --
        #-[ result  +:=  the lines of foldedList, with continuations
        #                reassembled and all line terminators removed
        #-]
        while  len ( foldedList ) > 0:
            #-- 3 body --
            #-[ foldedList  :=   foldedList with its first line removed
            #                    and all following lines that start with
            #                    at least one space
            #   result      +:=  contents of the first line from foldedList,
            #                    without its line terminator, followed by
            #                    the contents of any continuations trimmed
            #                    of their leading spaces and trailing line
            #                    terminators
            #-]
            result.append ( self.__trimGroup ( foldedList ) )

        #-- 4 --
        return result


# - - -   _ _ t r i m G r o u p   - - -

    def __trimGroup ( self, L ):
        """Method to remove the next line from L with its continuations.
            [ if L is a nonempty list of strings ->
                L  :=  L with its first element removed and all following
                       lines that start with at least one space
                return a string containing the first element of L without
                its line terminator, followed by the contents of any
                continuations trimmed of their leading spaces and trailing
                line terminators
            ]
        """
        #-- 1 --
        #-[ result  :=  the first element of L with its line terminator
        #               removed     
        #   L       :=  L with its first element removed
        #-]
        result  =  self.__termStrip(L[0])
        del L[0]

        #-- 2 --
        #-[ if L begins with a line that starts with a space ->
        #     result  +:=  concatenation of all leading lines from L that
        #                  start with spaces, but with leading spaces
        #                  and line terminators removed
        #   else -> I
        #-]
        while ( ( len ( L ) > 0 ) and
                ( len ( L[0] ) > 0 ) and
                ( L[0][0] == " " ) ):
            #-- 2 loop --
            #-[ result  +:=  contents of L[0] without leading spaces or
            #                line terminators
            #-] L       :=   L with its first element removed
            result  =  result + string.lstrip ( self.__termStrip ( L[0] ) )
            del L[0]

        #-- 3 --
        return result


# - - -   _ _ t e r m S t r i p   - - -

    def __termStrip ( self, S ):
        """Remove the line terminator from S.
            [ if S is a string ->
                if S ends with a linefeed ->
                  return S without its last character
                else ->
                  return S
            ]
        """
        if ( ( len ( S ) > 0 ) and
             ( S[-1] == "\n" ) ):
            return S[:-1]
        else:
            return S


# - - -   _ _ p r o c e s s L i s t   - - -

    def __processList ( self, L ):
        """Parse the lines of a Pine address book.
            [ if L is the address book as a list of long (not folded)
              lines ->
                if L represents a valid Pine address book ->
                  self.nickMap  +:=  entries mapping each nickname
                                     from L to the corresponding
                                     Address object
                else ->
                  sys.stderr  +:=  error message(s)
                  raise IOError
            ]
        """
        #-- 1 --
        anyError  =  0

        #-- 2 --
        #-[ if L contains no errors ->
        #     self.nickMap  +:=  entries mapping nicknames from L to
        #                        the corresponding Address objects
        #   else ->
        #     self.nickMap  +:=  entries mapping valid nicknames from L to
        #                        the corresponding Address objects
        #     sys.stderr    +:=  error message(s)
        #     anyError      :=   1
        #-]
        for line in L:
            #-- 2 loop --
            #-[ if line contains an error ->
            #     sys.stderr  +:=  error message(s)
            #     anyError    :=   1
            #   else ->
            #     self.nickMap  +:=  an entry mapping the nickname from
            #                        line to an Address object representing
            #                        line
            #-]
            anyError  =  anyError or self.__parseAddressLine ( line )

        #-- 3 --
        if anyError:
            raise IOError, "Errors in the address book"


# - - -   _ _ p a r s e A d d r e s s L i n e   - - -

    def __parseAddressLine ( self, line ):
        """Parses one address book entry (as a reunified, long line).
            [ if line is a valid address line in the context of self ->
                self.nickMap  +:=  an entry mapping the nickname from
                                   line to an Address object representing
                                   that line
                return 0
              else ->
                sys.stderr  +:=  error message(s)
                return 1
            ]
        """
        #-- 1 --
        #-[ fields  :=  line, split on TAB characters
        #-]
        fields  =  string.split ( line, "\t" )

        #-- 2 --
        #-[ if fields has 3-5 parts ->
        #     nickname  :=  fields[0]
        #     fullName  :=  fields[1]
        #     email     :=  fields[2]
        #     fcc       :=  fields[3], or None if len(fields)<4
        #     comment   :=  fields[4], or None if len(fields)<5
        #   else ->
        #     sys.stderr  +:=  error message
        #     return 1
        #-]
        if  ( 3 <= len ( fields ) <= 5 ):
            nickname  =  fields[0]
            fullName  =  fields[1]
            email     =  fields[2]
            fcc       =  None
            comment   =  None
            if len(fields) > 3:
                fcc  =  fields[3]
                if len(fields) > 4:
                    comment  =  fields[4]

        else:
            sys.stderr.write ( "*** Lines should have 3-5 fields:\n" +
                               line + "\n" )
            return 1

        #-- 3 --
        address  =  Address ( nickname, fullName, email, fcc, comment )

        #-- 4 --
        #-[ if self.nickMap has a key (nickname) ->
        #     sys.stderr  +:=  error message
        #     return 1
        #   else -> I
        #-]
        if  self.nickMap.has_key ( nickname ):
            sys.stderr.write ( "*** Duplicate nickname:\n" +
                               line + "\n" )
            sys.stderr.write ( "*** Other nickname is for " +
                               self.nickMap[nickname].fullName + "\n" )
            return 1

        #-- 5 --
        self.nickMap[nickname]  =  address
        return 0


# - - - - -   C l a s s   A d d r e s s   - - - - -

class Address:
    """Address book entry object

        Each instance represents one entry in a Pine address book.

        Exports:
          Address ( nickname, fullName, address, fcc, comments )
            [ if (nickname is the nickname as a string without tabs)
              and (fullName is the full name as a string without tabs)
              and (address is the e-mail address as a string without tabs)
              and (fcc is the file-copy-to attribute as a string without
              tabs, or None)
              and (comments is a comments string without tabs, or None) ->
                return a new Address object with those attributes
            ]
          .show ( )
            [ returns a string containing the fields of self in
              a human-readable format
            ]
          .nickname     [ The nickname as a string ]
          .fullName     [ The full name as a string ]
          .address      [ The e-mail address as a string ]
          .fcc          [ The fcc attribute as a string, or None ]
          .comments     [ The comments as a string, or None ]
          .__str__()
            [ self, represented as a list of lines wrapped as per the
              Pine addressbook format, each line ending with newline
            ]
          .__cmp__()
            [ return cmp() value, using fullName as the major key
              and nickname as the minor key
            ]
    """

# - - -   _ _ i n i t _ _   - - -

    def __init__ ( self, nickname, fullName, address, fcc, comments ):
        """Constructor for Address
        """
        self.nickname  =  nickname
        self.fullName  =  fullName
        self.address   =  address
        self.fcc       =  fcc
        self.comments  =  comments


# - - -   . s h o w   - - -

    def show ( self ):
        return ( "%s (%s) %s" %
                 ( self.nickname, self.fullName, self.address ) )


# - - -   _ _ s t r _ _   - - -

    def __str__ ( self ):
        """Translate self to external form.
            [ return self as a list of strings, each ending with newline,
              such that the one-long-line form of self is broken on
              TABS, or commas in a distribution list
            ]
        """
        #-- 1 --
        outList  =  []

        #-- 2 --
        #-[ outList  :=  outList with self's nickname added
        #-]
        self.__addField ( outList, self.nickname + "\t" )

        #-- 3 --
        #-[ outList  +:=  TAB + self's fullname
        #-]
        self.__addField ( outList, self.fullName + "\t" )

        #-- 4 --
        #-[ outList  :=  outList with self's address added, followed by a TAB,
        #               and breaking address lists on commas if necessary
        #-]
        self.__breakAddress ( outList, self.address )
        
        #-- 5 --
        #-[ outList  :=  outList with self's fcc added, if any, followed by a
        #               TAB
        #-]
        if self.fcc is not None:
            self.__addField ( outList, "\t" + self.fcc )

        #-- 6 --
        #-[ outList  :=  outList with self's comments added, if any,
        #-]
        if self.comments is not None:
            self.__addField ( outList, "\t" + self.comments )

        #-- 7 --
        result  =  ""
        for i in range(len(outList)):
            result  =  result + outList[i] + "\n"
        result  =  result[:-1]
        return result


# - - -   _ _ c m p _ _   - - -

    def __cmp__ ( self, other ):
        """Compare function for address book entries.  Keys are:
            1. All non-list entries come before all list entries.
            2. Entries with fullnames are sorted by fullname.
            3. Entries without fullnames are sorted by nickname.
        """
        a1  =  ( self.address[0] == "(" )
        a2  =  ( other.address[0] == "(" )
        c   =  cmp ( a1, a2 )
        if  c <> 0:
            return c

        c  =  cmp ( string.upper ( self.fullName ),
                    string.upper ( other.fullName ) )
        if  c <> 0:
            return c

        return cmp ( string.upper ( self.nickname ),
                     string.upper ( other.nickname ) )



# - - -   _ _ a d d F i e l d _ _   - - -

    def __addField ( self, result, s ):
        """Add s to result list with folding on tabs
            [ if (result is empty) ->
                result  +:=  s
              else if ((last line of result + s) would exceed 50 chars) ->
                result  :=  result with ("   " + s appended)
              else ->
                result[-1]  +:=  s
            ]
        """
        if len ( result ) == 0:
            result.append ( s )
        elif ( len ( result[-1] ) + len ( s ) ) > 50:
            result.append ( "   " + s )
        else:
            result[-1]  =  result[-1] + s


# - - -   _ _ b r e a k A d d r e s s   - - -

    def __breakAddress ( self, result, address ):
        """Fold the address portion, breaking between commas.
        """
        brokenList  =  string.split ( address, "," )
        last        =  brokenList[-1]
        del brokenList[-1]

        for b in brokenList:
            self.__addField ( result, b + "," )

        self.__addField ( result, last )



# - - -   U s a g e   - - -

def Usage ( L ):
    """Write a usage message and terminate execution.
        [ if L is a string ->
            sys.stderr  +:=  L
            terminate execution
          if L is a list of strings ->
            sys.stderr  +:=  concatenation of elements of L
            terminate execution
        ]
    """
    if type ( L ) is types.ListType:
        L = string.join ( L, "" )

    if type ( L ) is not types.StringType:
        sys.stderr.write ( "*** Usage routine called with bogus "
                           "argument: " + str(L) + ".\n" )
        raise TypeError, "Bogus argument type to Usage()"
    
    sys.stderr.write ( "*** Usage:\n"
        "  pinemerge f1 f2 ...\n"
        "where f1, f2, ... are Pine addressbooks to be merged.\n" )
    sys.stderr.write ( "*** Error: " + L + "\n" )
    sys.exit ( 1 )


# - - - - -   p i n e m e r g e . p y   - -   m a i n   - - -

#--
# Create an empty address book.
#--

outBook  =  AddrBook ( )

#--
# Read each file named on the command line.  For each file,
# process it into an address book, then attempt to add 
# each entry to outBook.  Duplicates are flagged if any
# of the nickname/fullname/address fields differ.
#--

argList  =  sys.argv[1:]

if  len ( argList ) < 1:
    Usage ( "At least two address book files must be supplied." )

for fileName in argList:
    sys.stderr.write ( "=== Reading %s ===\n" % fileName )
    book  =  AddrBook ( fileName )

    for nickname in book.nickMap.keys():
        addr  =  book.nickMap[nickname]

        try:
            outBook.insert ( addr )
        except:
            other  =  outBook.nickMap[nickname]
            if ( ( addr.fullName <> other.fullName) or
                 ( addr.address <> other.address ) ):
                sys.stderr.write (
                  "\nDuplicate nickname, omitted:\n%s\n"
                  "Conflicts with:\n%s\n" %
                  ( addr.show(), other.show() ) )

#--
# Output the merged address book
#--

outBook.write ( sys.stdout )
