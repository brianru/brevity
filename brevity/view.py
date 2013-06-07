#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os

import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'])

class WebTemplateGenerator(object):
    def __init__(self):
        self.CHILD_TEMPLATES = os.listdir('./templates/')

    def template_selector(self, action, kind=''):
        return '/templates/' + self.getTemplateIfValid(action + kind + 'page.html')

    def template_for(self, variables):
        if ('action', 'kind') in variables.keys():
            return self.template_selector(variables['action'], variables['kind'])
        elif 'action' in variables.keys():
            return self.template_selector(variables['action'])
        else:
            raise KeyError

    def getTemplateIfValid(self, proposed_template):
        if proposed_template in self.CHILD_TEMPLATES:
            return proposed_template
        else:
            raise KeyError

    def render_template_for(self, variables):
        jinja_template = JINJA_ENVIRONMENT.get_template(self.template_for(variables))
        return jinja_template.render(variables)


class MobileWebPresentation(object):
    pass
