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
from os import getpid
#https://api.telegram.org/bot<token>/METHOD_NAME

url=''
users={}
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
	for x in users.keys():
		user_text.append(' :: '.join([x, users[x][0], users[x][1]]))

	f=open('files/tl_users.db','w')
	f.write('@ '+' ;\n@ '.join(user_text)+' ;\n')
	f.close()





# returns a line with info about user. also returns it`s index
def get_tl_user(user_id):
	if user_id in users.keys():
		return users[user_id]
	#for x in users.keys:
	#	if x[0]==user_id:
	#		return x, y
	#	y+=1
	return []



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
	users={}
	for x in userstext:
		curruser = strip_list(x.split(' :: '))
		users[curruser[0]] = curruser[1], curruser[2]
	print(users)
		#users.append(strip_list(x.split(' :: ')))






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
#**********************************sorry,_dict***********************************************#
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
		#f=open('files/tl_users.db','a')
		# checking if hash(publickey) is in token`s list and if this user is not logged in
		if publickey in tokens and not get_tl_user(message[1]):
			# writing new user to user table
			users[message[1]] = tl.get_users_name(url, message), 'all'
			#f.write('@ {0} :: {1} :: all ;'.format(message[1], tl.get_users_name(message[1])))
			# sending welcome message with some info about user
			write_users_table()
			tl.sendmsg(url, message[1], "Welcome! You are now successfully authenticated as {0}.\nYou can change your nicname via /chname <new_nick> or you can view a help message via /help.".format(users[message[1]][0]))
			# writing list of publickeys without recently used publickey
			tokens.pop(tokens.index(publickey))
			g=open('files/tokens.db','w')
			g.write('\n'.join(tokens))
			g.close()
		# if computed hash not in the list of available publickeys increase number of tryes of current user
	elif publickey not in tokens and not get_tl_user(message[1])[0]:
		# sending warning message
		tl.sendmsg(url, message[1], 'Wrong key.')
	# sending message if user already logged in or typed absolutely wrong token or user is in Black_List
	else:
		tl.sendmsg(url, message[1], 'You are already logged in. You can change your nick via /chname <new_nick>')

	#f.close() # closing user`s file





def change_users_name(message):
	global url
	global users
	newusers=[]
	#getting new nickname and writing it to log
	curruser = get_tl_user(message[1])
	if not curruser:
		return

	users[message[1]] = message[2][8:], users[message[1]][1]
	tl.sendmsg(url, message[1], "The nickname has been changed")

	write_users_table()




def change_users_mode(message):
	global url

	curruser = get_tl_user(message[1])
	if not curruser or not message[2][6:] in ['all','no','imnt']:
		return

	users[message[1]] = users[message[1]][0], message[2][6:]
	tl.sendmsg(url, message[1], "The mode has been changed")

	write_users_table()





# sends information about user
def send_users_info(message):
	curruser = get_tl_user(message[1])
	if not curruser:
		return
	tl.sendmsg(url, message[1] ,"You are logged in as {0} with recieving {1} messages.".format(curruser[0], curruser[1]))


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
def msg_send_to_vk(message, tl_msgs):
	global url

	curruser = get_tl_user(message[1])

	if not curruser:
		return

	tl_msgs.append('{0}: {1} ;\n'.format(curruser[0], message[2][5:]))

	# sending info message
	tl.sendmsg(url, message[1], "The message will be sent soon.")
	for qw in users.keys():
		if not qw == message[1] and users[qw][1] == 'all':
			tl.sendmsg(url, qw, 'From TL`s {0}: {1};'.format(curruser[0], message[2][5:]))



#writes text and message_id(will be deleted as it sent) that will be sent to vk.
def ach_send_to_vk(message, tl_msgs):
	global url

	curruser = get_tl_user(message[1])

	if not curruser:
		return

	tl_msgs.append('{0}: {1} ;\n'.format(curruser[0], message[2][5:].upper()))

	# sending info message
	tl.sendmsg(url, message[1], "The achtung will be sent soon.")
	for qw in users:
		if not qw == message[1] and not users[qw][1] == 'no':
			tl.sendmsg(url, qw, 'ACHTUNG! From TL`s {0}: {1};'.format(curruser[0], message[2][5:].upper()))






# sends last N messages from VK
def send_vk_log(message, msghistory):
	global users
	global url

	if get_tl_user(message[1]):
		# loading list of VK messages
		vk_messages = msghistory.read().strip(' ;').strip("@ ").replace(' :: ',' : ').split(';\n@')

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
	global url
	# loading help message
	f=open('files/info.db','r')
	helpmsg=f.read().split('VK@@##@@TL')[1].strip()
	f.close()

	# sending description
	tl.sendmsg(url, message[1], helpmsg)





