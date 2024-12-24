import cloudinary
from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@127.0.0.1:3306/benhvientu?charset=utf8mb4" % quote('minhtri123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "mInHtRiBnGuYeNTnGuYeN"
app.config["PAGE_SIZE_THUOC"] = 10

db = SQLAlchemy(app)
login = LoginManager(app)

cloudinary.config(
    cloud_name = "dwivkhh8t",
    api_key = "925656835271691",
    api_secret = "xggQhqIzVzwLbOJx05apmM4Od7U",
    secure=True
)