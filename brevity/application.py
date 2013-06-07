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
model.py
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
Web Presentation Layer
TEMPLATES

Construct view per controller's instructions. Display data using appropriate resources.

------------------
--- CONTROLLER ---
------------------
web_controller.py
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
;: iOS
:: Android

"""
import os

import jinja2
import webapp2

import model
import view


JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'])

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.templates = view.WebTemplates()
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {'welcome_message': 'Hello, world!'}
        template = JINJA_ENVIRONMENT.get_template(self.templates.templateForAction('main'))
        self.response.write(template.render(template_values))

class ViewPage(webapp2.RequestHandler):
    def get(self, url_safe_key):
        self.templates = view.WebTemplates()
        if url_safe_key is not '':
            self.response.headers['Content-Type'] = 'text/html'
            template_values = {
                              'key': url_safe_key,
                              'object_kind': model.kindFromURLSafeKey(url_safe_key),  
                              'object_instance': model.objectFromURLSafeKey(url_safe_key),
                              }
            template = JINJA_ENVIRONMENT.get_template(self.templates.templateForObject('view', template_values['object_kind']))
            self.response.write(template.render(template_values))
        else:
            self.objectFactory = model.SampleObjectFactory()
            url_safe_key = model.urlSafeKeyFromObject(self.objectFactory.randomSocket()) 
            self.redirect('/view/' + str(url_safe_key))


class EditPage(webapp2.RequestHandler):
    def get(self, url_safe_key):
        self.templates = view.webTemplates()
        if url_safe_key is not '':
            self.response.headers['Content-Type'] = 'text/html'
            data_object = model.objectFromURLSafeKey(url_safe_key)
            template_values = {
                              'url_safe_key': url_safe_key,
                              'object_kind': model.kindFromURLSafeKey(url_safe_key),
                              'object_instance': data_object,
                              }
            template = JINJA_ENVIRONMENT.get_template(self.templates.templateForObject('edit', template_values['object_kind']))
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
        self.response.write(self.EDIT_PAGE_HTML % (
                 url_safe_key,
                 data_object.text,
                 data_object.variables,
                 data_object.linked_node
                 ))
        
    

class CreatePage(webapp2.RequestHandler):
    def get(self):
        pass

    def post(self):
        pass

application = webapp2.WSGIApplication([(r'/', MainPage),
                                       (r'/view/(.*)', ViewPage),
                                       (r'/edit/(.*)', EditPage),
                                       (r'/create/', CreatePage)], debug=True)

