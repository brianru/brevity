#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os

class WebPresentation(object):
    def __init__(self):
        self.CHILD_TEMPLATES = os.listdir('./')

    def templateForObject(self, action, object_kind):
        return self.getTemplateIfValid(action + object_kind + '.html')

    def templateForAction(self, action):
        return self.getTemplateIfValid(action + 'page.html')

    def getTemplateIfValid(self, proposed_template):
        if proposed_template in self.CHILD_TEMPLATES:
            return proposed_template
        else:
            raise KeyError

class MobileWebPresentation(object):
    pass
