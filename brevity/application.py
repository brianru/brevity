#!/usr/bin/env python
"""Brevity. It's github+legos for lawyers.
#################

-----------------
------ API ------
-----------------

#########################

-----------------
----- MODEL -----
_________________
Socket
Node
Document
Amendment
Agreement
RandomDataGenerator
SampleObjectFactory

------------------
------ VIEW ------
------------------
MainPage
ViewPage


------------------
--- CONTROLLER ---
------------------
ServerController
ClientController


#################

-----------------
---- GAE::NDB ---- (MODEL)
-----------------

------------------
-- GAE::WEBAPP2 -- (CONTROLLER)
-----------------

---------------------
------JINJA2------- (VIEW)
-------------------
Desktop
Smartphone
:: iOS
:: Android
Tablet
;: iOS
:: Android

"""

import webapp2
import model

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
            self.response.write(self.VIEW_PAGE_HTML %\
                    (model.objectFromURLSafeKey(url_safe_key)))
        else:
            self.response.write(self.VIEW_PAGE_HTML % ('Explore Brevity!'))
            # display randomInstanceOfEach()


class EditPage(webapp2.RequestHandler):
    EDIT_PAGE_HTML = """\
    <!DOCTYPE html>
    <html>
      <head>
        <title>Brevity</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- Bootstrap -->
        <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
      </head>
      <body>
        <form action="/edit/%s" method="post">
          <div><textarea name="content" rows="9" cols="80">%s</textarea></div>
          <div><input type="submit" value="Submit"></div>
        </form>
        <script src="http://code.jquery.com/jquery.js"></script>
        <script src="js/bootstrap.min.js"></script>
      </body>
    </html>
    """
    
    def get(self, url_safe_key):
        self.response.headers['Content-Type'] = 'text/html'
        if url_safe_key is not '':
            self.response.write(self.EDIT_PAGE_HTML %\
                    (url_safe_key, model.objectFromURLSafeKey(url_safe_key)))
        else:
            self.redirect('/create/')

    def post(self, url_safe_key):
        # reconstitute json from form text area
        self.request.get('content')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(self.EDIT_PAGE_HTML)
        # translate contents of form into object

class CreatePage(webapp2.RequestHandler):
    CREATE_PAGE_HTML = """\
    """

    def get(self):
        pass

application = webapp2.WSGIApplication([(r'/', MainPage),
                                       (r'/view/(.*)', ViewPage),
                                       (r'/edit/(.*)', EditPage),
                                       (r'/create/', CreatePage)], debug=True)

