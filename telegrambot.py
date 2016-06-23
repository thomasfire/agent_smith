#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this is bot "Agent Smith beta". He chats in Telegram with people
""" Developer and Author: Thomas Fire https://github.com/thomasfire
### Main manager: Uliy Bee
"""

import urllib
import urllib.request
import codecs
#import requests
from urllib.parse import quote, urlsplit, urlunsplit


#https://api.telegram.org/bot<token>/METHOD_NAME
#TODO пересылка сообщений из вк в телеграм,пересылка из телеграма в вк,предоставлять лог последних n сообщений

g=open('files/telegram.token')
url='https://api.telegram.org/bot'+g.read().strip()+'/'
g.close()

def testbot():
    global url
    f=urllib.request.urlopen(url+'getUpdates')
    print(codecs.decode(str(f.read(), encoding="utf-8"),'unicode_escape'))
    f.close()
    print(urllib.request.urlopen(url+'sendMessage?chat_id=83931532&text=message+word').read())
#testbot()

def sendmsg(chatid,text):
    global url
    ntext=quote(text.encode('utf-8'))
    req=urllib.request.urlopen(url+'sendMessage?chat_id='+str(chatid)+'&text='+ntext)
    requ=req.read()
    req.close()
    #html_page = requests.get(url, params={'chat_id':chatid, 'text':text})
    return codecs.decode(str(requ, encoding="utf-8"),'unicode_escape')

def main():
    print(sendmsg(83931532,'привет нео!'))




if __name__ == '__main__':
    main()
