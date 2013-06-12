#!/usr/bin/env python

import webapp2
from pprint import pprint

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

    def post(self, id):
        self.gen_template = view.WebTemplateGenerator()
        data_object = model.get_instance(id)
        # PARSE REQUEST
        parsed_data = []
        for arg in self.request.arguments():
            a, b = arg.split('_')
            parsed_data.append(dict(zip(('id', 'attr', 'val'),
                                        (a, b, self.request.get(arg)))))
        pprint(parsed_data)
        for arg in parsed_data:
            data_object.__setattr__(arg['attr'], arg['val'])
            # FIXME working for text but no other attr.
            print(dir(data_object))
            data_object.put()
        values = model.data_from_id(id)
        values.update({'action': 'edit', 'message': 'Victory!!!'})
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
