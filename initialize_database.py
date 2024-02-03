import json
from sqlalchemy.sql import text
from services import adventures
from db import db

def add_adventures_to_db():
    adventures_json_path = "data/adventures.json"

    with open(adventures_json_path, encoding="utf-8") as file:
        data = json.load(file)

    delete_adventures_in_db()

    for adventure in data:
        adventures.add_adventure(adventure)

def delete_adventures_in_db():
    delete_sql = text("DELETE FROM adventures")
    db.session.execute(delete_sql)
    db.session.commit()
