from flask import render_template, redirect, request, flash, session, url_for
from flask_login import logout_user, current_user, login_user, login_required
from app import app, db
from app.models import User, Restaurant, Cuisine, Rating,Locality
import pandas as pd
import numpy as np
from datetime import datetime
from app.collabrative_filtering import *

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


@app.route('/cuisine',)
@login_required
def cuisine():
    return render_template('cuisine.html', title='Cuisines')

@app.route('/query')
def query():
    if 'cuisine' in request.args:
        cuisine = request.args.get('cuisine')
        data = Restaurant.query.filter(Restaurant.cuisine.contains(cuisine)).order_by(Restaurant.rating.desc())
        return render_template('cuisine_wise.html',title=f"{cuisine} restaurant",data=data) 
    else:
        return redirect('/cuisine')


@app.route('/search',methods=['POST','GET'])
def search():
    results = None
    options = None
    if request.method =='POST':
        locality = request.form.get('locality')
        cuisine = request.form.get('cuisine')
        price_min = request.form.get('price_min')
        price_max = request.form.get('price_max')
        options = request.form
        results = Restaurant.query.filter(Restaurant.area.contains(locality))
        print(options)
        if cuisine != 'All':
            results = results.filter(Restaurant.cuisine.like(cuisine))
        if price_max.isnumeric() and price_min.isnumeric():
            results = results.filter(Restaurant.cost_for_two.in_([price_min, price_max]))
        print(results)
    localities = Locality.query.all()
    cusines = Cuisine.query.all()
    dataset = []
    for row in cusines:
        if ',' in row.name:
            dataset.extend(row.name.split(','))
        else:
            dataset.append(row.name)
    cusineslist = list(set(dataset))
    return render_template('search.html', title='guest search', cusineslist=cusineslist, localities=localities,results=results, options=options)

@app.route('/price',methods=['POST','GET'])
@login_required
def price():
    results = None
    options = None
    if request.method =='POST':
        locality = request.form.get('locality')
        cuisine = request.form.get('cuisine')
        price_min = request.form.get('price_min')
        price_max = request.form.get('price_max')
        options = request.form
        results = Restaurant.query.filter(Restaurant.area.contains(locality))
        print(options)
        if cuisine != 'All':
            results = results.filter(Restaurant.cuisine.like(cuisine))
        if price_max.isnumeric() and price_min.isnumeric():
            results = results.filter(Restaurant.cost_for_two.in_([price_min, price_max]))
        print(results)
    localities = Locality.query.all()
    cusines = Cuisine.query.all()
    dataset = []
    for row in cusines:
        if ',' in row.name:
            dataset.extend(row.name.split(','))
        else:
            dataset.append(row.name)
    cusineslist = list(set(dataset))
    return render_template('price.html', title='price based search', cusineslist=cusineslist, localities=localities,results=results, options=options)


@app.route('/top_rest',methods=['POST','GET'])
@login_required
def top_rest():
    results = None
    options = None
    if request.method =='POST':
        locality = request.form.get('locality')
        cuisine = request.form.get('cuisine')
        price_min = request.form.get('price_min')
        price_max = request.form.get('price_max')
        options = request.form
        results = Restaurant.query.filter(Restaurant.area.contains(locality))
        print(options)
        if cuisine != 'All':
            results = results.filter(Restaurant.cuisine.like(cuisine))
        if price_max.isnumeric() and price_min.isnumeric():
            results = results.filter(Restaurant.rating.in_([price_min, price_max]))
        results = results.order_by(Restaurant.rating.desc())
    localities = Locality.query.all()
    cusines = Cuisine.query.all()
    dataset = []
    for row in cusines:
        if ',' in row.name:
            dataset.extend(row.name.split(','))
        else:
            dataset.append(row.name)
    cusineslist = list(set(dataset))
    return render_template('top_rest.html', title='price based search', cusineslist=cusineslist, localities=localities,results=results, options=options)


@app.route('/history')
@login_required
def history():
    history = Rating.query.filter_by(username=current_user.username)
    dataset =[]
    for row in history:
        rest = Restaurant.query.filter_by(id = row.rest_id).first_or_404()
        dataset.append({
            'id':row.id,
            'rest_name':rest.name,
            'address':rest.address,
            'latitude':rest.latitude,
            'longitude':rest.longitude,
            'link':rest.zomato_url,
            'rest_id':row.rest_id,
            'rating':row.rating,
            'username':row.username,
            'date_posted':row.date_posted,
        })
    return render_template('history.html', title='about_1',data = dataset)


@app.route('/recommend', methods=['GET','POST'])
@login_required
def recommend():
    try:
        username = current_user.username
        if request.method =='POST':
            name = request.form.get('name')
            if name:
                uname =  User.query.filter_by(username=name).first()
                username = uname.username
                print(username)
        user= pd.read_sql('rating',db.engine)
        user[user.username==username]
        a= user[user.username==username]
        b= a.rating
        b.tolist()
        df = user.set_index('id', drop = True)
        a1= df.loc[10:20,"rating"]
        a2= list(a1)
        hotel = pd.read_sql("restaurant", db.engine)
        Ratings = pd.read_sql("rating", db.engine)
        Mean = Ratings.groupby(by="username",as_index=False)['rating'].mean()
        Rating_avg = pd.merge(Ratings,Mean,on='username')
        Rating_avg['adg_rating']=Rating_avg['rating_x']-Rating_avg['rating_y']
        Rating_avg.head(15)

        hotel.rename(columns = {'id':'rest_id'}, inplace = True) 

        check = pd.pivot_table(Rating_avg,values='rating_x',index='username',columns='rest_id')
        final = pd.pivot_table(Rating_avg,values='adg_rating',index='username',columns='rest_id')

        # Replacing NaN by restuarant Average
        final_restuarant = final.fillna(final.mean(axis=0))

        # Replacing NaN by user Average
        final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)
        b = cosine_similarity(final_user)
        np.fill_diagonal(b, 0 )
        similarity_with_user = pd.DataFrame(b,index=final_user.index)
        similarity_with_user.columns=final_user.index

        # user similarity on replacing NAN by item(restuarant) avg
        cosine = cosine_similarity(final_restuarant)
        np.fill_diagonal(cosine, 0 )
        similarity_with_restuarant = pd.DataFrame(cosine,index=final_restuarant.index)
        similarity_with_restuarant.columns=final_user.index

        # top 30 neighbours for each user
        sim_user_30_u = find_n_neighbours(similarity_with_user,30)

        # top 30 neighbours for each user
        sim_user_30_m = find_n_neighbours(similarity_with_restuarant,30)
        
        score = User_item_score(username,74385,sim_user_30_m,final_restuarant,Mean,similarity_with_restuarant)
        Rating_avg = Rating_avg.astype({"rest_id": str})
        restuarant_user = Rating_avg.groupby(by = 'username')['rest_id'].apply(lambda x:','.join(x))
        user = current_user.username
        pred_rest = User_item_score1(user, Mean, similarity_with_restuarant, check,sim_user_30_m, restuarant_user, final_restuarant, hotel,)
    except Exception as e:
        pred_rest = None
        score = 0
    return render_template('top_rest.html',user=username, title='about_1',score=str(score)[:5], data= pred_rest)


@app.route('/demo_map')
@login_required
def demo_map():
    return render_template('demo_map.html', title='about_1')


@app.route('/feature_selection')
@login_required
def feature_selection():
    return render_template('feature_selection.html', title='about_1')




