import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from posts import app
from .database import session
from .database import Post

post_schema = {
    "properties": {
        "title": {"type": "string"},
        "body": {"type": "string"}
    },
    "required": ["title", "body"]
}

@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """ Get a list of posts """
    title_like = request.args.get("title_like")
    body_like = request.args.get("body_like")

    posts = session.query(Post)
    if title_like:
        posts = posts.filter(Post.title.contains(title_like))
    elif body_like: 
        posts = posts.filter(Post.body.contains(body_like))
    elif title_like and body_like:
        posts.filter(Post.title.contains(title_like)).filter(Post.body.contains(body_like))
    else:
        posts = posts.order_by(Post.id)

    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/posts/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def post_get(id):
    """ Single post endpoint """
    post = session.query(Post).get(id)
     
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
        
    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")
    
@app.route("/api/posts/<int:id>", methods=["DELETE"])
@decorators.accept("application/json")
def post_delete(id):
    """ Delete a single post """
    post = session.query(Post).get(id)
    
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
        
    session.delete(post)
    session.commit()
    
    data = json.dumps([])
    return Response(data, 200, mimetype="application/json")
    
@app.route("/api/posts", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def posts_post():
    """Add a new post"""
    data = request.json
    
    try: 
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
    
    post = Post(title=data["title"], body=data["body"])
    session.add(post)
    session.commit()
    
    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers, mimetype="application/json")
    
@app.route("/api/post/<id>")
@decorators.accept("application/json")
@decorators.require("application/json")
def posts_edit(id):
    """Edit a post"""
    data = request.json
    
    try: 
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
        
    post = session.query(Post).get(id)
    post.title = data["title"]
    post.body = data["body"]
    
    session.commit()
    
    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers, mimetype="application/json")
    
    