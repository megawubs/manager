from manager import Manager
import unittest


class ManagerTest(unittest.TestCase):
	def testMove(self):
		extentions = ['*.mkv', '*.avi', '*.mp4', '*.ts', '*.srt']
		m = Manager('input', 'output/movies', 'output/series', extentions);
		m.manage();


if __name__ == '__main__':
	unittest.main()