# sends citation
def send_citation(message):
	global url
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
# 		   _    ____  __  __ ___ _   _
# 		  / \  |  _ \|  \/  |_ _| \ | |
# 		 / _ \ | | | | |\/| || ||  \| |
# 		/ ___ \| |_| | |  | || || |\  |
#	   /_/   \_|____/|_|  |_|___|_| \_|



# [Odmin function] sends N messages bot received from TL
def send_tl_log(message):
	global odmins
	global url
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
	global url
	if message[1] not in odmins:
		return

	user_text=[]
	for x in users.keys():
		user_text.append(' : '.join([x, users[x][0], users[x][1]]))

	tl.sendmsg(url, message[1], '\n'.join(user_text))





def send_adm_msg(message, tl_msgs):
	global odmins
	global url

	if message[1] not in odmins:
		return

	curruser = message[1]
	tl_msgs.append('{0} \n'.format(message[2][5:]))

	# sending info message
	tl.sendmsg(url, curruser, "The Admin-message will be sent soon.")
	for qw in users.keys():
		if not qw == curruser:
			tl.sendmsg(url, qw, message[2][5:])





def send_stat(message, curr_stat):
	global odmins
	global url
	if message[1] not in odmins:
		return
	out_string = '''Temp: {0} C; \nSpeed_TL: {1}; \nSpeed_VK: {2}; \nPID_VK: {3}; \nPID_TL: {4}'''

	tl.sendmsg(url, message[1], out_string.format(curr_stat['temp'], curr_stat['iter_tl'], curr_stat['iter_vk'], curr_stat['PID_VK'], curr_stat['PID_TL']))




def send_bug(message):
	global url
	global odmins

	curruser = get_tl_user(message[1])

	if not curruser:
		return

	for x in odmins:
		tl.sendmsg(url, x, 'BUG! {0}'.format(message[2][5:]))

#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#








###############        THIS IS TRASPORTER OF MESSAGES FROM VK TO TELEGRAM      ###############
#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#



# sends messages from vk to Telegram
def fromvktotl(list_of_alles, list_of_imnts):
	global url
	global users

	if not list_of_alles:
		return

	toall = []
	toimnt = []

	while list_of_alles:
		toall.append(' : '.join(list_of_alles.pop(0)[1:]))
	toall=';\n'.join(toall)

	# making message what to send to users with mode 'imnt'
	while list_of_imnts:
		toimnt.append(' : '.join(list_of_imnts.pop(0)[1:]))
	toimnt=';\n'.join(toimnt)

	# cycling through user`s table
	for x in users.keys():
		# loading user`s mode and ID
		usermode, userid = users[x][1], x
		# doesn`t send if user`s mode is 'no'
		if usermode=='no':
			continue
		# sends important messages to user with 'imnt' mode
		elif toimnt and usermode=='imnt':
			tl.sendmsg(url, userid, toimnt)
		# sends all messages to user with 'all' mode
		elif usermode=='all':
			tl.sendmsg(url, userid, toall)





#********************************************************************************************#
#********************************************************************************************#
#********************************************************************************************#









#############################        MAIN         #################################################
#*************************************************************************************************#
#*************************************************************************************************#
#*************************************************************************************************#
#*************************************************************************************************#
def tlmain(urltl, tl_msgs, msghistory, list_of_alles, list_of_imnts, iterations_tl, curr_stat):
	global url
	url=urltl

	update_users_table()
	update_odmins_list()
	curr_stat['PID_TL'] = str(getpid())
	print('PID_TL: {0}'.format(curr_stat['PID_TL']))

	offset=0
	cycle=0
	while True:
		if cycle>=1000:
			#print('\n{0}:  1000 TL cycles!;    tllast = {1};'.format(str(datetime.now()), offset))
			cycle=0
			tl.cleanup()

		try:
			# getting new last message and list of messages
			offset, messaglist = tl.getmsg(url, offset)
			if messaglist:
				print(messaglist)

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
					msg_send_to_vk(x, tl_msgs)
				elif x[2][1:4]=='adm' or x[2][1:5]=='anon':
					send_adm_msg(x, tl_msgs)
				elif x[2][1:4]=='bug' or x[2][1:4]=='баг':
					send_bug(x)
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
				elif x[2][1:5]=='stat':
					send_stat(x, curr_stat)
				elif x[2][1:4]=='imp' or x[2][1:4]=='ach' or x[2][1:4]=='важ':
					ach_send_to_vk(x, tl_msgs)

			# send messages from VK to Telegram
			fromvktotl(list_of_alles, list_of_imnts)
			cycle += 1
			iterations_tl.value += 1
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
