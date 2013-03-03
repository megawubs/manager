import logging
import os

class Logger:

	def __init__(self, name, path):
		self.logger = logging.getLogger(name)
		path = os.path.realpath(path)
		handler = logging.FileHandler(os.path.join(path, 'manager.log'))
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		self.logger.setLevel(logging.INFO)
		self.logger.propagate = False