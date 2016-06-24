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
import datetime
from urllib.parse import quote, urlsplit, urlunsplit
import json


#https://api.telegram.org/bot<token>/METHOD_NAME
#TODO пересылка сообщений из вк в телеграм,пересылка из телеграма в вк,предоставлять лог последних n сообщений

#url of api Telegram
g=open('files/telegram.token')
url='https://api.telegram.org/bot'+g.read().strip()+'/'
g.close()


#sends a message to Telegram
def sendmsg(chatid,text):
    global url
    ntext=quote(text.encode('utf-8'))

    try:
        req=urllib.request.urlopen(url+'sendMessage?chat_id='+str(chatid)+'&text='+ntext)
        requ=req.read()
        req.close()
    except urllib.error.HTTPError as msg_error:
        print(' sendMessage have gone wrong; ')
        print(msg_error)
        return 'error'
    except urllib.error.URLError as msg_error:
        print(' Check your connection status; ')
        print(msg_error)
        return 'error'

    return codecs.decode(str(requ, encoding="utf-8"),'unicode_escape')


#gets and logs to file new messages
def getmsg():
    global url
    try:
        f=urllib.request.urlopen(url+'getUpdates')
        requ=json.loads(codecs.decode(str(f.read(), encoding="utf-8"),'unicode_escape'))
        f.close()
        f=open('files/tl_msgs.db','r')
        msglist=f.read()
        f.close()
        f=open('files/tl_msgs.db','a')
        #logging to file
        for x in requ['result']:

            if (('@ msg_id='+str(x['message']['message_id']) not in msglist and
            (not x['message']['text'][0]=='/' or x['message']['text'][0:4]=='/msg'
            or x['message']['text'][0:5]=='/mode' or x['message']['text'][0:7]=='/chname'
            or x['message']['text'][0:5]=='/help' or x['message']['text'][0:5]=='/auth' ))
            and ';\n@' not in x['message']['text']):

                f.write('@ msg_id='+str(x['message']['message_id'])+' :: '+
                str(x['message']['from']['id'])+' :: '+
                datetime.datetime.fromtimestamp(x['message']['date']).strftime('%Y-%m-%d %H:%M:%S')+' :: '+
                x['message']['text']+' ;\n')

        f.close()
    except Exception as e:
        print(' A error occured while getting updates in Telegram:\n',e)
        return 'error'
    return requ



def updateusers():
    f=open('files/tl_msgs.db','r')
    msgs=f.read().split(' ;\n@ ')
    f.close()
    f=open('files/tl_msgs.made','r')
    maden=f.read()
    f.close()
    for x in msgs:

        if x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:7]=='/chname':
            f=open('files/tl_users.db','r')
            users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
        #    print(users)
            newusers=[]
            f.close()
            for y in users:
                if x.split(' :: ')[1].strip()==y.split(' :: ')[0].strip():
                    newusers.append('  :: '.join([x.split(' :: ')[1],x.split(' :: ')[3][8:].strip().strip(' ;'),y.split(' :: ')[2]]))
                    #print(newusers[-1])
                    sendmsg(y.split(' :: ')[0],"The nicname has been changed")
                else:
                    newusers.append(y)
                    #print(newusers[-1])

            f=open('files/tl_users.db','w')
            f.write('@ '+' ;\n@ '.join(newusers)+' ;')
            f.close()
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()

        elif x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:5]=='/auth':
            f=open('files/tokens.db','r')
            tokens=f.read().split('\n')
            f.close()
            f=open('files/tl_users.db','r')
            users=f.read()
            f.close()
            f=open('files/tl_users.db','a')
            if x.split(' :: ')[3][6:71].strip() in tokens and x.split(' :: ')[1] not in users:
                f.write('@ '+x.split(' :: ')[1]+' :: '+'Anonymous'+x.split(' :: ')[1]+' :: '+'all ;\n')
                sendmsg(x.split(' :: ')[1],"You are now successfully authenticated as "+'Anonymous'+x.split(' :: ')[1]+
                '.\nYou can change your nicname via /chname <new_nick> or you can view a help message via /help.')

                g=open('files/tokens.db','w')
                g.write('\n'.join(tokens).replace(x.split(' :: ')[3][6:71].strip()+'\n',''))
                g.close()
            else:
                sendmsg(x.split(' :: ')[1],'This token is wrong.')
            f.close()
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()





def main():
    getmsg()
    updateusers()



if __name__ == '__main__':
    main()
