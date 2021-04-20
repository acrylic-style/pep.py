import tornado.gen
import tornado.web
from common.web import requestsManager
from objects import glob
import time

class handler(requestsManager.asyncRequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.engine
	def asyncGet(self):
		self.write("Nope")
