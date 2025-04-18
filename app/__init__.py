from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# from yolo_service import analyze_image  # استدعاء الدالة



def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.secret_key = 'my-secret-key-123'
    db.init_app(app)


    from app.route import main_bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

 
# if __name__ == "__main__":
#     app=create_app()
#     app.run(debug=True)   
