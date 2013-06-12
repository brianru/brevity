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
            sample_socket = factory.random_document()
            id = model.id_from(sample_socket)
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
<<<<<<< HEAD
            url_safe_key = model.urlsafekey_from(self.factory.random_document())
            self.redirect('/edit/' + str(url_safe_key))
=======
            id = model.id_from(self.factory.random_socket())
            self.redirect('/edit/' + str(id))
>>>>>>> zachallaun-code-review

    # TODO Refactor editpage post request.
    def post(self, id):
        data_object = model.get_instance(id)
        data_object.text = self.request.get('content')
        print('get items: %s' % self.request.POST.items())
        data_object.put()
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(self.EDIT_PAGE_HTML % (
            id,
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
