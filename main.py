from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
ma = Marshmallow()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(100))
    author = db.Column(db.String(100))

    def __init__(self, title, description, author) -> None:
        self.title = title
        self.description = description
        self.author = author


class PostSchema(ma.Schema):
    class Meta:
        fields = ("title", "description", "author")


post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@app.route('/post', methods=['POST'])
def create_post():
    title = request.json("title")
    description = request.json("description")
    author = request.json("author")

    post = Post(title=title, description=description, author=author)
    db.session.add(post)
    db.commit()
    return post_schema.jsonify(post)


@app.route('/')
def home():
    return jsonify({"test": "test"})


if __name__ == "__main__":
    app.run(debug=True)
