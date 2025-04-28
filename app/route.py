from flask import Flask,send_file,Blueprint, flash, redirect,request,jsonify,render_template, session, url_for
# from flask_sqlalchemy import SQLAlchemy
import numpy as np
from werkzeug.security import generate_password_hash,check_password_hash  
from app.models import Image, ProjectEstimation, User, db
from flask_login import login_user, logout_user, login_required, current_user
import os, io
import cv2
from PIL import Image as PILImage
from ultralytics import YOLO
from app.utils.yolo_detect import analyze_diagram

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def Home():
    return render_template('Home.html')


@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        hashed_password = generate_password_hash(password)
       
       # 🔽 هون بتحط الكود يلي سألته عنه
        new_user = User(full_name=full_name, email=email, password_hash=hashed_password)

        # فحص كلمة السر
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('main.signup'))

        # تأكد إن المستخدم غير موجود
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "warning")
            return redirect(url_for('main.signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(full_name=full_name, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!", "success")
        print("User created:", new_user.email)
        return redirect(url_for('main.index'))

    return render_template('signup.html')

@main_bp.route('/index')
@login_required
def index():
    return render_template('index.html')



@main_bp.route('/history')
def show_history():
        from models import Estimation  # حسب اسم الموديل عندك
        estimations = Estimation.query.order_by(Estimation.created_at.desc()).all()
        return render_template('history.html', estimations=estimations)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password_hash, password):
                login_user(user)
                # flash(f"Welcome back, {user.full_name}!", "success")
                return redirect(url_for('main.index'))
            else:
                flash("Invalid password. Please try again.", "danger")
        else:
            flash("User not found. Please check your email or sign up.", "danger")

        return redirect(url_for('main.login'))  # لو فشل يرجعه

    return render_template('login.html')
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    # session.pop('_flashes', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('main.login'))

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    project_name = request.form.get('project_name')
    diagram = request.files.get('diagram')

    if not project_name or not diagram:
        flash("All fields are required", "warning")
        return redirect(url_for('main.index'))

    estimation = ProjectEstimation(name=project_name)
    db.session.add(estimation)
    db.session.commit()
    # do something with the file...
    flash("File uploaded successfully!", "success")
    return redirect(url_for('main.results', estimation_id=estimation.id)) # أو أي صفحة بدك توديه عليها

@main_bp.route('/save-image', methods=['POST'])
def save_image():
    if current_user.is_authenticated:
        new_img = Image(
            user_id=current_user.id,
            # باقي الحقول...
        )
        db.session.add(new_img)
        db.session.commit()
        return "✅ Saved to DB"
    else:
        return "❌ User not logged in", 401

@main_bp.route('/analyze', methods=['POST'])
@login_required
def analyze_image():
    if 'diagram' not in request.files:
        flash("No file part", "danger")
        return redirect(url_for('main.index'))

    file = request.files['diagram']
    if file.filename == '':
        flash("No selected file", "danger")
        return redirect(url_for('main.index'))

    image_bytes = file.read()

    try:
        class_counts = analyze_diagram(image_bytes)
        flash("✅ Diagram analyzed and saved to database", "success")
    except Exception as e:
        flash(f"❌ Error during analysis: {e}", "danger")

    return redirect(url_for('main.index'))


from flask import render_template
from flask_login import login_required, current_user
from app.models import Image

# @main_bp.route('/my-crops')
# @login_required
# def show_cropped_images():
#     images = Image.query.filter_by(user_id=current_user.id).all()
#     return render_template('cropped_images.html', images=images)

@main_bp.route('/image/<int:image_id>')
def display_image(image_id):
    img = Image.query.get_or_404(image_id)
    return send_file(io.BytesIO(img.image_data), mimetype='image/png')


