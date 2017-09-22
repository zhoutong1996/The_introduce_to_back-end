import tornado.web
from tornado import escape
import json

class LoginWEB(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        print(username,password)
        if username=="test":
            if password=="123456":
                result = {"state":"true","text":"hello user:"+username}
            else:
                result = {"state":"false","text":"username or password error"}
        else:
            result = {"state":"false","text":"username or password error"}
        self.write(escape.json_decode(json.dumps(result)))
