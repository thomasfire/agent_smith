#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

from time import sleep as tsleep
from multiprocessing import Event

# multi IN_OUT module.



"""Class, that safely works with files, that are used in many processes.
 Takes filename and link to multiprocessing.Value.
 Creates new event."""
class SharedFile(object):

	def __init__(self, filename):
		self.filename = filename
		self.fevent = Event()

		self.fevent.set()


	def write(self, mode, data):
		self.wait_freedom_and_lock()

		f=open(self.filename, mode)
		f.write(data)
		f.close
		self.unlock()



	def read(self):
		self.wait_freedom_and_lock()

		f=open(self.filename, 'r')
		data=f.read()
		f.close
		self.unlock()
		return data


	def wait_freedom_and_lock(self):
		self.fevent.wait()
		self.fevent.clear()


	def unlock(self):
		self.fevent.set()
		tsleep(0.001)
