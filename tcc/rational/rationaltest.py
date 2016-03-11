#!/usr/bin/env python
#================================================================
# rationaltest:  A test driver for the rational.py module.
#----------------------------------------------------------------

import sys
from rational import *

def main():
    """
    """
    generalTests()
    mixedTests()
    errorTests()

def generalTests():
    """Test basic functionality
    """
    print "  -- Ambition/distraction/uglification/derision"
    third=Rational(1,3)
    print "Should be 1/3:", third
    fifth=Rational(1,5)
    print "Should be 1/5:", fifth
    print "Should be 8/15:", third + fifth
    print "Should be 1/15:", third * fifth
    print "Should be 2/15:", third-fifth
    print "Should be 3/5:", fifth/third

    print "  -- float()"
    print "Should be 0.2:", float(fifth)
    print "Should be 0.3333...:", float(third)

def mixedTests():
    """Test the .mixed() method cases
    """
    print "  -- mixed()"
    badPi = Rational(22,7)
    print "Should be '3 and 1/7':", badPi.mixed()

    properFraction = Rational(3,5)
    print "Should be 3/5:", properFraction.mixed()

    wholeNum  =  Rational ( 8,2 )
    print "Should be 4:", wholeNum.mixed()

    zero  =  Rational(0,1)
    print "Should be 0:", zero.mixed()

def errorTests():
    """Test error conditions
    """
    try:
        badIdea = Rational ( 5, 0 )
        print "Fail: didn't detect zero denominator."
    except ZeroDivisionError, detail:
        print "Pass: Zero denominator blowed up real good."

#================================================================
# Epilogue
#----------------------------------------------------------------

if __name__ == "__main__":
    main()

