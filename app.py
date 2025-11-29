from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        name = request.form['name']
        length = int(request.form['password'])
        characters = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choice(characters) for _ in range(length))
        new_user = user(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users_list'))
    return render_template("index.html")


@app.route("/users_list", methods=["GET", "POST"])
def users_list():
    all_users = user.query.all()
    return render_template('users.html', users=all_users)

if __name__ == "__main__":
    app.run(debug=True)