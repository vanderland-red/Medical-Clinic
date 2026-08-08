from flask import Flask
from config import *
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from blueprints.general import bp as general
from blueprints.admin import bp as admin
from blueprints.user import bp as user
from blueprints.doctor import bp as doctor
from blueprints.payment import bp as payment
from extentions import db
from models.tables import User
from flask_migrate import Migrate


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_CONFIG
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY

csrf = CSRFProtect(app)

db.init_app(app)

migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login" 
login_manager.login_message = "قبل از ثبت درخواست سرویس، ابتدا وارد حساب کاربری شوید."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(doctor)
app.register_blueprint(payment)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


# {% if request.endpoint.startswith("general") %}
#   {% if current_user.is_authenticated %}
#          <a href="{{ url_for('user.dashboard') }}" class="header-btn">حساب کاربری</a>
#        {% else %}
#             <a href="{{ url_for('user.register') }}" class="header-btn">ثبت نام</a>
#        {% endif%}
#    {% endif %}