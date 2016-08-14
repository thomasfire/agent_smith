#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Developer and Author: Thomas Fire https://github.com/thomasfire (Telegram: @Thomas_Fire)
### Main manager: Uliy Bee
"""

from time import sleep as tsleep
from multiprocessing import Event, Value
#import inspect
# multi IN_OUT module.



"""Class, that safely works with files, that are used in many processes.
 Takes filename and link to multiprocessing.Value.
 Creates new event."""
class SharedFile(object):

	def __init__(self, filename):
		self.filename = filename
		self.fevent = Event()
		#self.state = Value('i', 0)
		self.fevent.set()


	def write(self, mode, data):
		#print("Write {}".format(inspect.stack()[1][3]))
		self.wait_freedom_and_lock()

		f=open(self.filename, mode)
		f.write(data)
		f.close
		self.unlock()



	def read(self):
		#print("Read {}".format(inspect.stack()[1][3]))
		self.wait_freedom_and_lock()

		f=open(self.filename, 'r')
		data=f.read()
		f.close
		self.unlock()
		return data


	def wait_freedom_and_lock(self):
		#print("Wait {}".format(inspect.stack()[1][3]))
		self.fevent.wait()
		self.fevent.clear()
		#while self.state.value:
		#	tsleep(0.0001)
		#self.state.value = 1


	def unlock(self):
		#print("Unlock {}".format(inspect.stack()[1][3]))
		self.fevent.set()
		#tsleep(0.001)
		#self.state.value = 0
		#tsleep(0.001)
