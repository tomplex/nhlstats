VERSION = (0, 0, 2)

POST = None

__version__ = '.'.join(map(str, VERSION)) + ('.{}'.format(POST) if POST else '')
