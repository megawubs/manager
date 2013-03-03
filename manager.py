#!/usr/bin/env python
import os
import glob
import re
import shutil
import grp
import guessit
from pprint import pprint
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
	def __init__(self, user, downloadPath, moviePath, showPath, extentions):
		self.user = user
		self.downloadPath = downloadPath
		self.moviePath = moviePath
		self.showPath = showPath
		self.extentions = extentions

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
		if path:
			self.makeDest(path)
			print "moving %s to %s" % (fileName, path)
			completePath = os.path.join(path, fileName)
			if not os.path.isfile(completePath):
				fileName = os.path.join(self.downloadPath, fileName)
				shutil.move(fileName, path)
			else:
				print "File Already exsists"

	def getInfo(self, media):
		return guessit.guess_file_info(media, 'autodetect')
		
	
	def getMoveToPath(self, fileInfo):
		if fileInfo['type'] == 'episode':
			show = fileInfo['series']
			e = self.parseNumber(fileInfo['episodeNumber'])
			s = fileInfo['season']
			season = "Season "+str(s)
			s = self.parseNumber(s)
			path =  os.path.join(show, os.path.join(season, "S"+s+"E"+e))
			return os.path.join(self.showPath, path)
		elif fileInfo['type'] == 'movie':
			print "Movies can't be handled processed now"

	def parseNumber(self, number):
		if number < 10:
			number = '0'+str(number)
		return str(number)

	def makeDest(self, path):
		if not os.path.exists(path):
			os.makedirs(path)
		