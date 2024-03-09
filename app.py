from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/RickAndMorty'

CORS(app)

db = SQLAlchemy(app)

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(80))
    status = db.Column(db.String(20))
    species = db.Column(db.String(50))
    type = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    origin_name = db.Column(db.String(50))
    location_name = db.Column(db.String(50))
    image_url = db.Column(db.String(100))
    
    def __init__(self, name, status, species, type, gender, origin_name, location_name, image_url):
        self.name = name
        self.status = status
        self.species = species
        self.type = type
        self.gender = gender
        self.origin_name = origin_name
        self.location_name = location_name
        self.image_url = image_url

# route to get all characters
@app.route('/')
def list_all_characters():
    page = int(request.args.get('page', 1))
    nameSearch = request.args.get('name', '')
    per_page = 20

    characters = Characters.query.filter(Characters.name.ilike(f'%{nameSearch}%')).paginate(page=page, per_page=per_page, error_out=False)

    character_list = [{
        'id': character.id,
        'name': character.name,
        'species': character.species,
        'origin': character.origin_name,
        'location': character.location_name,
        'image_url': character.image_url
    } for character in characters]

    total_pages = characters.pages

    if character_list:
        return jsonify({
            "success": True,
            "message": "Characters Found!",
            "data": {
                'character_list': character_list, 
                'total_pages': total_pages
            }
        })
    else:
        return jsonify({
            "success": False,
            "message": "No characters found."
        })
    

# route to get one character
@app.route('/<int:character_id>')
def detail_character(character_id):
    charater = Characters.query.get(character_id)
    character_dict = {
        'id': charater.id,
        'name': charater.name,
        'type': charater.type,
        'gender': charater.gender,
        'origin_name': charater.origin_name,
        'location_name': charater.location_name,
        'image_url': charater.image_url
    }
    return jsonify(character_dict)

if __name__ == '__main__':
    app.run(debug=True)