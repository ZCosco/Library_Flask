from flask import Blueprint, render_template
from models import Book

site = Blueprint('site', __name__, template_folder='site_templates')


@site.route('/')
def home():
    books = Book.query.all()
    return render_template('index.html', books=books)

@site.route('/profile')
def profile():
    return render_template('profile.html')