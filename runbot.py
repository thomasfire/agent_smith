#!/usr/bin/python3

#runs all modules in correct way
""" Developer and Author: Thomas Fire https://github.com/thomasfire
### Main manager: Uliy Bee
"""

import vk_api
import getmsg
import updatemedia
import makeseq
import sendtovk
import telegrambot
import re
import fcrypto
import getpass
import tlapi as tl
import logging
from sys import stdout
from datetime import datetime

#configuring logs
logging.basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s',
level = logging.WARNING, filename = 'logs/logs.log')

lastid=0
url=''

def captcha_handler(captcha):
    global lastid
    key = tl.getcaptcha(url,captcha.get_url().strip(),lastid).strip(';').strip()
    return captcha.try_again(key)

def clearsent():
    f=open('files/msgs.sent','r')
    sent=f.read().split()
    f.close()
    f=open('files/msgs.sent','w')
    f.write(' '.join(sent))
    f.close()

def main():
    psswd=fcrypto.gethash(getpass.getpass(),mode='pass')
    settings=fcrypto.fdecrypt("files/vk.settings",psswd)
    login="".join(re.findall(r"login=(.+)#endlogin",settings))
    password="".join(re.findall(r"password=(.+)#endpass",settings))
    chatid=int("".join(re.findall(r"chatid=(\d+)#endchatid",settings)))
    albumid=int("".join(re.findall(r"album_id=(\d+)#endalbumid",settings)))
    userid=int("".join(re.findall(r"userid=(\d+)#enduserid",settings)))

    try:
        vk_session = vk_api.VkApi(login, password,captcha_handler=captcha_handler)
    except:
        logging.exception('smth goes wrong at getting vk_session')

    #authorization
    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        logging.exception(error_msg)
        return
    try:
        vk = vk_session.get_api()
    except Exception as e:
        logging.exception('smth goes wrong at geting api\n')

    #getting url
    global url
    url=tl.geturl(psswd)

    cycles=0
    global lastid
    tllast=0
    print('Logged in, starting bot...')
    while True:
        try:
            if cycles%3==0:
                print('.',end='')
                stdout.flush()
            lastid=getmsg.main(vk,chatid,lastid)
            if cycles>=500:
                updatemedia.main(vk_session,albumid,userid,vk)
                cycles=0
                print('\n',str(datetime.now()),':  Big cycle done!;    vklast=',lastid,';  tllast=',tllast)
            makeseq.main()
            tllast=telegrambot.main(psswd,url,tllast)
            sendtovk.main(vk,chatid)
            clearsent()
            cycles+=1
        except Exception as exp:
            logging.exception("Something gone wrong in bot:\n")





if __name__ == '__main__':
    main()
