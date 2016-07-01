# agent_smith
Retranslator of choosen chat in VK to Telegram with some extra features written in Python3

Some information about commands you can find in files/info.db and telegrambot.py  or after you started you can type /help into Telegram or /info into VK chat. 

How to setup and configure bot:
1. You need to install twofish lib. We included its installer into agent_smith as twofish-0.3.0.tar.gz. But you can download latest version at https://pypi.python.org/pypi/twofish. There are installation guides in both archives. 

2. Run $ python3 fcrypto.py -setup to setup bot. It will ask you for password to encrypt settings files, chat ID of needed chat in VK, login and password from VK, album`s and your VK account`s ID. Also it requaries your bot`s token(it is given to you as you registered your bot in Telegram). https://core.telegram.org/bots/api. Album ID is album from where Smith will send photos to VK by typing /photo. After entering all needed fields files/vk.settings and files/telegram.token will be encrypted with the password.

3. Fill your VK account with gifs,audios and photos. It will be sent to VK chat after typing /gis or /audio or /pic in that chat.

4. Now you can generate keys to give access to bot in Telegram to others. Just run $ python3 fcrypto -addkeys . It will generate public and private keys. Public key is stored in files/tokens.db. Private one will be shown in the your terminal. You should send that private keys to people you want to share access to bot in Telegram. One key for one person. After person types in Telegram /auth <private_key> the sha512 of this key will be computed and checked. For details how it is computed see fcrypto.py at genhash() and gethash() functions.

5. Now you can run bot via $ python3 runbot.py . It will ask you for the password to decrypt the settings files (it is password you entered in the beginning of the 2nd point of this guide).

Main features, issues, and description of files and modules:

