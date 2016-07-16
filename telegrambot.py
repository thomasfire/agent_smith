#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this is bot "Agent Smith beta". He chats in Telegram with people
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

from random import choice as randchoice
import re
from fcrypto import gethash
from getpass import getpass
import tlapi as tl
import makeseq as vkmkseq


#https://api.telegram.org/bot<token>/METHOD_NAME

url=''

# this function returns a dictionary of message_ID: message_Data , where messages are taken from VK
def makedict():
    # loading list VK messages
    f=open('files/msgshistory.db','r')
    msgs=f.read().strip('@ ').strip(' ;').split(' ;\n@ ')
    f.close()

    # making and returning dictionary
    ndict={}
    for x in msgs:
        currmsg=x.split(' :: ')
        # currmsg[0].strip() - message_ID  and   currmsg[1:] -message_Data
        ndict[currmsg[0].strip()] = ' : '.join(currmsg[1:]).strip()+' ;'

    return ndict



#updates information about users. Works with database of users
def updateusers():
    global url

    # loading last TL messages list
    f=open('files/tl_msgs.db','r')
    msgs=f.read().strip(' ;').strip('@ ').split(' ;\n@ ')[-100:]
    f.close()

    # loading list of proccessed messages
    f=open('files/tl_msgs.made','r')
    maden=f.read()
    f.close()

    # loading user`s Black_List
    f=open('files/shitlist.db','r')
    shitlist=f.read().strip().split()
    f.close()

    # cycling through list of messages
    for x in msgs:

        # CURRent MeSsaGe
        currmsg=x.strip().strip(';').strip().split(' :: ')

        # x CURRent USER
        xcurruser=currmsg[1].strip()

        # changes user`s NickName if there is command /chname
        if currmsg[0] not in maden and currmsg[3][:7]=='/chname':
            # loading TL user`s table
            f=open('files/tl_users.db','r')
            users=f.read().strip().strip('@ ').strip(' ;').split(' ;\n@ ')
            newusers=[]
            f.close()

            #getting new nickname and writing it to log
            for y in users:
                ycurruser=y.split(' :: ')[0].strip()
                # if user from message equals user in this line then append this user with new_nick,
                # in other cases just append user;
                # IT SHOULD BE REWRITTEN IF YOU HAVE A LOT OF USERS!!!
                if xcurruser==ycurruser:
                    newusers.append('  :: '.join([xcurruser,currmsg[3][8:].strip().strip(' ;'),y.split(' :: ')[2]]))
                    tl.sendmsg(url,ycurruser,"The nickname has been changed")
                else:
                    newusers.append(y)

            # writing new user`s table into file
            f=open('files/tl_users.db','w')
            f.write('@ '+' ;\n@ '.join(newusers)+' ;\n')
            f.close()

            # marking message as read
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()


        # allows users (except users in Black_List) to log in via 64 byte token (really it lenght is 32 byte,
        # but it has 64 symbols in hexademical mode);
        # Also checks if lenght of typed token is true;
        elif (currmsg[1] not in shitlist and currmsg[0] not in maden and len(currmsg[3])<75
        and len(currmsg[3])>60 and currmsg[3][:5]=='/auth'):

            # loading list of tokens
            f=open('files/tokens.db','r')
            tokens=f.read().split('\n')
            f.close()

            # loading users table
            f=open('files/tl_users.db','r')
            users=f.read()
            f.close()

            # getting hash (other name is publickey) of the token (secretkey)
            publickey=gethash(currmsg[3][6:71].strip())

            # opening TL user`s file in append mode
            f=open('files/tl_users.db','a')

            # loading how many tries people have been maden
            q=open('files/tl_tryes.db','r')
            tryusers=q.read()
            q.close()

            # checking if hash(publickey) is in token`s list and if this user is not logged in
            if publickey in tokens and ' '+currmsg[1]+' ' not in users:

                # writing new user to user table
                f.write('@ '+currmsg[1]+' :: '+'Anonymous'+currmsg[1]+' :: '+'all ;')

                # sending welcome message with some info about user
                tl.sendmsg(url,currmsg[1],"Welcome! You are now successfully authenticated as "+'Anonymous'+currmsg[1]+
                '.\nYou can change your nicname via /chname <new_nick> or you can view a help message via /help.')

                # writing list of publickeys without recently used publickey
                g=open('files/tokens.db','w')
                g.write('\n'.join(tokens).replace(publickey+'\n',''))
                g.close()

            # if computed hash not in the list of available publickeys increase number of tryes of current user
            elif publickey not in tokens and ' '+currmsg[1]+' ' not in users:

                # sending warning message
                tl.sendmsg(url,currmsg[1],'Wrong key.')

                # if it first wrong try add new user to the list, else increment number of tries
                if '@'+currmsg[1]+':' not in tryusers:
                    tryusers+=' @'+currmsg[1]+':1'
                else:
                    # loading list
                    ntryus=tryusers.split()
                    #cycling through users table
                    for y in ntryus:
                        curtry=y.strip().split(':')
                        # if users match increment it
                        if '@'+currmsg[1]+':' in y:
                            tryusers=tryusers.replace(y,
                            curtry[0]+':'+str(int(curtry[1])+1))
                            if int(curtry[1])>2:
                                tl.kickuser(currmsg[1])
                                tryusers=tryusers.replace(y,'')
                            break
                # writing new users table
                q=open('files/tl_tryes.db','w')
                q.write(tryusers)
                q.close()

            # sending message if user already logged in or typed absolutely wrong token or user is in Black_List
            else:
                tl.sendmsg(url,currmsg[1],'You are already logged in. You can change your nick via /chname <new_nick> if you are authenticated.')
            f.close() # closing user`s file

            # marking message as proccessed
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        # changes user`s mode of recieving messages
        elif currmsg[0] not in maden and currmsg[3][:5]=='/mode':
            # loading user`s table
            f=open('files/tl_users.db','r')
            users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
            newusers=[]
            f.close()

            # cycling through user`s list
            for y in users: #checking if it needable user and if command is correct
                curruser=y.split(' :: ')
                #checking if it needable user and if command is correct
                if (currmsg[1].strip()==curruser[0].strip() and
                currmsg[3][6:].strip().strip(' ;') in ['all','no','imnt']):

                    # adding user with new mode
                    newusers.append('  :: '.join([currmsg[1],curruser[1].strip(),
                    currmsg[3][6:].strip().strip(' ;')]))

                    # sending notification about changing NickName
                    tl.sendmsg(url,curruser[0],"The mode has been changed")

                else: # adding user without any changes
                    newusers.append(y)

            #writing to file and logging the id of the message
            f=open('files/tl_users.db','w')
            f.write('@ '+' ;\n@ '.join(newusers)+' ;\n')
            f.close()

            # marking message as proccessed
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        # sends info about user
        elif currmsg[0] not in maden and currmsg[3][:3]=='/me':

            # loading user`s table
            f=open('files/tl_users.db','r')
            users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
            f.close()

            # cycling through user`s table
            for y in users:
                curruser=y.split(' :: ')

                #checking if it needable user
                if currmsg[1].strip()==curruser[0].strip():
                    # sending information about user
                    tl.sendmsg(url,curruser[0],"You are logged in as "+curruser[1]+
                    ' with recieving '+curruser[2]+' messages.')
                # stoping cycling
                    break

            #writing to file and logging the id of the message
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()


