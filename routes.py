import secrets
from flask import render_template, request, redirect, session, abort
from app import app
from services import users

@app.route("/")
def index():
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
