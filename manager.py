import os
import glob
import shutil
import guessit
from logger import Logger
from pprint import pprint
try:
    from pwd import getpwnam
except:
    getpwnam = lambda x: (0,0,0)
    os.chown = lambda x, y, z: True
    os.chmod = lambda x, y: True
    os.fchown = os.chown
    os.fchmod = os.chmod
import argparse


class Manager():
	"""docstring for Manager"""
	def __init__(self, downloadPath, moviePath, showPath, extentions):
		p = argparse.ArgumentParser(description='Process downloaded files')
		p.add_argument('-v', '--verbose', action='store_true', default=False);
		args = p.parse_args()
		self.downloadPath = downloadPath
		self.moviePath = moviePath
		self.showPath = showPath
		self.extentions = extentions
		self.subtitle = False
		self.l = Logger('Manager', self.downloadPath, args).logger
		self.l.info("started")

	def manage(self):
		self.l.info('managing files in %s' % self.downloadPath)
		length = len(self.downloadPath)
		for extention in self.extentions:
			for _file in glob.glob( os.path.join(self.downloadPath, extention) ):
				self.fullPath = _file
				self.fileName = _file[(length+1):]
				print self.fileName
				self.move()
		self.l.info("done")

	def move(self):
		info = self.getInfo(self.fileName)
		path = self.getMoveToPath(info)
		if path:
			if self.subtitle:
				self.fileName = self.renameFile()
				if not self.fileName:
					return False
			self.makeDest(path)
			self.l.info("moving %s to %s" % (self.fileName, path))
			completePath = os.path.join(path, self.fileName)
			if not os.path.isfile(completePath):
				self.fileName = os.path.join(self.downloadPath, self.fileName)
				shutil.move(self.fileName, path)
			else:
				self.l.info("File Already exsists")
		else:
			self.l.error("No path to move %s to" % self.fileName)

	def getInfo(self, media):
		return guessit.guess_file_info(media, 'autodetect')
		
	
	def getMoveToPath(self, fileInfo):
		if fileInfo['type'] == 'episode':
			self.l.info("It's an episode")
			return os.path.join(self.showPath, self.getPathStringEpisode(fileInfo))
		elif fileInfo['type'] == 'movie':
			self.l.info("Movies can't be handled processed now")
			self.l.info("I'ts a movie")
			return os.path.join(self.moviePath, self.getPathStringMovie(fileInfo))
		elif fileInfo['type'] == 'episodesubtitle':
			self.l.info("It's a subtitle for a show")
			self.subtitle = True
			return os.path.join(self.showPath, self.getPathStringEpisode(fileInfo))
		elif fileInfo['type'] == 'moviesubtitle':
			self.l.info("I'ts a subtitle for a movie")
			self.subtitle = True
			return os.path.join(self.moviePath, self.getPathStringMovie(fileInfo))
		else:
			return False

	def parseNumber(self, number):
		if number < 10:
			number = '0'+str(number)
		return str(number)

	def makeDest(self, path):
		if not os.path.exists(path):
			os.makedirs(path, 0777)

	def getPathStringEpisode(self, fileInfo):
		show = fileInfo['series']
		e = self.parseNumber(fileInfo['episodeNumber'])
		s = fileInfo['season']
		season = "Season "+str(s)
		if 'year' in fileInfo:
			show += " "+ str(fileInfo['year'])
		s = self.parseNumber(s)
		return os.path.join(show, os.path.join(season, "S"+s+"E"+e))

	def getPathStringMovie(self, fileInfo):
		title = fileInfo['title']
		if 'year' in fileInfo:
			title += " "+str(fileInfo['year'])
		return title

	def renameFile(self):
		oldPath = os.getcwd()
		os.chdir(self.downloadPath)
		fileNameNoEx, ex = os.path.splitext(self.fileName)
		newName = fileNameNoEx+".nl"+ex
		os.rename(self.fileName, newName)
		if os.path.isfile(newName):
			os.chdir(oldPath)
			return newName
		else:
			os.chdir(oldPath)
			self.l.error("Something went wrong while trying to rename %s" % self.fileName)
			return False
