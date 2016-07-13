#!/usr/bin/python3

#runs all modules in correct way
""" Developer and Author: Thomas Fire https://github.com/thomasfire
### Main manager: Uliy Bee
"""

import vk_api
import getmsg
import updatemedia
import makeseq
import sendtovk
import telegrambot
import re
from fcrypto import gethash,fdecrypt
from getpass import getpass
from tlapi import geturl,getcaptcha
from logging import exception,basicConfig,WARNING
from sys import stdout
from datetime import datetime

#configuring logs
basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s',
level = WARNING, filename = 'logs/logs.log')

lastid=0
url=''

def captcha_handler(captcha):
	global lastid
	key = getcaptcha(url,captcha.get_url().strip(),lastid).strip(';').strip()
	return captcha.try_again(key)

def clearsent():
	f=open('files/msgs.sent','r')
	sent=f.read().split()
	f.close()
	f=open('files/msgs.sent','w')
	f.write(' '.join(sent))
	f.close()

def main():
	psswd=gethash(getpass(),mode='pass')
	settings=fdecrypt("files/vk.settings",psswd)
	login="".join(re.findall(r"login=(.+)#endlogin",settings))
	password="".join(re.findall(r"password=(.+)#endpass",settings))
	chatid=int("".join(re.findall(r"chatid=(\d+)#endchatid",settings)))
	albumid=int("".join(re.findall(r"album_id=(\d+)#endalbumid",settings)))
	userid=int("".join(re.findall(r"userid=(\d+)#enduserid",settings)))

	try:
		vk_session = vk_api.VkApi(login, password,captcha_handler=captcha_handler)
	except:
		exception('smth goes wrong at getting vk_session')

	#authorization
	try:
		vk_session.authorization()
	except vk_api.AuthorizationError as error_msg:
		exception(error_msg)
		return
	try:
		vk = vk_session.get_api()
	except Exception as e:
		exception('smth goes wrong at geting api\n')

	#getting url
	global url
	url=geturl(psswd)

	cycles=0
	global lastid
	tllast=0
	print('Logged in, starting bot...')
	while True:
		try:
			if cycles%3==0:
				print('.',end='')
				stdout.flush()
			lastid=getmsg.main(vk,chatid,lastid)
			if cycles>=500:
				updatemedia.main(vk,albumid,userid)
				cycles=0
				print('\n',str(datetime.now()),':  Big cycle done!;    vklast=',lastid,';  tllast=',tllast)
			makeseq.main()
			tllast=telegrambot.main(psswd,url,tllast)
			sendtovk.main(vk,chatid)
			clearsent()
			cycles+=1
		except Exception as exp:
			exception("Something gone wrong in bot:\n")





if __name__ == '__main__':
	main()
