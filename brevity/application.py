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

Define and provide interface to data model. Ensure consistency.

------------------
------ VIEW ------
------------------
TEMPLATES
HTML generators

Construct view per controller's instructions. Display data using appropriate resources.

------------------
--- CONTROLLER ---
------------------
MainPage
ViewPage
EditPage
CreatePage

CRUD data with Model. Tell view(s) what to display.

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
:: iOS
:: Android

"""

import jinja2
import webapp2
import model
import os

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"),
        extensions=['jinja2.ext.autoescape'])

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {'welcome_message': 'Hello, world!'}
        template = JINJA_ENVIRONMENT.get_template('mainpage.html')
        self.response.write(template.render(template_values))

class ViewPage(webapp2.RequestHandler):
    def get(self, url_safe_key):
        if url_safe_key is not '':
            self.response.headers['Content-Type'] = 'text/html'
            template_values = {'key': url_safe_key,
                               'object_instance': model.objectFromURLSafeKey(url_safe_key)}
            template = JINJA_ENVIRONMENT.get_template('viewpage.html')
            self.response.write(template.render(template_values))
        else:
            self.objectFactory = model.SampleObjectFactory()
            url_safe_key = model.urlSafeKeyFromObject(self.objectFactory.randomSocket()) 
            self.redirect('/view/' + str(url_safe_key))


class EditPage(webapp2.RequestHandler):
    def get(self, url_safe_key):
        if url_safe_key is not '':
            self.response.headers['Content-Type'] = 'text/html'
            data_object = model.objectFromURLSafeKey(url_safe_key)
            template_values = {'url_safe_key': url_safe_key,
                               'object_instance': data_object}
            template = JINJA_ENVIRONMENT.get_template('editpage.html')
            self.response.write(template.render(template_values))
        else:
            self.objectFactory = model.SampleObjectFactory()
            url_safe_key = model.urlSafeKeyFromObject(self.objectFactory.randomSocket())
            self.redirect('/edit/' + str(url_safe_key))

    def post(self, url_safe_key):
        data_object = model.objectFromURLSafeKey(url_safe_key)
        data_object.text = self.request.get('content')
        print('get items: %s' % self.request.POST.items())
        data_object.put()
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(self.EDIT_PAGE_HTML %\
                (url_safe_key,
                 data_object.text,
                 data_object.variables,
                 data_object.linked_node))
        
    

class CreatePage(webapp2.RequestHandler):
    def get(self):
        pass


application = webapp2.WSGIApplication([(r'/', MainPage),
                                       (r'/view/(.*)', ViewPage),
                                       (r'/edit/(.*)', EditPage),
                                       (r'/create/', CreatePage)], debug=True)

