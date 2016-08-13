#!/usr/bin/python3

#sorts and makes sequance
#also cleans up msgshistory.db
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

from re import findall
import multiio as io





def main(msghistory, vk_msgs, sent_msgs):
	listofmsgs=msghistory.read().split(' ;\n@ ')[-200:]

	f=open('files/keywords.db','r')
	keywords=f.read().split()
	f.close()

	impnt=[]
	allmsg=[]

	# making it more readable
	for x in range(len(listofmsgs)):
		listofmsgs[x]=listofmsgs[x].strip('@ ').strip(' ;')

	# loading sent messages
	sent = sent_msgs.read().split()

	# cycling through messages
	for x in listofmsgs:
		msg=x.split(' :: ')
		mess=True
		if len(msg)<4: # some messages maybe empty. it is normal.
			continue
		# not to send message if message consists commands
		for y in ['/quote','/music','/gif','/info','/pic']:
			if y in msg[3]:
				mess=False
				break
		if not mess: continue

		# making all and imnt sequances
		if msg[0].strip() not in sent:
			allmsg.append(msg[0].strip())
			# cycling through keywords
			for y in keywords:
				if y in msg[3].lower() or (msg[3]==msg[3].upper() and len(findall(r'[A-Za-zА-Яа-я]?',msg[3]))>=3):
					impnt.append(msg[0].strip())
					break
	# writing sequances
	vk_msgs.write('w', "important:{"+" ".join(impnt)+"}\n\n" +"all:{"+" ".join(allmsg)+"}")
	# cleaning up messages
	if len(listofmsgs)>1000:
		msghistory.write('w', '@ '+' ;\n@ '.join(listofmsgs[-100:]))





if __name__ == '__main__':
	main()
