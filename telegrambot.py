#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this is bot "Agent Smith beta". He chats in Telegram with people
""" Developer and Author: Thomas Fire https://github.com/thomasfire
### Main manager: Uliy Bee
"""

import urllib
import urllib.request
import codecs
import requests
import datetime
from urllib.parse import quote, urlsplit, urlunsplit
import json
import random
import re


#https://api.telegram.org/bot<token>/METHOD_NAME
#TODO пересылка сообщений из вк в телеграм,пересылка из телеграма в вк,предоставлять лог последних n сообщений из вк -almost done
#TODO 2: добавить возможность пересылки цитатки с помощью /quote; реализовать обработку /help и /msg и /log -done.
#добавить чистку логов -done
#/me -done


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
        requ=requests.get(url+'getUpdates').json()
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
            or x['message']['text'][0:4]=='/log' or x['message']['text'][0:3]=='/me'))
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



def makedict():
    f=open('files/msgshistory.db','r')
    msgs=f.read().split(' ;\n@ ')
    f.close()
    ndict={}
    for x in msgs:
        ndict[x.split(' :: ')[0].strip()]=' : '.join(x.split(' :: ')[1:]).strip()+' ;'
    return ndict




#updates information about users. works with database of users
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
            newusers=[]
            f.close()
            #getting new nickname and writing it to log
            for y in users:
                if x.split(' :: ')[1].strip()==y.split(' :: ')[0].strip():
                    newusers.append('  :: '.join([x.split(' :: ')[1],x.split(' :: ')[3][8:].strip().strip(' ;'),y.split(' :: ')[2]]))
                    sendmsg(y.split(' :: ')[0],"The nickname has been changed")
                else:
                    newusers.append(y)

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
                sendmsg(x.split(' :: ')[1],'This token is wrong or you are already logged in. You can change your nick via /chname <new_nick> if you are authenticated.')
            f.close()
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()

        elif x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:5]=='/mode':
            f=open('files/tl_users.db','r')
            users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
            newusers=[]
            f.close()

            for y in users: #checking if it needable user and if command is correct
                if (x.split(' :: ')[1].strip()==y.split(' :: ')[0].strip() and
                x.split(' :: ')[3][6:].strip().strip(' ;') in ['all','no','imnt']):
                    newusers.append('  :: '.join([x.split(' :: ')[1],y.split(' :: ')[1].strip(),
                    x.split(' :: ')[3][6:].strip().strip(' ;')]))
                    sendmsg(y.split(' :: ')[0],"The mode has been changed")
                else:
                    newusers.append(y)
            #writing to file and logging the id of the message
            f=open('files/tl_users.db','w')
            f.write('@ '+' ;\n@ '.join(newusers)+' ;')
            f.close()
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()

        elif x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:3]=='/me':
            f=open('files/tl_users.db','r')
            users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
            f.close()

            for y in users: #checking if it needable user and if command is correct
                if x.split(' :: ')[1].strip()==y.split(' :: ')[0].strip():
                    sendmsg(y.split(' :: ')[0],"You are logged in as "+y.split(' :: ')[1]+
                    ' with recieving '+y.split(' :: ')[2]+' messages.')
            #writing to file and logging the id of the message
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()


#writes text and message_id(will be deleted as it sent) that will be sent to vk.
def makeseq():
    f=open('files/tl_users.db','r')
    users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
    f.close()
    f=open('files/tl_msgs.made','r')
    maden=f.read()
    f.close()
    f=open('files/tl_msgs.db','r')
    msgs=f.read().split(' ;\n@ ')
    f.close()
    for x in msgs:
        if x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:4]=='/msg':
            for y in users:
                if x.split(' :: ')[1].strip()==y.split(' :: ')[0].strip():
                    g=open('files/tl_msgs.seq','a')
                    g.write('Not_sent_message: '+y.split(' :: ')[1].strip()+': ' +
                    x.split(' :: ')[3].strip().replace('/msg ',' ').strip(' ;')+' ;\n')
                    g.close()
                    sendmsg(y.split(' :: ')[0],"The message will be sent soon.")
                    f=open('files/tl_msgs.made','a')
                    f.write(' '+x.split(' :: ')[0])
                    f.close()



