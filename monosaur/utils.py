import random

from pip._vendor.requests.packages.urllib3.connectionpool import xrange


def randomword(length):
   valid_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
   return ''.join((random.choice(valid_letters) for i in xrange(length)))
