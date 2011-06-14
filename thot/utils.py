import sys

DEBUG_ACTIVE = False
SUCCESS_EXIT = 1
ERROR_EXIT = 2

def debug(msg):
	global DEBUG_ACTIVE
	if DEBUG_ACTIVE: sys.stdout.write("DEBUG:: %s\n" % msg)

def print_err(msg):
	sys.stderr.write("ERROR:: %s\n" % msg)

def exit(exit):
	sys.exit(exit)
