from flask import Flask
from flask_migrate import Migrate
import base64
from flask_mail import Message, Mail

from app.extensions import db, login_manager  # ✅ استخدام النسخة الصحيحة

migrate = Migrate()
mail = Mail() 

def create_app():
    app = Flask(__name__)
    
    # Basic Configuration
    app.config['SECRET_KEY'] = '12345'
    app.config['SQLALCHEMY_DATABASE_URI'] ='mssql+pyodbc://@DESKTOP-51BRH30/DiagraMind?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='your_email@gmail.com',
        MAIL_PASSWORD='your_email_password_or_app_password',
        MAIL_DEFAULT_SENDER=('Esti-Use', 'your_email@gmail.com')
    )
    mail = Mail(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Register user loader
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Jinja2 filters
    app.jinja_env.filters['b64encode'] = base64.b64encode

    # Register blueprints
    from app.route import main_bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# إعدادات البريد (مثال باستخدام Gmail SMTP)





# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager
# import base64



# # Initialize extensions
# db = SQLAlchemy()
# login_manager = LoginManager()
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)
    
#     # Basic Configuration
#     app.config['SECRET_KEY'] = '12345'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@JORY_MOSLEH\MSSQLSERVER01/DiagraMind?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#     # Initialize extensions with app
#     db.init_app(app)
#     migrate.init_app(app, db)
#     login_manager.init_app(app)
#     login_manager.login_view = 'main.login'
    
#     from app.models import User

#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))
#     # Jinja2 filters
#     app.jinja_env.filters['b64encode'] = base64.b64encode
    
#     # Register blueprints
#     from app.route import main_bp as main_blueprint
#     app.register_blueprint(main_blueprint)
    
#     return app



# from flask import Flask
# from flask_login import LoginManager
# from flask_migrate import Migrate
# from app.extensions import db
# import base64
# from app.models import User


# # from yolo_service import analyze_image  # استدعاء الدالة
# migrate = Migrate()
# login_manager = LoginManager()
# login_manager.login_view = 'main.login'  # اسم الراوت إذا المستخدم مو مسجل دخول



# def create_app():
#     app = Flask(__name__)
#     app.config.from_mapping(
#         SQLALCHEMY_DATABASE_URI='mssql+pyodbc://@JORY_MOSLEH\MSSQLSERVER01/DiagraMind?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes',
#         SQLALCHEMY_TRACK_MODIFICATIONS=False,
#         SECRET_KEY='my_secret_key=123'
#     )
#     # app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@JORY_MOSLEH\MSSQLSERVER01/DiagraMind?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
#     # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     # app.config['SECRET_KEY'] = '12345'

   
#     db.init_app(app)
#     migrate.init_app(app, db)
#     login_manager.init_app(app)

#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))
    
    
#     app.jinja_env.filters['b64encode'] = base64.b64encode
    

#     from app.route import main_bp as main_blueprint
#     app.register_blueprint(main_blueprint)
  


#     return app

# import base64



# if __name__ == "__main__":
#     app=create_app()
#     app.run(debug=True)   



