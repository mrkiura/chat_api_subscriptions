import os
from gino import Gino

db = Gino(
)

database_url = os.getenv("DATABASE_URL")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger(), primary_key=True)
    username = db.Column(db.Unicode(), default="unnamed")

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username
        }


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.BigInteger(), primary_key=True)
    content = db.Column(db.String)
    sender_id = db.Column(db.Unicode(), default="unnamed")
    recipient_id = db.Column(db.Unicode(), default="unnamed")

    def to_dict(self):
        return {
            "content": self.content,
            "recipient_id": self.recipient_id,
            "sender_id": self.sender_id
        }
