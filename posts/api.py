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

    posts = session.query(Post)
    if title_like:
        posts = posts.filter(Post.title.contains(title_like))
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