import random

from pip._vendor.requests.packages.urllib3.connectionpool import xrange


def randomword(length):
   valid_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
   return ''.join((random.choice(valid_letters) for i in xrange(length)))

def get_session_id(request, generate):
    session_id = None
    
    if 'sessionid' in request.COOKIES:
        session_id = request.COOKIES['sessionid']
 
    if session_id == None and 'mysessionid' in request.COOKIES:
        session_id = request.COOKIES['mysessionid']
        
    if generate and session_id == None:
        session_id = "rand-" + randomword(30)
    return session_id
