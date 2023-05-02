"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite_users, People, Favorite_people, Planets, Favorite_planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_user():
  
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(
        all_users
    ), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_user1(user_id):
  
    users = User.query.get(user_id)
    if users is None:
        raise APIException('User not found', status_code=404)

    return jsonify(
        users.serialize()
    ), 200

@app.route('/user', methods=['POST'])
def handle_user2():
    if request.method =='POST':
        data = request.json
        
        new_user = User()

        new_user.email = request.json.get('email')
        new_user.password = request.json.get('password')
        new_user.is_active = True

        new_user.save()

        return jsonify(new_user.serialize()), 201

@app.route('/favorite_users', methods=['GET'])
def handle_favorite_users():

    favorite_users= Favorite_planets.query.all()
    favorite_users = list(map(lambda Favorite_users: Favorite_users.serialize(), favorite_users))
    return jsonify(
        favorite_users
    ), 200

@app.route('/people', methods=['GET'])
def handle_people():

    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))
    return jsonify(
        all_people
    ), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_people1(people_id):

    people = People.query.get(people_id)
    if people is None:
        raise APIException('People not found', status_code=404)

    return jsonify({
        "people": people.serialize()
    }), 200

@app.route('/people', methods=['POST'])
def handle_people2():
    if request.method =='POST':
        
        people = People()
        people.name = request.json.get('name')
        people.gender = request.json.get('gender')
        
        people.save()

        return jsonify(people.serialize()), 201

@app.route('/favorite_people', methods=['GET'])
def handle_favorite_people():

    favorite_people = Favorite_people.query.all()
    favorite_people = list(map(lambda Favorite_people: Favorite_people.serialize(), favorite_people))
    return jsonify(
        favorite_people
    ), 200

@app.route('/favorite/people/', methods=['POST'])
def handle_favorite_people1():

    favorite = Favorite_people()
    favorite.users_id = request.json.get('users_id')
    favorite.people_id = request.json.get('people_id')
    favorite.save()
    return jsonify(
        favorite.serialize()
    ), 201

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def handle_favorite_people2(people_id):

    favorite = Favorite_people.query.get(people_id)
    favorite.delete()
    return jsonify(
        favorite.serialize()
    ), 201

@app.route('/planets', methods=['GET'])
def handle_planets():

    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(
        all_planets
    ), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def handle_planets1(planets_id):

    planets = Planets.query.get(planets_id)
    if planets is None:
        raise APIException('Planets not found', status_code=404)

    return jsonify({
        "planets": planets.serialize()
    }), 200

@app.route('/planets', methods=['POST'])
def handle_planets2():
    if request.method =='POST':
        
        planets = Planets()
        planets.name = request.json.get('name')
        planets.climate = request.json.get('climate')
        
        planets.save()

        return jsonify(planets.serialize()), 201

@app.route('/favorite_planets', methods=['GET'])
def handle_favorite_planets():

    favorite_planets = Favorite_planets.query.all()
    favorite_planets = list(map(lambda Favorite_planets: Favorite_planets.serialize(), favorite_planets))
    return jsonify(
        favorite_planets
    ), 200

@app.route('/favorite/planets/', methods=['POST'])
def handle_favorite_planets1():

    favorite = Favorite_planets()
    favorite.users_id = request.json.get('users_id')
    favorite.planets_id = request.json.get('planets_id')
    favorite.save()
    return jsonify(
        favorite.serialize()
    ), 201

@app.route('/favorite/planets/<int:planets_id>', methods=['DELETE'])
def handle_favorite_planets2(planets_id):

    favorite = Favorite_planets.query.get(planets_id)
    print (favorite)
    favorite.delete()
    return jsonify(
        favorite.serialize()
    ), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
