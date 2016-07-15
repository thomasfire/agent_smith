#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this is API for bot in Telegram
""" Developer and Author: Thomas Fire https://github.com/thomasfire
### Main manager: Uliy Bee
"""

from requests  import get as urlget
from datetime import datetime
from fcrypto import fdecrypt
from logging import exception,basicConfig,WARNING
from urllib.parse import quote, urlsplit, urlunsplit


#url of api Telegram
def geturl(password):
    url=('https://api.telegram.org/bot'+
    fdecrypt('files/telegram.token',password).split()[0].replace('token=','').replace(';','')+'/')
    return url


#sends a message to Telegram
def sendmsg(url,chatid,text):
    ntext=quote(text.encode('utf-8'))

    try:
        requ=urlget(url+'sendMessage?chat_id='+str(chatid)+'&text='+ntext).json()
    except Exception as msg_error:
        print(' sendMessage have gone wrong; ')
        exception(msg_error)
        return 'error'


    return str(requ)



#gets and logs to file new messages
def getmsg(url,offset=0):
    try:
        requ=urlget(url+'getUpdates'+'?offset='+str(offset)).json()
        f=open('files/tl_msgs.db','r')
        msglist=f.read()
        f.close()
        f=open('files/tl_msgs.db','a')
        #logging to file
        for x in requ['result']:
            #checking if it allowed command
            if (('@ msg_id='+str(x['message']['message_id']) not in msglist and
            (x['message']['text'][0:4]=='/msg' or x['message']['text'][0:6]=='/quote'
            or x['message']['text'][0:5]=='/mode' or x['message']['text'][0:7]=='/chname'
            or x['message']['text'][0:5]=='/help' or x['message']['text'][0:5]=='/auth'
            or x['message']['text'][0:4]=='/log' or x['message']['text'][0:3]=='/me'
            or x['message']['text'][0:6]=='/tllog' or x['message']['text'][0:8]=='/captcha'
            or x['message']['text'][0:8]=='/tlusers'))
            and ';\n@' not in x['message']['text']):

                f.write('@ msg_id='+str(x['message']['message_id'])+' :: '+
                str(x['message']['from']['id'])+' :: '+
                datetime.fromtimestamp(x['message']['date']).strftime('%Y-%m-%d %H:%M:%S')+' :: '+
                x['message']['text']+' ;\n')

        f.close()
    except Exception as e:
        exception(' A error occured while getting updates in Telegram:\n')
        return 'error'

    if len(requ['result']):
        return requ['result'][-1]['update_id']
    else:
        return 0
    


def kickuser(userid):
    f=open('files/shitlist.db','a')
    f.write(' '+str(userid))
    f.close()


#cleans up logs to make them small
def cleanup():
    f=open('files/tl_msgs.db','r')
    listofmsgs=f.read().split(' ;\n@ ')
    f.close()
    if len(listofmsgs)>1000:
        f=open('files/tl_msgs.db','w')
        f.write('@ '+' ;\n@ '.join(listofmsgs[-100:]))
        f.close()

    f=open('files/tl_msgs.made','r')
    listofmsgs=f.read().split()
    f.close()
    if len(listofmsgs)>1000:
        f=open('files/tl_msgs.made','w')
        f.write(' '.join(listofmsgs[-100:]))
        f.close()


#sending url with captcha and waiting for it
def getcaptcha(url,captcha,offset=0):
    f=open('files/admins.db','r')
    odmins=f.read().strip().split()
    f.close()
    f=open('files/tl_msgs.made','r')
    maden=f.read()
    f.close()


    for x in odmins:
        sendmsg(url,x,'Captcha is needed: '+str(captcha))

    while True:
        lastid=getmsg(url,offset)
        f=open('files/tl_msgs.db','r')
        listofmsgs=f.read().split(' ;\n@ ')
        f.close()
        for y in listofmsgs[-10:]:
            currmsg=y.split(' :: ')
            if currmsg[1] in odmins and currmsg[0] not in maden and currmsg[3][:8]=='/captcha':
                f=open('files/tl_msgs.made','a')
                f.write(' '+currmsg[0])
                f.close()
                return currmsg[3][8:].strip()
