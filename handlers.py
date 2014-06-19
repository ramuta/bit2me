import json
from google.appengine.ext import ndb
import jinja2
import os
import webapp2
from auth import make_pw_hash
from models import User


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_json(self, output):
        self.response.headers['Content-Type'] = 'application/json'  # ; charset=utf-8'
        self.write(json.dumps(output))

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))


class MainHandler(BaseHandler):
    def get(self):
        self.render("main.html")


class RegisterHandler(BaseHandler):
    def post(self):
        name = self.request.get("name")
        password = self.request.get("password")
        verify = self.request.get("verify")
        if password==verify and name != "":
            user_key = ndb.Key(User, name)
            check_name = user_key.get()
            if check_name is None:
                user = User(key=user_key, name=name, pw_hash=make_pw_hash(name, password))
                user.put()
                self.render("main.html", name=name)
            else:
                name = "user exists"
                self.render("main.html", name=name)


class LoginHandler(BaseHandler):
    def post(self):
        self.render("main.html")