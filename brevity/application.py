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
    def get(self, url_safe_key):
        self.gen_template = view.WebTemplateGenerator()
        if url_safe_key is not '':
            self.response.headers['Content-Type'] = 'text/html'
            values = model.view_data_from(url_safe_key)
            values.update({'action': 'view'})
            self.response.write(self.gen_template.render_template_for(values))
        else:
            factory = model.SampleObjectFactory()
            sample_socket = factory.random_document()
            url_safe_key = model.urlsafekey_from(sample_socket)
            self.redirect('/view/' + str(url_safe_key))


class EditPage(webapp2.RequestHandler):
    def get(self, url_safe_key):
        self.gen_template = view.WebTemplateGenerator()
        if url_safe_key is not '':
            self.response.headers['Content-Type'] = 'text/html'
            values = model.view_data_from(url_safe_key)
            values.update({'action': 'edit'})
            self.response.write(self.gen_template.render_template_for(values))
        else:
            self.factory = model.SampleObjectFactory()
            url_safe_key = model.urlsafekey_from(self.factory.random_document())
            self.redirect('/edit/' + str(url_safe_key))

    # TODO Refactor editpage post request.
    def post(self, url_safe_key):
        data_object = model.instance_from_urlsafe(url_safe_key)
        data_object.text = self.request.get('content')
        print('get items: %s' % self.request.POST.items())
        data_object.put()
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(self.EDIT_PAGE_HTML % (
            url_safe_key,
            data_object.text,
            data_object.variables,
            data_object.linked_node,
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

