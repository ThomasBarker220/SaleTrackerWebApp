import os
import secrets
from PIL import Image
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #get a random hex for the photo name so it doesn't clash with existing file names
    _, f_ext = os.path.splitext(form_picture.filename) #the file has filename attribute, using _ because we don't need the first variable
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) #create a variable equal to the full path of the new profile picture
    
    output_size = (125, 125) #set desired size
    i = Image.open(form_picture)
    i.thumbnail(output_size) #resize image before uploading

    i.save(picture_path)
    prev_picture = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file) #check for previous picture
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg': #remove previous picture if it is not the default picture
        os.remove(prev_picture)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit(): #if form is valid
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
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