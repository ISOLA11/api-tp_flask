import random

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.testing import db
from datetime import datetime
from faker import Faker


fake=Faker()
app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://root:root@localhost:5432/store"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)

@app.route("/user")
def get_user() :
    result=User.query.all()
    users = []
    for row in result :
        user = {
            "id" : row.ID,
            "firstname" : row.firstname,
            "lastname" : row.lastname,
            "age" : row.age,
            "email" : row.email,
            "job" : row.job
        }
        users.append(user)
    return jsonify(users)

class User (db.Model):
    ID = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer())
    email=db.Column(db.String(200))
    job=db.Column(db.String(100))
    application=db.relationship('Application')

    def __init__(self, firstname, lastname, age, email, job):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.email = email
        self.job = job

class Application (db.Model) :
    ID = db.Column(db.Integer, primary_key = True)
    appname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    lastconnection = db.Column(db.TIMESTAMP(timezone=True))
    user_id=db.Column(db.Integer, db.ForeignKey('user.ID'))

    def __init__(self,appname, username, lastconnection):
        self.appname = appname
        self.username = username
        self.lastconnection = lastconnection

def populate_tables() :
    application=["Facebook","Instagram","Twitter","Airbnb","TikTok","Linkedin"]
    for n in range(100) :
        firstname=fake.first_name()
        lastname=fake.last_name()
        age=random.randrange(18,50)
        email=fake.email()
        job=fake.job()
        user = User(firstname,lastname,age,email,job)
        apps_names = [random.choice(application) for n in range(1,random.randrange(1,5))]
        for app_name in  apps_names :
            username=fake.user_name()
            lastconnection=datetime.now()
            new_app= Application(app_name,username,lastconnection)
            user.application.append(new_app)

        with app.app_context():
            db.session.add(user)
            db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

    populate_tables()
    app.run(host="0.0.0.0", port=8081, debug=True)




