from ariadne import make_executable_schema, load_schema_from_path, \
    snake_case_fallback_resolvers
from ariadne.asgi import GraphQL
from models import db
from mutations import mutation
from queries import query
from starlette.applications import Starlette

from subscriptions import subscription

type_defs = load_schema_from_path("schema.graphql")


def make_app():
    application = Starlette(debug=True)
    db.init_app(application)
    return application


app = make_app()
schema = make_executable_schema(type_defs, query, mutation, subscription,
                                snake_case_fallback_resolvers)
app.mount("/graphql", GraphQL(schema, debug=True))
