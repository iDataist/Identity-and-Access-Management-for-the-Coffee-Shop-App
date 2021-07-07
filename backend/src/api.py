from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import logging
from .database.models import *
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
db_drop_and_create_all()
CORS(app)
logging.basicConfig(filename='app.log',level=logging.DEBUG)

@app.route('/drinks')
def get_drinks():
    drinks = [drink.short() for drink in Drink.query.all()]
    if len(drinks) == 0:
        abort(404)
    try:
        return jsonify({
            'success': True,
            'drinks': drinks
            })
    except Exception as e:
        app.logger.error(e)
        abort(422)

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(self):
    drinks = [drink.long() for drink in Drink.query.all()]
    if len(drinks) == 0:
        abort(404)
    try:
        return jsonify({
            'success': True,
            'drinks': drinks
            })
    except Exception as e:
        app.logger.error(e)
        abort(422)

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(self):
    body = request.get_json()
    try:
        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)
        if (new_title is None) or (new_recipe is None):
            abort(404)
        drink = Drink(title=new_title,
                      recipe=new_recipe)
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
            })
    except Exception as e:
        app.logger.error(e)
        abort(422)

@app.route('/drinks/<int:drink_id>')
def get_specific_drink(drink_id):
    drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
    if drink is None:
        abort(404)
    try:
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        app.logger.error(e)
        abort(422)

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_specific_drink(self, drink_id):
    drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
    if drink is None:
        abort(404)
    try:
        body = request.get_json()
        if 'title' in body:
            drink.title = body.get('title')
        if 'recipe' in body:
            drink.recipe = body.get('recipe')
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        app.logger.error(e)
        abort(422)

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_specific_drink(self, drink_id):
    drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
    if drink is None:
        abort(404)
    try:
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink_id
            })
    except Exception as e:
        app.logger.error(e)
        abort(422)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
    "success": False, 
    "error": 404,
    "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response