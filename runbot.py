#!/usr/bin/python3

#runs all modules in correct way
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
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


# handling captcha via Telegram. See vk_api docs for detailed info
def captcha_handler(captcha):
	global lastid
	key = getcaptcha(url,captcha.get_url().strip(),lastid).strip(';').strip()
	return captcha.try_again(key)

# cleans up files/msgs.sent
def clearsent():
	# loading and splitting it
	f=open('files/msgs.sent','r')
	sent=f.read().split()
	f.close()

	#joining and writing it
	f=open('files/msgs.sent','w')
	f.write(' '.join(sent))
	f.close()

def main():
	# getting password
	psswd=gethash(getpass(),mode='pass')

	# decrypting and loading settings
	settings=fdecrypt("files/vk.settings",psswd)
	login="".join(re.findall(r"login=(.+)#endlogin",settings))
	password="".join(re.findall(r"password=(.+)#endpass",settings))
	chatid=int("".join(re.findall(r"chatid=(\d+)#endchatid",settings)))
	albumid=int("".join(re.findall(r"album_id=(\d+)#endalbumid",settings)))
	userid=int("".join(re.findall(r"userid=(\d+)#enduserid",settings)))

	# getting session
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
	# getting vk_api tools
	try:
		vk = vk_session.get_api()
	except Exception as e:
		exception('smth goes wrong at geting api\n')

	#getting url
	url=geturl(psswd)

	# setting counts
	cycles=0
	lastid=0
	tllast=0
	lastidnew=0

	# starting bot
	print('Logged in, starting bot...')
	while True:
		try: # print point every 3rd iteration
			if cycles%3==0:
				print('.',end='')
				stdout.flush()

			# getting messages
			lastidnew=getmsg.main(vk,chatid,lastid)

			# update list of available media every 500th iterarion. It is about every 4-10th minute if you have non-server connection
			if cycles>=500:
				updatemedia.main(vk,albumid,userid)
				cycles=0
				print('\n',str(datetime.now()),':  Big cycle done!;    vklast=',lastid,';  tllast=',tllast)

			# running retranslation to TL only if there are new messages from VK
			if not lastid==lastidnew:
				makeseq.main()

			# updating messages in TL
			tllast=telegrambot.main(url,tllast)

			# processing commands and retranslation_from_TL in VK
			sendtovk.main(vk,chatid,lastidnew-lastid)

			# updating last number and cleaning up logs
			lastid=lastidnew
			clearsent()

			cycles+=1
		except ConnectionResetError: # there are often this type of errors, but it is not my fault
			continue
		except Exception as exp:
			exception("Something gone wrong in bot:\n")





if __name__ == '__main__':
	main()
