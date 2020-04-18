from search_api.models.base import db
from http import HTTPStatus
from flask import jsonify, request, Blueprint, current_app
from search_api.auth import authorized, jwt
from sqlalchemy import exc

API = Blueprint('AUTH_API', __name__, url_prefix='/api/v1/auth-check')


@API.route('/')
@jwt.requires_auth
def auth_check():
    account_id = request.headers.get('X-Account-Id', None)
    if not authorized(jwt, account_id):
        return (
            jsonify({'message': 'User is not authorized to access Director Search'}),
            HTTPStatus.UNAUTHORIZED,
        )

    # Include a database health check at this point, because it greatly improves query
    # perf in the next minute or so, if the database is warmed up.
    try:
        if current_app.config.get("IS_ORACLE"):
            db.engine.execute('SELECT 1 FROM CORP_PARTY WHERE ROWNUM = 1')
        else:
            db.engine.execute('SELECT 1')
    except exc.SQLAlchemyError:
        return {'message': 'authorized, but api is down'}, HTTPStatus.SERVICE_UNAVAILABLE

    # made it here, so all checks passed
    return {'message': 'authorized, api is healthy'}, HTTPStatus.OK
