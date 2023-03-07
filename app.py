from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '93e55391acfb950a54ffed2f30e5cb18'

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

