# -*- coding: utf-8 -*-
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import banDonCore
import order
import time
from threading import *


class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.controler = bandonControl(self,channel)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        print e.source.nick
        print e.arguments[0]
        #self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        user = e.source.nick
        print e.arguments[0]
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            rmsg =  irc.strings.lower(a[1]).strip()
            try:
                if len(rmsg.split(' ')) > 1:
                    command = rmsg.split(' ')[0]
                    msg= rmsg.split(' ')[1]
                else:
                    command = rmsg
                    msg=''
                self.controler.doCommand(c,user,irc.strings.lower(command).strip(),msg)
            except:
                self.sayTo(c,user,u'Command Error')
        return

    def say(self,c,msg):
        c.privmsg(self.channel,msg)

    def sayTo(self,c,user,msg):
        tomsg = user+': '+msg
        self.say(c,tomsg)

    def notice(self,c,noticeId,msg):
        c.notice(noticeId,msg)

class bandonControl(object):
    def __init__(self,ircbot,name):
        self.name = name
        self.core = banDonCore.core(name)
        self.bot = ircbot
        pass

    def doCommand(self,c,user,command,msg):
        """
        :param c:irc client
        :param user:notice user name
        :param msg:message
        """
        mname = 'do_' + command
        if hasattr(self, mname):
            method = getattr(self, mname)
            method(c,user,msg)
        else:
            self.error(c,user,msg)
        pass

    def getBandonList(self,menuStr):

        bdlist = []
        for oneline in menuStr.split(';'):
            itemName = oneline.split('-')[0]
            price = int(oneline.split('-')[1])
            bd = order.bandon(itemName,price)
            bdlist.append(bd)
            print bd
        return bdlist

    def do_setmenu(self,c,user,msg):
        """
        Set Menu
        format bandonname-momey;.....
        """
        bdlist = []
        try:
            bdlist = self.getBandonList(msg)
        except:
            print('error')
            pass
        if len(bdlist)>0:
            self.core.setMenu(bdlist)
            self.bot.sayTo(c,user,'Done')
        else:
            self.bot.notice(c,user,'no menu')

    def do_order(self,c,user,msg):
        """
        Set order
        format
        """
        bd = self.core.menu.getBandon(msg)
        if len(bd) == 0:
            self.bot.sayTo(c,user,'No bandon on menu')
            return
        else:
            userOrder = self.core.findUserOrder(user)
            if len(userOrder)>0:
                userOrder[0].bandon=bd[0]
                self.bot.sayTo(c,user,'Order Updated')
            else:
                o = order.order(user,bd[0])
                self.core.order.append(o)
                self.bot.sayTo(c,user,'Order Done')
        pass
    def do_getmenu(self,c,user,msg):
        if self.core.menu is None:
            self.bot.say(c,u'No Menu Now')
        else:
            msg = u''
            for bd in self.core.menu.bandonList:
                msg+= bd.name+'-'+str(bd.price)+'   '
            self.bot.say(c,msg)

    def do_reset(self,c,user,msg):
        self.core = banDonCore.core(self.name)
        self.bot.sayTo(c,user,'Done')

    def do_showorders(self,c,user,msg):

        if len(self.core.order)<1:
            self.bot.say(c,'No order now')
        else:
            msg = u''
            for o in self.core.order:
                msg+= o.user+'->'+o.bandon.name+'   '
            self.bot.say(c,msg)

    def do_help(self,c,user,msg):
        for m in self.getHelpMessage():
            self.bot.say(c,m)

    def error(self,c,user,msg):
        self.bot.sayTo(c,user,'Command not found')

    def getHelpMessage(self):
        ret = []
        ret.append(" setmenu bandon1-10;bandon2-20;....  ")
        ret.append(" order   bandon1  ")
        ret.append(" getmenu <Get all menu>  ")
        ret.append(" showorders <Get all orders>  ")
        return ret

