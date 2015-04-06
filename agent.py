import os
from xmlrpclib import ServerProxy

from utils import File

class Agent(object):
	SERVER = 'http://api.opensubtitles.org/xml-rpc'
	USER_AGENT = 'OSTestUserAgent'
	LANGUAGE = 'eng'

	def __init__(self, username, password, language=None):
		self.username = username
		self.password = password
		self.language = language or self.LANGUAGE

	def authenticate(self):
		self.xmlrpc = ServerProxy(self.SERVER)
		data = self.xmlrpc.LogIn(self.username, self.password, 
				self.language, self.USER_AGENT)

		status = int(data.get('status').split()[0])
		if status != 200:
			raise Exception('Authentication failed!')
		try:
			self.token = data.get('token')
		except Exception as e:
			print 'Failed to extract token from response'
			print data
			raise e


	def search_subtitles(self, **kwargs):
		if 'video' in kwargs.keys():
			f = kwargs['video']
			moviehash = f.hash_file()
			bytesize  = os.path.getsize(f.path())
		else:
			try:
				moviehash = kwargs['moviehash']
				bytesize  = kwargs['bytesize']
			except Exception as e:
				print 'Missing argument'
				raise e

		params = {
				'sublanguageid' : self.language,
				'moviehash' : moviehash,
				'moviebytesize' : bytesize,
		}

		result = self.xmlrpc.SearchSubtitles(self.token, [params])
		data = result['data']
		if data:
			key = kwargs.get('sort_by', None)
			if key:
				data.sort(key=lambda x : x[key], reverse=True)
		return data
