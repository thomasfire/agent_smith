#!/usr/bin/python3

#this is bot "Agent Smith". He chats in vk with other people
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""


import vk_api
from random import choice
from logging import exception,basicConfig,WARNING





##################     SEND FUN GIFS, PICS, CITES AND ETC      ###############################
#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#


# next 5 functions send citation, picture, audio, gif and info_message
# They all take similar arguments
'''
vk - vk_api tools. See "vk = vk_session.get_api()" at the end of this file.
chatid - chat_id of chat, where to send all this shit
num - id of message that is proccessing
'''
def sendcit(vk,chatid):
	f=open('files/citations.db','r')
	msg=choice(f.read().split('\n\n'))
	f.close()
	try:
		vk.messages.send(chat_id = chatid, message = msg)

	except Exception as e:
		exception('smth goes wrong at sending citation to vk:\n')





def sendpic(vk,chatid):
	f=open('files/media.db')
	pic='photo'+choice(f.read().split('\n\n')[1].split()[1:-1])
	f.close()
	try:
		vk.messages.send(chat_id = chatid, attachment = pic)

	except Exception as e:
		exception('smth goes wrong at sending picture:\n')





def sendaudio(vk,chatid):
	f=open('files/media.db')
	aud='audio'+choice(f.read().split('\n\n')[0].split()[1:-1])
	f.close()
	try:
		vk.messages.send(chat_id = chatid, attachment = aud)

	except Exception as e:
			exception('smth goes wrong at sending audio:\n')





def sendgif(vk,chatid):
	f=open('files/media.db')
	gif='doc'+choice(f.read().split('\n\n')[2].split()[1:-1])
	f.close()
	try:
		vk.messages.send(chat_id = chatid, attachment = gif)

	except Exception as e:
		exception('smth goes wrong at sending gif:\n')





def sendinfo(vk,chatid):
	f=open('files/info.db','r')
	msg=f.read().split('VK@@##@@TL')[0].strip()
	f.close()
	try:
		vk.messages.send(chat_id = chatid, message = msg)

	except Exception as e:
		exception('smth goes wrong at sending info:\n')



#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#





#sends messages from Telegram to vk
'''
vk - vk_api tools. See "vk = vk_session.get_api()" at the end of this file.
chatid - chat_id where to send messages
'''
def sendtl(vk, chatid, tl_msgs):
	nlist = []
	while tl_msgs:
		nlist.append(tl_msgs.pop(0))
	msgs = '\n'.join(nlist)

	try:
		vk.messages.send(chat_id = chatid, message = msgs)
	except Exception as e:
		exception('smth goes wrong at sending messages from Telegram:\n')







#############################        MAIN         #################################################
#*************************************************************************************************#
#*************************************************************************************************#
#*************************************************************************************************#
#*************************************************************************************************#


'''
vk - vk_api tools. See "vk = vk_session.get_api()" at the end of this file.
chatid - chat_id where to send messages
countofmsgs - count of received messages in latest update. It is useful for optimization
'''
def stvmain(vk, chatid, list_of_cmds, tl_msgs):
	#msgs=msghistory.read().strip().strip(';').split(';\n@')[-10:]
	#nmsg=[]
	# splitting it into parts
	#for x in msgs:
	#	nmsg.append(x.split(' :: '))

	# getting list of sent messages
	#f=open('files/msgs.made','r')
	#sent = f.read()
	#f.close()

	#looking for keywords
	while list_of_cmds:
		curcmd = list_of_cmds.pop(0)
		if '/quote' in curcmd[3]:
			sendcit(vk, chatid)

		elif '/music' in curcmd[3]:
			sendaudio(vk, chatid)

		elif '/gif' in curcmd[3]:
			sendgif(vk, chatid)

		elif '/info' in curcmd[3]:
			sendinfo(vk, chatid)

		elif '/pic' in curcmd[3]:
			sendpic(vk, chatid)

		else:
			continue

	if tl_msgs:
		sendtl(vk, chatid, tl_msgs)







def captcha_handler(captcha):
	key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
	return captcha.try_again(key)
