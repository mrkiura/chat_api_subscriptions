import asyncio

messages = []
users = {}

queue = asyncio.Queue()


def create_user(username):
    if not users.get(username):
        user = {
            "user_id": len(users) + 1,
            "username": username
        }
        users[username] = user
        return {
            "success": True,
            "user": user
        }