#!/usr/bin/env python
"""
main.py

Created by Morgan Mcclure on 2010-08-22.
Copyright (c) 2010 Morgan McClure.
"""

import sys
import getopt


help_message = '''
The help message goes here.
'''


def 

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg






def main(argv=None):
    
    foo = TVDB()
    sys.exit(0)
    
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:vd:", ["help", "output=", "directory="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option in ("-d", "--directory"):
                directory = value
             
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
