import unittest
import os

if __name__ == '__main__':
	for filename in os.listdir('.'):
		if filename.endswith('.py'):
			module = filename.replace('.py', '')
			try:
				m = __import__(module)
				globals()[m.__name__] = m
				for name in dir(m):
					if name.endswith('Test'):
						alltests.append(getattr(m, name)())
			except ImportError as e:
				print(e)
	unittest.main()
#	runner = unittest.TextTestRunner()
#	suite = unittest.TestSuite(alltests)
#	runner.run(suite)
