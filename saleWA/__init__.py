from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '93e55391acfb950a54ffed2f30e5cb18'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) #when working w db in terminal appctx = app.app_context(), appctx.push(), appctx.pop()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from saleWA import routes #has to be down here so there aren't circular imports