
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = "passcode"
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        print(old_name, form.name.data)
        if old_name is not None and old_name != form.name.data:
            print(old_name, form.name.data)
            flash("Looks like you have changed your name!")
        session["name"] = form.name.data
        return redirect(url_for("index"))
    return render_template("index.html", form=form, name=session.get("name"))


@app.errorhandler(404)
def page_not_found():
    return render_template("404.html"), 404
