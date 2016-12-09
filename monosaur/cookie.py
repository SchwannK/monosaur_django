import random
import string

from django.conf import settings
from django.utils.crypto import (
    get_random_string,
)


VALID_KEY_CHARS = string.ascii_lowercase + string.digits
MY_COOKIE_NAME = "mysessionid"

class MyCookieProcessingMiddleware(object):

    def process_request(self, request):
        get_session_id(request, True)
        print("request " + settings.SESSION_COOKIE_NAME + ": " + str(request.COOKIES.get(settings.SESSION_COOKIE_NAME)))
        print("request " + MY_COOKIE_NAME + ": " + str(request.COOKIES.get(MY_COOKIE_NAME)))

    def process_response(self, request, response):
        set_session_id(request, response)
        print("response " + settings.SESSION_COOKIE_NAME + ": " + str(response.cookies.get(settings.SESSION_COOKIE_NAME)))
        print("response " + MY_COOKIE_NAME + ": " + str(response.cookies.get(MY_COOKIE_NAME)))
        return response
    
def get_session_id(request, generate):
    session_id = None
    
    if settings.SESSION_COOKIE_NAME in request.COOKIES:
        session_id = request.COOKIES[settings.SESSION_COOKIE_NAME]
 
    if session_id == None and MY_COOKIE_NAME in request.COOKIES:
        session_id = request.COOKIES[MY_COOKIE_NAME]
        
    if generate and session_id == None:
        session_id = "my-" + get_random_string(32, VALID_KEY_CHARS)
        print("Generating my session id: " + session_id)
        request.COOKIES[MY_COOKIE_NAME] = session_id
    return session_id

def set_session_id(request, response):
    response.cookies[MY_COOKIE_NAME] = get_session_id(request, True)
