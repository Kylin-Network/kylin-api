from flask import Blueprint, request, make_response
from flask_restx import Resource, Namespace
from api.db.models import Users, db
import uuid
from api.manage import limiter

auth = Namespace('auth', description="authentication endpoints")

@auth.route('/register', endpoint='register')
@auth.param('wallet', 'Wallet address linked to returned API key')
class GetAPIKey(Resource):
    decorators = [limiter.exempt]
    def post(self):
        wallet = request.get_json()["wallet"] # check if wallet is valid format
        if Users.query.filter_by(wallet=wallet).first():
            raise RuntimeError("Existing user found") #ExistingUserFound()
        api_key = str(uuid.uuid4())
        new_user = Users(wallet=wallet, api_key=api_key)
        db.session.add(new_user)
        db.session.commit()
        return make_response({"api_key": api_key}, 200)
