#coding=utf-8

import threading

class GrabThread(threading.Thread):
	def __init__(self, func, args=()):
		super(GrabThread, self).__init__()
		self.func = func
		self.args = args
		self.setDaemon(True)

	def run(self):
		self.result = self.func(*self.args)

	def get_result(self):
		try:
			return self.result
		except:
			return