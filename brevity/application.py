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

class Document(ndb.Model):
    pass

class Amendment(ndb.Model):
    pass

class Agreement(ndb.Model):
    pass

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, webapp2 World!')

application = webapp2.WSGIApplication([('/', MainPage)],
                                      debug=True)

