from flask import render_template, redirect, request, flash, session, url_for
from flask_login import logout_user, current_user, login_user, login_required
from app import app, db
from app.models import User, Restaurant, Cuisine, Rating
import pandas as pd
import numpy as np
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user is None or not user.check_password(password):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template('login.html', title='Sign In')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        cpassword = request.form.get('cpassword')
        password = request.form.get('password')
        print(cpassword, password, cpassword == password)
        if username and password and cpassword and email:
            if cpassword != password:
                flash('Password do not match', 'danger')
                return redirect('/register')
            else:
                if User.query.filter_by(email=email).first() is not None:
                    flash('Please use a different email address', 'danger')
                    return redirect('/register')
                elif User.query.filter_by(username=username).first() is not None:
                    flash('Please use a different username', 'danger')
                    return redirect('/register')
                else:
                    user = User(username=username, email=email)
                    user.set_password(password)
                    db.session.add(user)
                    db.session.commit()
                    flash('Congratulations, you are now a registered user!', 'success')
                    return redirect(url_for('login'))
        else:
            flash('Fill all the fields', 'danger')
            return redirect('/register')

    return render_template('register.html', title='Sign Up page')


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            pass
    return render_template('forgot.html', title='Password reset page')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user, title=f'{user.username} profile')


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/profile')
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.username = request.form.get('username')
        current_user.about_me = request.form.get('aboutme')
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', title='Edit Profile', user=user)


@app.route('/cuisine')
@login_required
def cuisine():
    return render_template('cuisine.html', title='about_1')


@app.route('/search')
def search():
    return render_template('search.html', title='about_1')


@app.route('/price')
@login_required
def price():
    return render_template('price.html', title='about_1')


@app.route('/history')
@login_required
def history():
    return render_template('history.html', title='about_1')


@app.route('/top_rest')
@login_required
def top_rest():
    return render_template('top_rest.html', title='about_1')


@app.route('/demo_map')
@login_required
def demo_map():
    return render_template('demo_map.html', title='about_1')


@app.route('/feature_selection')
@login_required
def feature_selection():
    return render_template('feature_selection.html', title='about_1')


# TEMPORARY PAGES FOR DATA INSERTION
@app.route('/addcuisines', methods=['GET', 'POST'])
def addcuisines():
    if request.method == 'POST':
        cid = request.form.get('cid')
        cname = request.form.get('cname')
        if cid:  # not none
            if cname:
                Obj = Cuisine(id=cid, name=cname)
                db.session.add(Obj)  # save data in database
                db.session.commit()  # update database
                flash('entry added', 'success')
            else:
                flash('enter proper cuisine name', 'danger')
        else:
            flash('enter proper id')
    return render_template('addcuisines.html', title="Input data")


@app.route('/addlocality', methods=['GET', 'POST'])
def addlocality():
    if request.method == 'POST':
        locid = request.form.get('locid')
        locname = request.form.get('locname')
        loccity = request.form.get('loccity')
        if locid:  # not none
            if locname:
                if loccity:
                    Obj = Locality(id=locid, name=locname, city=loccity)
                    db.session.add(Obj)  # save data in database
                    db.session.commit()  # update database
                    flash('entry added', 'success')
                else:
                    flash('enter proper locality city', 'danger')
            else:
                flash('enter proper locality name', 'danger')
        else:
            flash('enter proper id')
    return render_template('addlocality.html', title="Input data")


@app.route('/addrest', methods=['GET', 'POST'])
def addrest():
    hotel = pd.read_csv('lko_final_01.csv', encoding='latin1')
    for i in range(0, hotel.size):
        rid = hotel.rest_id[i]
        name = hotel.name[i]
        add = hotel.address[i]
        phone = hotel.telephone[i]
        delivery = hotel.delivery_only[i]
        booking = hotel.table_reservation[i]
        url = hotel.zomato_url[i]
        Obj = Restaurant(id=rid, name=name, address=add, phone=phone, delivery=delivery, booking=booking, url=url)
        db.session.add(Obj)  # save data in database
        db.session.commit()  # update database
        flash('entry added', 'success')

    return render_template('addrest.html', title="Input data")


@app.route('/input', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        msg = request.form.get('msg')
        if msg:  # not none
            if len(msg) >= 10:  # just some validation
                msgObj = MessageData(message=msg)  # add data to model object
                db.session.add(msgObj)  # save data in database
                db.session.commit()  # update database
                # prediction logic
                flash('we have saved ur data, prediction result will be available shortly', 'success')
            else:
                flash('message smaller than 10 characters cannot be predicted', 'danger')
        else:
            flash('message not provided, please fill in some data to predict')
    return render_template('input.html', title="Input data")