#checks for /log or /help or /quote and responses to user
def response():
    helpmsg="""I`m Agent Smith (beta0.0 June 27 2016). I`m builded with elastic methods, ad-hoc solvings
     and nonstop integration. Beta is unstable, something can work incorrect or do not work. Please report @Thomas_Fire if you
     find a bug. I can execute some commands and send messages from VK to this chat and back. So you can do not open
     VK without worrying miss something imortant. But you need allowance of the @Thomas_Fire to use this bot. He will send you
     an token to log in and use all features. So you need first /auth <token> to log in and start receiving messages.\n
     There are commands I can do:\n
     /auth <token> - log in via <token> you have,after you log in you will be receiving all messages and your nick will
      be Anonymous<some numbers>, but you can change mode or nick;\n
     /help - view this message;\n
     /me - information about you: your nickname and mode of receiving messages;\n
     /log <N> - where <N> is integer number. You will receive N latest messages from VK;\n
     /msg <message_text> - sends <your_nick>:<message_text> to VK;\n
     /chname <new_nick> - changes <your_nick> to <new_nick>;\n
     /mode <new_mode> - changes <your_mode> to <new_mode>. Must be all for receiving all messages from VK, imnt
     for receiving important messages and no for receiving no messages;\n
     /quote - sends my random citation from The Matrix;"""
     
    f=open('files/tl_msgs.made','r')
    maden=f.read()
    f.close()
    f=open('files/tl_msgs.db','r')
    msgs=f.read().strip('@ ').strip(' ;').split(' ;\n@ ')
    f.close()
    f=open('files/tl_users.db','r')
    users=f.read()
    f.close()
    for x in msgs:
        if '@ '+x.split(' :: ')[1].strip()+'  :: ' in users and x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:4]=='/log':
            f=open("files/msgshistory.db","r")
            messages=f.read().strip(' ;').strip("@ ").replace(' :: ',' : ').split(';\n@')
            f.close()
            newmsg=[]

            for y in messages:
                newmsg.append(' : '.join(y.split(' : ')[1:]).strip(' ;'))
            try:
                tosend='\n'.join(newmsg[-int(x.split(' :: ')[3][5:].strip().strip(' ;')):])
            except Exception as e:
                print('Error in making message')
                tosend='You typed incorrect value. Maybe you requested more messages I have, or you typed non integer number.'
            sendmsg(x.split(' :: ')[1].strip(), tosend)
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()

        elif x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:5]=='/help':
            sendmsg(x.split(' :: ')[1].strip(), helpmsg)
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()

        elif '@ '+x.split(' :: ')[1].strip() in users and x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:6]=='/quote':
            f=open('files/citations.db','r')
            tosend=random.choice(f.read().split('\n\n'))
            f.close()
            sendmsg(x.split(' :: ')[1].strip(), tosend)
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
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

#sends messages from vk to Telegram
def fromvktotl():
    f=open('files/msgs.seq','r')
    seq=f.read()
    f.close()
    allmsg=''.join(re.findall(r'all:{(.*?)}',seq)).split()
    imnt=''.join(re.findall(r'important:{(.*?)}',seq)).split()
    msgdict=makedict()

    toall=[]
    toimnt=[]

    for x in allmsg:
        if x in msgdict.keys():
            toall.append(msgdict[x])
    toall='\n'.join(toall)

    for x in imnt:
        if x in msgdict.keys():
            toimnt.append(msgdict[x])
    toimnt='\n'.join(toimnt)
    if toall:
        f=open('files/tl_users.db','r')
        users=f.read().strip('@ ').strip(' ;').split(' ;\n@ ')
        f.close()
        for x in users:
            if x.split(' :: ')[2].strip()=='no':
                continue
            elif toimnt and x.split(' :: ')[2].strip().strip(' ;')=='imnt':
                sendmsg(x.split(' :: ')[0].strip(), toimnt)
            elif x.split(' :: ')[2].strip().strip(' ;')=='all':
                sendmsg(x.split(' :: ')[0].strip(), toall)

    f=open('files/msgs.sent','a')
    f.write(' '+' '.join(allmsg))
    f.close()




def main():
    getmsg()
    updateusers()
    makeseq()
    response()
    fromvktotl()
    cleanup()



if __name__ == '__main__':
    main()
