# db_create.py


from rounds import db

db.create_all()

db.session.commit()