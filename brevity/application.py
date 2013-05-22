"""Brevity: TDD Edition"""

import webapp2

from google.appengine.ext import ndb

class Agreement(ndb.Model):
    pass
#    documents = []
#    other meta data (status, dates and stuff)

class Document(ndb.Model):
    pass
#    nodes = []
#    variables = 

class Amendment(Document):
    pass
#    old_obj = ndb.Key()
#    new_obj = ndb.Key()

class Node(ndb.Model):
    pass
#    socket = ndb.KeyProperty(kind=Socket, repeated=True)

class Socket(ndb.Model):
    text = ndb.StringProperty()
    variables = ndb.JsonProperty()
    linked_node = ndb.StructuredProperty(Node)

class MainPage(webapp2.RequestHandler):

    MAIN_PAGE_HTML = """\
    <!DOCTYPE html>
    <html>
      <head>
        <title>Brevity</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- Bootstrap -->
        <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
      </head>
      <body>
        <h1>%s</h1>
        <script src="http://code.jquery.com/jquery.js"></script>
        <script src="js/bootstrap.min.js"></script>
      </body>
    </html>
    """
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(self.MAIN_PAGE_HTML % ('Hello, world!'))

class ViewPage(webapp2.RequestHandler):

    VIEW_PAGE_HTML = """\
    <!DOCTYPE html>
    <html>
      <head>
        <title>Brevity</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- Bootstrap -->
        <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
      </head>
      <body>
        <h1>%s</h1>
        <script src="http://code.jquery.com/jquery.js"></script>
        <script src="js/bootstrap.min.js"></script>
      </body>
    </html>
    """
    
    def get(self, url_safe_key):
        self.response.headers['Content-Type'] = 'text/html'
        if url_safe_key is not '':
            self.response.write(self.VIEW_PAGE_HTML % (self.objectFromURLSafeKey(url_safe_key)))
        else:
            self.response.write(self.VIEW_PAGE_HTML % ('Explore Brevity!'))

    def objectFromURLSafeKey(self, url_safe_key):
        raw_key = ndb.Key(urlsafe=url_safe_key)
        return raw_key.get() 

application = webapp2.WSGIApplication([(r'/', MainPage),
                                       (r'/view/(.*)', ViewPage)], debug=True)
                                    #  (r'/edit/(.*)', EditPage),
                                    #  (r'/create/', CreatePage),