#writes text and message_id(will be deleted as it sent) that will be sent to vk.
def makeseq():
    global url

    # loading user`s table
    f=open('files/tl_users.db','r')
    users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
    f.close()

    # loading list of proccessed messages
    f=open('files/tl_msgs.made','r')
    maden=f.read()
    f.close()

    # loading list of messages
    f=open('files/tl_msgs.db','r')
    msgs=f.read().strip().strip(' ;').strip('@ ').split(' ;\n@ ')
    f.close()

    # cycling through list of messages
    for x in msgs:
        currmsg=x.strip(';').strip().split(' :: ')
        # checking if it is needable command
        if currmsg[0] not in maden and currmsg[3][:4]=='/msg':

            # cycling through list of users
            for y in users:
                curruser=y.strip().strip(';').strip().split(' :: ')
                # if user from message matchs with user from current line in users table
                # then write message to the sequence of what to send
                if currmsg[1].strip()==curruser[0].strip():
                    # writing sequence of messages in append mode in case if Something went wrong in VK module
                    g=open('files/tl_msgs.seq','a')
                    g.write('Not_sent_message: '+curruser[1].strip()+': ' +
                    currmsg[3].strip().replace('/msg ',' ').strip(' ;')+' ;\n')
                    g.close()

                    # sending info message
                    tl.sendmsg(url,curruser[0],"The message will be sent soon.")
                    f=open('files/tl_msgs.made','a')
                    f.write(' '+currmsg[0])
                    f.close()
                    for qw in users:
                        if not qw == y:
                            tl.sendmsg(url,qw.strip().strip(';').strip().split(' :: ')[0],'From TL`s '+curruser[1].strip()+': ' +
                            currmsg[3].strip().replace('/msg ',' ').strip(' ;'))
                    break



