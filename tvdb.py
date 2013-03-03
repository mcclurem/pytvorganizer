#!/usr/bin/env python

import pycurl
from StringIO import StringIO

APIKEY="92C6A6742D538A23"

class TVDB(object):
    def __init__(self, apikey):
        self.apikey=apikey
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
