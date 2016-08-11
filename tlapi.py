#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this is API for bot in Telegram
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

from requests  import get as urlget
from datetime import datetime
from fcrypto import fdecrypt
from logging import exception,basicConfig,WARNING
from urllib.parse import quote, urlsplit, urlunsplit


# returns a list of stripped values
def strip_list(somelist):
	newlist=[]
	for x in somelist:
		if str(type(x))=="<class 'str'>":
			newlist.append(x.strip())
		else:
			newlist.append(x)
	return newlist


#url of api Telegram. Takes password,that is used in encrypting settings. Without password you cannot do anything
def geturl(password):
	url=('https://api.telegram.org/bot'+
	fdecrypt('files/telegram.token',password).split()[0].replace('token=','').replace(';','')+'/')
	return url


#sends a message to Telegram.
'''
url can be received via geturl();
chatid is chat_id of where to send
text is text you want to send. Must be less than 4096 bytes.
See https://core.telegram.org/bots/api for more information about parametres
'''
def sendmsg(url,chatid,text):
	ntext=quote(text.encode('utf-8'))

	try:
		requ=urlget(url+'sendMessage?chat_id='+str(chatid)+'&text='+ntext).json()
	except Exception as msg_error:
		print(' sendMessage have gone wrong; ')
		exception(msg_error)
		return 'error'

	# sometimes it is useful, not in my case
	return str(requ)



#gets and logs to file new messages
'''
url can be received from geturl();
offset is number of message that must be received first
See https://core.telegram.org/bots/api for more information about parametres
'''
def getmsg(url,offset=0):
	try:
		# getting updates via requests.get()
		requ=urlget(url+'getUpdates'+'?offset='+str(offset)).json()

		# loading list of messages
		f=open('files/tl_msgs.db','r')
		msglist=f.read()
		f.close()

		# opening file in append mode
		f=open('files/tl_msgs.db','a')
		# logging to file and to the list
		messaglist=[]
		for x in requ['result']:
			#checking if it allowed command
			# it is rather difficult to read. It checks if message is not in file already, if command is allowed
			# and some security checks
			if (('@ msg_id='+str(x['message']['message_id']) not in msglist and
			(x['message']['text'][0:4]=='/msg' or x['message']['text'][0:6]=='/quote'
			or x['message']['text'][0:5]=='/mode' or x['message']['text'][0:7]=='/chname'
			or x['message']['text'][0:5]=='/help' or x['message']['text'][0:5]=='/auth'
			or x['message']['text'][0:4]=='/log' or x['message']['text'][0:3]=='/me'
			or x['message']['text'][0:6]=='/tllog' or x['message']['text'][0:8]=='/captcha'
			or x['message']['text'][0:8]=='/tlusers'))
			and ';\n@' not in x['message']['text']):

				#writing this message
				f.write('@ msg_id='+str(x['message']['message_id'])+' :: '+
				str(x['message']['from']['id'])+' :: '+
				datetime.fromtimestamp(x['message']['date']).strftime('%Y-%m-%d %H:%M:%S')+' :: '+
				x['message']['text']+' ;\n')

				# appending list
				messaglist.append(strip_list([str(x['message']['message_id']), str(x['message']['from']['id']), x['message']['text'].strip()]))

		f.close()
	except Exception as e:
		exception(' A error occured while getting updates in Telegram:\n')
		return 0, []

	# if you do not send anything to bot for 24 hours, requ['result'] will be empty.
	if len(requ['result']):
		return requ['result'][-1]['update_id'], messaglist
	else:
		return 0, []


# writes user to Black_List. I think it is understoodable without my commentary
def kickuser(userid):
	f=open('files/shitlist.db','a')
	f.write(' '+str(userid))
	f.close()



#cleans up logs to make them small
def cleanup():
	#loading list of messages
	f=open('files/tl_msgs.db','r')
	listofmsgs=f.read().split(' ;\n@ ')
	f.close()
	# writing last 100 messages if there are more than 1000 messages
	if len(listofmsgs)>1000:
		f=open('files/tl_msgs.db','w')
		f.write('@ '+' ;\n@ '.join(listofmsgs[-100:]))
		f.close()

	# loading list of maden messages
	f=open('files/tl_msgs.made','r')
	listofmsgs=f.read().split()
	f.close()
	# writing last 100 maden messages if there are more than 1000 maden messages
	if len(listofmsgs)>1000:
		f=open('files/tl_msgs.made','w')
		f.write(' '.join(listofmsgs[-100:]))
		f.close()




#sending url with captcha and waiting for response from God-Odmin *There must be picture with holy Linus or Richard Stallman*
'''
url can be received via geturl()
captcha is url to captcha
offset is last update_id
See https://core.telegram.org/bots/api for more information about parametres
'''
def getcaptcha(url,captcha,offset=0):
	# loading list of Admins
	f=open('files/admins.db','r')
	odmins=f.read().strip().split() # Odmins is joke about Admin
	f.close()

	# loading meden messages
	f=open('files/tl_msgs.made','r')
	maden=f.read()
	f.close()

	# sending captha to all Odmins. Telegram will paste a picture of the captcha so Odmins will see it in TL
	for x in odmins:
		sendmsg(url,x,'Captcha is needed: '+str(captcha))

	# waiting for response from Odmins
	while True:
		# updating messages
		lastid=getmsg(url,offset)

		# loading list of messages
		f=open('files/tl_msgs.db','r')
		listofmsgs=f.read().split(' ;\n@ ')
		f.close()

		# cycling through last 10 messages. If there will be an DDoS on your bot, Odmin cannot type a captcha
		# But getUpdates is rather fast method, so it is rather hard to DDoS bot if you have small auditory of enemies
		for y in listofmsgs[-10:]:
			currmsg=y.split(' :: ')
			if currmsg[1] in odmins and currmsg[0] not in maden and currmsg[3][:8]=='/captcha':
				# writing maden messages
				f=open('files/tl_msgs.made','a')
				f.write(' '+currmsg[0])
				f.close()
				# returning text of captcha
				return currmsg[3][8:].strip()
