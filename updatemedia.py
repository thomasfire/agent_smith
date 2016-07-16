#!/usr/bin/python3

# updates list of available media(files/media.db)
# this module is used periadically, so bot is rather dinamic:
# you can not to restart bot if you are updating info message or available media
""" Developer and Author: Thomas Fire https://github.com/thomasfire  (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

import vk_api
from logging import exception,basicConfig,WARNING



# These three functions update available list of media, such as audio, gifs, and pictures from your page
'''
They all need file, opened in write mode and of course vk_api tools. See vk_api docs for detailed info
'''
def updateaudio(vk,mediafile):
    audlist=vk.audio.get(need_user=1,count=0)
    newaud=[]
    for x in audlist['items'][1:]:
        newaud.append(str(x['owner_id'])+'_'+str(x['id']))
    mediafile.write('audio:{ '+' '.join(newaud)+' };\n\n')

'''
This function also needs a your user_id and album_id from where to take pictures
'''
def updatepics(vk,mediafile,album_id,user_id):
    piclist=vk.photos.get(owner_id=user_id,album_id=album_id)
    newpic=[]
    for x in piclist['items'][1:]:
        newpic.append(str(x['owner_id'])+'_'+str(x['id']))
    mediafile.write('photo:{ '+' '.join(newpic)+' };\n\n')

def updategifs(vk,mediafile):
    giflist=vk.docs.get(type=3) # type=3 is gif
    newgif=[]
    for x in giflist['items'][1:]:
        newgif.append(str(x['owner_id'])+'_'+str(x['id']))
    mediafile.write('doc:{ '+' '.join(newgif)+' };\n\n')

# it is main function,that starts updating media in correct way
''' Takes:
vk - vk_api tools, see 90-95 lines of this module to see what it is
album_id - from where bot should take media list
user_id - your id
''' # I think it can be understood without my explanation
def main(vk,album_id,user_id):

        mediafile=open('files/media.db','w')
        try:
            updateaudio(vk,mediafile)
            updatepics(vk,mediafile,album_id,user_id)
            updategifs(vk,mediafile)
        except Exception as e:
            exception("smth goes wrong at updating media: \n")
        mediafile.close()


def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

if __name__ == '__main__':
    from fcrypto import gethash,fdecrypt
    from getpass import getpass
    import re
    basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s',
    level = WARNING, filename = 'logs/updatemedia.log')

    #auth
    psswd=gethash(getpass(),mode='pass')
    settings=fdecrypt("files/vk.settings",psswd)
    login="".join(re.findall(r"login=(.+)#endlogin",settings))
    password="".join(re.findall(r"password=(.+)#endpass",settings))
    chatid=int("".join(re.findall(r"chatid=(\d+)#endchatid",settings)))
    albumid=int("".join(re.findall(r"album_id=(\d+)#endalbumid",settings)))
    userid=int("".join(re.findall(r"userid=(\d+)#enduserid",settings)))
    try:
        vk_session = vk_api.VkApi(login, password,captcha_handler=captcha_handler)
    except Exception as e:
        exception('smth goes wrong at getting vk_session\n')
    #authorization
    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        exception(error_msg)

    #getting api
    try:
        vk = vk_session.get_api()
    except Exception as e:
        exception('smth goes wrong at getting vk api\n')

    main(vk,albumid,userid)
