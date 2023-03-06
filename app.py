from flask import Flask, render_template, url_for
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


@app.route('/register')

def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route('/login')

def login():
    form = LoginForm()
    return render_template('register.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)

