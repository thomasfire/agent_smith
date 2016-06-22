#!/usr/bin/python3

#gets and writes messages

import vk_api
import datetime
import re

def getname(user_id,vk_session):
        db=open("vk_users.db","r")
        users=db.read()

        #checking if there are information about this user in database

        if str(user_id) in users:
            users=users.split("\n")
            for x in users:
                if str(user_id) in x:
                    return x.split(':')[1]
        else:
            db.close()
            vk = vk_session.get_api()
            name=vk.users.get(user_ids=user_id)
            #saving info of this id to the file for the fast working next time
            db=open("vk_users.db","a")
            db.write(str(user_id)+":"+" ".join([name[0]['first_name'],name[0]['last_name']])+"\n")
            db.close()

            return " ".join([name[0]['first_name'],name[0]['last_name']])


def main(vk_session,chatid):

    #authorization and getting needable tools

    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)
    msgs = tools.get_all('messages.get',1,values={'count': 100, 'chat_id': chatid},limit=1)

    histmsg=open('msgshistory.db','r')
    msglog=histmsg.read()
    histmsg.close()
    histmsg=open('msgshistory.db','a')

    #writing the messages to the file
    for x in reversed(msgs['items'][:99]):
        #checking if it is needed message
        if 'chat_id' in x.keys() and x['chat_id']==chatid and str(x['id']) not in msglog:
            histmsg.write('@ '+str(x['id'])+' : '+getname(x['user_id'],vk_session)+"  "+
            datetime.datetime.fromtimestamp(x['date']).strftime('%Y-%m-%d %H:%M:%S')+' : '+x['body'])
            #writing action
            if 'action' in x.keys():
                if x['action']=='chat_kick_user':
                    histmsg.write('Escaped this chat')
                elif x['action']=='chat_invite_user':
                    histmsg.write('Joined this chat')
            #writing attachments
            if 'attachments' in x.keys():
                for y in x['attachments']:
                    if y['type']=='photo':
                        if 'photo_1280' in y['photo'].keys():
                            histmsg.write(' photo '+y['photo']['photo_1280'] + ' ')
                        elif 'photo_807' in y['photo'].keys():
                            histmsg.write(' photo '+y['photo']['photo_807'] + ' ')
                        elif 'photo_604' in y['photo'].keys():
                            histmsg.write(' photo '+y['photo']['photo_604'] + ' ')
                        elif 'photo_130' in y['photo'].keys():
                            histmsg.write(' photo '+y['photo']['photo_130'] + ' ')
                        elif 'photo_75' in y['photo'].keys():
                            histmsg.write(' photo '+y['photo']['photo_75'] + ' ')

                    elif y['type']=='video':
                        histmsg.write(' video '+y['video']['title'] + ' ')
                    elif y['type']=='audio':
                        histmsg.write(' audio '+y['audio']['artist']+y['audio']['title'] +y['audio']['url']+ ' ')
                    elif y['type']=='doc':
                            histmsg.write(' doc '+y['doc']['title'] +' '+ y['doc']['url']+ ' ')
            #writing forwarded messages
            if 'fwd_messages' in x.keys():
                for y in x['fwd_messages']:
                    histmsg.write(" forwarded from "+getname(y['user_id'],vk_session)+" "+
                    datetime.datetime.fromtimestamp(y['date']).strftime('%Y-%m-%d %H:%M:%S')+
                    " : "+y['body'])


            histmsg.write(';\n')


if __name__ == '__main__':
    #auth
    vset=open("vk.settings","r")
    settings=vset.read()
    vset.close()
    login="".join(re.findall(r"login=(.+)#endlogin",settings))
    password="".join(re.findall(r"password=(.+)#endpass",settings))
    chatid=int("".join(re.findall(r"chatid=(\d+)#endchatid",settings)))
    vk_session = vk_api.VkApi(login, password)

    main(vk_session,chatid)
