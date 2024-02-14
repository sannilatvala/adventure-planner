import json
from sqlalchemy.sql import text
from services import adventures
from db import db

def add_adventures_to_db():
    if not adventures_exist():
        adventures_json_path = "data/adventures.json"

        with open(adventures_json_path, encoding="utf-8") as file:
            data = json.load(file)

        for adventure in data:
            adventures.add_adventure(adventure)

def adventures_exist():
    sql = text("SELECT * FROM adventures")
    result = db.session.execute(sql)
    all_adventures = result.fetchall()
    if all_adventures:
        return True
    return False
