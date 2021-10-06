from flask import make_response
from flask_restx import Resource
from api.db.models import db
from api.blueprints import api
from api.manage import create_app, limiter

app = create_app()

api.init_app(app)
db.init_app(app)
limiter.init_app(app)

@api.route('/health', endpoint='health')
class Health(Resource):
    decorators = [limiter.exempt]
    def get(self):
        return make_response({"message": "OK"}, 200)

if __name__ == "__main__":
    app.run()
