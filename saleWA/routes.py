from flask import render_template, url_for, flash, redirect, request
from saleWA.forms import RegistrationForm, LoginForm, UpdateAccountForm
from saleWA.models import Users, Post
from saleWA import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

clothes = [
    {
        'name': 'Sweater',
        'price': '$50',
        'link': 'www.abercrombie.com',
        'image': 'sweaterimage.png'
    },
    {
        'name': 'Sweater',
        'price': '$50',
        'link': 'www.abercrombie.com',
        'image': 'sweaterimage.png'
    }
]


@app.route('/')

def home():
    return render_template('home.html')

@app.route('/items')
def items():
    return render_template('items.html', clothes=clothes, title='Items Page')


@app.route('/register', methods=['GET', 'POST'])

def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hashing password, string instead of bytes
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You may now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first() #check to see if there is a user with this email in the database, if so grab it, if not this will be none
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home')) #redirect to the next page if it exists, else just go to home page
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
            
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')

def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit(): #if form is valid
        current_user.username = form.username.data
        current_user.email  = form.email.data
        db.session.commit()
        flash('Your account information has been updated!', 'success') #success is the bootstrap class, flash a message if info is updated
        return redirect(url_for('account')) #redirect so you don't get another post request
    elif request.method == 'GET': #automatically populate form with current users data
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) #use the image file stored in the database with this user
    return render_template('account.html', title='Account', 
                           image_file=image_file, form=form)