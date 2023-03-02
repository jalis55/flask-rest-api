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
def post():

    title = request.json['title']
    description = request.json['description']
    author = request.json['author']

    post = Post(title=title, description=description, author=author)
    db.session.add(post)
    db.session.commit()
    return post_schema.jsonify(post)


@app.route('/all-posts')
def all_posts():
    posts = Post.query.all()
    return posts_schema.jsonify(posts)


@app.route('/update-post/<int:id>', methods=["PUT"])
def update_post(id):
    post = Post.query.get(id)
    post.title = request.json['title']
    post.description = request.json['description']
    post.author = request.json['author']

    db.session.commit()
    return post_schema.jsonify(post)


@app.route('/delete-post/<int:id>', methods=["DELETE"])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return post_schema.jsonify(post)


@app.route('/post/<int:id>')
def home(id):
    post = Post.query.get(id)
    return post_schema.jsonify(post)
    # return jsonify({"test": "test"})


if __name__ == "__main__":
    app.run(debug=True)
