from flask import Flask,Blueprint,request,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum, Boolean, Table
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from app import db  # استورد من نفس النسخة المعرفة في __init__.py
from flask_login import UserMixin

class User(db.Model,UserMixin):
    """User table for authentication and user management"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100))
    user_type = db.Column(db.String(50))
    terms_accepted = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
       return f"<User {self.first_name}>"
images=db.relationship('Image',backref='author',lazy=True)

class Image(db.Model):
    __tablename__='image'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    label = db.Column(db.String(50))  # مثلاً "Actor" أو "Use Case"
    image_data = db.Column(db.LargeBinary) 



class ProjectEstimation(db.Model):
    """Project estimation table for storing calculated estimations"""
    __tablename__ = 'project_estimations'
    
    id = db.Column(db.Integer, primary_key=True)
    total_requirements = db.Column(db.Integer, nullable=False)
    total_hours = db.Column(db.Float, nullable=False)
    team_size = db.Column(db.Integer, nullable=False)
    duration_weeks = db.Column(db.Integer, nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    budget_usd = db.Column(db.Float, nullable=False)
    def __repr__(self):
        return f"<ProjectEstimation for Project {self.total_hours}{self.total_requirements}>"



