import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from root.create_app import app

load_dotenv(".env")

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB = os.getenv("DB")
AUTH = os.getenv("AUTH")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}?sslmode=disable"
db = SQLAlchemy(app)