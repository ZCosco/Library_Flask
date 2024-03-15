from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def get_data():
    return {'yee': 'haw'}

@api.route('/books', methods=['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    author_name = request.json['author_name']
    title = request.json['title']
    book_length = request.json['book_length']
    year_of_release = request.json['year_of_release']
    in_stock = request.json['in_stock']
    user_token = current_user_token.token

    book = Book(isbn=isbn, author_name=author_name, title=title, book_length=book_length,
                year_of_release=year_of_release, in_stock=in_stock, user_token=user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods=['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token= a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/<id>', methods=['GET'])
@token_required
def get_single_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods=['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    book.isbn = request.json['isbn']
    book.author_name = request.json['author_name']
    book.title = request.json['title']
    book.book_length = request.json['book_length']
    book.year_of_release = request.json['year_of_release']
    book.in_stock = request.json['in_stock']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods=['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)
