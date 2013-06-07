#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os

class WebPresentation(object):
    def __init__(self):
        self.CHILD_TEMPLATES = os.listdir('./templates/')

    def templateForObject(self, action, object_kind):
        return self.getTemplateIfValid(action + object_kind + '.html')

    def templateForAction(self, action):
        return self.getTemplateIfValid(action + 'page.html')

    def getTemplateIfValid(self, proposed_template):
        if proposed_template in self.CHILD_TEMPLATES:
            return proposed_template
        else:
            raise KeyError

    def forPresentationDict(self, presentation_dict):
        return self.getTemplateIfValid(self.template_path_from(presentation_dict))

    def template_path_from(self, presentation_dict):
        return presentation_dict['action'] + presentation_dict['kind'] + '.html'


class MobileWebPresentation(object):
    pass
