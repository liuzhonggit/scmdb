from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Pass123!@localhost/python'
db = SQLAlchemy(app)
from main import views
