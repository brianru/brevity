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
    socket = ndb.KeyProperty(repeated=True)

class Socket(ndb.Model):
    text = ndb.StringProperty()
    variables = ndb.JsonProperty()
    linked_node = ndb.StructuredProperty(Node)

class RandomDataGenerator(object):
    def __init__(self):
        self.text_source = '/test/mobydick.txt'
        self.key_source = ''

    def randomText(self, numberOfLines):
        return ''

    def randomDictionary(self):
        return {'a': 0}

    def randomVariableKeys(self, numberOfKeys):
        return ['a', 'b', 'c']
    
    def randomDictionaryFromKeys(self, keys):
        return dict(zip(keys, 0))

class SampleObjectFactory(object):
    def __init__(self):
        self.dataGenerator = RandomDataGenerator()
    
    def objectsWithSingleModifications(self, original_object, property_list):
        """For each property in original_object,
        return a new object with that property modified.
        
        """

    def randomSocket(self):
        return br.Socket(text=self._randomText(),
                         variables=self.testDataGenerator.randomDictionary,
                         linked_node=None)

    def randomSocketWithVariableKeys(self, variable_keys):
        return br.Socket(text=self._randomText(),
                         variables=self.testDataGenerator.randomDictionaryFromVariableKeys(variable_keys),
                         linked_node=None)

    def randomNode(self):
        return br.Node(socket=[self.randomSocket() for x in xrange(0, self.SAMPLE_SIZE)])

    def randomDocument(self):
        pass
    #   return br.Document(node=[self.randomNode() for x in xrange(0,3)])

    def randomAmendment(self):
        pass

    def randomAgreement(self):
        pass

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