#checks for /log or /help or /quote and responses to user
def response():
    global url

    # loading list of proccessed messages
    f=open('files/tl_msgs.made','r')
    maden=f.read()
    f.close()

    # loading last messages
    f=open('files/tl_msgs.db','r')
    msgs=f.read().strip('@ ').strip(' ;').split(' ;\n@ ')[-50:]
    f.close()

    # loading users table
    f=open('files/tl_users.db','r')
    users=f.read()
    f.close()
    # loading list of Odmins
    f=open('files/admins.db','r')
    odmins=f.read().strip().split()
    f.close()

    # cycling through messages
    for x in msgs:
        currmsg=x.strip(';').strip().split(' :: ')

        # sends last N messages from VK
        if '@ '+currmsg[1].strip()+' ' in users and currmsg[0] not in maden and currmsg[3][:4]=='/log':
            # loading list of VK messages
            f=open("files/msgshistory.db","r")
            messages=f.read().strip(' ;').strip("@ ").replace(' :: ',' : ').split(';\n@')
            f.close()

            # making more readable list of messages and deleting users IDs
            newmsg=[]
            for y in messages:
                newmsg.append(' : '.join(y.split(' : ')[1:]).strip(' ;'))

            # checking if TL user typed all correct. please do not beat me for this
            try:
                tosend='\n'.join(newmsg[-int(currmsg[3][5:].strip().strip(' ;')):])
            except Exception as e:
                tosend='You typed incorrect value. Maybe you requested more messages I have, or you typed non integer number.'

            # sending message with ErrorMessage or log
            tl.sendmsg(url,currmsg[1].strip(), tosend)

            # marking message as proccessed
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        elif currmsg[0] not in maden and currmsg[3][:5]=='/help':
            # loading description
            f=open('files/info.db','r')
            helpmsg=f.read().split('VK@@##@@TL')[1].strip()
            f.close()

            # sending description
            tl.sendmsg(url,currmsg[1].strip(), helpmsg)

            # marking message as proccessed
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        # sends citation
        elif '@ '+currmsg[1].strip() in users and currmsg[0] not in maden and currmsg[3][:6]=='/quote':

            # loading and choosing citation
            f=open('files/citations.db','r')
            tosend = randchoice(f.read().split('\n\n'))
            f.close()

            # sending citation
            tl.sendmsg(url,currmsg[1].strip(), tosend)

            # marking message as proccessed
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        # [Odmin function] sends N messages bot received from TL
        elif currmsg[1].strip() in odmins and currmsg[0] not in maden and currmsg[3][:6]=='/tllog':
            # loading TL messages list
            f=open("files/tl_msgs.db","r")
            messages=f.read().strip(' ;').strip("@ ").replace(' :: ',' : ').split(';\n@')
            f.close()
            newmsg=[]

            # making them more readable and deleting their [messages`] IDs
            for y in messages:
                newmsg.append(' : '.join(y.split(' : ')[1:]).strip(' ;'))

            # checking if Odmin typed correct value
            try:
                tosend='\n'.join(newmsg[-int(currmsg[3][7:].strip().strip(' ;')):])
            except Exception as e:
                tosend='You typed incorrect value. Maybe you requested more messages I have, or you typed non integer number.'

            # sending messages
            tl.sendmsg(url,currmsg[1].strip(), tosend)

            # marking message as proccessed
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()
        # [Odmin function] sends list of TL users
        elif currmsg[1].strip() in odmins and currmsg[0] not in maden and currmsg[3][:8]=='/tlusers':
            tl.sendmsg(url,currmsg[1].strip(), users.replace(' ;\n@ ','\n').replace(' :: ', ' : ').strip(' ;').strip('@ '))

            #marking message as proccessed
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()



# sends messages from vk to Telegram
def fromvktotl():
    global url

    # loading sequence of what to send. This sequence is generated in makeseq.py module
    f=open('files/msgs.seq','r')
    seq=f.read()
    f.close()
    allmsg=''.join(re.findall(r'all:{(.*?)}',seq)).split()
    imnt=''.join(re.findall(r'important:{(.*?)}',seq)).split()
    # getting dictionary of messages,it looks like message_ID: message_Data
    msgdict=makedict()

    toall=[]
    toimnt=[]

    # making message what to send to users with mode 'all'
    for x in allmsg:
        if x in msgdict.keys():
            toall.append(msgdict[x])
    toall='\n'.join(toall)

    # making message what to send to users with mode 'imnt'
    for x in imnt:
        if x in msgdict.keys():
            toimnt.append(msgdict[x])
    toimnt='\n'.join(toimnt)

    # if toall is not empty then send messages to all users
    if toall:
        # loading user`s table
        f=open('files/tl_users.db','r')
        users=f.read().strip('@').strip(';').strip().split(' ;\n@ ')
        f.close()

        # cycling through user`s table
        for x in users:
            # loading current user
            curruser=x.strip('@').strip(';').strip().split(' :: ')
            # loading user`s mode and ID
            usermode,userid=curruser[2].strip(),curruser[0].strip()

            # doesn`t send if user`s mode is 'no'
            if usermode=='no':
                continue
            # sends important messages to user with 'imnt' mode
            elif toimnt and usermode=='imnt':
                tl.sendmsg(url,userid, toimnt)
            # sends all messages to user with 'all' mode
            elif usermode=='all':
                tl.sendmsg(url,userid, toall)

    # marking messages as sent
    f=open('files/msgs.sent','a')
    f.write(' '+' '.join(allmsg))
    f.close()

    # updating sequance. This is crutch because of optimization.
    if toall:
        vkmkseq.main()



def main(urltl,lastid=0):
    global url
    # writing url from argument to global variable 'url'
    url=urltl

    # getting new last message
    offset=tl.getmsg(url,lastid)

    # if id of last message received equals to id before you updated then do nothing with messages
    if not offset==lastid:
        updateusers()
        makeseq()
        response()
        tl.cleanup()
    # send messages from VK to Telegram
    fromvktotl()

    #returning ID of last messages
    return offset



if __name__ == '__main__':
    psswd=gethash(getpass(),mode='pass')
    url=tl.geturl(psswd)
    main(psswd,url)
