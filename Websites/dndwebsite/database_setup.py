from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# Base class, which will derive other sqlalchemy classes
Base = declarative_base()

# Create tables

class Characters(Base):
    __tablename__ = 'characters'

    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)

    char_class = Column(String(15), nullable = False)
    char_race = Column(String(15), nullable = False)
    level = Column(Integer, nullable = False)
    maxhp = Column(Integer, nullable = False)
    armor_class = Column(Integer, nullable = False)
    initiative = Column(Integer, nullable = False)
    speed = Column(Integer, nullable = False)

    strength = Column(Integer, nullable = False)
    dexterity = Column(Integer, nullable = False)
    constitution = Column(Integer, nullable = False)
    intelligence = Column(Integer, nullable = False)
    wisdom = Column(Integer, nullable = False)
    charisma = Column(Integer, nullable = False)

    image_path = Column(String(200))

class Equipment(Base):
    __tablename__ = 'equipment'

    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))

    character_id = Column(Integer, ForeignKey('characters.id'))
    characters = relationship(Characters)

class Spells(Base):
    __tablename__ = 'spells'

    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)

    character_id = Column(Integer, ForeignKey('characters.id'))
    characters = relationship(Characters)

class Features(Base):
    __tablename__ = 'features'

    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))

    character_id = Column(Integer, ForeignKey('characters.id'))
    characters = relationship(Characters)

# Populate PostgresQL database with tables
# DB was created outside this script using psql through bash
if __name__ == '__main__':
    engine = create_engine('postgresql://roush:password@localhost/dnd')
    Base.metadata.create_all(engine)