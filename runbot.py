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


def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


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
        print('smth goes wrong at getting vk_session')

    #authorization
    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return
    try:
        vk = vk_session.get_api()
    except Exception as e:
        print('smth goes wrong at geting api\n',e)

    #getting url
    url=telegrambot.geturl(psswd)

    cycles=0
    lastid=0
    tllast=0
    while True:
        try:
            print('cycle=',cycles,';    vklast=',lastid,';  tllast=',tllast)
            lastid=getmsg.main(vk_session,chatid,vk,lastid)
            if cycles>=100:
                updatemedia.main(vk_session,albumid,userid,vk)
                cycles=0
            makeseq.main()
            tllast=telegrambot.main(psswd,tllast,url)
            sendtovk.main(vk_session,chatid,vk)
            cycles+=1
        except Exception as exp:
            print("Something gone wrong in bot:\n",exp)






if __name__ == '__main__':
    main()
