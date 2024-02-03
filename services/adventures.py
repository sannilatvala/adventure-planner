from sqlalchemy.sql import text
from db import db
import random

def create_adventures(user_preferences):
    sql = text("SELECT * FROM adventures")
    result = db.session.execute(sql)

    columns = result.keys()

    adventures = result.fetchall()

    adventures_list = [dict(zip(columns, adventure)) for adventure in adventures]

    duration_preference = user_preferences["duration"]
    budget_preference = user_preferences["budget"]
    difficulty_preference = user_preferences["difficulty"]
    environment_preference = user_preferences["environment"]
    group_size_preference = user_preferences["group_size"]
    season_preference = user_preferences["season"]

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
