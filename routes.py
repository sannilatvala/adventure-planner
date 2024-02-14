import secrets
from flask import render_template, request, redirect, session, abort
from app import app
from services import users, adventures, reviews
import initialize_database

@app.route("/")
def index():
    initialize_database.add_adventures_to_db()
    return render_template("index.html")

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Wrong username or password")
        return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("error.html", message="Passwords differ")

        registration_successful = users.register(username, password1)

        if registration_successful:
            return redirect("/")

        return render_template("error.html", message="Registration failed")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/home", methods=["get", "post"])
def home():
    if request.method == "GET":
        return render_template("home.html")

    if request.method == "POST":

        user_preferences = {
            "duration": request.form["duration"],
            "budget": request.form["budget"],
            "difficulty": request.form["difficulty"],
            "environment": request.form["environment"],
            "group_size": request.form["group_size"],
            "season": request.form["season"]
        }

        created_adventures = adventures.create_adventures(user_preferences)

        adventures_with_reviews = []
        for adventure in created_adventures:
            adventure["reviews"] = reviews.get_reviews(adventure["id"])
            adventures_with_reviews.append(adventure)

        return render_template(
            "home.html", preferences_submitted=True, adventures=adventures_with_reviews)

@app.route("/review", methods=["post"])
def add_review():
    if request.method == "POST":
        user_id = users.user_id()
        adventure_id = request.form["adventure_id"]
        stars = request.form["stars"]
        comment = request.form["comment"]

    reviews.add_review(user_id, adventure_id, stars, comment)

    return render_template("home.html")
