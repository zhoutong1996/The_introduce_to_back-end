import os
import tornado.web
from views import MainHandler,LoginHandler,HeaderModule,LoginModule
from webAPI import LoginWEB

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SETTINGS = {
    "template_path": os.path.join(BASE_DIR, "templates"),
    "static_path": os.path.join(BASE_DIR, "static")
}

HANDLERS = [
    (r"/", LoginHandler),
    (r"/login", MainHandler),
    (r"/ajax/login", LoginWEB),
]

UI_MODULES={
    'Login': LoginModule ,
    'Header': HeaderModule
}

application = tornado.web.Application(
    handlers = HANDLERS,
    ui_modules=UI_MODULES,
**SETTINGS)
