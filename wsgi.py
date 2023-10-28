
import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config["SECRET_KEY"] = "passcode"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)


class UserType(db.Model):
    __tablename__ = "user_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return f"<Role {self.name} >"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("user_type.id"))

    def __repr__(self):
        return f"<User {self.username}>"


class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        form_name = form.name.data
        user = User.query.filter_by(username=form_name).first()
        if user is None:
            user = User(username=form_name)
            db.session.add(user)
            db.session.commit()
        else:
            session["known"] = True
        session["name"] = form_name
        form.name.data = ""        
        return redirect(url_for("index"))
    return render_template(
        "index.html", 
        form=form, 
        name=session.get("name"), 
        known=session.get("known", False)
    )


@app.errorhandler(404)
def page_not_found():
    return render_template("404.html"), 404
