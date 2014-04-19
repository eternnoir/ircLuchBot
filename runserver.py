# -*- coding: utf-8 -*-
from lunchBot import ircBot

def main():
    channel= '#'
    nickname= 'LunchBot'
    server='chat.freenode.net'
    bot = ircBot.Bot(channel, nickname, server)
    bot.start()

if __name__ == '__main__' :
    main()

