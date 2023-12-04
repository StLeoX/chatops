# Flask modules
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Local modules
from app.models.auth import User

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    print("load_user", user_id)
    user = User()
    user.load(user_id)

    return user

