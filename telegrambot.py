#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this is bot "Agent Smith beta". He chats in Telegram with people
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

from random import choice as randchoice
import re
from fcrypto import gethash
from getpass import getpass
import tlapi as tl
from datetime import datetime
from time import sleep as tsleep
from logging import exception,basicConfig,WARNING
from sys import stdout
#https://api.telegram.org/bot<token>/METHOD_NAME

url=''
users=[]
odmins=[]





##################      SOME USEFUL FUNCTIONS       ##########################################
#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#


# this function returns a dictionary of message_ID: message_Data , where messages are taken from VK
def makedict():
	# loading list VK messages
	f=open('files/msgshistory.db','r')
	msgs=f.read().strip('@ ').strip(' ;').split(' ;\n@ ')
	f.close()

	# making and returning dictionary
	ndict={}
	for x in msgs:
		currmsg=x.split(' :: ')
		# currmsg[0].strip() - message_ID  and   currmsg[1:] -message_Data
		ndict[currmsg[0].strip()] = ' : '.join(currmsg[1:]).strip()+' ;'

	return ndict





# writes current table of users to the file
def write_users_table():
	user_text=[]
	for x in users:
		user_text.append(' :: '.join(x))

	f=open('files/tl_users.db','w')
	f.write('@ '+' ;\n@ '.join(user_text)+' ;\n')
	f.close()





# returns a line with info about user. also returns it`s index
def get_tl_user(user_id):
	y=0
	for x in users:
		if x[0]==user_id:
			return x, y
		y+=1
	return [], -1



# returns a list of stripped values
def strip_list(somelist):
	newlist=[]
	for x in somelist:
		if str(type(x))=="<class 'str'>":
			newlist.append(x.strip())
		else:
			newlist.append(x)
	return newlist





# updates list of users. Is needable when there were some operations with users
def update_users_table():
	global users
	# loading user`s table
	f=open('files/tl_users.db','r')
	userstext=f.read().strip('@ ').strip(' ;\n').split(' ;\n@ ')
	f.close()
	users=[]
	for x in userstext:
		users.append(strip_list(x.split(' :: ')))






# updates list of Odmins
def update_odmins_list():
	global odmins
	# loading list of Odmins
	f=open('files/admins.db','r')
	odmins=f.read().strip().split()
	f.close()



#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#









###############      THESE FUNCTIONS WORK WITH USER`S TABLE      #############################
#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#


# authes user.
def auth_user(message):
	global url
	global users

	# allows users to log in via 64 byte token (really it lenght is 32 byte,
	# but it has 64 symbols in hexademical mode);
	# Also checks if lenght of typed token is true;
	if len(message[2])<75 and len(message[2])>60:
		# loading list of tokens
		f=open('files/tokens.db','r')
		tokens=f.read().split('\n')
		f.close()
		if not tokens:
			return
		# getting hash (other name is publickey) of the token (secretkey)
		publickey=gethash(message[2][6:71].strip())

		# opening TL user`s file in append mode
		f=open('files/tl_users.db','a')
		# checking if hash(publickey) is in token`s list and if this user is not logged in
		if publickey in tokens and not get_tl_user(message[1])[0]:
			# writing new user to user table
			f.write('@ '+message[1]+' :: '+'Anonymous'+message[1]+' :: '+'all ;')
			# sending welcome message with some info about user
			tl.sendmsg(url, message[1], "Welcome! You are now successfully authenticated as "+'Anonymous'+message[1]+
			'.\nYou can change your nicname via /chname <new_nick> or you can view a help message via /help.')
			# writing list of publickeys without recently used publickey
			g=open('files/tokens.db','w')
			g.write('\n'.join(tokens).replace(publickey+'\n',''))
			g.close()
		# if computed hash not in the list of available publickeys increase number of tryes of current user
	elif publickey not in tokens and not get_tl_user(message[1])[0]:
		# sending warning message
		tl.sendmsg(url, message[1], 'Wrong key.')
	# sending message if user already logged in or typed absolutely wrong token or user is in Black_List
	else:
		tl.sendmsg(url, message[1], 'You are already logged in. You can change your nick via /chname <new_nick> if you are authenticated.')

	f.close() # closing user`s file





