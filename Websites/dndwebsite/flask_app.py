from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Characters, Equipment, Spells, Features
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/character_pics'

engine = create_engine('postgresql://roush:password@localhost/dnd')
Base.metadata.bind = engine

@app.route('/') # Homepage
def homepage():
    return render_template('homepage.html')

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
    if request.method == 'GET':
        return render_template('one_char.html', character = this_char)
    if request.method == 'POST':
        print(os.getcwd())
        os.remove(os.path.join(os.getcwd(), url_for('static', filename=this_char.image_path)))
        session.delete(this_char)
        session.commit()
        return redirect(url_for('characters'))

@app.route('/characters/<char_name>/edit', methods=['POST', 'GET'])
def edit_character(char_name):
    session = sessionmaker(bind=engine)()
    this_char = session.query(Characters).filter_by(name = char_name).one()
    if request.method == 'POST':
        this_char.char_class = request.form['new_class']
        this_char.char_race = request.form['new_race']
        this_char.level = request.form['new_level']
        this_char.maxhp = request.form['new_hp']
        this_char.strength = request.form['new_strength']
        this_char.dexterity = request.form['new_dexterity']
        this_char.constitution = request.form['new_constitution']
        this_char.intelligence = request.form['new_intelligence']
        this_char.wisdom = request.form['new_wisdom']
        this_char.charisma = request.form['new_charisma']
        session.commit()
        return redirect(url_for('character_page', char_name = char_name))
    if request.method == 'GET':
        return render_template('edit_char.html', character = this_char)




@app.route('/add_adventurer', methods = ['GET', 'POST'])
def add_adventurer():
    if request.method == 'POST':
        file = request.files['char_photo']
        file_name = secure_filename(file.filename)
        # return abs path of the flask app for the system it's being run on
        basedir = os.path.abspath(app.config['UPLOAD_FOLDER'])
        abs_file_path = os.path.join(basedir, file_name)
        file.save(abs_file_path)

        session = sessionmaker(bind = engine)()
        new_character = Characters(name = request.form['char_name'], 
                                    char_class = request.form['char_class'],
                                    char_race = request.form['char_race'],
                                    level = request.form['char_level'],
                                    maxhp = request.form['char_maxhp'],
                                    strength = request.form['char_strength'],
                                    dexterity = request.form['char_dexterity'],
                                    constitution = request.form['char_constitution'],
                                    intelligence = request.form['char_intelligence'],
                                    wisdom = request.form['char_wisdom'],
                                    charisma = request.form['char_charisma'],
                                    image_path = 'character_pics/' + file_name) # don't want to use os.join because windows filepaths are dumb
        session.add(new_character)
        session.commit()
        return redirect(url_for('characters'))
    else:
        return render_template('add_adventurer.html')
    


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)