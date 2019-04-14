from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Characters, Equipment, Spells, Features
from werkzeug.utils import secure_filename
from forms import LoginForm
import os

""" TODO
- Modify CSS for all pages to make them responsive/mobile friendly
- Add styling to:
    - Character creation
    - Character editing
- Add login feature
    - Will only have an admin account for now
    - Give admin login info to IRL party members
    - Admin can create/modify/delete any character
- Editing a description of an item, spell, or feature will not update it - fix
"""

app = Flask(__name__)
# Only thing this website uploads is character pics so this is fine
app.config['UPLOAD_FOLDER'] = 'static\\character_pics'
app.secret_key = b'J\xba\xd9\x8e\x0f\x9f\x99\xc9\x13\xc8\x80Ums*\x14'

engine = create_engine('postgresql://roush:password@localhost/dnd')
Base.metadata.bind = engine

@app.route('/') # Homepage
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'password':
            flash('Successfully logged in')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid login')
    return render_template('login.html', form=form)

@app.route('/characters')
def characters():
    session = sessionmaker(bind=engine)()
    all_characters = session.query(Characters).all()
    return render_template('characters.html', characters = all_characters)

@app.route('/characters/<char_name>', methods = ['POST', 'GET'])
def character_page(char_name):
    session = sessionmaker(bind=engine)()
    # filtering by name - maybe change to ID in future?
    this_char = session.query(Characters).filter_by(name = char_name).one()
    this_char_equipment = session.query(Equipment).filter_by(character_id = this_char.id)
    this_char_spells = session.query(Spells).filter_by(character_id = this_char.id)
    this_char_features = session.query(Features).filter_by(character_id = this_char.id)
    if request.method == 'GET':
        return render_template('one_char.html', character = this_char,
                                                all_equipment = this_char_equipment,
                                                all_spells = this_char_spells,
                                                all_features = this_char_features)
    if request.method == 'POST':
        if this_char.image_path:
            os.remove(os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), this_char.image_path))
        session.delete(this_char)
        session.commit()
        return redirect(url_for('characters'))

@app.route('/characters/<char_name>/edit', methods=['POST', 'GET'])
def edit_character(char_name):
    session = sessionmaker(bind=engine)()
    this_char = session.query(Characters).filter_by(name = char_name).one()
    this_char_equipment = session.query(Equipment).filter_by(character_id = this_char.id)
    this_char_spells = session.query(Spells).filter_by(character_id = this_char.id)
    this_char_features = session.query(Features).filter_by(character_id = this_char.id)
    if request.method == 'POST':
        this_char.level = request.form['new_level']
        this_char.maxhp = request.form['new_hp']
        this_char.strength = request.form['new_strength']
        this_char.dexterity = request.form['new_dexterity']
        this_char.constitution = request.form['new_constitution']
        this_char.intelligence = request.form['new_intelligence']
        this_char.wisdom = request.form['new_wisdom']
        this_char.charisma = request.form['new_charisma']
        # For equipment, spells, and features:
        ### Update equipment
        # If there's an item in the DB that's not in the request, delete it from the DB
        items_from_db = [(item.name, item.id) for item in session.query(Equipment).filter_by(character_id = this_char.id)]
        deleted_items = [item for item in items_from_db if item[0] not in request.form.getlist('item_name')]
        if len(deleted_items) > 0:
            for item in deleted_items:
                deleted_item = session.query(Equipment).filter_by(id = item[1]).one()
                session.delete(deleted_item)
        # Then, if there's an item in the request not in the DB, add it to the DB
        items_with_desc = zip(request.form.getlist('item_name'), request.form.getlist('item_desc'))
        for name,desc in items_with_desc:
            if name not in [item[0] for item in items_from_db]: # Looks through names already in DB
                new_item = Equipment(name = name,
                                        description = desc,
                                        character_id = this_char.id)
                session.add(new_item)
        ### Update spells
        spells_from_db = [(item.name, item.id) for item in session.query(Spells).filter_by(character_id = this_char.id)]
        deleted_spells = [item for item in spells_from_db if item[0] not in request.form.getlist('spell_name')]
        if len(deleted_spells) > 0:
            for spell in deleted_spells:
                deleted_spell = session.query(Spells).filter_by(id = spell[1]).one()
                session.delete(deleted_spell)
        # If there's a spell in the request not in the DB, add it to the DB
        for name in request.form.getlist('spell_name'):
            if name not in [item[0] for item in spells_from_db]: # Looks through names already in DB
                new_spell = Spells(name = name,
                                    character_id = this_char.id)
                session.add(new_spell)
        ### Update features
        # If there's a feature in the DB that's not in the request, delete it from the DB
        features_from_db = [(item.name, item.id) for item in session.query(Features).filter_by(character_id = this_char.id)]
        deleted_features = [item for item in features_from_db if item[0] not in request.form.getlist('feature_name')]
        if len(deleted_features) > 0:
            for item in deleted_features:
                deleted_feature = session.query(Features).filter_by(id = item[1]).one()
                session.delete(deleted_feature)
        # Then, if there's a feature in the request not in the DB, add it to the DB
        features_with_desc = zip(request.form.getlist('feature_name'), request.form.getlist('feature_desc'))
        for name,desc in features_with_desc:
            if name not in [item[0] for item in features_from_db]: # Looks through names already in DB
                new_feature = Features(name = name,
                                        description = desc,
                                        character_id = this_char.id)
                session.add(new_feature)

        session.commit()
        return redirect(url_for('character_page', char_name = char_name))
    if request.method == 'GET':
        return render_template('edit_char.html', character = this_char,
                                                all_equipment = this_char_equipment,
                                                all_spells = this_char_spells,
                                                all_features = this_char_features)




