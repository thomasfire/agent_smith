#!/usr/bin/python3

#updates list of available media(files/media.db)
""" Developer and Author: Thomas Fire https://github.com/thomasfire
### Main manager: Uliy Bee
"""

import vk_api
import re
import fcrypto
import getpass

def updateaudio(vk,mediafile):
    audlist=vk.audio.get(need_user=1,count=0)
    newaud=[]
    for x in audlist['items'][1:]:
        newaud.append(str(x['owner_id'])+'_'+str(x['id']))
    mediafile.write('audio:{ '+' '.join(newaud)+' };\n\n')

def updatepics(vk,mediafile,album_id,user_id):
    piclist=vk.photos.get(owner_id=user_id,album_id=album_id)
    newpic=[]
    for x in piclist['items'][1:]:
        newpic.append(str(x['owner_id'])+'_'+str(x['id']))
    mediafile.write('photo:{ '+' '.join(newpic)+' };\n\n')

def updategifs(vk,mediafile):
    giflist=vk.docs.get(type=3)
    newgif=[]
    for x in giflist['items'][1:]:
        newgif.append(str(x['owner_id'])+'_'+str(x['id']))
    mediafile.write('doc:{ '+' '.join(newgif)+' };\n\n')

def main(vk_session,album_id,user_id,vk):

        mediafile=open('files/media.db','w')
        try:
            updateaudio(vk,mediafile)
            updatepics(vk,mediafile,album_id,user_id)
            updategifs(vk,mediafile)
        except Exception as e:
            print("smth goes wrong at updating media: \n",e)
        mediafile.close()


def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

if __name__ == '__main__':
    #auth
    psswd=fcrypto.gethash(getpass.getpass(),mode='pass')
    settings=fcrypto.fdecrypt("files/vk.settings",psswd)
    login="".join(re.findall(r"login=(.+)#endlogin",settings))
    password="".join(re.findall(r"password=(.+)#endpass",settings))
    chatid=int("".join(re.findall(r"chatid=(\d+)#endchatid",settings)))
    albumid=int("".join(re.findall(r"album_id=(\d+)#endalbumid",settings)))
    userid=int("".join(re.findall(r"userid=(\d+)#enduserid",settings)))
    try:
        vk_session = vk_api.VkApi(login, password,captcha_handler=captcha_handler)
    except Exception as e:
        print('smth goes wrong at getting vk_session\n',e)
    #authorization
    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        
    #getting api
    try:
        vk = vk_session.get_api()
    except Exception as e:
        print('smth goes wrong at getting vk api\n',e)

    main(vk_session,albumid,userid,vk)
