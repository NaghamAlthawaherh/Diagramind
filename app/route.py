from flask import Flask,Blueprint, flash, redirect,request,jsonify,render_template, url_for
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash  
from app.models import ProjectEstimation, User, db


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
                flash(f"Welcome back, {user.full_name}!", "success")
                return redirect(url_for('main.index'))
            else:
                flash("Invalid password. Please try again.", "danger")
        else:
            flash("User not found. Please check your email or sign up.", "danger")

        return redirect(url_for('main.login'))  # لو فشل يرجعه

    return render_template('login.html')

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
