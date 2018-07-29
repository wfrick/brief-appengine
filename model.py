from google.appengine.ext import ndb

class Article(ndb.Model):
	search_id = ndb.StringProperty(indexed=True)
	summary = ndb.StringProperty(indexed=False)
	URL = ndb.StringProperty(indexed=False)
	title = ndb.StringProperty(indexed=False)
	source = ndb.StringProperty(indexed=False)
	votes = ndb.IntegerProperty(indexed=False)

class Search(ndb.Model):
	request_id = ndb.StringProperty(indexed=True)
	search_term = ndb.StringProperty(indexed=False)
	sites = ndb.StringProperty(indexed=False)