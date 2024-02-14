import os
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
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

    return True

def register(username, password):
    sql = text("SELECT password, id FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username": username}).fetchone()

    if user:
        return False

    hash_value = generate_password_hash(password)
    sql = text(
        "INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

    login_successful = login(username, password)

    return login_successful

def logout():
    del session["user_id"]
    del session["user_name"]

def user_id():
    return session.get("user_id")
