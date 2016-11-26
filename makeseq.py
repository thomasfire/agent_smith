#!/usr/bin/python3

# sorts and makes sequance
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""


def load_keywords():
    f = open('files/keywords.db', 'r')
    keywords = f.read().split()
    f.close()

    return keywords


def mkmain(message, keywords, list_of_alles, list_of_imnts, list_of_cmds):
    impnt = []
    allmsg = []

    # not to send message if message consists commands
    for y in ['/quote', '/music', '/gif', '/info', '/pic']:
        if y in message[3]:
            list_of_cmds.append(message)
            return

    list_of_alles.append(message)
    # cycling through keywords
    for y in keywords:
        if y in message[3].lower() or message[3] == message[3].upper():
            list_of_imnts.append(message)
            return
