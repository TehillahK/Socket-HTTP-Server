#   cookies.py
#   Tehillah Kangamba 7859367   
#   Comp3010
#   Assignment 2
#   This creates authenticated session cookies 

import uuid
import tempfile
success_http ='''
HTTP/2.0 200 OK
Content-Type: text/html
Set-Cookie: {cookie_name}={cookie_val}
Content-Length: {size}
'''

body = '''<html>
<body>
</body>
</html>
'''

# class SessionCookie
# This is a utility class to help create session cookies for the Cookies class
class SessionCookie:
    def __init__(self):
        self._id = uuid.uuid4
        self.body_size = len(body)
        self.name = "sessionID"
        self.cookieVal = uuid.UUID('12345678123456781234567812345678')

    #   get_cookie
    #   this returns a cookie http response as a string
    def get_cookie(self):
        result = ""
        header = success_http.format(cookie_name = self.name, 
                                     cookie_val = self.cookieVal , 
                                     size = self.body_size )
        result = header + "/n" + body
        return result

# class Cookies
# this is a utitlity class used to create a store cookies
class Cookies:
     def __init__(self):
        self.user_cookies = []

    #   create_cookie
    #   returns a session cookie to authenticate a user and store it in the list of offical cookies 
     def create_cookie(self):
         result = ""
         cookie = SessionCookie()
         user_cookie = cookie.cookieVal
         self.user_cookies.append(user_cookie) # add it to official cookie vals of this session
         result = cookie.get_cookie()
         return result
    
     #  authenticate_cookie
     #  check if user computer is an actual user of this session
     #  accepts sessionID param
     #  returns True if its an authenticated user of the session
     def authenticate_cookie(self, sessionID):
         result = False
         if sessionID in self.user_cookies:
             result = True
         return result

    


        
