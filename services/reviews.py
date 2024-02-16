from sqlalchemy.sql import text
from db import db

def add_review(user_id, adventure_id, stars, comment):
    sql = text(
        """INSERT INTO reviews (user_id, adventure_id, stars, comment)
        VALUES (:user_id, :adventure_id, :stars, :comment)
        """)
    db.session.execute(sql, {
        "user_id":user_id, "adventure_id":adventure_id,"stars":stars, "comment":comment})
    db.session.commit()

def get_reviews(adventure_id):
    sql = text(
        """SELECT users.username, reviews.stars, reviews.comment
        FROM reviews, users
        WHERE reviews.user_id=users.id AND reviews.adventure_id=:adventure_id
        ORDER BY reviews.id
        """)
    result = db.session.execute(sql, {"adventure_id": adventure_id}).fetchall()
    return result
