#!/usr/bin/python3

#gets and writes messages

import vk_api
import os
import shutil
import sys
import re
import datetime

def getname(user_id,vk_session):
        db=open("vk_users.db","r")
        users=db.read()
        if str(user_id) in users:
            users=users.split("\n")
            for x in users:
                if str(user_id) in x:
                    return x.split(':')[1]
        else:
            db.close()
            vk = vk_session.get_api()
            name=vk.users.get(user_ids=user_id)
            db=open("vk_users.db","a")
            db.write(str(user_id)+":"+" ".join([name[0]['first_name'],name[0]['last_name']])+"\n")
            db.close()
            return " ".join([name[0]['first_name'],name[0]['last_name']])


def main():
    vset=open("vk.settings","r")
    settings=vset.read()
    vset.close()
    login="".join(re.findall(r"login=(.+)#endlogin",settings))
    password="".join(re.findall(r"password=(.+)#endpass",settings))
    chatid="".join(re.findall(r"chatid=(\d+)#endchatid",settings))

    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return


    tools = vk_api.VkTools(vk_session)
    msgs = tools.get_all('messages.get',1,values={'count': 1, 'chat_id': chatid},limit=1)
    for x in msgs['items']:
        print(getname(x['user_id'],vk_session)+"  "+
        datetime.datetime.fromtimestamp(x['date']).strftime('%Y-%m-%d %H:%M:%S')+' : '+x['body'])
        if 'fwd_messages' in x.keys():
            for y in x['fwd_messages']:
                print(" forwarded from "+getname(y['user_id'],vk_session)+" "+
                datetime.datetime.fromtimestamp(y['date']).strftime('%Y-%m-%d %H:%M:%S')+
                " : "+y['body'])
        #print(getname(msgs['items'][x]['user_id'],vk_session))

if __name__ == '__main__':
    main()
