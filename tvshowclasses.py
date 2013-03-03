#!/usr/bin/env python
import hashlib
import os
import re
from os import listdir
from os.path import  isdir
from glob import glob

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

    @property
    def show(self):
        return os.path.basename(self.directory)

    @lazy_property
    def seasons(self):
        return [ SeasonDirectory(folder,self) for folder in self.folders]
    
    @property
    def orphanFiles(self):
        return self.mediaFiles
        #return [ MediaFile(filename) for filename in self.mediaFilenames ]


class SeasonDirectory(Directory):
    def __init__(self, directory, parent):
        super(SeasonDirectory, self).__init__(directory)
        self.parent = parent
   
    def __str__(self):
        if self.season is None:
            return "Unknown season: %s" % self.directory
        else:
            return "Season %d" % self.season

    def __repr__(self):
        return self.__str__()

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
        return self.mediaFilenames

    @property
    def rogueDirectories(self):
        return self.folders
        

class MediaFile(object):
    def __init__(self, filename, parent=None):
        self.filename = os.path.abspath(filename)
        self.parent = parent

    @property
    def season(self):
        if isinstance(self.parent, SeasonDirectory):
            return parent.season()
        else:
            import ipdb;ipdb.set_trace()
            return None

    def __str__(self):
        if isinstance(self.parent, SeasonDirectory): 
            return "Episode from season %s of %s" % (self.season, self.parent.show)

    def _guessSeasonEpisode(self):
        os.path.basename(self.filename)
    
    @lazy_property
    def md5(self):
        hasher = hashlib.md5()
        with open(self.filename, "r") as afile:
            buf = afile.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(65536)
        return hasher.hexdigest()




