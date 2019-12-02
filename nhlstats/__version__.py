__author__ = 'tcaruso'

VERSION = (0, 0, 4)

POST = None

__version__ = '.'.join(map(str, VERSION)) + ('.{}'.format(POST) if POST else '')
