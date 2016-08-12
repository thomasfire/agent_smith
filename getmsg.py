#!/usr/bin/python3

#gets and writes messages
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

import vk_api
from datetime import datetime
from logging import exception,basicConfig,WARNING,warning
import multiio as io


# returns '<first_name> <last_name>' associated with user_id
def getname(user_id,vk):
	if int(user_id)<0:
		return '<club>'

	db=open("files/vk_users.db","r")
	users=db.read()

	#checking if there are information about this user in database

	if str(user_id) in users:
		users=users.split("\n")
		for x in users:
			if str(user_id) in x:
				return x.split('::')[1]
	else:
		db.close()
		# getting name
		name=vk.users.get(user_ids=user_id)

		#saving info of this id to the file for the fast working next time
		db=open("files/vk_users.db","a")
		db.write(str(user_id)+" :: "+" ".join([name[0]['first_name'],name[0]['last_name']])+"\n")
		db.close()

		return " ".join([name[0]['first_name'],name[0]['last_name']])

# marks messages as read via vk_api and id of last message
def markasread(vk,msgid):
	vk.messages.markAsRead(message_ids=msgid,start_message_id=msgid)



#finds attachments in message. Needs received message(one item from received list),
# also needs file opened in append mode
# and ,of course, vk_api tools
def findattachment(x,histmsg,vk):
	#writing action
	if 'action' in x.keys():
		if x['action']=='chat_kick_user':
			histmsg.write('Escaped this chat  ')

		elif x['action']=='chat_invite_user':
			histmsg.write('Joined this chat  ')

		elif x['action']=='chat_title_update':
			histmsg.write('Title updated  ')

		elif x['action']=='chat_photo_remove':
			histmsg.write('Chat photo removed  ')

		elif x['action']=='chat_photo_update':
			histmsg.write('Chat photo updated  ')

		elif x['action']=='chat_create':
			histmsg.write('Chat created  ')

		else:
			histmsg.write('<UNKNOWN ACTION>')
			warning(x)

	#writing attachments
	if 'attachments' in x.keys():

		# cycling through list of attachments
		for y in x['attachments']:
			# checking if it is photo. If it is photo,checking for max available size of this photo and writing its link
			if y['type']=='photo':
				if 'photo_1280' in y['photo'].keys():
					histmsg.write(' photo '+y['photo']['photo_1280'] + '\n ')

				elif 'photo_807' in y['photo'].keys():
					histmsg.write(' photo '+y['photo']['photo_807'] + '\n ')

				elif 'photo_604' in y['photo'].keys():
					histmsg.write(' photo '+y['photo']['photo_604'] + '\n ')

				elif 'photo_130' in y['photo'].keys():
					histmsg.write(' photo '+y['photo']['photo_130'] + '\n ')

				elif 'photo_75' in y['photo'].keys():
					histmsg.write(' photo '+y['photo']['photo_75'] + '\n ')

			# if current attachment is video, just writes its title. VK doesn`t give a link to the videos.
			elif y['type']=='video':
				histmsg.write(' video '+y['video']['title'] + '\n ')

			# if current attachment is audio, write its artist, title and url.
			# PS Yes, vk doesnt gives a link to the video but gives a link to the audio. VK is VK, i cant do anything
			elif y['type']=='audio':
				histmsg.write(' audio '+y['audio']['artist']+' - '+y['audio']['title'] +' ' +y['audio']['url']+ '\n ')

			# if current attachment is document, write its title and url.
			elif y['type']=='doc':
				histmsg.write(' doc '+y['doc']['title'] +' '+ y['doc']['url']+ '\n ')

			# if current attachment is link, write its title and url
			elif y['type']=='link':
				histmsg.write(' link '+y['link']['title'] +' '+ y['link']['url']+ '\n ')

			# if current attachment is post/repost write its text and name of club/user
			elif y['type']=='wall':
				# security checking. Some people doesnt like such bots and they want to brake it
				if not ';\n@' in y['wall']['text']:
					histmsg.write(' wall '+getname(y['wall']['from_id'],vk)
					+': '+y['wall']['text']+'\n ')

			# if current attachment is commentary write its text and name of club/user
			elif y['type']=='wall_reply':
				if not ';\n@' in y['wall_reply']['text']:
					histmsg.write(' comment '+getname(y['wall_reply']['from_id'],vk)+
					': '+y['wall_reply']['text'] +'\n ')

			# if current attachment is sticker write its url
			elif y['type']=='sticker':
				#checking for max available size
				if 'photo_512' in y['sticker'].keys():
					histmsg.write(' sticker '+y['sticker']['photo_512'] + '\n ')

				elif 'photo_352' in y['sticker'].keys():
					histmsg.write(' sticker '+y['sticker']['photo_352'] + '\n ')

				elif 'photo_256' in y['sticker'].keys():
					histmsg.write(' sticker '+y['sticker']['photo_256'] + '\n ')

				elif 'photo_128' in y['sticker'].keys():
					histmsg.write(' sticker '+y['sticker']['photo_128'] + '\n ')

				elif 'photo_64' in y['sticker'].keys():
					histmsg.write(' sticker '+y['sticker']['photo_64'] + '\n ')

			# if current attachment is gift write url to its picture
			elif y['type']=='gift':
				# checking for max size of picture
				if 'thumb_256' in y['gift'].keys():
					histmsg.write(' gift '+y['gift']['thumb_256'] + '\n ')

				elif 'thumb_96' in y['gift'].keys():
					histmsg.write(' gift '+y['gift']['thumb_96'] + '\n ')

				elif 'thumb_48' in y['gift'].keys():
					histmsg.write(' gift '+y['gift']['thumb_48'] + '\n ')

			# logging message about unknown type
			else:
				histmsg.write('<UNKNOWN TYPE>')
				print(x)
				warning(x)

	# writing coordinates of geoposition if map is attached
	if 'geo' in x.keys():
		histmsg.write(' geo '+x['geo']['coordinates'] +' ')

	#writing forwarded messages
	if 'fwd_messages' in x.keys():
		# cycling through list of forwarded messages
		for y in x['fwd_messages']:
			# security checking. Some people doesnt like such bots and they want to brake it
			if not ';\n@' in y['body']:
				# writing it
				histmsg.write(" forwarded from "+getname(y['user_id'],vk)+" :: "+
				datetime.fromtimestamp(y['date']).strftime('%Y-%m-%d %H:%M:%S')+
				" :: "+y['body']+'\n ')
				# find attachments in forwarded message. Forwarded are recursive now
				findattachment(y,histmsg,vk)




