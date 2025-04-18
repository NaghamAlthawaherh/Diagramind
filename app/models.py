from flask import Flask,Blueprint,request,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum, Boolean, Table
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash  
import enum
from app import db  # استورد من نفس النسخة المعرفة في __init__.py




class User(db.Model):
    """User table for authentication and user management"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    full_name=db.Column(db.String(50),nullable=False)
   
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    def __repr__(self):
       return f"<User {self.full_name}>"



class UseCaseDiagram(db.Model):
    """Use case diagram table for storing uploaded diagrams"""
    __tablename__ = 'use_case_diagrams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    extracted_text = db.Column(db.Text, nullable=True) 
    use_cases = db.relationship('UseCase', back_populates='diagram')  
    requirements = db.relationship("FunctionalRequirement", back_populates="diagram")
    actors = db.relationship('Actor', backref='use_case_diagram')
    def __repr__(self):
        return f"<UseCaseDiagram {self.name}>"

class Actor(db.Model):
    """Actor table for storing actors extracted from use case diagrams"""
    __tablename__ = 'actors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    diagram_id = db.Column(db.Integer, db.ForeignKey('use_case_diagrams.id'), nullable=False)
    diagram = relationship("UseCaseDiagram", back_populates="actors")
    requirements = relationship("FunctionalRequirement", back_populates="actor")
    
    def __repr__(self):
        return f'<Actor {self.name}>'

class UseCase(db.Model):
    """Use case table for storing use cases extracted from diagrams"""
    __tablename__ = 'use_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    diagram_id = db.Column(db.Integer, db.ForeignKey('use_case_diagrams.id'), nullable=False)
    def __repr__(self):
        return f'<UseCase {self.name}>' 
 # Relationships
    diagram = relationship("UseCaseDiagram", back_populates="use_cases")
    requirements = relationship("FunctionalRequirement", back_populates="use_case")

class ComplexityEnum(enum.Enum):
    """Enum for requirement complexity levels"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class FunctionalRequirement(db.Model):
    """Functional requirement table for storing requirements extracted from diagrams"""
    __tablename__ = 'functional_requirements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    complexity = db.Column(db.Enum(ComplexityEnum), default=ComplexityEnum.MEDIUM)
    estimated_hours = db.Column(db.Float, nullable=True)
# Foreign Keys
    diagram_id = db.Column(db.Integer, db.ForeignKey('use_case_diagrams.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=True)
    use_case_id = db.Column(db.Integer, db.ForeignKey('use_cases.id'), nullable=True)
   # Relationships
    diagram = relationship("UseCaseDiagram", back_populates="requirements")
    actor = relationship("Actor", back_populates="requirements")
    use_case = relationship("UseCase", back_populates="requirements")
    
    def __repr__(self):
        return f'<FunctionalRequirement {self.title}>' 

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



