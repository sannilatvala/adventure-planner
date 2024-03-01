import random
import json
from sqlalchemy.sql import text
from db import db
from flask import session

def create_adventures(user_id):
    sql = text("SELECT * FROM preferences WHERE user_id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    columns = result.keys()

    user_preferences = result.fetchone()

    user_preferences_dict = dict(zip(columns, user_preferences))

    sql = text("SELECT * FROM adventures")
    result = db.session.execute(sql)

    columns = result.keys()

    adventures = result.fetchall()

    adventures_list = [dict(zip(columns, adventure)) for adventure in adventures]

    duration_preference = user_preferences_dict["duration_preference"]
    budget_preference = user_preferences_dict["budget_preference"]
    difficulty_preference = user_preferences_dict["difficulty_preference"]
    environment_preference = user_preferences_dict["environment_preference"]
    group_size_preference = user_preferences_dict["group_size_preference"]
    season_preference = user_preferences_dict["season_preference"]

    recommended_adventures = []

    for adventure in adventures_list:
        if (
            duration_preference == adventure["duration"] and
            int(budget_preference) >= int(adventure["cost"]) and
            difficulty_preference == adventure["difficulty_level"] and
            environment_preference in adventure["environment"] and
            group_size_preference in adventure["group_size"] and
            season_preference in adventure["season"]
        ):
            recommended_adventures.append(adventure)

    random.shuffle(recommended_adventures)

    random_recommended_adventures = recommended_adventures[:min(5, len(recommended_adventures))]

    serialized_adventures = json.dumps(random_recommended_adventures)

    session["created_adventures"] = serialized_adventures

    print(serialized_adventures)

    return random_recommended_adventures

def add_adventure(adventure):
    title = adventure["title"]
    description = adventure["description"]
    duration =  adventure["duration"]
    cost = adventure["cost"]
    difficulty_level = adventure["difficulty_level"]
    environment = adventure["environment"]
    group_size = adventure["group_size"]
    season = adventure["season"]

    sql = text(
        """INSERT INTO adventures 
            (title, description, duration, cost, difficulty_level, 
            environment, group_size, season) VALUES 
            (:title, :description, :duration, :cost, 
            :difficulty_level, :environment, :group_size, :season)
        """)
    db.session.execute(sql, {
        "title": title, "description": description, "duration": duration, 
        "cost": cost, "difficulty_level": difficulty_level, 
        "environment": environment, "group_size": group_size, "season": season})
    db.session.commit()

def get_created_adventures():
    return session.get("created_adventures")
