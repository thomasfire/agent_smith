#!/usr/bin/python3

#sorts and makes sequance
#also cleans up msgshistory.db
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

from re import findall

def main():
    # loading list of messages and list of keywords
    histmsg=open('files/msgshistory.db','r')
    f=open('files/keywords.db','r')
    keywords=f.read().split()
    listofmsgs=histmsg.read().split(' ;\n@ ')[-200:]
    histmsg.close()
    f.close()

    impnt=[]
    allmsg=[]

    # making it more readable
    for x in range(len(listofmsgs)):
        listofmsgs[x]=listofmsgs[x].strip('@ ').strip(' ;')

    # loading sent messages
    f=open('files/msgs.sent','r')
    sent=f.read().split()
    f.close

    # opening sequnce file
    f=open('files/msgs.seq','w')

    # cycling through messages
    for x in listofmsgs:
        msg=x.split(' :: ')
        mess=True
        if len(msg)<4: # some messages maybe empty. it is normal.
            continue
        # not to send message if message consists commands
        for y in ['/quote','/music','/gif','/info','/pic']:
            if y in msg[3]:
                mess=False
                break
        if not mess: continue

        # making all and imnt sequances
        if msg[0].strip() not in sent:
            allmsg.append(msg[0].strip())
            # cycling through keywords
            for y in keywords:
                if y in msg[3].lower() or (msg[3]==msg[3].upper() and len(findall(r'[A-Za-zА-Яа-я]?',msg[3]))>=3):
                    impnt.append(msg[0].strip())
                    break
    # writing sequances
    f.write("important:{"+" ".join(impnt)+"}\n\n" +"all:{"+" ".join(allmsg)+"}")
    f.close()

    # cleaning up messages
    if len(listofmsgs)>1000:
        f=open('files/msgshistory.db','w')
        f.write('@ '+' ;\n@ '.join(listofmsgs[-100:]))
        f.close()

if __name__ == '__main__':
    main()
