import sys
from thot.core import Application

__author__ = 'Gustavo Dutra'
__versioninfo__ = (0, 1)
__version__ = '.'.join(map(str, __versioninfo__))

__all__ = ['Application']

def main():
	Application(sys.argv[1:]).run()

if __name__ == '__main__':
	main()
