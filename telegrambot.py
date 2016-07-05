#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this is bot "Agent Smith beta". He chats in Telegram with people
""" Developer and Author: Thomas Fire https://github.com/thomasfire
### Main manager: Uliy Bee
"""

import random
import re
import fcrypto
import getpass
import tlapi as tl


#https://api.telegram.org/bot<token>/METHOD_NAME

url=''


def makedict():
    f=open('files/msgshistory.db','r')
    msgs=f.read().split(' ;\n@ ')
    f.close()
    ndict={}
    for x in msgs:
        currmsg=x.split(' :: ')
        ndict[currmsg[0].strip()]=' : '.join(currmsg[1:]).strip()+' ;'
    return ndict



#updates information about users. works with database of users
def updateusers():
    global url

    f=open('files/tl_msgs.db','r')
    msgs=f.read().split(' ;\n@ ')
    f.close()
    f=open('files/tl_msgs.made','r')
    maden=f.read()
    f.close()
    f=open('files/shitlist.db','r')
    shitlist=f.read().strip().split()
    f.close()
    for x in msgs:
        currmsg=x.strip().strip(';').strip().split(' :: ')
        xcurruser=currmsg[1].strip()
        if currmsg[0] not in maden and currmsg[3][:7]=='/chname':
            f=open('files/tl_users.db','r')
            users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
            newusers=[]
            f.close()
            #getting new nickname and writing it to log
            for y in users:
                ycurruser=y.split(' :: ')[0].strip()
                if xcurruser==ycurruser:
                    newusers.append('  :: '.join([xcurruser,currmsg[3][8:].strip().strip(' ;'),y.split(' :: ')[2]]))
                    tl.sendmsg(url,ycurruser,"The nickname has been changed")
                else:
                    newusers.append(y)

            f=open('files/tl_users.db','w')
            f.write('@ '+' ;\n@ '.join(newusers)+' ;\n')
            f.close()
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        elif (currmsg[1] not in shitlist and currmsg[0] not in maden and len(currmsg[3])<75
        and len(currmsg[3])>60 and currmsg[3][:5]=='/auth'):
            f=open('files/tokens.db','r')
            tokens=f.read().split('\n')
            f.close()

            f=open('files/tl_users.db','r')
            users=f.read()
            f.close()

            publickey=fcrypto.gethash(currmsg[3][6:71].strip())

            f=open('files/tl_users.db','a')

            q=open('files/tl_tryes.db','r')
            tryusers=q.read()
            q.close()
            if publickey in tokens and ' '+currmsg[1]+' ' not in users:
                f.write('@ '+currmsg[1]+' :: '+'Anonymous'+currmsg[1]+' :: '+'all ;')
                tl.sendmsg(url,currmsg[1],"You are now successfully authenticated as "+'Anonymous'+currmsg[1]+
                '.\nYou can change your nicname via /chname <new_nick> or you can view a help message via /help.')

                g=open('files/tokens.db','w')
                g.write('\n'.join(tokens).replace(publickey+'\n',''))
                g.close()
            elif publickey not in tokens and ' '+currmsg[1]+' ' not in users:
                tl.sendmsg(url,currmsg[1],'Wrong key.')
                if '@'+currmsg[1]+':' not in tryusers:
                    tryusers+=' @'+currmsg[1]+':1'
                else:
                    ntryus=tryusers.split()
                    for y in ntryus:
                        curtry=y.strip().split(':')
                        if '@'+currmsg[1]+':' in y:
                            tryusers=tryusers.replace(y,
                            curtry[0]+':'+str(int(curtry[1])+1))
                            if int(curtry[1])>2:
                                tl.kickuser(currmsg[1])
                                tryusers=tryusers.replace(y,'')
                            break

                q=open('files/tl_tryes.db','w')
                q.write(tryusers)
                q.close()
            else:
                tl.sendmsg(url,currmsg[1],'You are already logged in. You can change your nick via /chname <new_nick> if you are authenticated.')
            f.close()
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        elif currmsg[0] not in maden and currmsg[3][:5]=='/mode':
            f=open('files/tl_users.db','r')
            users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
            newusers=[]
            f.close()

            for y in users: #checking if it needable user and if command is correct
                curruser=y.split(' :: ')
                if (currmsg[1].strip()==curruser[0].strip() and
                currmsg[3][6:].strip().strip(' ;') in ['all','no','imnt']):
                    newusers.append('  :: '.join([currmsg[1],curruser[1].strip(),
                    currmsg[3][6:].strip().strip(' ;')]))
                    tl.sendmsg(url,curruser[0],"The mode has been changed")
                else:
                    newusers.append(y)
            #writing to file and logging the id of the message
            f=open('files/tl_users.db','w')
            f.write('@ '+' ;\n@ '.join(newusers)+' ;\n')
            f.close()
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        elif currmsg[0] not in maden and currmsg[3][:3]=='/me':
            f=open('files/tl_users.db','r')
            users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
            f.close()

            for y in users: #checking if it needable user and if command is correct
                curruser=y.split(' :: ')
                if currmsg[1].strip()==curruser[0].strip():
                    tl.sendmsg(url,curruser[0],"You are logged in as "+curruser[1]+
                    ' with recieving '+curruser[2]+' messages.')
            #writing to file and logging the id of the message
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()


