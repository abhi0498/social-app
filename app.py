from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
uid = ''
app = Flask(__name__)
# app.config['MONGO_URI']='mongodb://localhost:27017/social'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social.db'

db = SQLAlchemy(app)


class User(db.Model):
    uid = db.Column(db.String(20), primary_key=True)

    passw = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.uid


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usid = request.form['UserId']
        passw = request.form['Password']

        new_user = User.query.get(usid)

        print(usid)
        print(passw)
        print(new_user.uid)
        print(new_user.passw)

        if new_user.uid == usid and new_user.passw == passw:
            global uid
            uid = new_user.uid
            return redirect('/home')
        else:
            return "Wrong password or userid"
    else:
        return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        uid = request.form['UserId']
        passw = request.form['Password']
        cpassw = request.form['CPassword']

        check_id = User.query.get(uid)
        if check_id:
            if check_id.uid == uid:
                return render_template("signup.html", match=True)

        try:
            user = User(uid=uid, passw=passw)
            db.session.add(user)
            db.session.commit()
            return 'Signed Up'
        except:
            return 'Signup error'

    else:
        return render_template('signup.html')


@app.route('/home')
def home():
    return render_template('home.html', uid=uid)


@app.route('/logout')
def logout():
    global uid
    uid = ''
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
