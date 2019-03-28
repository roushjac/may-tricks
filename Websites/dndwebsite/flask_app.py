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

@app.route('/add_adventurer', methods = ['GET', 'POST'])
def add_adventurer():
    if request.method == 'POST':
        file = request.files['char_photo']
        file_name = secure_filename(file.filename)
        basedir = os.path.abspath(app.config['UPLOAD_FOLDER']) # returns abs path of the flask app for the system it's being run on
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

@app.route('/test')
def test():
    return """
    <img src='/static/character_pics/mambo_car.jpg'>
    """
    



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)