import secrets
from flask import render_template, request, redirect, flash, session
from app import app
from services import users, adventures, reviews, favorites, preferences
import initialize_database
import json

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
            flash("Wrong username or password")
            return redirect("/login")
        return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        error_message = users.validate_registration(username, password1, password2)

        if error_message:
            flash(error_message)
            return redirect("/register")

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
        if not users.user_id():
            return redirect("/")

        serialized_adventures = adventures.get_created_adventures()

        if serialized_adventures and session.get("form_submitted"):
            deserialized_adventures = json.loads(serialized_adventures)

            adventures_with_reviews = []
            for adventure in deserialized_adventures:
                adventure["reviews"] = reviews.get_reviews(adventure["id"])
                adventures_with_reviews.append(adventure)

            return render_template("home.html", preferences_submitted=True,
                                   adventures=adventures_with_reviews)

        return render_template("home.html")

    if request.method == "POST":
        session["form_submitted"] = True
        users.check_csrf()
        user_id = users.user_id()

        user_preferences = {
            "duration": request.form["duration"],
            "budget": request.form["budget"],
            "difficulty": request.form["difficulty"],
            "environment": request.form["environment"],
            "group_size": request.form["group_size"],
            "season": request.form["season"]
        }

        preferences.create_preferences(user_id, user_preferences)

        adventures.create_adventures(user_id)

        return redirect("/home")

@app.route("/review", methods=["post"])
def add_review():
    if request.method == "POST":
        users.check_csrf()
        user_id = users.user_id()
        adventure_id = request.form["adventure_id"]
        stars = request.form["stars"]
        comment = request.form["comment"]

    reviews.add_review(user_id, adventure_id, stars, comment)

    return redirect(request.referrer or "/home")

@app.route("/get_favorites", methods=["get"])
def get_favorites():
    if request.method == "GET":
        if not users.user_id():
            return redirect("/")
        user_id = users.user_id()
        favorite_adventures = favorites.get_favorites(user_id)

        adventures_with_reviews = []
        for adventure in favorite_adventures:
            adventure["reviews"] = reviews.get_reviews(adventure["id"])
            adventures_with_reviews.append(adventure)

        return render_template("favorites.html", favorite_adventures = adventures_with_reviews)

@app.route("/add_to_favorites", methods=["post"])
def add_to_favorites():
    if request.method == "POST":
        users.check_csrf()
        user_id = users.user_id()
        adventure_id = request.form["adventure_id"]

    added_to_favorites = favorites.add_to_favorites(user_id, adventure_id)

    if added_to_favorites:
        flash("Adventure added to favorites")
    else:
        flash("Adventure already in favorites")

    return redirect("/home")

@app.route("/delete_from_favorites", methods=["post"])
def delete_from_favorites():
    if request.method == "POST":
        users.check_csrf()
        user_id = users.user_id()
        adventure_id = request.form["adventure_id"]

        favorites.delete_from_favorites(user_id, adventure_id)

        flash("Adventure deleted from favorites")

        return redirect("/get_favorites")
