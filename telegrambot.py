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
        ndict[x.split(' :: ')[0].strip()]=' : '.join(x.split(' :: ')[1:]).strip()+' ;'
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
    shitlist=f.read().split()
    f.close()
    for x in msgs:

        if x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:7]=='/chname':
            f=open('files/tl_users.db','r')
            users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
            newusers=[]
            f.close()
            #getting new nickname and writing it to log
            for y in users:
                if x.split(' :: ')[1].strip()==y.split(' :: ')[0].strip():
                    newusers.append('  :: '.join([x.split(' :: ')[1],x.split(' :: ')[3][8:].strip().strip(' ;'),y.split(' :: ')[2]]))
                    tl.sendmsg(url,y.split(' :: ')[0],"The nickname has been changed")
                else:
                    newusers.append(y)

            f=open('files/tl_users.db','w')
            f.write('@ '+' ;\n@ '.join(newusers)+' ;\n')
            f.close()
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()

        elif (x.split(' :: ')[1] not in shitlist and x.split(' :: ')[0] not in maden and len(x.split(' :: ')[3])<75
        and len(x.split(' :: ')[3])>60 and x.split(' :: ')[3][:5]=='/auth'):
            f=open('files/tokens.db','r')
            tokens=f.read().split('\n')
            f.close()
            f=open('files/tl_users.db','r')
            users=f.read()
            f.close()
            publickey=fcrypto.gethash(x.split(' :: ')[3][6:71].strip())
            f=open('files/tl_users.db','a')
            q=open('files/tl_tryes.db','r')
            tryusers=q.read()
            q.close()
            if publickey in tokens and ' '+x.split(' :: ')[1]+' ' not in users:
                f.write('@ '+x.split(' :: ')[1]+' :: '+'Anonymous'+x.split(' :: ')[1]+' :: '+'all ;')
                tl.sendmsg(url,x.split(' :: ')[1],"You are now successfully authenticated as "+'Anonymous'+x.split(' :: ')[1]+
                '.\nYou can change your nicname via /chname <new_nick> or you can view a help message via /help.')

                g=open('files/tokens.db','w')
                g.write('\n'.join(tokens).replace(publickey+'\n',''))
                g.close()
            elif publickey not in tokens and ' '+x.split(' :: ')[1]+' ' not in users:
                tl.sendmsg(url,x.split(' :: ')[1],'Wrong key.')
                if '@'+x.split(' :: ')[1]+':' not in tryusers:
                    tryusers+=' @'+x.split(' :: ')[1]+':1'
                else:
                    ntryus=tryusers.split()
                    for y in ntryus:
                        if '@'+x.split(' :: ')[1]+':' in y:
                            print(y)
                            print(y.split(':')[0]+':'+str(int(y.split(':')[1])+1))
                            tryusers=tryusers.replace(y,
                            y.split(':')[0]+':'+str(int(y.split(':')[1])+1))
                            if int(y.split(':')[1])>2:
                                tl.kickuser(x.split(' :: ')[1])
                                tryusers=tryusers.replace(y,'')
                            break

                q=open('files/tl_tryes.db','w')
                q.write(tryusers)
                q.close()
            else:
                tl.sendmsg(url,x.split(' :: ')[1],'You are already logged in. You can change your nick via /chname <new_nick> if you are authenticated.')
            f.close()
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()

        elif x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:5]=='/mode':
            f=open('files/tl_users.db','r')
            users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
            newusers=[]
            f.close()

            for y in users: #checking if it needable user and if command is correct
                if (x.split(' :: ')[1].strip()==y.split(' :: ')[0].strip() and
                x.split(' :: ')[3][6:].strip().strip(' ;') in ['all','no','imnt']):
                    newusers.append('  :: '.join([x.split(' :: ')[1],y.split(' :: ')[1].strip(),
                    x.split(' :: ')[3][6:].strip().strip(' ;')]))
                    tl.sendmsg(url,y.split(' :: ')[0],"The mode has been changed")
                else:
                    newusers.append(y)
            #writing to file and logging the id of the message
            f=open('files/tl_users.db','w')
            f.write('@ '+' ;\n@ '.join(newusers)+' ;\n')
            f.close()
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()

        elif x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:3]=='/me':
            f=open('files/tl_users.db','r')
            users=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
            f.close()

            for y in users: #checking if it needable user and if command is correct
                if x.split(' :: ')[1].strip()==y.split(' :: ')[0].strip():
                    tl.sendmsg(url,y.split(' :: ')[0],"You are logged in as "+y.split(' :: ')[1]+
                    ' with recieving '+y.split(' :: ')[2]+' messages.')
            #writing to file and logging the id of the message
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
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
        if x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:4]=='/msg':
            for y in users:
                if x.split(' :: ')[1].strip()==y.split(' :: ')[0].strip():
                    g=open('files/tl_msgs.seq','a')
                    g.write('Not_sent_message: '+y.split(' :: ')[1].strip()+': ' +
                    x.split(' :: ')[3].strip().replace('/msg ',' ').strip(' ;')+' ;\n')
                    g.close()
                    tl.sendmsg(url,y.split(' :: ')[0],"The message will be sent soon.")
                    f=open('files/tl_msgs.made','a')
                    f.write(' '+x.split(' :: ')[0])
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
    for x in msgs:
        if '@ '+x.split(' :: ')[1].strip()+' ' in users and x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:4]=='/log':
            f=open("files/msgshistory.db","r")
            messages=f.read().strip(' ;').strip("@ ").replace(' :: ',' : ').split(';\n@')
            f.close()
            newmsg=[]

            for y in messages:
                newmsg.append(' : '.join(y.split(' : ')[1:]).strip(' ;'))
            try:
                tosend='\n'.join(newmsg[-int(x.split(' :: ')[3][5:].strip().strip(' ;')):])
            except Exception as e:
                print('Error in making message')
                tosend='You typed incorrect value. Maybe you requested more messages I have, or you typed non integer number.'
            tl.sendmsg(url,x.split(' :: ')[1].strip(), tosend)
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()

        elif x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:5]=='/help':
            #loading description
            f=open('files/info.db','r')
            helpmsg=f.read().split('VK@@##@@TL')[1].strip()
            f.close()

            tl.sendmsg(url,x.split(' :: ')[1].strip(), helpmsg)
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
            f.close()

        elif '@ '+x.split(' :: ')[1].strip() in users and x.split(' :: ')[0] not in maden and x.split(' :: ')[3][:6]=='/quote':
            f=open('files/citations.db','r')
            tosend=random.choice(f.read().split('\n\n'))
            f.close()
            tl.sendmsg(url,x.split(' :: ')[1].strip(), tosend)
            f=open('files/tl_msgs.made','a')
            f.write(' '+x.split(' :: ')[0])
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
            if x.split(' :: ')[2].strip()=='no':
                continue
            elif toimnt and x.split(' :: ')[2].strip().strip(' ;')=='imnt':
                tl.sendmsg(url,x.split(' :: ')[0].strip(), toimnt)
            elif x.split(' :: ')[2].strip().strip(' ;')=='all':
                tl.sendmsg(url,x.split(' :: ')[0].strip(), toall)

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
