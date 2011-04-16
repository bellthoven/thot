#!/usr/bin/env python3

import sys
import core

def main(args):
	app = core.Application(args)
	app.bootstrap()
	app.run()

if __name__ == '__main__':
	main(sys.argv[1:])
