#!/usr/bin/python3
# -*- coding: utf-8 -*-
from time import sleep as tsleep
#import inspect
# multi IN_OUT module.

def write_shared_file(filename, mode, data, state):
	#print("Write {}".format(inspect.stack()[1][3]))
	wait_freedom_and_lock(state)

	f=open(filename, mode)
	f.write(data)
	f.close
	unlock(state)


def read_shared_file(filename, state):
	#print("Read {}".format(inspect.stack()[1][3]))
	wait_freedom_and_lock(state)

	f=open(filename, 'r')
	data=f.read()
	f.close
	unlock(state)
	return data


def wait_freedom_and_lock(state):
	#print("Lock {}".format(inspect.stack()[1][3]))
	while state.value:
		tsleep(0.0001)
	state.value=1

def unlock(state):
	#print("Unlock {}".format(inspect.stack()[1][3]))
	state.value=0
	tsleep(0.001)
