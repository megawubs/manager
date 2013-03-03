from manager import Manager
from pprint import pprint

if __name__ == '__main__':
	extentions = ['*.mkv', '*.avi', '*.mp4', '*.srt']
	m = Manager('bwubs', '/Volumes/media/Downloads', '/Volumes/media/Series/', '/Volumes/media/Videos/', extentions)
	m.manage()


