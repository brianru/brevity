"""Brevity: TDD Edition"""

import webapp2

from google.appengine.ext import ndb

class Socket(ndb.Model):
    pass
#    text = ndb.StringProperty()
#    variables = ndb.Key()  # reference ndb.Expando object
#    linked_node = ndb.Key()  # refernces a Node or Null

class Node(ndb.Model):
    pass
#    sockets = 

class Document(ndb.Model):
    pass
#    nodes = []
#    variables = 

class Amendment(Document):
    pass
#    old_obj = ndb.Key()
#    new_obj = ndb.Key()

class Agreement(ndb.Model):
    pass
#    documents = []
#    other meta data (status, dates and stuff)

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # header
        # footer
        # body
        # response = header + body + footer
        self.response.write('Hello, webapp2 World!')

class ViewPage(webapp2.RequestHandler):

    def get(self, url_safe_key):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(str(self.objectFromURLSafeKey(url_safe_key)))

    def objectFromURLSafeKey(self, url_safe_key):
        raw_key = ndb.Key(urlsafe=url_safe_key)
        return raw_key.get() 

application = webapp2.WSGIApplication([(r'/', MainPage),
                                       (r'/view/(.*)', ViewPage)], debug=True)

