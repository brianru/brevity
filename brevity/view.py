#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os

import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
)


class WebTemplateGenerator(object):
    def __init__(self):
        self.CHILD_TEMPLATES = os.listdir('./templates/')

    def _template_selector(self, action, kind=''):
        return (self._get_template_if_valid(action + kind + '.html'))

    def _template_for(self, variables):
        if 'kind' in variables.keys() and 'action' in variables.keys():
            return self._template_selector(variables['action'],
                                           variables['kind'])
        elif 'action' in variables.keys():
            return self._template_selector(variables['action'])
        else:
            raise KeyError(variables)

    def _get_template_if_valid(self, proposed_template):
        if proposed_template in self.CHILD_TEMPLATES:
            return proposed_template
        else:
            raise KeyError(proposed_template)

    def render_template_for(self, variables):
        template = 'templates/' + self._template_for(variables)
        jinja_template = JINJA_ENVIRONMENT.get_template(template)
        return jinja_template.render(variables)


class MobileWebPresentation(object):
    pass

