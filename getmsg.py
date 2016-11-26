#!/usr/bin/python3

# gets and writes messages
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

from datetime import datetime
from logging import exception, warning

user_dict = {}


def get_user_dict():
    db = open("files/vk_users.db", "r")
    userlist = db.read().split('\n')
    newdict = {}

    for x in userlist:
        curruser = x.split(' :: ')
        if len(curruser) == 2:
            newdict[curruser[0]] = curruser[1]
    return newdict


def write_user_dict():
    global user_dict
    db = open("files/vk_users.db", "w")
    for x in user_dict.keys():
        db.write("{0} :: {1}\n".format(x, user_dict[x]))
    db.close()


# returns '<first_name> <last_name>' associated with user_id
def getname(user_id, vk):
    if int(user_id) < 0:
        return '<club>{0}'.format(abs(user_id))
    global user_dict

    # checking if there are information about this user in database

    if str(user_id) in user_dict.keys():
        return user_dict[str(user_id)]
    else:
        # getting name
        name = vk.users.get(user_ids=user_id)
        user_dict[str(user_id)] = " ".join([name[0]['first_name'], name[0]['last_name']])
        write_user_dict()

        return " ".join([name[0]['first_name'], name[0]['last_name']])


# marks messages as read via vk_api and id of last message
def markasread(vk, msgid):
    vk.messages.markAsRead(message_ids=msgid, start_message_id=msgid)


# finds attachments in message. Needs received message(one item from received list),
# also needs string to write
# and ,of course, vk_api tools
def findattachment(x, histmsg, vk):
    # writing action
    if 'action' in x.keys():
        if x['action'] == 'chat_kick_user':
            histmsg += ('Escaped this chat  ')

        elif x['action'] == 'chat_invite_user':
            histmsg += ('Joined this chat  ')

        elif x['action'] == 'chat_title_update':
            histmsg += ('Title updated  ')

        elif x['action'] == 'chat_photo_remove':
            histmsg += ('Chat photo removed  ')

        elif x['action'] == 'chat_photo_update':
            histmsg += ('Chat photo updated  ')

        elif x['action'] == 'chat_create':
            histmsg += ('Chat created  ')

        else:
            histmsg += ('<UNKNOWN ACTION>')
            warning(x)

    # writing attachments
    if 'attachments' in x.keys():

        # cycling through list of attachments
        for y in x['attachments']:
            # checking if it is photo. If it is photo,checking for max available size of this photo and writing its link
            if y['type'] == 'photo':
                if 'photo_1280' in y['photo'].keys():
                    histmsg += (' photo ' + y['photo']['photo_1280'] + '\n ')

                elif 'photo_807' in y['photo'].keys():
                    histmsg += (' photo ' + y['photo']['photo_807'] + '\n ')

                elif 'photo_604' in y['photo'].keys():
                    histmsg += (' photo ' + y['photo']['photo_604'] + '\n ')

                elif 'photo_130' in y['photo'].keys():
                    histmsg += (' photo ' + y['photo']['photo_130'] + '\n ')

                elif 'photo_75' in y['photo'].keys():
                    histmsg += (' photo ' + y['photo']['photo_75'] + '\n ')

            # if current attachment is video, just writes its title. VK doesn`t give a link to the videos.
            elif y['type'] == 'video':
                histmsg += (' video ' + y['video']['title'] + '\n ')

            # if current attachment is audio, write its artist, title and url.
            # PS Yes, vk doesnt gives a link to the video but gives a link to the audio. VK is VK, i cant do anything
            elif y['type'] == 'audio':
                histmsg += (
                ' audio ' + y['audio']['artist'] + ' - ' + y['audio']['title'] + ' ' + y['audio']['url'] + '\n ')

            # if current attachment is document, write its title and url.
            elif y['type'] == 'doc':
                histmsg += (' doc ' + y['doc']['title'] + ' ' + y['doc']['url'] + '\n ')

            # if current attachment is link, write its title and url
            elif y['type'] == 'link':
                histmsg += (' link ' + y['link']['title'] + ' ' + y['link']['url'] + '\n ')

            # if current attachment is post/repost write its text and name of club/user
            elif y['type'] == 'wall':
                histmsg += (' wall ' + getname(y['wall']['from_id'], vk)
                            + ': ' + y['wall']['text'].replace(';\n@', ':\n:') + '\n ')

            # if current attachment is commentary write its text and name of club/user
            elif y['type'] == 'wall_reply':
                histmsg += (' comment ' + getname(y['wall_reply']['from_id'], vk) +
                            ': ' + y['wall_reply']['text'].replace(';\n@', ':\n:') + '\n ')

            # if current attachment is sticker write its url
            elif y['type'] == 'sticker':
                # checking for max available size
                if 'photo_512' in y['sticker'].keys():
                    histmsg += (' sticker ' + y['sticker']['photo_512'] + '\n ')

                elif 'photo_352' in y['sticker'].keys():
                    histmsg += (' sticker ' + y['sticker']['photo_352'] + '\n ')

                elif 'photo_256' in y['sticker'].keys():
                    histmsg += (' sticker ' + y['sticker']['photo_256'] + '\n ')

                elif 'photo_128' in y['sticker'].keys():
                    histmsg += (' sticker ' + y['sticker']['photo_128'] + '\n ')

                elif 'photo_64' in y['sticker'].keys():
                    histmsg += (' sticker ' + y['sticker']['photo_64'] + '\n ')

            # if current attachment is gift write url to its picture
            elif y['type'] == 'gift':
                # checking for max size of picture
                if 'thumb_256' in y['gift'].keys():
                    histmsg += (' gift ' + y['gift']['thumb_256'] + '\n ')

                elif 'thumb_96' in y['gift'].keys():
                    histmsg += (' gift ' + y['gift']['thumb_96'] + '\n ')

                elif 'thumb_48' in y['gift'].keys():
                    histmsg += (' gift ' + y['gift']['thumb_48'] + '\n ')

            # logging message about unknown type
            else:
                histmsg += ('<UNKNOWN TYPE>')
                print(x)
                warning(x)

    # writing coordinates of geoposition if map is attached
    if 'geo' in x.keys():
        histmsg += (' geo ' + x['geo']['coordinates'] + ' ')

    # writing forwarded messages
    if 'fwd_messages' in x.keys():
        # cycling through list of forwarded messages
        for y in x['fwd_messages']:
            # writing it
            histmsg += (" forwarded from " + getname(y['user_id'], vk) + " :: " +
                        datetime.fromtimestamp(y['date']).strftime('%Y-%m-%d %H:%M:%S') +
                        " :: " + y['body'].replace(';\n@', ':\n:') + '\n ')
            # find attachments in forwarded message. Forwarded are recursive now
            histmsg = findattachment(y, histmsg, vk)
    return histmsg


