# agent_smith
Retranslator of choosen chat in VK to Telegram with some extra features written in Python3

Some information about commands you can find in files/info.db and telegrambot.py  or after you started you can type /help into Telegram or /info into VK chat. 

How to setup and configure bot:
1. You need to install dependencies. Just run as root $ [sudo] ./install_libs.sh . It installs twofish and vk_api via pip.

2. Run $ python3 fcrypto.py -setup to setup bot. It will ask you for password to encrypt settings files, chat ID of needed chat in VK, login and password from VK, album`s and your VK account`s ID. Also it requaries your bot`s token(it is given to you as you registered your bot in Telegram). https://core.telegram.org/bots/api. Album ID is album from where Smith will send photos to VK by typing /photo. After entering all needed fields files/vk.settings and files/telegram.token will be encrypted with the password.

3. Fill your VK account with gifs,audios and photos. It will be sent to VK chat after typing /gis or /audio or /pic in that chat.

4. Now you can generate keys to give access to bot in Telegram to others. Just run $ python3 fcrypto -addkeys . It will generate public and private keys. Public key is stored in files/tokens.db. Private one will be shown in the your terminal. You should send that private keys to people you want to share access to bot in Telegram. One key for one person. After person types in Telegram /auth [private_key] the sha512 of this key will be computed and checked. For details how it is computed see fcrypto.py at genhash() and gethash() functions.

5. Now you can run bot via $ python3 runbot.py . It will ask you for the password to decrypt the settings files (it is password you entered in the beginning of the 2nd point of this guide).

Main features, issues, and description of files and modules:

Features:

	1. Sending messages from VK chat to Telegram and from Telegram to VK;

	2. Sending gifs, music, photos from choosen album VK to VK chat;

	3. Three modes of receiving messages from VK: all, imnt [important] and no;

	4. Info,help and citation to VK and Telegram;

	5. Logging in by 64 symbol key;

	6. Changing name that others see in VK when you send message from Telegram;

	7. Default name when you logged in is Anonymous[some numbers], we recomend to change it;


Issues:

	Real:

		1. double semicolumn in transfered messages;

	Possible:

		1. [NOT CHECKED] Successful sslstrip attack if you allow http in VK;

		2. [NOT CHECKED] sslsplit attacks;

Description about files and modules:

	fcrypto.py - set of functions, that allows to easy encrypt,decrypt files and generate keys;

	getmsg.py - gets messages from VK and writes it to the file, writes to files/msgshistory.db;

	runbot.py - runs all modules in correct way;

	updatemedia.py - updates available media to send to VK, writes to files/media.db; 

	makeseq.py - makes sequence of what messages will be sent to Telegram in two branches: all and imnt , writes to files/msgs.seq;

	sendtovk.py - send needed content to VK, writes processed messages to files/msgs.sent;

	telegrambot.py - bot in Telegram, works with many files;

	tlapi.py - some often used functions for Telegram API;

	files/:
		
		admins.db - list of admins in Telegram bot;

		citations.db - list of citations to send to VK;

		info.db - information to send to VK;

		keywords.db - list of keywords of important messages. It is one of two ways to mark message as important: use one of the words in the list or write like this: THIS IS IMPORTANT MESSAGE;

		media.db - list of available audios, gifs and photos. One random audio, gif or photo will be sent to VK by special comands from this list;

		msgs.made - list of processed messages in VK;

		msgs.sent - list of sent messages in VK;

		msgs.seq - list of messages to send to VK;

		msgshistory.db - list of received messages from VK;

		shitlist.db - list of blocked users in VK;

		telegram.token - [ENCRYPTED] token of your Telegram bot;

		tl_msgs.db - list of messages received from Telegram;

		tl_msgs.made - list of processed messages received from Telegram;

		tl_msgs.seq - list of messages to send from Telegram to VK;

		tl_tryes.db - this file is used to count how many tryes users have made by logging in;

		tl_users.db - list of connected users in Telegram;

		tokens.db - list of public keys (they are hashes from private keys);

		vk_users.db - list of VK users in VK chat(only who made any action in chat e.g. send a message or leave group for example);

		vk.settings - [ENCRYPTED] settings of your VK bot;


	
	logs/:

		getmsg.log - log file for getmsg.py module, is not used in server mode;

		logs.log -log file for runbot.py module, used in server mode;

		sendtovk.log - log file for sendtovk.py modile, is not used in server mode;

		updatemedia.log - log file for updatemedia.py module, is not used in server mode;


	vk_api/ - foreign library with Apache license for easy using VK API;

	jconfig/ - library that is used by vk_api;
