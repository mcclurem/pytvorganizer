#!/usr/bin/env python
"""
main.py

Created by Morgan Mcclure on 2010-08-22.
Copyright (c) 2010 Morgan McClure.
"""

import sys
import getopt
import pycurl
from StringIO import StringIO

APIKEY="92C6A6742D538A23"

help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg



class TVDB(object):
    def __init__(self):
        self.apikey="92C6A6742D538A23"
        self.fetch("http://www.thetvdb.com/api/GetSeries.php?seriesname=Futurama")
        self.zipMirror = "http://www.thetvdb.com"
        self.get_series_data(73871)
        return
        
        self.mirrorurl = "http://www.thetvdb.com/api/%s/mirrors.xml" % self.apikey
        self.fetch(self.mirrorurl)
        self.currentTime = self.fetch("http://www.thetvdb.com/api/Updates.php?type=none")
        self.get_series_blurb("Family+Guy")

    
    def get_series_data(self, seriesID):
        self.fetch("%s/api/%s/series/%s/all/en.zip" % (self.zipMirror, self.apikey, seriesID) )
    
    def get_series_blurb(self, seriesname):
        return self.fetch("http://www.thetvdb.com/api/GetSeries.php?seriesname=%s" % seriesname)
    
    def fetch(self, url):
        resultBuffer = open('./foo.zip', 'w')
        #resultBuffer = StringIO()
        mycurl = pycurl.Curl()

        mycurl.setopt(pycurl.URL, url)
        mycurl.setopt(pycurl.WRITEFUNCTION, resultBuffer.write)
        mycurl.perform()
        mycurl.close()
        
        resultBuffer.close()
        return
        
        #print mycurl.answered()
        resultBuffer.seek(0)
        print resultBuffer.readlines()
        resultBuffer.seek(0)
        return resultBuffer.readlines()



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
