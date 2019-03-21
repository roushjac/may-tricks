from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Characters, Equipment, Spells, Features

app = Flask(__name__)

engine = create_engine('postgresql://roush:password@localhost/dnd')
Base.metadata.bind = engine

@app.route('/') # Homepage
def homepage():
    session = sessionmaker(bind=engine)()
    all_characters = session.query(Characters).all()
    return render_template('homepage.html', characters = all_characters)

@app.route('/add_adventurer', methods = ['GET', 'POST'])
def add_adventurer():
    if request.method == 'POST':
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
                                    charisma = request.form['char_charisma'])
        session.add(new_character)
        session.commit()
        return redirect(url_for('homepage'))
    else:
        return render_template('add_adventurer.html')
    



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)