#!/usr/bin/env python
import hashlib
import os
import re
from os import listdir
from os.path import  isdir
from glob import glob
from copy import copy

seasonEpisodeRegex = re.compile(r"s(\d+)e(\d+)", re.IGNORECASE)
seasonXEpisodeRegex = re.compile(r"(\d+)x(\d+)", re.IGNORECASE)

#Taken from stack overflow
class lazy_property(object):
    '''
    meant to be used for lazy evaluation of an object attribute.
    property should represent non-mutable data, as it replaces itself.
    '''
    def __init__(self,fget):
        self.fget = fget
        self.func_name = fget.__name__

    def __get__(self,obj,cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj,self.func_name,value)
        return value


class Directory(object):
    def __init__(self, directory):
        if not os.path.isdir(directory):
            raise Exception("Not a directory")
        self.directory = os.path.abspath(directory)
        self.fileExtensions = ["mkv", "avi", "mpg", "mpeg", "mp4"]

    @property
    def dirName(self):
        return os.path.basename(self.directory)

    @property
    def mediaFilenames(self):
        media = []
        for extension in self.fileExtensions:
            media.extend(glob(os.path.join(self.directory, "*.%s" % extension)))
        return media 

    @property
    def mediaFiles(self):
        return [ MediaFile(filename, self) for filename in self.mediaFilenames ]

    @property
    def folders(self):
        return [ self.fullFilePath(filename) for filename in self.listing if isdir(self.fullFilePath(filename))]

    def fullFilePath(self, filename):
        return os.path.abspath(os.path.join(self.directory, filename))

    @property
    def listing(self):
        return [ self.fullFilePath(filename) for filename in listdir(self.directory)]

    @property
    def rogueFilenames(self):
        return [ filename for filename in self.listing if filename not in self.folders and filename not in self.mediaFilenames ]


class TVCollectionDirectory(Directory):
    def __init__(self, directory):
        super(TVCollectionDirectory, self).__init__(directory)

    @lazy_property
    def shows(self):
        return [ TVShowDirectory(filename) for filename in self.folders ]


class TVShowDirectory(Directory):
    def __init__(self, directory):
        super(TVShowDirectory, self).__init__(directory)

    def __repr__(self):
        return "TVShowDirectory('%s')" % self.show

    @property
    def show(self):
        return os.path.basename(self.directory)

    @lazy_property
    def seasons(self):
        foo = [ SeasonDirectory(folder,self) for folder in self.folders]
        foo.sort()
        return foo

    @property
    def allFiles(self):
        foo = copy(self.mediaFiles)
        for season in self.seasons:
            foo.extend(season.episodes)
        return foo

    @property
    def orphanFiles(self):
        return self.mediaFiles


class SeasonDirectory(Directory):
    def __init__(self, directory, parent):
        super(SeasonDirectory, self).__init__(directory)
        self.parent = parent

    def __repr__(self):
        return "SeasonDirectory(%s Season %d, '%s')" % (self.show, self.season, self.dirName)

    def __cmp__(self, other):
        return self.season.__cmp__(other.season)

    @property
    def season(self):
        matchobj = re.search(r"\d+", self.dirName)
        if matchobj is None:
            return None
        else:
            return int(matchobj.group())
    
    @property
    def show(self): return self.parent.show

    @property
    def episodes(self):
        return self.mediaFiles

    @property
    def rogueDirectories(self):
        return self.folders
        

class MediaFile(object):
    def __init__(self, filename, parent=None):
        self.filename = os.path.abspath(filename)
        self.shortFilename = os.path.basename(filename)
        self.parent = parent
        self._parseFilename()
   
    def __repr__(self):
        return "MediaFile(%s, Season %d Episode %d, '%s')" % (self.show, self.season, self.episodeNumber, self.shortFilename)

    @property
    def show(self):
        return self.parent.show if hasattr(self.parent, "show") else None

    @property
    def season(self):
        if hasattr(self, "_season"):
            return self._season
        else:
            return self.parent.season if hasattr(self.parent, "season") else None

    @season.setter
    def season(self, value):
        self._season = int(value)

    @property
    def episodeNumber(self):
        return self._episodeNumber if hasattr(self, "_episodeNumber") else 0

    @episodeNumber.setter
    def episodeNumber(self, value):
        self._episodeNumber = int(value)

    def __str__(self):
        if isinstance(self.parent, SeasonDirectory): 
            return "Episode %d from season %s of %s" % (self.episodeNumber, self.season, self.show)

    def _parseFilename(self):
        nameToParse = os.path.basename(self.filename)
        matchObj = seasonEpisodeRegex.search(nameToParse)
        if matchObj is None: matchObj = seasonXEpisodeRegex.search(nameToParse)
        if matchObj is not None:
            self.season,self.episodeNumber = matchObj.groups()
    
    @lazy_property
    def md5(self):
        hasher = hashlib.md5()
        with open(self.filename, "r") as afile:
            buf = afile.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(65536)
        return hasher.hexdigest()




