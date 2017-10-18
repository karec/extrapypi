from flask_login import LoginManager
from flask_principal import Principal
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy


csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
principal = Principal()
