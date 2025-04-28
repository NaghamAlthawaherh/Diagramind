from flask import Flask, app
from flask_migrate import Migrate
from app.extensions import db, login_manager
import base64

from app.models import User


# from yolo_service import analyze_image  # استدعاء الدالة
migrate = Migrate()
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'main.login'  # اسم الراوت إذا المستخدم مو مسجل دخول



def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.secret_key = 'my-secret-key-123'
    db.init_app(app)
    migrate.init_app(app, db)

    app.jinja_env.filters['b64encode'] = base64.b64encode
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from app.route import main_bp as main_blueprint
    app.register_blueprint(main_blueprint)
    login_manager.init_app(app)


    return app

import base64



# if __name__ == "__main__":
#     app=create_app()
#     app.run(debug=True)   
