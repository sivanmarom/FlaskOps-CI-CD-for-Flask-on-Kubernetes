from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
my_users = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registered.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)

    def __str__(self):
        return f"Username: {self.user_name}, password:{self.password}"


@app.route('/signup', methods=['POST', 'GET'])
def Signup():
    if request.method == 'POST':
        user_name = request.form.get("username")
        password = request.form.get("password")
        my_users.append(user_name)
        p = Profile(user_name=user_name, password=password)
        db.session.add(p)
        db.session.commit()
        return redirect("/registered")
    return render_template("signup.html")


@app.route('/')
def homepage():
    return render_template("homepage.html")


@app.route('/registered')
def registered():
    return render_template("hello_user.html", my_users=my_users)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