#writes text and message_id(will be deleted as it sent) that will be sent to vk.
def makeseq():
    global url

    f=open('files/tl_users.db','r')
    users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
    f.close()
    f=open('files/tl_msgs.made','r')
    maden=f.read()
    f.close()
    f=open('files/tl_msgs.db','r')
    msgs=f.read().split(' ;\n@ ')
    f.close()
    for x in msgs:
        currmsg=x.strip(';').strip().split(' :: ')
        if currmsg[0] not in maden and currmsg[3][:4]=='/msg':
            for y in users:
                curruser=y.strip().strip(';').strip().split(' :: ')
                if currmsg[1].strip()==curruser[0].strip():
                    g=open('files/tl_msgs.seq','a')
                    g.write('Not_sent_message: '+curruser[1].strip()+': ' +
                    currmsg[3].strip().replace('/msg ',' ').strip(' ;')+' ;\n')
                    g.close()
                    tl.sendmsg(url,curruser[0],"The message will be sent soon.")
                    f=open('files/tl_msgs.made','a')
                    f.write(' '+currmsg[0])
                    f.close()



#checks for /log or /help or /quote and responses to user
def response():
    global url

    f=open('files/tl_msgs.made','r')
    maden=f.read()
    f.close()

    f=open('files/tl_msgs.db','r')
    msgs=f.read().strip('@ ').strip(' ;').split(' ;\n@ ')
    f.close()

    #loading users table
    f=open('files/tl_users.db','r')
    users=f.read()
    f.close()
    f=open('files/admins.db','r')
    odmins=f.read().strip().split()
    f.close()
    for x in msgs:
        currmsg=x.strip(';').strip().split(' :: ')
        if '@ '+currmsg[1].strip()+' ' in users and currmsg[0] not in maden and currmsg[3][:4]=='/log':
            f=open("files/msgshistory.db","r")
            messages=f.read().strip(' ;').strip("@ ").replace(' :: ',' : ').split(';\n@')
            f.close()
            newmsg=[]

            for y in messages:
                newmsg.append(' : '.join(y.split(' : ')[1:]).strip(' ;'))
            try:
                tosend='\n'.join(newmsg[-int(currmsg[3][5:].strip().strip(' ;')):])
            except Exception as e:
                print('Error in making message')
                tosend='You typed incorrect value. Maybe you requested more messages I have, or you typed non integer number.'
            tl.sendmsg(url,currmsg[1].strip(), tosend)
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        elif currmsg[0] not in maden and currmsg[3][:5]=='/help':
            #loading description
            f=open('files/info.db','r')
            helpmsg=f.read().split('VK@@##@@TL')[1].strip()
            f.close()

            tl.sendmsg(url,currmsg[1].strip(), helpmsg)
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        elif '@ '+currmsg[1].strip() in users and currmsg[0] not in maden and currmsg[3][:6]=='/quote':
            f=open('files/citations.db','r')
            tosend=random.choice(f.read().split('\n\n'))
            f.close()
            tl.sendmsg(url,currmsg[1].strip(), tosend)
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        elif currmsg[1].strip() in odmins and currmsg[0] not in maden and currmsg[3][:6]=='/tllog':
            f=open("files/tl_msgs.db","r")
            messages=f.read().strip(' ;').strip("@ ").replace(' :: ',' : ').split(';\n@')
            f.close()
            newmsg=[]

            for y in messages:
                newmsg.append(' : '.join(y.split(' : ')[1:]).strip(' ;'))
            try:
                tosend='\n'.join(newmsg[-int(currmsg[3][7:].strip().strip(' ;')):])
            except Exception as e:
                print('Error in making message')
                tosend='You typed incorrect value. Maybe you requested more messages I have, or you typed non integer number.'
            tl.sendmsg(url,currmsg[1].strip(), tosend)
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()

        elif currmsg[1].strip() in odmins and currmsg[0] not in maden and currmsg[3][:8]=='/tlusers':
            tl.sendmsg(url,currmsg[1].strip(), users)
            f=open('files/tl_msgs.made','a')
            f.write(' '+currmsg[0])
            f.close()



#sends messages from vk to Telegram
def fromvktotl():
    f=open('files/msgs.seq','r')
    seq=f.read()
    f.close()
    allmsg=''.join(re.findall(r'all:{(.*?)}',seq)).split()
    imnt=''.join(re.findall(r'important:{(.*?)}',seq)).split()
    msgdict=makedict()

    toall=[]
    toimnt=[]

    for x in allmsg:
        if x in msgdict.keys():
            toall.append(msgdict[x])
    toall='\n'.join(toall)

    for x in imnt:
        if x in msgdict.keys():
            toimnt.append(msgdict[x])
    toimnt='\n'.join(toimnt)
    if toall:
        f=open('files/tl_users.db','r')
        users=f.read().strip('@').strip(';').strip().split(' ;\n@ ')
        f.close()
        for x in users:
            curruser=x.strip('@').strip(';').strip().split(' :: ')
            usermode,userid=curruser[2].strip(),curruser[0].strip()

            if usermode=='no':
                continue
            elif toimnt and usermode=='imnt':
                tl.sendmsg(url,userid, toimnt)
            elif usermode=='all':
                tl.sendmsg(url,userid, toall)

    f=open('files/msgs.sent','a')
    f.write(' '+' '.join(allmsg))
    f.close()



def main(password,lastid,urltl):
    global url
    url=urltl
    offset=tl.getmsg(url,lastid)
    updateusers()
    makeseq()
    response()
    fromvktotl()
    tl.cleanup()
    return offset



if __name__ == '__main__':
    psswd=fcrypto.gethash(getpass.getpass(),mode='pass')
    url=tl.geturl(psswd)
    main(psswd)
