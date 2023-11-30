import datetime
import os
from time import sleep
from .FROCR import OCR, FV_check
import cv2
from flask import Blueprint, flash, redirect, url_for
from flask import render_template, Response, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .first_last_names import first_names, last_names, load_names
from sqlalchemy import  update
from . import db
from .models import User

auth = Blueprint('auth', __name__)

global capture, f_name, l_name, check, FV_t, of_name, ol_name
load_names()

capture = 0
check = 0
FV_t = 0
of_name = 0
ol_name = 0
try:
    os.mkdir('./shots')
except OSError as error:
    pass
try:
    os.mkdir('./ocr_pic')
except OSError as error:
    pass

camera = cv2.VideoCapture(0)


def gen_frames():
    global capture, check, FV_t, f_name, l_name, of_name, ol_name, frame
    while True:
        success, frame = camera.read()
        if success:
            if capture:
                capture = 0
                imgname = image
                p = os.path.sep.join(['shots', imgname])
                cv2.imwrite(p, frame)
                print("image saved!")
            elif check:
                check = 0
                imgname = 'ocr_testing.jpg'
                p = os.path.sep.join(['ocr_pic', imgname])
                cv2.imwrite(p, frame)
                print("OCR image saved!")

            elif FV_t:
                FV_t = 0
                imgname = 'FV_testing.jpg'
                p = os.path.sep.join(['ocr_pic', imgname])
                cv2.imwrite(p, frame)
                print("FV image saved!")

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            pass


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName').upper()
        last_name = request.form.get('lastName').upper()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 1:
            flash('last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            global image
            image = first_name + last_name + "_img.jpg"
            new_user = User(email=email, first_name=first_name, last_name=last_name, image=image,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            load_names()
            flash('Account created!', category='success')
            return render_template("userpic.html", user=current_user)

    return render_template("sign_up.html", user=current_user)


@auth.route('/userphoto')
@login_required
def userphoto():
    return render_template('userpic.html', user=current_user)


@auth.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@auth.route('/requests', methods=['POST', 'GET'])
def Cap():
    global of_name, ol_name
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
            return redirect(url_for('views.home'))
    elif request.method == 'GET':
        return render_template('userpic.html', user=current_user)


@auth.route('/ocr', methods=['POST', 'GET'])
def ocr():
    global of_name, ol_name
    if request.method == 'POST':
        if request.form.get('check') == 'check':
            global check, f_name, l_name
            check = 1
            sleep(1)
            f_name, l_name = OCR('ocr_pic/ocr_testing.jpg')
            print(f_name)
            print(l_name)
            of_name = f_name in first_names
            ol_name = l_name in last_names
            if of_name and ol_name:
                of_name = 0
                ol_name = 0
                print("OCR passed")
                flash('User recognized !', category='success')
                return redirect(url_for('auth.FV'))
            else:
                flash('User is not found.', category='error')
    return render_template('ocr.html', user=current_user)


@auth.route('/FV', methods=['POST', 'GET'])
def FV():
    if request.method == 'POST':
        if request.form.get('check') == 'check':
            global FV_t, f_name, l_name
            FV_t = 1
            sleep(1)
            FV_result = FV_check("ocr_pic/FV_testing.jpg", f_name + l_name)
            if FV_result:
                flash('User verified !', category='success')
                print("Face verified!")
                return redirect(url_for('auth.update_password'))
            else:
                flash('User did not verified.', category='error')

    return render_template('FV.html', user=current_user)


@auth.route('/Update_Password', methods=['POST', 'GET'])
def update_password():
    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            stm = update(User).where(User.first_name == f_name).values(password=generate_password_hash(password1, method='sha256'))
            db.session.execute(stm)
            db.session.commit()
            print("password changed")
            return redirect(url_for('auth.login'))

    return render_template('update_password.html', user=current_user)
