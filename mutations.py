import os

import aioredis
from ariadne import ObjectType, convert_kwargs_to_snake_case

from models import Message, User, db, database_url

mutation = ObjectType("Mutation")


@mutation.field("createMessage")
@convert_kwargs_to_snake_case
async def resolve_create_message(obj, info, content, sender_id, recipient_id):
    try:
        redis_url = os.getenv("REDIS_URL")
        channel_name = "MESSAGES"
        publisher = await aioredis.create_redis(redis_url)
        async with db.with_bind(database_url) as engine:
            message = await Message.create(content=content, sender_id=sender_id,
                                           recipient_id=recipient_id)
            serialized_message = message.to_dict()
            await publisher.publish_json(channel_name, serialized_message)
            publisher.close()
            return {
                "success": True,
                "message": serialized_message
            }
    except Exception as error:
        return {
            "success": False,
            "errors": [str(error)]
        }


@mutation.field("createUser")
@convert_kwargs_to_snake_case
async def resolve_create_user(obj, info, username):
    try:
        async with db.with_bind(database_url) as engine:
            user = await User.create(username=username)
            return {
                "success": True,
                "user": user.to_dict()
            }
    except Exception as error:
        return {
            "success": False,
            "errors": [str(error)]
        }
