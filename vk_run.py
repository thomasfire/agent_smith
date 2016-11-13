#!/usr/bin/python3

#runs VK modules in correct way
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""



import vk_api
import getmsg
import updatemedia
import makeseq
import sendtovk
from os import getpid
from logging import exception, basicConfig, WARNING



def get_last_msg():
	f = open('files/msgshistory.db', 'r')
	num = int(f.read().strip('@ ').strip(' ;').split(' ;\n@ ')[-1].split(' :: ')[0])
	print(num)
	f.close()
	return num


def run_vk_bot(vk, chatid, albumid, userid, msgshistory, tl_msgs, list_of_alles, list_of_imnts, list_of_cmds, iterations_vk, curr_stat):
	userdic = getmsg.get_user_dict()
	keywords = makeseq.load_keywords()
	lastid = get_last_msg()
	updatemedia.main(vk, albumid, userid)
	curr_stat['PID_VK'] = str(getpid())
	print('VK is ready to start...PID_VK: {0}'.format(curr_stat['PID_VK']))

	cycles = 0

	while True:
		try:
			# getting messages
			lastid, userdic, messages = getmsg.getmain(vk, chatid, msgshistory, userdic, lastid)

			# update list of available media every 1000th iterarion. It is about every 8-20th minute if you have non-server connection
			if cycles >= 1000:
				#clearsent(sent_msgs)
				updatemedia.main(vk, albumid, userid)
				cycles = 0
				#print('\n',str(datetime.now()),':  Big cycle done!;    vklast=',lastid,';')

			# running retranslation to TL only if there are new messages from VK
			for x in messages:
				makeseq.mkmain(x, keywords, list_of_alles, list_of_imnts, list_of_cmds)

			# processing commands and retranslation_from_TL in VK
			sendtovk.stvmain(vk, chatid, list_of_cmds, tl_msgs)

			cycles += 1
			iterations_vk.value += 1
		except ConnectionResetError: # there are often this type of errors, but it is not my fault
			continue
		except Exception as exp:
			exception("Something gone wrong in vk_bot:\n")
