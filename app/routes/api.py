from flask import Blueprint, request, jsonify
import jwt

from ..models.models import db, User, Product, Transaction, Review, Productsize
from ..config import Configuration


bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/users", methods=["POST"])
def signup_user():
    print(request.get_json)
    data = request.json
    user = User(first_name=data["firstName"], last_name=data["lastName"], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    access_token = jwt.encode({'email': user.email}, Configuration.SECRET_KEY)
    return {'access_token': access_token.decode('UTF-8'), 'user': user.to_dict()}


@bp.route("/users/session", methods=['POST'])
def signin_user():
    data = request.json
    user = User.query.filter(User.email == data['email']).first()
    if not user:
        return {"error": "Email not found"}, 422
    if user.check_password(data['password']):
        if user.first_name == 'demo':
            db.session.query(Review).filter(Review.user_id==1).delete()
            db.session.query(Transaction).filter(Transaction.user_id==1).delete()
            review1 = Review(user_id=1, first_name='demo', last_name='user', product_id=1, review_body='My team only wears Supreme')
            review2 = Review(user_id=1, first_name='demo', last_name='user', product_id=7, review_body='Perfect for the outdoors.')
            review3 = Review(user_id=1, first_name='demo', last_name='user', product_id=26, review_body='I gotta have it!')
            review4 = Review(user_id=1, first_name='demo', last_name='user', product_id=37, review_body='Say Hello to my little friend.')
            review5 = Review(user_id=1, first_name='demo', last_name='user', product_id=43, review_body='Bruh, so clean!')
            transaction1 = Transaction(products=[1, 25, 38], user_id=1, total=56000)
            transaction2 = Transaction(products=[43, 47], user_id=1, total=110300)
            transaction3 = Transaction(products=[51, 61], user_id=1, total=27600)
            db.session.add(review1)
            db.session.add(review2)
            db.session.add(review3)
            db.session.add(review4)
            db.session.add(review5)
            db.session.add(transaction1)
            db.session.add(transaction2)
            db.session.add(transaction3)
            db.session.commit()
        access_token = jwt.encode({'email': user.email}, Configuration.SECRET_KEY)
        return { 'access_token': access_token.decode('UTF-8'), 'user': user.to_dict() }
    else:
        return {"error": "Incorrect password"}, 401



@bp.route("/all")
def get_all_products():
    fetchedProducts = Product.query.all()
    products = [product.to_dict() for product in fetchedProducts]
    return {"products": products}


@bp.route("/size")
def get_product_sizes():
    fetchedProductsizes = Productsize.query.all()
    productsizes = [productsizes.to_dict() for productsizes in fetchedProductsizes]
    return {"productsizes": productsizes}


@bp.route("/transactions", methods=["POST"])
def create_transaction():
    data = request.json
    try:
        transaction = Transaction(products=data["products"], user_id=data["userId"], total=data["total"])
        db.session.add(transaction)
        db.session.commit()
        return jsonify({"transaction": "transaction created"})
    except AssertionError as message:
        print(str(message))
        return jsonify({"error": str(message)}), 400


@bp.route("/transactions/<int:userId>")
def get_transaction(userId):
    fetchedTrans = Transaction.query.filter(Transaction.user_id == userId).all()
    transactions = [transaction.to_dict() for transaction in fetchedTrans] 
    return jsonify({"transactions": transactions})


@bp.route("/reviews/<int:productId>", methods=["POST"])
def create_reviews(productId):
    data = request.json
    try:
        review = Review(user_id=data["userId"], first_name=data["firstName"], last_name=data["lastName"], product_id=data["productId"], review_body=data["reviewBody"])
        db.session.add(review)
        db.session.commit()
        return jsonify({"review": review.to_dict()})
    except AssertionError as message:
        print(str(message))
        return jsonify({"error": str(message)}), 400


@bp.route("/reviews/<int:productId>")
def get_reviews(productId):
    fetchedReviews = Review.query.filter(Review.product_id == productId).all()
    reviews = [review.to_dict() for review in fetchedReviews]
    return {"reviews": reviews}