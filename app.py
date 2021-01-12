import asyncio

from ariadne import make_executable_schema, load_schema_from_path, \
    snake_case_fallback_resolvers
from ariadne.asgi import GraphQL
from mutations import mutation
from queries import query
from subscriptions import subscription


type_defs = load_schema_from_path("schema.graphql")


schema = make_executable_schema(type_defs, query, mutation, subscription,
                                snake_case_fallback_resolvers)
app = GraphQL(schema, debug=True)
