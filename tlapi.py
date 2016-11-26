#!/usr/bin/python3
# -*- coding: utf-8 -*-

# this is API for bot in Telegram
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

from datetime import datetime
from logging import exception
from requests import get as urlget
from urllib.parse import quote
from fcrypto import fdecrypt


# returns a list of stripped values
def strip_list(somelist):
    newlist = []
    for x in somelist:
        if str(type(x)) == "<class 'str'>":
            newlist.append(x.strip())
        else:
            newlist.append(x)
    return newlist


# url of api Telegram. Takes password,that is used in encrypting settings. Without password you cannot do anything
def geturl(password):
    url = ('https://api.telegram.org/bot' +
           fdecrypt('files/telegram.token', password).split()[0].replace('token=', '').replace(';', '') + '/')
    return url


# sends a message to Telegram.
def sendmsg(url, chatid, text):
    """
    url can be received via geturl();
    chatid is chat_id of where to send
    text is text you want to send. Must be less than 4096 bytes.
    See https://core.telegram.org/bots/api for more information about parametres
    """
    ntext = quote(text.encode('utf-8'))

    try:
        requ = urlget('{0}sendMessage?chat_id={1}&text={2}'.format(url, str(chatid), ntext)).json()
    except Exception as msg_error:
        print(' sendMessage have gone wrong; ')
        exception(msg_error)
        return 'error'

    # sometimes it is useful, not in my case
    return str(requ)


# gets and logs to file new messages
def getmsg(url, offset=0, lastid=0):
    """
    url can be received from geturl();
    offset is number of message that must be received first
    See https://core.telegram.org/bots/api for more information about parametres
    """
    try:
        # getting updates via requests.get()
        requ = urlget(url + 'getUpdates' + '?offset=' + str(offset)).json()

        # opening file in append mode
        f = open('files/tl_msgs.db', 'a')
        # logging to file and to the list
        messaglist = []
        for x in requ['result']:
            if x['message']['message_id'] > lastid and 'text' in x['message'].keys():
                # writing this message

                f.write('@ msg_id={0} :: {1} :: {2} :: {3} ;\n'.format(str(x['message']['message_id']),
                                                                       str(x['message']['from']['id']),
                                                                       datetime.fromtimestamp(
                                                                           x['message']['date']).strftime(
                                                                           '%Y-%m-%d %H:%M:%S'),
                                                                       x['message']['text'].replace(';\n@', ':\n:')
                                                                       ))

                # appending list
                messaglist.append(strip_list([str(x['message']['message_id']), str(x['message']['from']['id']),
                                              x['message']['text'].strip()]))

        f.close()
    except Exception as e:
        exception(e)
        return 0, lastid, []

    # if you do not send anything to bot for 24 hours, requ['result'] will be empty.
    if len(requ['result']):
        return requ['result'][-1]['update_id'], requ['result'][-1]['message']['message_id'], messaglist
    else:
        return 0, lastid, []


# gets user`s name
def get_users_name(url, message):
    try:
        requ = urlget(url + 'getUpdates').json()
        for x in requ['result']:
            if str(message[1]) == str(x['message']['from']['id']):

                if 'last_name' in x['message']['from'].keys() and 'first_name' in x['message']['from'].keys():
                    return '{0} {1}'.format(x['message']['from']['first_name'], x['message']['from']['last_name'])

                elif 'first_name' in x['message']['from'].keys():
                    return '{0}'.format(x['message']['from']['first_name'])

                else:
                    return 'Anonymous{0}'.format(message[1])

            else:
                return 'Anonymous{0}'.format(message[1])
    except Exception as e:
        exception(' A error occured while getting updates in Telegram:\n')
        return 'Anonymous{0}'.format(message[1])


# cleans up logs to make them small
def cleanup():
    # loading list of messages
    f = open('files/tl_msgs.db', 'r')
    listofmsgs = f.read().split(' ;\n@ ')
    f.close()
    # writing last 100 messages if there are more than 1000 messages
    if len(listofmsgs) > 1000:
        f = open('files/tl_msgs.db', 'w')
        f.write('@ ' + ' ;\n@ '.join(listofmsgs[-100:]))
        f.close()


# sending url with captcha and waiting for response from God-Odmin
# *There must be picture with holy Linus or Richard Stallman*
def getcaptcha(url, captcha, offset=0):
    """
    url can be received via geturl()
    captcha is url to captcha
    offset is last update_id
    See https://core.telegram.org/bots/api for more information about parametres
    """
    # loading list of Admins
    f = open('files/admins.db', 'r')
    odmins = f.read().strip().split()  # Odmins is joke about Admin
    f.close()

    # sending captha to all Odmins. Telegram will paste a picture of the captcha so Odmins will see it in TL
    for x in odmins:
        sendmsg(url, x, 'Captcha is needed: {0}'.format(str(captcha)))

    # waiting for response from Odmins
    while True:
        # updating messages
        offset, lastid, messaglist = getmsg(url, offset)

        # cycling through last 10 messages. If there will be an DDoS on your bot, Odmin cannot type a captcha
        # But getUpdates is rather fast method, so it is rather hard to DDoS bot if you have small auditory of enemies
        for currmsg in messaglist[-10::-1]:
            if currmsg[1] in odmins and currmsg[3][:8] == '/captcha':
                # returning text of captcha
                return currmsg[3][8:].strip()
