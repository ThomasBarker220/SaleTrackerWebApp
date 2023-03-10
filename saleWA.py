from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '93e55391acfb950a54ffed2f30e5cb18'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Users(db.Model): #create classes for database, each class is like a table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') #have to have at least default image
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) #relationship to Post model, pass in as string, backref allows us to use the author attribute to get user who made the post, lazy=True means SQLAlchemy loads data as necessary in one go

    def __repr__(self): #returns printable representation of the object as a string
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    

class Post(db.Model): # this is just from video walkthrough, will probably need to change/check and make sure this is how it should run
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #using lowercase user here because we're referencing table name

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# class Item(db.Model): # this is just from video walkthrough, will probably need to change/check and make sure this is how it should run
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False)
#     price = db.Column(db.Integer, nullable=False)

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created successfully for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
            
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)

