import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from posts import app
from .database import session
from .database import Post

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
        posts = posts.filter(Post.title.contains(body_like))
    elif title_like and body_like:
        posts.filter(Post.title.contains(title_like)).filter(Post.title.contains(body_like))
    else:
        posts = posts.order_by(Post.id)

    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/posts/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def post_get():
    """ Single post endpoint """
    post = session.query(Post).get(id)
     
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
        
    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")
    
@app.route("/api/posts/<int:id>", methods=["DELETE"])
def post_delete():
    """ Delete a single post """
    post = session.query(Post).get(id)
    
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    
    data = json.dumps([])
    return Response(data, 200, mimetype="application/json")