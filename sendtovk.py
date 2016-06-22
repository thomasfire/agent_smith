#!/usr/bin/python3

#this is bot "Agent Smith beta". He chats in vk with other people

#TODO лог обработанных сообщений,ответ на сообщения,пересылка сообщений из лога телеграма


import vk_api
import re

def sendcit(vk_session,chatid,num):
    vk = vk_session.get_api()
    pass

def sendpic(vk_session,chatid,num):
    vk = vk_session.get_api()
    pass

def sendaudio(vk_session,chatid,num):
    vk = vk_session.get_api()
    pass

def sendgif(vk_session,chatid,num):
    vk = vk_session.get_api()
    pass

def sendinfo(vk_session,chatid,num):
    vk = vk_session.get_api()
    pass


def main(vk_session,chatid):
    f=open('files/msgshistory.db','r')
    msgs=f.read().split(';\n@')[-10:]
    f.close()
    nmsg=[]
    for x in msgs:
        nmsg.append(x.split(' : '))
    f=open('files/msgs.made','r')
    sent=f.read()
    f.close()
    for x in nmsg:
        if '/quote' in x[2] and x[0] not in sent:
            sendcit(vk_session,chatid,num)
        elif '/audio' in x[2]:
            sendaudio(vk_session,chatid,num)
        elif '/gif' in x[2]:
            sendgif(vk_session,chatid,num)
        elif '/info' in x[2]:
            sendgif(vk_session,chatid,num)
        elif '/pic' in x[2]:
            sendpic(vk_session,chatid,num)
        else:
            continue


if __name__ == '__main__':
    #auth
    vset=open("files/vk.settings","r")
    settings=vset.read()
    vset.close()
    login="".join(re.findall(r"login=(.+)#endlogin",settings))
    password="".join(re.findall(r"password=(.+)#endpass",settings))
    chatid=int("".join(re.findall(r"chatid=(\d+)#endchatid",settings)))
    vk_session = vk_api.VkApi(login, password)

    main(vk_session,chatid)
