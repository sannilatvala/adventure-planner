import os
import secrets
import re
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, abort, request
from db import db

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username": username}).fetchone()

    if not user:
        return False

    user_id, hash_value = user

    if not check_password_hash(hash_value, password):
        return False

    session["user_id"] = user_id
    session["user_name"] = username
    session["csrf_token"] = secrets.token_hex(16)

    return True

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text(
            "INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False

    login_successful = login(username, password)

    return login_successful

def validate_registration(username, password1, password2):
    if not username or not password1:
        return "Username and password required"
    if len(username) < 3:
        return "Username must be at least 3 characters long"
    if len(password1) < 5:
        return "Password must be at least 5 characters long"
    if not re.match("^[a-z0-9]+$", username):
        return "Username can only contain lowercase letters and numbers"
    if not re.search(r"[a-zA-Z]", password1) or not re.search(r"\d", password1):
        return "Password must include both letters and numbers"
    if password1 != password2:
        return "Passwords do not match"

    sql = text("SELECT password, id FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username": username}).fetchone()

    if user:
        return "Username already exists"
    return None

def logout():
    session.clear()

def user_id():
    return session.get("user_id")

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
