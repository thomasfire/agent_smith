#!/usr/bin/python3

#gets and writes messages

import vk_api
import os
import shutil
import sys
import re


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
    print(str(msgs['items'][0]['user_id'])+"  "+str(msgs['items'][0]['date'])+' : '+msgs['items'][0]['body'])


if __name__ == '__main__':
    main()



def startuploading(resource):
    print("Uploading....")
    main(resource)
