import os

import aioredis
from ariadne import convert_kwargs_to_snake_case, SubscriptionType

from store import queue

subscription = SubscriptionType()


@subscription.source("messages")
@convert_kwargs_to_snake_case
async def messages_source(obj, info, user_id):
    while True:
        message = await queue.get()
        # retrieve message and yield it if it matches our user
        if message["recipient_id"] == user_id:
            queue.task_done()
            yield message
        else:
            # return the message to the queue (belongs to different user)
            queue.put(message)


@subscription.field("messages")
@convert_kwargs_to_snake_case
async def messages_resolver(message, info, user_id):
    return message
