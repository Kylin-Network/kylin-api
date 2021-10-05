from flask import Response
from flask_restx import Resource
from api.db.models import db
from api.apis import api
from api.manage import create_app, limiter

app = create_app()

api.init_app(app)
db.init_app(app)
limiter.init_app(app)

@api.route('/health', endpoint='health')
class Health(Resource):
    decorators = [limiter.exempt]
    def get(self):
        return Response("OK", status=200)

if __name__ == "__main__":
    app.run()
