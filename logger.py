import logging
import os

class Logger:

	def __init__(self, name, path, args):
		self.logger = logging.getLogger(name)
		path = os.path.realpath(path)
		handler = logging.FileHandler(os.path.join(path, 'manager.log'))
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		if not args.verbose:
			self.logger.setLevel(logging.INFO)
			
		else:
			console = logging.StreamHandler()
			console.setLevel(logging.INFO)
			self.logger.addHandler(console)
			self.logger.setLevel(logging.INFO)

		self.logger.propagate = True
