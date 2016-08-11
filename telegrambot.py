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
import makeseq as vkmkseq


#https://api.telegram.org/bot<token>/METHOD_NAME

url=''
users=[]
odmins=[]
#maden=[]

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

# authes user.
def auth_user(message):
	global url
	global users

	# loading user`s Black_List
	#f=open('files/shitlist.db','r')
	#shitlist=f.read().strip().split()
	#f.close()

	# allows users (except users in Black_List) to log in via 64 byte token (really it lenght is 32 byte,
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

		# loading how many tries people have been maden
		#q=open('files/tl_tryes.db','r')
		#tryusers=q.read()
		#q.close()

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

		# if it first wrong try add new user to the list, else increment number of tries
#		if '@'+message[1]+':' not in tryusers:
#			tryusers+=' @'+message[1]+':1'
#		else:
#			# loading list
#			ntryus=tryusers.split()
#			#cycling through users table
#			for y in ntryus:
#				curtry=y.strip().split(':')
#				# if users match increment it
#				if '@'+message[1]+':' in y:
#					tryusers=tryusers.replace(y,
#					curtry[0]+':'+str(int(curtry[1])+1))
#					if int(curtry[1])>2:
#						tl.kickuser(message[1])
#						tryusers=tryusers.replace(y,'')
#					break
#		# writing new users table
#		q=open('files/tl_tryes.db','w')
#		q.write(tryusers)
#	q.close()

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
	#print(curruser, line)
	if not curruser:
		return
	tl.sendmsg(url, curruser[0] ,"You are logged in as "+curruser[1]+
	' with recieving '+curruser[2]+' messages.')



#writes text and message_id(will be deleted as it sent) that will be sent to vk.
def msg_send_to_vk(message):
	global url

	curruser, line = get_tl_user(message[1])

	if not curruser:
		return

	# writing sequence of messages in append mode in case if Something went wrong in VK module
	g=open('files/tl_msgs.seq','a')
	g.write('Not_sent_message: '+curruser[1]+': ' +
	message[2][5:]+' ;\n')
	g.close()

	# sending info message
	tl.sendmsg(url, curruser[0], "The message will be sent soon.")
	for qw in users:
		if not qw[0] == curruser[0]:
			tl.sendmsg(url, qw[0], 'From TL`s ' + curruser[1] + ': ' + message[2][5:])


# sends last N messages from VK
def send_vk_log(message):
	global users

	if get_tl_user(message[1])[0]:
		# loading list of VK messages
		f=open("files/msgshistory.db","r")
		vk_messages=f.read().strip(' ;').strip("@ ").replace(' :: ',' : ').split(';\n@')
		f.close()

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

		# marking message as proccessed
		f=open('files/tl_msgs.made','a')
		f.write(' '+message[0])
		f.close()



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


#checks for /log or /help or /quote and responses to user
#def response():
#    global url
#
#    # loading list of proccessed messages
#    f=open('files/tl_msgs.made','r')
#    maden=f.read()
#    f.close()
#
#    # loading last messages
#    f=open('files/tl_msgs.db','r')
#    msgs=f.read().strip('@ ').strip(' ;').split(' ;\n@ ')[-50:]
#    f.close()
#
#    # loading users table
#    f=open('files/tl_users.db','r')
#    users=f.read()
#    f.close()
#    # loading list of Odmins
#    f=open('files/admins.db','r')
#    odmins=f.read().strip().split()
#    f.close()



# sends messages from vk to Telegram
def fromvktotl():
	global url
	global users
	# loading sequence of what to send. This sequence is generated in makeseq.py module
	f=open('files/msgs.seq','r')
	seq=f.read()
	f.close()

	if not seq:
		return

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
	f=open('files/msgs.sent','a')
	f.write(' '+' '.join(allmsg))
	f.close()

	# updating sequance. This is crutch because of optimization.
	if toall:
		vkmkseq.main()


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



#**************************************************************************************************
#**************************************************************************************************
#**************************************************************************************************
#**************************************************************************************************
def main(urltl,lastid=0):
	global url
	#global users
	#global maden
	# writing url from argument to global variable 'url'
	url=urltl

	update_users_table()
	update_odmins_list()

	# getting new last message and list of messages
	offset, messaglist = tl.getmsg(url, lastid)

	# if id of last message received equals to id before you updated then do nothing with messages
	if not offset==lastid:
		for x in messaglist:
			# adds new user if token is correct
			if x[2][:5]=='/auth':
				auth_user(x)
				update_users_table()

			# changes user`s NickName if there is command /chname
			elif x[2][:7]=='/chname':
				change_users_name(x)
				#update_users_table()

			# changes user`s mode of recieving messages
			elif x[2][:5]=='/mode':
				change_users_mode(x)
				#update_users_table()

			# sends info about user
			elif x[2][:3]=='/me':
				send_users_info(x)

			# send to vk
			elif x[2][:4]=='/msg':
				msg_send_to_vk(x)

			# sending last N messages from VK
			elif x[2][:4]=='/log':
				send_vk_log(x)

			# sending help message
			elif x[2][:5]=='/help':
				send_help(x)

			elif x[2][:6]=='/quote':
				send_citation(x)

			elif x[2][:6]=='/tllog':
				send_tl_log(x)

			elif x[2][:8]=='/tlusers':
				send_tl_users(x)
			#updateusers()
			#makeseq()
			#response()
			tl.cleanup()
	# send messages from VK to Telegram
	fromvktotl()

	#returning ID of last messages
	return offset



if __name__ == '__main__':
	psswd=gethash(getpass(),mode='pass')
	url=tl.geturl(psswd)
	main(psswd,url)
