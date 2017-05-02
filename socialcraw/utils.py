# -*- coding: utf-8 -*-

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


class cprint :

	@staticmethod
	def fail(msg) :
		print(bcolors.FAIL + str(msg) + bcolors.ENDC)

	@staticmethod
	def warn(msg) :
		print(bcolors.WARNING + str(msg) + bcolors.ENDC)

	@staticmethod
	def ok(msg) :
		print(bcolors.OKGREEN + str(msg) + bcolors.ENDC)

	@staticmethod
	def okb(msg) :
		print(bcolors.OKBLUE + str(msg) + bcolors.ENDC)

	
