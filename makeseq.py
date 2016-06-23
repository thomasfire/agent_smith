#!/usr/bin/python3

#sorts and makes sequance
#also cleans up msgshistory.db
""" Developer and Author: Thomas Fire https://github.com/thomasfire
### Main manager: Uliy Bee
"""


def main():
    histmsg=open('files/msgshistory.db','r')
    f=open('files/keywords.db','r')
    keywords=f.read().split()
    listofmsgs=histmsg.read().split(';\n@')
    histmsg.close()
    f.close()
    impnt=[]
    allmsg=[]

    for x in range(len(listofmsgs)):
        listofmsgs[x]=listofmsgs[x].strip('@ ').strip(';')

    f=open('files/msgs.sent','r')
    sent=f.read()
    f.close
    f=open('files/msgs.seq','w')

    for x in listofmsgs:
        msg=x.split(' : ')
        mess=True
        for y in ['/quote','/audio','/gif','/info','/pic']:
            if y in msg[2]:
                mess=False
                break
        if not mess: continue
        if msg[0].strip() not in sent:
            allmsg.append(msg[0].strip())
            for y in keywords:
                if y in msg[2].lower() or msg[2]==msg[2].upper():
                    impnt.append(msg[0].strip())
                    break
    f.write("important:{"+" ".join(impnt)+"}\n\n" +"all:{"+" ".join(allmsg)+"}")
    f.close()

    if len(listofmsgs)>1000:
        f=open('files/msgshistory.db','w')
        f.write('@ '+' ;\n@ '.join(listofmsgs[-100:]))
        f.close()

if __name__ == '__main__':
    main()