# logs new messages
def log_this(messages, iofile):
    for x in messages:
        iofile.write('a', '@ {} ;\n'.format(' :: '.join(x)))


# cleans from extra info and writes into the file. Returns id of last message
# needs list of received messages, chat_id and vk_api
def cleanup(msgs, chatid, vk, iofile):
    # opening file in append mode
    # msghistory.wait_freedom_and_lock()
    # histmsg=open('files/msgshistory.db','a')
    to_log = []
    # writing the messages to the file
    for x in reversed(msgs['items'][:99]):
        # checking if it is needed message and security checking. Some people doesnt like such bots and they want to brake it
        if 'chat_id' in x.keys() and x['chat_id'] == chatid:
            # histmsg.write('@ '+str(x['id'])+' :: '+getname(x['user_id'],vk)+" :: "+
            # datetime.fromtimestamp(x['date']).strftime('%Y-%m-%d %H:%M:%S')+' :: '+x['body'].replace(';\n@', ':\n:'))
            histmsg = x['body'].replace(';\n@', ':\n:')
            histmsg = findattachment(x, histmsg, vk)

            to_log.append([str(x['id']), getname(x['user_id'], vk),
                           datetime.fromtimestamp(x['date']).strftime('%Y-%m-%d %H:%M:%S'), histmsg])

            log_this(to_log, iofile)
    # returning ID of last message

    # msghistory.unlock()
    return msgs['items'][0]['id'], to_log


def getmain(vk, chatidget, msghistory, userdic, lastid=0):
    global user_dict
    try:
        # getting messages. See vk_api docs
        msgs = vk.messages.get(count=200, chat_id=chatidget, last_message_id=lastid)

        user_dict = userdic
        # writing to the file and marking as read
        if msgs['items']:
            msgid, messages = cleanup(msgs, chatidget, vk, msghistory)
            print(messages)
            if msgid:
                try:
                    markasread(vk, msgid)
                except:
                    exception('smth goes wrong at marking as read')
                return msgid, user_dict, messages  # returning ID of last message
        return lastid, user_dict, []
    except ConnectionResetError:
        return lastid, user_dict, []
    except Exception as e:
        exception('smth goes wrong at getting messages: ', e)


# handling captcha мia Terminal
def captcha_handler(captcha):
    key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)
