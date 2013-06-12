#!/usr/bin/env python

import webapp2

import model
import view


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.gen_template = view.WebTemplateGenerator()
        self.response.headers['Content-Type'] = 'text/html'
        values = {
            'action': 'main',
            'welcome_message': 'Hello, world!',
        }
        self.response.write(self.gen_template.render_template_for(values))


class ViewPage(webapp2.RequestHandler):
    def get(self, id):
        self.gen_template = view.WebTemplateGenerator()
        if id is not '':
            self.response.headers['Content-Type'] = 'text/html'
            values = model.data_from_id(id)
            values.update({'action': 'view'})
            self.response.write(self.gen_template.render_template_for(values))
        else:
            factory = model.SampleObjectFactory()
            id = model.id_from(factory.random_document())
            self.redirect('/view/' + str(id))


class EditPage(webapp2.RequestHandler):
    def get(self, id):
        self.gen_template = view.WebTemplateGenerator()
        if id is not '':
            self.response.headers['Content-Type'] = 'text/html'
            values = model.data_from_id(id)
            values.update({'action': 'edit'})
            self.response.write(self.gen_template.render_template_for(values))
        else:
            self.factory = model.SampleObjectFactory()
            id = model.id_from(self.factory.random_socket())
            self.redirect('/edit/' + str(id))

    # TODO Refactor editpage post request.
    def post(self, id):
        self.gen_template = view.WebTemplateGenerator()
        data_object = model.get_instance(id)
        for arg in self.request.arguments():
            pass
        print('Request attributes: %s' % self.request.arguments())
        # TODO modify data object per textareas in self.request
        data_object.put()
        values = model.data_from_id(id)
        values.update({'action': 'edit'})
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(self.gen_template.render_template_for(values))


class CreatePage(webapp2.RequestHandler):
    def get(self):
        pass

    def post(self):
        pass

application = webapp2.WSGIApplication([(r'/', MainPage),
                                       (r'/view/(.*)', ViewPage),
                                       (r'/edit/(.*)', EditPage),
                                       (r'/create/', CreatePage)], debug=True)