def change_users_name(message):
	global url
	global users
	newusers=[]
	#getting new nickname and writing it to log
	curruser, line = get_tl_user(message[1])
	if not curruser:
		return

	users[line][1] = message[2][8:]
	tl.sendmsg(url, message[1], "The nickname has been changed")

	write_users_table()




def change_users_mode(message):
	global url

	curruser, line = get_tl_user(message[1])
	if not curruser or not message[2][6:] in ['all','no','imnt']:
		return

	users[line][2] = message[2][6:]
	tl.sendmsg(url, message[1], "The mode has been changed")

	write_users_table()





# sends information about user
def send_users_info(message):
	curruser, line = get_tl_user(message[1])
	if not curruser:
		return
	tl.sendmsg(url, curruser[0] ,"You are logged in as "+curruser[1]+
	' with recieving '+curruser[2]+' messages.')


#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#








###############      THESE FUNCTIONS ARE ASSOCIATED WITH VK      #############################
#*****************  ****************  ******  *****  ****************************************#
#*******************  ************  ********  ***  ******************************************#
#*********************  *******  ***********  *  ********************************************#
#***********************  ***  *************  ***  ******************************************#
#************************    ***************  *****  ****************************************#


#writes text and message_id(will be deleted as it sent) that will be sent to vk.
def msg_send_to_vk(message, tl_msgs, new_to_vk):
	global url

	curruser, line = get_tl_user(message[1])

	if not curruser:
		return

	tl_msgs.write('a', '{0}: {1} ;\n'.format(curruser[1], message[2][5:]))

	new_to_vk.value = 1
	# sending info message
	tl.sendmsg(url, curruser[0], "The message will be sent soon.")
	for qw in users:
		if not qw[0] == curruser[0]:
			tl.sendmsg(url, qw[0], 'From TL`s ' + curruser[1] + ': ' + message[2][5:])





# sends last N messages from VK
def send_vk_log(message, msghistory):
	global users

	if get_tl_user(message[1])[0]:
		# loading list of VK messages
		vk_messages=msghistory.read().strip(' ;').strip("@ ").replace(' :: ',' : ').split(';\n@')

		# making more readable list of messages and deleting users IDs
		newmsg=[]
		for y in vk_messages:
			newmsg.append(' : '.join(y.split(' : ')[1:]).strip(' ;'))

		# checking if TL user typed all correct. please do not beat me for this
		try:
			tosend='\n'.join(newmsg[-int(message[2][5:].strip()):])
		except Exception as e:
			tosend='You typed incorrect value. Maybe you requested more messages I have, or you typed non integer number.'

		# sending message with ErrorMessage or log
		tl.sendmsg(url, message[1].strip(), tosend)



#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#







###############      THESE FUNCTIONS SEND INFO OR FUN MESSAGES      ##########################
#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#


# sends help message
def send_help(message):
	# loading help message
	f=open('files/info.db','r')
	helpmsg=f.read().split('VK@@##@@TL')[1].strip()
	f.close()

	# sending description
	tl.sendmsg(url, message[1], helpmsg)





# sends citation
def send_citation(message):
	if get_tl_user(message[1]):
		# loading and choosing citation
		f=open('files/citations.db','r')
		tosend = randchoice(f.read().split('\n\n'))
		f.close()

		# sending citation
		tl.sendmsg(url, message[1], tosend)



#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#








##########################        THIS IS ODMIN FUNCTIONS       ##############################
#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#



# [Odmin function] sends N messages bot received from TL
def send_tl_log(message):
	global odmins
	if message[1] not in odmins:
		return
	# loading TL messages list
	f=open("files/tl_msgs.db","r")
	messages=f.read().strip(' ;').strip("@ ").replace(' :: ',' : ').split(';\n@')
	f.close()
	newmsg=[]

	# making them more readable and deleting their [messages`] IDs
	for y in messages:
		newmsg.append(' : '.join(y.split(' : ')[1:]).strip(' ;'))

	# checking if Odmin typed correct value
	try:
		tosend='\n'.join(newmsg[-int(message[2][7:]):])
	except Exception as e:
		tosend='You typed incorrect value. Maybe you requested more messages I have, or you typed non integer number.'

	# sending messages
	tl.sendmsg(url, message[1], tosend)





