import os

import aioredis
from ariadne import convert_kwargs_to_snake_case, SubscriptionType

subscription = SubscriptionType()


@subscription.source("messages")
@convert_kwargs_to_snake_case
async def messages_source(obj, info, user_id):
    redis_url = os.getenv("REDIS_URL")
    channel_name = "MESSAGES"
    subscriber = await aioredis.create_redis(redis_url)
    channels = await subscriber.subscribe(channel_name)
    channel = channels[0]
    while await channel.wait_message():
        message = await channel.get_json()
        print(message)
        if message["recipient_id"] == user_id:
            yield message


@subscription.field("messages")
@convert_kwargs_to_snake_case
async def messages_resolver(message, info, user_id):
    return message
