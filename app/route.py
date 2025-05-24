from flask import Flask, make_response,send_file,Blueprint, flash, redirect,request,jsonify,render_template, send_from_directory, session, url_for,flash
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
import random
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')


# @main_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         first_name = request.form['firstname']
#         last_name = request.form['lastname']
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirmPassword']
#         hashed_password = generate_password_hash(password)
       
#        # 🔽 هون بتحط الكود يلي سألته عنه
#         new_user = User(first_name=first_name,last_name=last_name, email=email, password_hash=hashed_password)

#         # فحص كلمة السر
#         if password != confirm_password:
#             flash("Passwords do not match.", "danger")
#             return redirect(url_for('main.signup'))

#         # تأكد إن المستخدم غير موجود
#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             flash("Email already registered.", "warning")
#             return redirect(url_for('main.signup'))

#         hashed_password = generate_password_hash(password)
#         new_user = User(first_name=first_name,last_name=last_name, email=email, password_hash=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()

#         flash("Account created successfully!", "success")
#         print("User created:", new_user.email)
#         return redirect(url_for('main.index'))

#     return render_template('signup.html')
@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirmPassword')
            company = data.get('company', '')
            user_type = data.get('userType')
            terms_agreed = data.get('termsCheck', False)

            # نفس التحقق السابق ...
            if password != confirm_password:
                return {"message": "Passwords do not match."}, 400

            if not terms_agreed:
                return {"message": "You must agree to the terms and conditions."}, 400

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {"message": "Email already in use."}, 400

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                company=company,
                user_type=user_type,
                terms_accepted=True
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            return {"message": "Account created successfully!"}, 200

        else:
            # إذا كانت البيانات ليست JSON (مثلاً طلب مباشر من form)
            # تعامل كما كان في الكود القديم، أو أرجع خطأ
            return {"message": "Invalid request"}, 400

    # عند GET فقط عرض صفحة التسجيل
    return render_template('signup.html')


@main_bp.route('/index')
# @login_required  
def index():
    print("main route accessed")
    return render_template('index.html')

@main_bp.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory('static', 'sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Content-Type'] = 'application/javascript'
    return response


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('rememberMe')

        # Check if user exists
        user = User.query.filter_by(email=email).first()

        # if not user:
        #     flash('Invalid email or password', 'error')
        #     return redirect(url_for('main.login'))
        
        # Verify password
        # if not check_password_hash(User['password'], password):
        #     flash('Invalid email or password', 'error')
        #     return redirect(url_for('main.login'))
        
        # Set session
        session['user_email'] = email
        session['user_name'] = user['name']
        
        # Handle remember me
        # if remember_me:
        #     session.permanent = True
        
        flash('Login successful!', 'success')
        return redirect(url_for('main.index'))
    
    # GET request - show login form
    return render_template('login.html')


# @main_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         user = User.query.filter_by(email=email).first()
#         if user and check_password_hash(user.password_hash, password):
#             login_user(user)
#             return redirect(url_for('main.index1'))
#         else:
#             flash("Invalid email or password", "danger")
#             return redirect(url_for('main.login'))

#     return render_template('login.html')


@main_bp.route('/forgot-password')
def main():
    return render_template('index.html')

@main_bp.route('/wizard')
def wizard():
    return render_template('wizard.html')  

@main_bp.route('/report')
def report():
    return render_template('report.html')  

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    # session.pop('_flashes', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('main.login'))

@main_bp.route('/upload', methods=['POST'])
def upload():
    project_name = request.form.get('project_name')
    diagram = request.files.get('diagram')

    if not project_name or not diagram:
        flash("All fields are required", "warning")
        return redirect(url_for('main.home'))

    estimation = ProjectEstimation(name=project_name)
    db.session.add(estimation)
    db.session.commit()
    # do something with the file...
    flash("File uploaded successfully!", "success")
    return redirect(url_for('main.home', estimation_id=estimation.id)) # أو أي صفحة بدك توديه عليها

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



@main_bp.route('/analyze', methods=['POST','GET'])
# @login_required
def analyze_image():
    if 'diagram' not in request.files:
        flash("❌ No file part", "danger")
        # return redirect(url_for('main.index'))
        return 'No file part'

    file = request.files['diagram']
    if file.filename == '':
        flash("❌ No selected file", "danger")
        # return redirect(url_for('main.index'))
        return'No selected file'
    image_bytes = file.read()

    try:
        class_counts = analyze_diagram(image_bytes)
        flash("✅ Diagram analyzed and saved to database", "success")
        return'Diagram analyzed and saved to database'
    except Exception as e:
        flash(f"❌ Error during analysis: {str(e)}", "danger")
        # return f"Error during analysis: {str(e)}"

    return redirect(url_for('main.main'))




# @main_bp.route('/analyze', methods=['POST'])
# @login_required
# def analyze_image():
#     if "diagram" not in request.files:
#         flash("No file part", "danger")
#         return redirect(url_for('main.index'))

#     file = request.files['diagram']
#     if file.filename == '':
#         flash("No selected file", "danger")
#         return redirect(url_for('main.index'))

#     image_bytes = file.read()

#     try:
#         class_counts = analyze_diagram(image_bytes)
#         flash("✅ Diagram analyzed and saved to database", "success")
#     except Exception as e:
#         flash(f"❌ Error during analysis: {e}", "danger")
#     print("asd")
#     return redirect(url_for('main.index'))


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


@main_bp.route('/help')
def help():
    return render_template('help.html')

@main_bp.route('/settings')
def settings():
    return render_template('settings.html')




