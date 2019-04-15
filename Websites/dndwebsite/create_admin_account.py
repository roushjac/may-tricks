from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import bcrypt
from database_setup import Users

# Only running this script once - creating general admin account that 
# allows access to any interactive features like character creation, editing, or deletion

engine = create_engine('postgresql://roush:password@localhost/dnd')
session = sessionmaker(bind = engine)()

new_account = Users(username = 'admin', password = bcrypt.generate_password_hash('password').decode('utf-8'))

session.add(new_account)
session.commit()