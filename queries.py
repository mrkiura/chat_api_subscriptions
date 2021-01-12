from ariadne import ObjectType, convert_kwargs_to_snake_case
from store import messages, users

query = ObjectType("Query")


@query.field("messages")
@convert_kwargs_to_snake_case
async def resolve_messages(obj, info, user_id):
    def filter_by_userid(message):
        if message["sender_id"] == user_id or \
                message["recipient_id"] == user_id:
            return message

    user_messages = filter(filter_by_userid, messages)
    return {
        "success": True,
        "messages": user_messages
    }


@query.field("userId")
@convert_kwargs_to_snake_case
async def resolve_user_id(obj, info, username):
    user = users.get(username)
    if user:
        return user["user_id"]
