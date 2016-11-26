#!/usr/bin/python3

# updates list of available media(files/media.db)
# this module is used periodically, so bot is rather dynamic:
# you can not to restart bot if you are updating info message or available media
""" Developer and Author: Thomas Fire https://github.com/thomasfire  (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

from logging import exception

##################     UPDATING MEDIA FUNCTIONS       ########################################
# ********************************************************************************************#
# ********************************************************************************************#
# ********************************************************************************************#


# These three functions update available list of media, such as audio, gifs, and pictures from your page
'''
They all need file, opened in write mode and of course vk_api tools. See vk_api docs for detailed info
'''


def updateaudio(vk, mediafile):
    audlist = vk.audio.get(need_user=1, count=0)
    newaud = []
    for x in audlist['items'][1:]:
        newaud.append(str(x['owner_id']) + '_' + str(x['id']))
    mediafile.write('audio:{ ' + ' '.join(newaud) + ' };\n\n')


'''
This function also needs a your user_id and album_id from where to take pictures
'''

def updatepics(vk, mediafile, album_id, user_id):
    piclist = vk.photos.get(owner_id=user_id, album_id=album_id)
    newpic = []
    for x in piclist['items'][1:]:
        newpic.append(str(x['owner_id']) + '_' + str(x['id']))
    mediafile.write('photo:{ ' + ' '.join(newpic) + ' };\n\n')


def updategifs(vk, mediafile):
    giflist = vk.docs.get(type=3)  # type=3 is gif
    newgif = []
    for x in giflist['items'][1:]:
        newgif.append(str(x['owner_id']) + '_' + str(x['id']))
    mediafile.write('doc:{ ' + ' '.join(newgif) + ' };\n\n')


# it is main function,that starts updating media in correct way
''' Takes:
vk - vk_api tools, see 90-95 lines of this module to see what it is
album_id - from where bot should take media list
user_id - your id
'''  # I think it can be understood without my explanation


def main(vk, album_id, user_id):
    mediafile = open('files/media.db', 'w')
    try:
        updateaudio(vk, mediafile)
        updatepics(vk, mediafile, album_id, user_id)
        updategifs(vk, mediafile)
    except Exception as e:
        exception("smth goes wrong at updating media: \n")
    mediafile.close()


# ********************************************************************************************#
# ********************************************************************************************#
# ********************************************************************************************#


def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

