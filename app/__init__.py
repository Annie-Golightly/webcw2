from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask import Flask,request, session
from flask_admin import Admin
from flask_babel import Babel
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
#from flask_user import roles_required, UserManager

def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

app = Flask (__name__)
app.config.from_object('config')


admin = Admin(app,template_mode='bootstrap4')


login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)



db = SQLAlchemy(app)
migrate = Migrate(app,db)
from app import views, models

#user_manager = UserManager(app,db,models.Member)
babel = Babel(app, locale_selector=get_locale)