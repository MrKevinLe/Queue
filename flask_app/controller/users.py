from flask_app import app
from flask import Flask, render_template, redirect, request, session
from flask_app.models.event_model import Event
from flask_app.models.user_model import User
from flask_app.models.attendace import Attendance
from flask_app.models.attendace_has_event import Attendance_has_event
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Start Python project !!
# pip install pipenv
# pipenv install flask PyMySQL
# pipenv shell
# pipenv install flask-bcrypt
# python server.py

# login and register page

@app.route("/")
def homepage2():
    data = {
        "id": session
    }
    all_events = Event.get_all(data)
    all_attend = Attendance.get_all(data)
    print()
    return render_template("homepage2.html",all_events=all_events,all_attend=all_attend)
@app.route('/login')

def frontPage():

    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/login')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "phone_number": request.form['phone_number'],
        "about": request.form['about'],
        "age": request.form['age'],
        "gamer_tag":request.form['gamer_tag'],
        "password": pw_hash,
    }
    # print(pw_hash)
    user = User.save(data)
    session['user'] = user
    return redirect('/homepage')

@app.route("/homepage")
def homepage():
    if "user" not in session:
        return redirect('/')
    data = {
        "ids": session['user']
    }
    logged_in = User.get_by_id(data)
    all_events = Event.get_all(data)
    all_attend = Attendance.get_all(data)
    all_users = User.get_all(data)
    print()
    return render_template("homepage.html",logged_in=logged_in,all_events=all_events,all_attend=all_attend,all_users=all_users)

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/login')
    data = {"email": request.form["email"]}
    user = User.get_by_email(data)
    if not user:
        flash("Invalid Email/Password", "login")
        return redirect("/login")

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/homepage')
    session['user'] = user.id
    return redirect('/homepage')
    
@app.route('/submit', methods=['POST'])
def submit_event():
    if not Event.validate_event(request.form):
        return redirect('/homepage')
    data = {
        'title':request.form ['title'],
        'location':request.form['location'],
        'activity' :request.form['activity'],
        'image_url':request.form['image_url'],
        'user_id': session ['user']
    }
    Event.save_event(data)
    return redirect('/homepage')

@app.route('/view/<int:id>')
def view(id):
    data ={
        'id': id,
        "ids": session['user']
    }
    single_e = Event.get_both_by_event_id(data)
    all_attend = Attendance.get_all(data)
    logged_in = User.get_by_id(data)
    manytomany = Attendance_has_event.get_by_id(data)
    # print(manytomany)
    # print(single_e)
    # print(all_attend)

    return render_template ('view.html', single_e=single_e,all_attend=all_attend,logged_in=logged_in, manytomany=manytomany)

@app.route('/view2/<int:id>')
def view2(id):
    data ={
        'id': id,
        "ids": session
    }
    single_e = Event.get_both_by_event_id(data)
    all_attend = Attendance.get_all(data)
    logged_in = User.get_by_id(data)
    manytomany = Attendance_has_event.get_by_id(data)
    # print(manytomany)
    # print(single_e)
    # print(all_attend)

    return render_template ('view2.html', single_e=single_e,all_attend=all_attend,manytomany=manytomany)

@app.route('/submit_attend', methods=['POST'])
def submit_attend():
    data = {
        'name':request.form ['name'],
    }   
    Attendance.save_attend(data)
    return redirect('/homepage')

@app.route('/delete_attend/<int:id>')
def delete(id):
    data = {
        "id" : id
    }
    Attendance.delete(data)
    return redirect('/homepage')

@app.route('/submit_players', methods=['POST'])
def submit_players():
    data = {
        'event_id':request.form ['event_id'],
        'attendance_id':request.form ['attendance_id'],    }
    Attendance_has_event.save_manytomany(data)
    return redirect("/homepage")

@app.route('/delete_many/<int:id>/<int:ids>')
def delete_many(id , ids):
    data = {
        "id" : id,
        "ids" : ids
    }
    Attendance_has_event.delete_many(data)
    return redirect("/homepage")

@app.route('/delete_event/<int:id>')
def delete_event(id):
    data = {
        "id" : id
    }
    Event.delete(data)
    return redirect("/homepage")

@app.route('/create')
def create():
    if "user" not in session:
        return redirect('/')
    data = {
        "ids": session['user']
    }
    logged_in = User.get_by_id(data)

    return render_template("create.html", logged_in=logged_in)

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect('/')
    data = {
        "ids": session['user']
    }
    manytomany = Attendance_has_event.get_all(data)
    logged_in = User.get_by_id(data)
    all_events = Event.get_all(data)
    all_attend = Attendance.get_all(data)
    return render_template("profile.html", logged_in=logged_in, manytomany=manytomany,all_events=all_events,all_attend=all_attend)

@app.route("/profile2/<int:id>")
def profile_view(id):
    data = {
        "ids" : id,

    }
    manytomany = Attendance_has_event.get_all(data)
    all_events = Event.get_all(data)
    all_attend = Attendance.get_all(data)

    logged_in = User.get_by_id(data)
    return render_template("profile2.html",logged_in=logged_in, manytomany=manytomany,all_events=all_events,all_attend=all_attend)

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/homepage')