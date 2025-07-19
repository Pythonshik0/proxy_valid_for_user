from flask import request, jsonify
from db import init_db, insert_review, get_reviews
from sentiment import get_sentiment


def register_routes(app):
    @app.before_first_request
    def setup():
        init_db()

    @app.route('/reviews', methods=['POST'])
    def add_review():
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text'}), 400
        text = data['text']
        sentiment = get_sentiment(text)
        review = insert_review(text, sentiment)
        return jsonify(review), 201

    @app.route('/reviews', methods=['GET'])
    def get_reviews_route():
        sentiment = request.args.get('sentiment')
        reviews = get_reviews(sentiment)
        return jsonify(reviews) 