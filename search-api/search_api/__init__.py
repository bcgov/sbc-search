import datetime
import os

from flask_cors import CORS

from search_api import config
from flask_migrate import Migrate
from dotenv import load_dotenv

from search_api.resources import DIRECTORS_API, BUSINESSES_API

from search_api.models import app

load_dotenv(verbose=True)


def create_app(run_mode=os.getenv("FLASK_ENV", "production")):
    """Return a configured Flask App using the Factory method."""
    # app = Flask(__name__)
    app.config.from_object(config.CONFIGURATION[run_mode])
    CORS(app)

    # Configure Sentry
    if app.config.get("SENTRY_DSN", None):
        sentry_sdk.init(
            dsn=app.config.get("SENTRY_DSN"), integrations=[FlaskIntegration()]
        )

    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_URL', 'postgresql://postgres:password@db/postgres')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
    # migrate = Migrate(app, db)

    app.register_blueprint(DIRECTORS_API)
    app.register_blueprint(BUSINESSES_API)

    @app.route("/ops/readyz")
    @app.route("/ops/healthz")
    def check():
        return {}, 200

    # setup_jwt_manager(app, jwt)

    # @app.after_request
    # def add_version(response):  # pylint: disable=unused-variable
    #     version = get_run_version()
    #     response.headers['API'] = f'search_api/{version}'
    #     return response

    # register_shellcontext(app)

    return app
