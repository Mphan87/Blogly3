"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, Blogly, Post, PostTag, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)
db.create_all()

@app.route('/')
def index():
    """This is just the form"""
    return redirect("/users/new")

@app.route("/users/new", methods=["GET"])
def newform():
    return render_template("new.html")

@app.route("/users/new", methods=["POST"])
def getusers():
    # this adds the new user into the database
    new_user = Blogly(
        first_name=request.form["first"],
        last_name=request.form["last"],
        image_url=request.form["image"])

    # this will commit and add it to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route("/users", methods=["GET"])
def list():
    blogly = Blogly.query.all()
    """shows list of all names in db"""
    return render_template("users.html", blogly=blogly)

@app.route("/users/<int:blogly_id>")
def details(blogly_id):
    fname = Blogly.query.get(blogly_id).first_name
    lname = Blogly.query.get(blogly_id).last_name
    imgsrc = Blogly.query.get(blogly_id).image_url
    post = Post.query.filter(Post.blogly_id == blogly_id).all()
    return render_template("details.html", blogly_id=blogly_id, fname=fname, lname=lname, imgsrc=imgsrc, post=post)

@app.route('/users/<int:blogly_id>/edit', methods=["GET"])
def users_edit(blogly_id):
    """Show a form to edit an existing user"""

    user = Blogly.query.get_or_404(blogly_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:blogly_id>/edit', methods=["POST"])
def users_update(blogly_id):
    """Handle form submission for updating an existing user"""
    user = Blogly.query.get_or_404(blogly_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['image']
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{blogly_id}")

@app.route('/users/<int:blogly_id>/delete', methods=["POST"])
def users_destroy(blogly_id):
    """Handle form submission for deleting an existing user"""
    user = Blogly.query.get_or_404(blogly_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:blogly_id>/posts/new', methods=["GET"])
def show_postform(blogly_id):
    tags = Tag.query.all()
    return render_template("postform.html", tags = tags)

@app.route('/users/<int:blogly_id>/posts/new', methods=["POST"])
def newpost(blogly_id):  
    new_post = Post(
        title=request.form["title"],
        content=request.form["content"],
        blogly_id=blogly_id)
    db.session.add(new_post)
    db.session.commit()

    new_posttage = PostTag(
        post_id = new_post.id,
        tag_id = request.form["tags"])
    db.session.add(new_posttage)
    db.session.commit()
    return redirect(f"/users/{blogly_id}")

@app.route('/post/<int:post_id>/edit', methods=["GET"])
def show_postedit(post_id):
    return render_template("postedit.html", post_id=post_id)

@app.route('/post/<int:post_id>/edit', methods=["POST"])
def postedit(post_id):
    edit = Post.query.get_or_404(post_id)
    blogly_id = edit.blogly_id
    edit.title = request.form['title']
    edit.content = request.form['content']
    db.session.add(edit)
    db.session.commit()
    return redirect(f"/users/{blogly_id}")

@app.route('/post/<post_id>/delete', methods=["POST"])
def postdelete(post_id):
    post = Post.query.get_or_404(post_id)
    blogly_id = post.blogly_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{blogly_id}")

@app.route('/tags/new', methods=["GET"])
def show_tagform():
    return render_template("tagform.html")

@app.route('/tags/new', methods=["POST"])
def newtag():
    new_post = Tag(
        name=request.form["name"])
    db.session.add(new_post)
    db.session.commit()
    return redirect("/tags")

@app.route('/tags', methods=["GET"])
def show_taglist():
    tags = Tag.query.all()

    return render_template("taglist.html", tags=tags)

@app.route('/tags/<int:tag_id>', methods=["GET"])
def tag_details(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template("tagdetails.html", posts = posts, tag = tag)


