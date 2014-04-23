# -*- coding: utf-8 -*-
__author__ = 'eternnoir'

class order(object):
    def __init__(self,user,bandon):
        self.user = user
        self.pandon = bandon
        pass

class bandon(object):
    def __init__(self,itemName,price):
        self.name = itemName
        self.price = price

class menu(object):
    def __init__(self,list):
        self.bandonList = list
        pass

    def getBandon(self,itemName):
        return [x for x in self.bandonList if x.name is itemName]

class user(object):
    def __init__(self):
        self.order = []
        pass

    def addOrder(self,order):
        self.order.append(order)
        pass