def send_tl_users(message):
	global odmins
	if message[1] not in odmins:
		return

	user_text=[]
	for x in users:
		user_text.append(' : '.join(x))

	tl.sendmsg(url, message[1], '\n'.join(user_text))



#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#








###############        THIS IS TRASPORTER OF MESSAGES FROM VK TO TELEGRAM      ###############
#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#



# sends messages from vk to Telegram
def fromvktotl(vk_msgs, sent_msgs, new_to_tl):
	global url
	global users

	if not new_to_tl.value:
		return
	new_to_tl.value = 0

	seq = vk_msgs.read()


	allmsg=''.join(re.findall(r'all:{(.*?)}',seq)).split()
	imnt=''.join(re.findall(r'important:{(.*?)}',seq)).split()
	# getting dictionary of messages,it looks like message_ID: message_Data
	msgdict=makedict()

	toall=[]
	toimnt=[]

	# making message what to send to users with mode 'all'
	for x in allmsg:
		if x in msgdict.keys():
			toall.append(msgdict[x])
	toall='\n'.join(toall)

	# making message what to send to users with mode 'imnt'
	for x in imnt:
		if x in msgdict.keys():
			toimnt.append(msgdict[x])
	toimnt='\n'.join(toimnt)

	# if toall is not empty then send messages to all users
	if toall:
		# cycling through user`s table
		for x in users:
			# loading user`s mode and ID
			usermode, userid=x[2], x[0]

			# doesn`t send if user`s mode is 'no'
			if usermode=='no':
				continue
			# sends important messages to user with 'imnt' mode
			elif toimnt and usermode=='imnt':
				tl.sendmsg(url, userid, toimnt)
			# sends all messages to user with 'all' mode
			elif usermode=='all':
				tl.sendmsg(url, userid, toall)

	# marking messages as sent
	sent_msgs.write('a', ' '+' '.join(allmsg))

	vk_msgs.write('w', "important:{}\n\nall:{}")
	new_to_tl.value = 0




#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#









#############################        MAIN         #################################################
#*************************************************************************************************#
#*************************************************************************************************#
#*************************************************************************************************#
#*************************************************************************************************#
def tlmain(urltl, vk_msgs, tl_msgs, msghistory, sent_msgs, new_to_tl, new_to_vk):
	global url
	url=urltl

	update_users_table()
	update_odmins_list()

	offset=0
	cycle=0
	while True:
		#print('TL_CYCLE {}'.format(str(datetime.now())))
		if cycle%3==0:
			print(',',end='')
			stdout.flush()
		if cycle>=1000:
			print('\n{0}:  1000 TL cycles!;    tllast = {1};'.format(str(datetime.now()), offset))
			cycle=0
			tl.cleanup()

		try:
			# getting new last message and list of messages
			offset, messaglist = tl.getmsg(url, offset)

			# if id of last message received equals to id before you updated then do nothing with messages
			for x in messaglist:
				if x[2][1:5]=='auth':
					auth_user(x)
					update_users_table()
				elif x[2][1:7]=='chname':
					change_users_name(x)
				elif x[2][1:5]=='mode':
					change_users_mode(x)
				elif x[2][1:3]=='me':
					send_users_info(x)
				elif x[2][1:4]=='msg' or x[2][1:4]=='смс':
					msg_send_to_vk(x, tl_msgs, new_to_vk)
				elif x[2][1:4]=='log':
					send_vk_log(x, msghistory)
				elif x[2][1:5]=='help':
					send_help(x)
				elif x[2][1:6]=='quote':
					send_citation(x)
				elif x[2][1:6]=='tllog':
					send_tl_log(x)
				elif x[2][1:8]=='tlusers':
					send_tl_users(x)

			# send messages from VK to Telegram
			fromvktotl(vk_msgs, sent_msgs, new_to_tl)
			cycle+=1
		except Exception as e:
			exception(e)

#*************************************************************************************************#
#*************************************************************************************************#
#*************************************************************************************************#
#*************************************************************************************************#






if __name__ == '__main__':
	psswd=gethash(getpass(),mode='pass')
	url=tl.geturl(psswd)
	main(url)