# cleans from extra info and writes into the file. Returns id of last message
# needs list of received messages, chat_id and vk_api
def cleanup(msgs, chatid, vk, state_msghistory):
	#io.wait_freedom_and_lock(state_msghistory)
	# loading list of messages
	#histmsg=open('files/msgshistory.db','r')
	#msglog=histmsg.read()
	#histmsg.close()
	msglog=io.read_shared_file('files/msgshistory.db', state_msghistory)
	# opening file in append mode
	io.wait_freedom_and_lock(state_msghistory)
	histmsg=open('files/msgshistory.db','a')

	#writing the messages to the file
	for x in reversed(msgs['items'][:99]):
		#checking if it is needed message and security checking. Some people doesnt like such bots and they want to brake it
		if 'chat_id' in x.keys() and x['chat_id']==chatid and '@ '+str(x['id'])+' ' not in msglog and not ';\n@' in x['body']:
			histmsg.write('@ '+str(x['id'])+' :: '+getname(x['user_id'],vk)+" :: "+
			datetime.fromtimestamp(x['date']).strftime('%Y-%m-%d %H:%M:%S')+' :: '+x['body'])
			# find attachments and forwarded messages
			findattachment(x,histmsg,vk)
			# writing it
			histmsg.write(' ;\n')
	# returning ID of last message

	io.unlock(state_msghistory)
	return msgs['items'][0]['id']



def main(vk,chatidget, state_msghistory,lastid=0):
	try:
		# getting messages. See vk_api docs
		msgs = vk.messages.get(count=200, chat_id=chatidget,last_message_id=lastid)
	# writing to the file and marking as read
		if msgs['items']:
			msgid=cleanup(msgs, chatidget, vk, state_msghistory)
			if msgid:
				try:
					markasread(vk,msgid)
				except:
					exception('smth goes wrong at marking as read')
				return msgid # returning ID of last message
		return lastid
	except ConnectionResetError:
		return lastid
	except Exception as e:
		exception('smth goes wrong at getting messages: ')

# handling captcha мia Terminal
def captcha_handler(captcha):
	key = input("Enter Captcha {0}: ".format(captcha.get_url())).strip()
	return captcha.try_again(key)


if __name__ == '__main__':
	from fcrypto import gethash,fdecrypt
	from getpass import getpass
	import re
	#configuring logs
	basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s',
	level = WARNING, filename = 'logs/getmsg.log')

	#auth
	# getting password to decrypt settings files
	psswd=fcrypto.gethash(getpass(),mode='pass')

	# loading settings
	settings=fcrypto.fdecrypt("files/vk.settings",psswd)
	login="".join(re.findall(r"login=(.+)#endlogin",settings))
	password="".join(re.findall(r"password=(.+)#endpass",settings))
	chatidget=int("".join(re.findall(r"chatid=(\d+)#endchatid",settings)))

	# getting session
	try:
		vk_session = vk_api.VkApi(login, password,captcha_handler=captcha_handler)
	except Exception as e:
		exception('smth goes wrong at getting vk_session:')

	#authorization
	try:
		vk_session.authorization()
	except vk_api.AuthorizationError as error_msg:
		exception(error_msg)
# there some bugs,but if you use it only as module it is stable as a table
	main(vk,chatidget)
