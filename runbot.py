#!/usr/bin/python3

#runs all modules in correct way
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

import vk_run
import vk_api
import telegrambot
import re
from fcrypto import gethash,fdecrypt
from getpass import getpass
from tlapi import geturl,getcaptcha
from logging import exception, basicConfig, WARNING
from datetime import datetime
from multiprocessing import Process, Value, Manager
from time import sleep as tsleep
import multiio as io
from sys import argv

#import curses

#configuring logs
basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s',
level = WARNING, filename = 'logs/logs.log')





# handling captcha via Telegram. See vk_api docs for detailed info
def captcha_handler(captcha):
	global lastid
	key = getcaptcha(url,captcha.get_url().strip(),lastid).strip(';').strip()
	return captcha.try_again(key)




# cleans up files/msgs.sent
#def clearsent(sent_msgs):
#	sent = sent_msgs.read().split()
#	sent_msgs.write('w', ' '.join(sent))






def main():
	# getting password
	psswd=gethash(getpass(),mode='pass')

	# decrypting and loading settings
	settings=fdecrypt("files/vk.settings",psswd)
	#print(settings)
	login="".join(re.findall(r"login=(.+)#endlogin",settings))
	password="".join(re.findall(r"password=(.+)#endpass",settings))
	chatid=int("".join(re.findall(r"chatid=(\d+)#endchatid",settings)))
	albumid=int("".join(re.findall(r"album_id=(\d+)#endalbumid",settings)))
	userid=int("".join(re.findall(r"userid=(\d+)#enduserid",settings)))

	state_auth = False
	# getting session
	while not state_auth:
		try:
			vk_session = vk_api.VkApi(login, password,captcha_handler=captcha_handler)
			vk_session.authorization()
			vk = vk_session.get_api()
			state_auth = True
		except:
			state_auth = False
			tsleep(30)
			exception('smth goes wrong at geting api\n')



	# getting url
	url=geturl(psswd)

	# Lists of messages
	msg_man = Manager()
	list_of_cmds, list_of_alles, list_of_imnts, tl_msgs = msg_man.list(), msg_man.list(), msg_man.list(), msg_man.list()

	# accounting the speed
	iterations_vk = Value('i', 0)
	iterations_tl = Value('i', 0)

	# file`s safe work
	msgshistory = io.SharedFile('files/msgshistory.db')

	# stats Manager
	stat_man = Manager()
	curr_stat = stat_man.dict()
	curr_stat['temp'] = 0
	curr_stat['iter_tl'] = 0
	curr_stat['iter_vk'] = 0
	curr_stat['PID_VK'] = 0
	curr_stat['PID_TL'] = 0


	# starting bot
	print('Logged in, starting bot...')

	vk_process = Process(target=vk_run.run_vk_bot, args=(vk, chatid, albumid, userid, msgshistory, tl_msgs, list_of_alles, list_of_imnts, list_of_cmds, iterations_vk, curr_stat))
	tl_process = Process(target=telegrambot.tlmain, args=(url,tl_msgs, msgshistory, list_of_alles, list_of_imnts, iterations_tl, curr_stat))

	print('Starting VK bot...')
	vk_process.start()

	print('Starting TL bot...')
	tl_process.start()

	# checking if admin gave argument "--screen"
	if len(argv)>1 and argv[1]=='--screen':
		import curses
		stdscr = curses.initscr()
		curses.noecho()
		stdscr.keypad(True)

	# crutch
	iterations_tl.value = 1
	iterations_vk.value = 1

	while True:
		out_string = '''Temp: {0} C; \nSpeed_TL: {1}; \nSpeed_VK: {2};'''
		tempfile=open('/sys/class/thermal/thermal_zone0/temp', 'r')
		#print('Temp: ' + str(float(tempfile.read().strip())/1000) + ' C ', end='')
		ctemp = str(float(tempfile.read().strip())/1000)
		tempfile.close()

		curr_stat['temp'] = ctemp
		curr_stat['iter_tl'] = iterations_tl.value
		curr_stat['iter_vk'] = iterations_vk.value

		if len(argv)>1 and argv[1]=='--screen':
			stdscr.clear()
			stdscr.addstr(out_string.format(ctemp, iterations_tl.value, iterations_vk.value))
			stdscr.refresh()

		# checking if process is alive. If not, restarting process
		if iterations_tl.value == 0:
			tl_process.terminate()
			tl_process = Process(target=telegrambot.tlmain, args=(url,tl_msgs, msgshistory, list_of_alles, list_of_imnts, iterations_tl, curr_stat))
			print('Restarting TL bot...')
			tl_process.start()
			#iterations_tl.value = 1

		if iterations_vk.value == 0:
			vk_process.terminate()
			vk_process = Process(target=vk_run.run_vk_bot, args=(vk, chatid, albumid, userid, msgshistory, tl_msgs, list_of_alles, list_of_imnts, list_of_cmds, iterations_vk, curr_stat))
			print('Restarting VK bot...')
			vk_process.start()
			#iterations_vk.value = 1

		#stdout.flush()
		iterations_tl.value = 0
		iterations_vk.value = 0
		tsleep(60)


	tl_process.join()
	vk_process.join()

	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()
	print('Exit...')





if __name__ == '__main__':
	main()
