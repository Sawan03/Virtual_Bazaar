from flask import Flask, render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///demo.db'
app.config['SECRET_KEY'] = 'af6bdb14f5611dc9e5b46068'   #af6bdb14f5611dc9e5b46068
#app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db1 = SQLAlchemy(app)

bcrypt  = Bcrypt(app)


app.app_context().push()

login_manager = LoginManager()
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
login_manager.init_app(app)
from market.module import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

from market import route