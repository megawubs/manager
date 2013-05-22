#!/usr/bin/env python
from manager import Manager
from pprint import pprint

if __name__ == '__main__':
	extentions = ['*.mkv', '*.avi', '*.mp4', '*.ts', '*.srt']
	m = Manager('/Volumes/media/Downloads', '/Volumes/media/Videos/','/Volumes/media/Series/', extentions)
	m.manage()


