import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('main.html')

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('demo.html')
        
class HeaderModule(tornado.web.UIModule):
    def render(self):
        return self.render_string(
            "header.html"
        )
        
    def css_files(self):
        return "/static/css/xgxt_login.css"
        
class LoginModule(tornado.web.UIModule):
    def render(self):
        return self.render_string(
            "login.html"
        )
        
    def javascript_files(self):
        return ["/static/js/login.js", "/static/js/jquery.js"]
