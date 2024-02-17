from sqlalchemy.sql import text
from db import db

def create_preferences(user_id, user_preferences):
    if preferences_exists(user_id):
        sql = text(
            """DELETE FROM preferences
            WHERE user_id = :user_id
            """
        )
        db.session.execute(sql, {"user_id": user_id})
        db.session.commit()

    duration_preference = user_preferences["duration"]
    budget_preference = user_preferences["budget"]
    difficulty_preference = user_preferences["difficulty"]
    environment_preference = user_preferences["environment"]
    group_size_preference = user_preferences["group_size"]
    season_preference = user_preferences["season"]

    sql = text(
        """INSERT INTO preferences 
            (user_id, duration_preference, budget_preference, difficulty_preference, 
            environment_preference, group_size_preference, season_preference) VALUES 
            (:user_id, :duration_preference, :budget_preference, :difficulty_preference, 
            :environment_preference, :group_size_preference, :season_preference)
        """)
    db.session.execute(sql, {
        "user_id": user_id,
        "duration_preference": duration_preference, 
        "budget_preference": budget_preference, 
        "difficulty_preference": difficulty_preference, 
        "environment_preference": environment_preference, 
        "group_size_preference": group_size_preference, 
        "season_preference": season_preference})
    db.session.commit()

def get_preferences(user_id):
    sql = text("SELECT * FROM preferences WHERE user_id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    columns = result.keys()

    user_preferences = result.fetchone()

    user_preferences_dict = dict(zip(columns, user_preferences))

    return user_preferences_dict

def preferences_exists(user_id):
    sql = text("SELECT * FROM preferences WHERE user_id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    preferences = result.fetchone

    if preferences:
        return True
    return False
