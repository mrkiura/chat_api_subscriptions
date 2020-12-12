from ariadne import ObjectType, convert_kwargs_to_snake_case

from models import Message

query = ObjectType("Query")


@query.field("messages")
@convert_kwargs_to_snake_case
async def resolve_messages(obj, info, user_id):
    messages = await Message.query.where((Message.sender_id == user_id) | (
            Message.recipient_id == user_id)).gino.all()
    return {
        "success": True,
        "messages": messages
    }
