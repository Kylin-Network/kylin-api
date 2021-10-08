from flask import request, make_response
from flask_restx import Resource, Namespace
from api.db.models import Users, db
import uuid
from api.manage import limiter
from api.errors.exceptions import ExistingUserFound

auth = Namespace('auth', description="Authentication endpoints.")

@auth.route('/register', endpoint='auth/register')
@auth.param('wallet', 'Substrate wallet address or unique identifier linked to API key.')
class GetAPIKey(Resource):
    # decorators = [limiter.limit("10/second")]
    def post(self):
        wallet = request.get_json()["wallet"]
        if Users.query.filter_by(wallet=wallet).first():
            raise ExistingUserFound(payload=wallet)
        api_key = str(uuid.uuid4())
        new_user = Users(wallet=wallet, api_key=api_key)
        db.session.add(new_user)
        db.session.commit()
        return make_response({"message": "api key successfully created", "api_key": api_key}, 200)
