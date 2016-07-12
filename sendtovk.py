#!/usr/bin/python3

#this is bot "Agent Smith beta". He chats in vk with other people
""" Developer and Author: Thomas Fire https://github.com/thomasfire
### Main manager: Uliy Bee
"""


import vk_api
from random import choice
from logging import exception,basicConfig,WARNING




def sendcit(vk,chatid,num):
    f=open('files/citations.db','r')
    msg=choice(f.read().split('\n\n'))
    f.close()
    try:
        vk.messages.send(chat_id=chatid,message=msg)
        f=open('files/msgs.made','a')
        f.write(' :'+str(num)+': ')
        f.close()
    except Exception as e:
        exception('smth goes wrong at sending citation to vk:\n')

def sendpic(vk,chatid,num):
    f=open('files/media.db')
    pic='photo'+choice(f.read().split('\n\n')[1].split()[1:-1])
    f.close()
    try:
        vk.messages.send(chat_id=chatid,attachment=pic)
        f=open('files/msgs.made','a')
        f.write(' :'+str(num)+': ')
        f.close()
    except Exception as e:
        exception('smth goes wrong at sending picture:\n')

def sendaudio(vk,chatid,num):
    f=open('files/media.db')
    aud='audio'+choice(f.read().split('\n\n')[0].split()[1:-1])
    f.close()
    try:
        vk.messages.send(chat_id=chatid,attachment=aud)
        f=open('files/msgs.made','a')
        f.write(' :'+str(num)+': ')
        f.close()
    except Exception as e:
            exception('smth goes wrong at sending audio:\n')

def sendgif(vk,chatid,num):
    f=open('files/media.db')
    gif='doc'+choice(f.read().split('\n\n')[2].split()[1:-1])
    f.close()
    try:
        vk.messages.send(chat_id=chatid,attachment=gif)
        f=open('files/msgs.made','a')
        f.write(' :'+str(num)+': ')
        f.close()
    except Exception as e:
        exception('smth goes wrong at sending gif:\n')

def sendinfo(vk,chatid,num):
    f=open('files/info.db','r')
    msg=f.read().split('VK@@##@@TL')[0].strip()
    f.close()
    try:
        vk.messages.send(chat_id=chatid,message=msg)
        f=open('files/msgs.made','a')
        f.write(' :'+str(num)+': ')
        f.close()
    except Exception as e:
        exception('smth goes wrong at sending info:\n')

#sends messages from Telegram to vk
def sendtl(vk, chatid):
    try:
        f=open('files/tl_msgs.seq','r')
        msgs=f.read().replace('Not_sent_message: ','')
        f.close()
        if msgs:
            vk.messages.send(chat_id=chatid,message=msgs)
        f=open('files/tl_msgs.seq','w')
        f.write('')
        f.close()
    except Exception as e:
        exception('smth goes wrong at sending messages from Telegram:\n')



def main(vk,chatid):
    f=open('files/msgshistory.db','r')
    msgs=f.read().split(';\n@')[-10:]
    f.close()
    nmsg=[]
    for x in msgs:
        nmsg.append(x.split(' :: '))
    f=open('files/msgs.made','r')
    sent=f.read()
    f.close()

    #looking for keywords
    for x in nmsg:
        if '/quote' in x[3] and ': '+str(x[0]).strip()+': ' not in sent:
            sendcit(vk,chatid,x[0])
        elif '/audio' in x[3] and ': '+str(x[0]).strip()+': ' not in sent:
            sendaudio(vk,chatid,x[0])
        elif '/gif' in x[3] and ': '+str(x[0]).strip()+': ' not in sent:
            sendgif(vk,chatid,x[0])
        elif '/info' in x[3] and ': '+str(x[0]).strip()+': ' not in sent:
            sendinfo(vk,chatid,x[0])
        elif '/pic' in x[3] and ': '+str(x[0]).strip()+': ' not in sent:
            sendpic(vk,chatid,x[0])
        else:
            continue

    sendtl(vk,chatid)


def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

if __name__ == '__main__':
    from fcrypto import gethash,fdecrypt
    from getpass import getpass
    import re
    #configuring logs
    basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s',
    level = WARNING, filename = 'logs/sendtovk.log')

    #auth
    psswd=gethash(getpass(),mode='pass')
    settings=fdecrypt("files/vk.settings",psswd)
    login="".join(re.findall(r"login=(.+)#endlogin",settings))
    password="".join(re.findall(r"password=(.+)#endpass",settings))
    chatid=int("".join(re.findall(r"chatid=(\d+)#endchatid",settings)))
    try:
        vk_session = vk_api.VkApi(login, password,captcha_handler=captcha_handler)
        main(vk_session,chatid)
    except Exception as e:
        exception('smth goes wrong at getting vk_session\n')

    #authorization and getting needable tools
    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        exception(error_msg)

    try:
        vk = vk_session.get_api()
    except Exception as e:
        exception('smth goes wrong at geting api\n')

    main(vk,chatid)
