from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
app= Flask (__name__)

@app.route('/',methods=['GET'])
def home():
    return jsonify(
        {
            'name':'Dharanidharan S',
            'msg':'Welcome to page'
         })

basedir=os.path.abspath(os.path.dirname(__file__))
#print(basedir)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
ma = Marshmallow(app)
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    contact=db.Column(db.String(100),unique=True)
    def __init__(self,name,contact):
        self.name=name
        self.contact=contact
class userSchema(ma.Schema):
    class Meta:
        fileds=('id','name','contact')
user_Schema=userSchema()
users_Schema=userSchema(many=True)
# Create database
def create_tables():
    db.create_all()
#add new user
@app.route('/user',methods=['POST'])
def add_user():
    name=request.json['name']
    contact=request.json['contact']
    new_User=User(name,contact)
    db.session.add(new_User)
    db.session.commit()
    return user_Schema.jsonify(new_User)
#show all users
@app.route('/user',methods=['GET'])
def getAlluser():
    all_users=User.query.all()
    result=users_Schema.dump(all_users)
    return jsonify(result)
#show user by ID
@app.route('/user/<id>',methods=['GET'])
def getUserByid(id):
    user=User.query.get(id)
    return user_Schema.jsonify(user)
#update user by ID
@app.route('/user/<id>',methods=['PUT'])
def updateUser(id):
    user=User.query.get(id)
    name=request.json['name']
    contact=request.json['contact']
    user.name=name
    user.contact=contact
    db.session.commit()
    return user_Schema.jsonify(user)
#delete user by ID
@app.route('/user/<id>',methods=['DELETE'])
def DeleteuserByid(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_Schema.jsonify(user)






if __name__=='__main__':
    app.run(debug=True,port=5000)