@app.route('/add_adventurer', methods = ['GET', 'POST'])
def add_adventurer():
    if request.method == 'POST':
        if request.files['char_photo']: # evaluates to true if a file has been uploaded
            file = request.files['char_photo']
            file_name = secure_filename(file.filename)
            # return abs path of the flask app for the system it's being run on
            # could also use app.instance_path?
            basedir = os.path.abspath(app.config['UPLOAD_FOLDER'])
            abs_file_path = os.path.join(basedir, file_name)
            file.save(abs_file_path)
        else: # filename will evaluate to false when checking if filepath is there in template
            file_name = ''

        session = sessionmaker(bind = engine)()
        new_character = Characters(name = request.form['char_name'], 
                                    char_class = request.form['char_class'],
                                    char_race = request.form['char_race'],
                                    level = request.form['char_level'],
                                    maxhp = request.form['char_maxhp'],
                                    armor_class = request.form['char_ac'],
                                    initiative = request.form['char_initiative'],
                                    speed = request.form['char_speed'],
                                    strength = request.form['char_strength'],
                                    dexterity = request.form['char_dexterity'],
                                    constitution = request.form['char_constitution'],
                                    intelligence = request.form['char_intelligence'],
                                    wisdom = request.form['char_wisdom'],
                                    charisma = request.form['char_charisma'],
                                    image_path = file_name)
        session.add(new_character)
        session.flush() # Pushes new character to database temporarily so it can be queried below

        # Add items, if any were submitted
        if len(request.form.getlist('item_name')) > 0: # if any items have been submitted
            items_with_desc = zip(request.form.getlist('item_name'), request.form.getlist('item_desc'))
            for name,desc in items_with_desc: # Add items with desc and character ID
                new_item = Equipment(name = name,
                                        description = desc,
                                        character_id = new_character.id)
                session.add(new_item)
        # Add spells, if any were submitted
        if len(request.form.getlist('spell_name')) > 0:
            spells = request.form.getlist('spell_name')
            for name in spells:
                new_spell = Spells(name = name,
                                    character_id = new_character.id)
                session.add(new_spell)
        # Add features, if any were submitted
        if len(request.form.getlist('feature_name')) > 0:
            features_with_desc = zip(request.form.getlist('feature_name'), request.form.getlist('feature_desc'))
            for name,desc in features_with_desc:
                new_feature = Features(name = name,
                                        description = desc,
                                        character_id = new_character.id)
                session.add(new_feature)

        session.commit()
        return redirect(url_for('characters'))
    else:
        return render_template('add_adventurer.html')
    


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)