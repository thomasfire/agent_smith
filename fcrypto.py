#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this is lib for easy using Twofish encryption
""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

from twofish import Twofish
from hashlib import sha512,sha256
from codecs import decode
from sys import argv
from getpass import getpass
from os import urandom

#returns secure hash
'''
smstr is string you wanna to take hash
mode can be "token" if you want to take publickey from privatekey
    or it can be "pass" if you want to take password from string
'''
def gethash(smstr, mode='token'):
    # getting salt. You should change it if you want to avoid finding your hashes in Internet
    salt=sha512(b'fghjfjkjlktycvq/.,ASS ON KEYBOARD t567 tx546e!@$^*#)%&/*-+-thgklh;xmnvhgjfty'+
    smstr.encode('ascii')).hexdigest()
    nhash=sha256(salt.encode('ascii')+smstr.encode('ascii')).hexdigest()

    # in pass mode hash is computed about 2^18 times. It is defense from bruteforcing
    if mode=='pass':
        for x in range(2**18):
            nhash=sha256(salt.encode('ascii')+nhash.encode('ascii')).hexdigest()
        return sha256(salt.encode('ascii')+nhash.encode('ascii')).digest()

    # in token mode hash is computed about 1024 times, so you can be sure that there will be
    # no one who can recreate privatekey from publickey
    elif mode=='token':
        for x in range(2**10):
            nhash=sha512(salt.encode('ascii')+nhash.encode('ascii')).hexdigest()
        return sha512(salt.encode('ascii')+nhash.encode('ascii')).hexdigest()

#encrypts file via password
def fencrypt(filen,password):
    f=open(filen,'r')
    smstr=f.read()
    f.close()
    # splitting it to blocks with 16-bytes len
    if len(smstr)%16:
        nstr=str(smstr+'%'*(16-len(smstr)%16)).encode('utf-8')
    else:
        nstr=smstr.encode('utf-8')

    psswd=Twofish(password)
    encredstr=b'' # ENCRyptED STRing

    # encrypting blocks
    for x in range(int(len(nstr)/16)):
        encredstr+=psswd.encrypt(nstr[x*16:(x+1)*16])

    # writing it to file
    f=open(filen,'wb')
    f.write(encredstr)
    f.close()

#decrypts file via password,returns decrypted text
def fdecrypt(filen,password):
    # reading file in byte mode
    f=open(filen,'rb')
    smstr=f.read()
    f.close()

    psswd=Twofish(password)
    decredstr=b'' # decrypted string

    # decrypting it and joining
    for x in range(int(len(smstr)/16)):
        decredstr+=psswd.decrypt(smstr[x*16:(x+1)*16])

    return decode(decredstr,'utf-8').strip('%')

#generates private and public hashes to auth from string
def genhash(smstr):
    # randomizing string because most people do not like to write secure phrases
    nstring=str(urandom(16))+smstr+str(urandom(16))

    # getting salt
    salt=sha512(b'fghjfjkjlktycvq/.,ASS ON KEYBOARD t567 tx546e!@$^*#)%&/*-+-thgklh;thicxxbmnvhgjfty'+
    smstr.encode('ascii')).hexdigest()

    # getting secure hash
    nhash=sha256(salt.encode('ascii')+nstring.encode('ascii')).hexdigest()
    for x in range(2**10):
        nhash=sha256(salt.encode('ascii')+nhash.encode('ascii')).hexdigest()

    # getting privatekey from hash
    privatekey=sha256(salt.encode('ascii')+nhash.encode('ascii')).hexdigest()
    # getting publickey from privatekey
    publickey=gethash(privatekey)

    return privatekey,publickey

def main():
    if len(argv)>1 and argv[1]=='-setup': # running setup if argument is -setup
        vari=False
        while not vari: # checking if it is needed password
            inone=getpass('Password to encrypt files: ')
            intwo=getpass('Re-enter : ')
            if inone==intwo:
                password=gethash(inone,mode='pass')
                vari=True
            else:
                print('Wrong validation,retry\n')

        # running asking data
        # VK:
        f=open('files/vk.settings','w')
        f.write('chatid={0}#endchatid\n'.format(input('Enter chat id: ')))
        f.write('login={0}#endlogin\n'.format(input('Enter login: ')))
        f.write('password={0}#endpass\n'.format(getpass('Enter password: ')))
        f.write('album_id={0}#endalbumid\n'.format(input('Enter album id: ')))
        f.write('userid={0}#enduserid\n'.format(input('Enter user id: ')))
        f.write('ACHTUNG!THIS IS UNENCRYPTED TEXT!')
        f.close()
        fencrypt('files/vk.settings',password)

        # TL:
        f=open('files/telegram.token','w')
        f.write('token={0};'.format(input('Enter token of your TelegramBot: ')))
        f.write('\nACHTUNG!THIS IS UNENCRYPTED TEXT!')
        f.close()
        fencrypt('files/telegram.token',password)
        print('Now you can add keys to send to your users via $ python3 fcrypto.py -addkeys')

    elif len(argv)>1 and argv[1]=='-addkeys': # adding key to list
        # getting keys from string you typed
        privatekey,publickey=genhash(input('Enter any ascii string: '))

        # writing it to file. "He does not use encryption!" - you might say. But hashes are pretty unforcable
        f=open('files/tokens.db','a')
        f.write(publickey+'\n')
        f.close()

        # printing privatekey. You must copy it and give it to user you want to share access to bot.
        print('Private key: '+privatekey)
    # getting publickey if you have only privatekey. This is for emergency cases such as lost of files/tokens.db
    elif len(argv)>1 and argv[1]=='-hash':
        print(gethash(input('Enter any ascii string: '),mode='token'))

    else:
        print('Usage: python3 fcrypto.py [-addkeys , -setup]')



if __name__ == '__main__':
    main()
