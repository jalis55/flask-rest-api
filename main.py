from flask import Flask, jsonify, request
from sql_alchemy import SQLALCHEMY
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLALCHEMY(app)
ma = Marshmallow()


@app.route('/')
def home():
    return jsonify({"test": "test"})


if __name__ == "__main__":
    app.run(debug=True)
