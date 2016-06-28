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

    cycles=0
    while True:
        try:
            getmsg.main(vk_session,chatid)
            if cycles>=100:
                updatemedia.main(vk_session,albumid,userid)
                cycles=0
            makeseq.main()
            telegrambot.main(psswd)
            sendtovk.main(vk_session,chatid)
            print(cycles)
            cycles+=1
        except Exception as exp:
            print("Something gone wrong in bot:\n",exp)






if __name__ == '__main__':
    main()
