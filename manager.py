#!/usr/bin/env python
import os
import glob
import shutil
import guessit
from logger import Logger
try:
    from pwd import getpwnam
except:
    getpwnam = lambda x: (0,0,0)
    os.chown = lambda x, y, z: True
    os.chmod = lambda x, y: True
    os.fchown = os.chown
    os.fchmod = os.chmod



class Manager():
	"""docstring for Manager"""
	def __init__(self, downloadPath, moviePath, showPath, extentions):
		self.downloadPath = downloadPath
		self.moviePath = moviePath
		self.showPath = showPath
		self.extentions = extentions
		self.l = Logger('Manager', self.downloadPath).logger
		self.l.info("started")

	def manage(self):
		self.filesToProces = []
		length = len(self.downloadPath)
		for extention in self.extentions:
			for _file in glob.glob( os.path.join(self.downloadPath, extention) ):
				fileName = _file[(length+1):]
				self.move(fileName)

	def move(self, fileName):
		info = self.getInfo(fileName)
		path = self.getMoveToPath(info)
		self.l.info("moving %s to %s" % (fileName, path))
		if path:
			self.makeDest(path)
			completePath = os.path.join(path, fileName)
			if not os.path.isfile(completePath):
				fileName = os.path.join(self.downloadPath, fileName)
				shutil.move(fileName, path)
			else:
				self.l.info("File Already exsists")

	def getInfo(self, media):
		return guessit.guess_file_info(media, 'autodetect')
		
	
	def getMoveToPath(self, fileInfo):
		if fileInfo['type'] == 'episode':
			show = fileInfo['series']
			e = self.parseNumber(fileInfo['episodeNumber'])
			s = fileInfo['season']
			season = "Season "+str(s)
			if 'year' in fileInfo:
				show += " "+ str(fileInfo['year'])
			s = self.parseNumber(s)
			path =  os.path.join(show, os.path.join(season, "S"+s+"E"+e))
			return os.path.join(self.showPath, path)
		elif fileInfo['type'] == 'movie':
			self.l.info("Movies can't be handled processed now")

	def parseNumber(self, number):
		if number < 10:
			number = '0'+str(number)
		return str(number)

	def makeDest(self, path):
		if not os.path.exists(path):
			os.makedirs(path, 0777)
		