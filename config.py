# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://@DESKTOP-51BRH30/DiagraMind?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
    # db = SQLAlchemy(app)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
