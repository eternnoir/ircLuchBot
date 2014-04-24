# -*- coding: utf-8 -*-
__author__ = 'eternnoir'
import order

class core(object):
    def __init__(self, name):
        self.name = name
        self.menu = None
        self.order = []

    def setMenu(self,menu):
        self.menu = order.menu(menu)
        pass

    def findUserOrder(self,userName):
        return [x for x in self.order if x.user == userName]

    def getStatus(self):
        pass

    def clear(self):
        pass

    def getMenu(self):
        pass
