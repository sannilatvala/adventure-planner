from sqlalchemy.sql import text
from db import db

def get_favorites(user_id):
    sql = text(
        """SELECT adventures.*
        FROM favorites
        JOIN adventures ON favorites.adventure_id = adventures.id
        WHERE favorites.user_id = :user_id
        """)
    result = db.session.execute(sql, {"user_id": user_id})
    columns = result.keys()
    favorites = result.fetchall()
    favorites_list = [dict(zip(columns, adventure)) for adventure in favorites]

    return favorites_list

def add_to_favorites(user_id, adventure_id):
    if not adventure_in_favorites(user_id, adventure_id):
        sql = text(
            """INSERT INTO favorites (user_id, adventure_id)
            VALUES (:user_id, :adventure_id)
            """)
        db.session.execute(sql, {
            "user_id":user_id, "adventure_id":adventure_id})
        db.session.commit()

def delete_from_favorites(user_id, adventure_id):
    sql = text(
        """DELETE FROM favorites
        WHERE user_id = :user_id AND adventure_id = :adventure_id
        """)
    db.session.execute(sql, {
        "user_id": user_id, "adventure_id": adventure_id})
    db.session.commit()

def adventure_in_favorites(user_id, adventure_id):
    sql = text(
        """SELECT * FROM favorites 
        WHERE user_id = :user_id AND adventure_id = :adventure_id
        """)
    result = db.session.execute(sql, {
        "user_id": user_id, "adventure_id": adventure_id}).fetchall()

    if result:
        return True
    return False
