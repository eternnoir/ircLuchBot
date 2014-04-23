ircLuchBot
==========

An irc lunch order bot

##Command

####Set menus
botId: setmenu 便當名-價格;便當2-價格;.......

```
LunchBot: setmenu 海南機-50;雞腿-60 
```
####Show Menu
botId: getmenu
```
<•eternnoir> LunchBot: setmenu 海南機-50;雞腿-60 
<•eternnoir> LunchBot: getmenu
<LunchBot> 海南機-50   雞腿-60
```

####定便當
botId: order 便當名
```
<•eternnoir> LunchBot: order 雞腿
<LunchBot> eternnoir: Order Done
```

####更新便當
botId: order 便當名

####Get All Order
botId: showorders
