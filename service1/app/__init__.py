from flask import Flask
from flask_cors import CORS
# from flask_talisman import Talisman
from app.routes.routes import api_bp


def create_app():
    # Create Flask app
    app = Flask(__name__)  # Create Flask app
    # api = Api(app)  # Create API
    CORS(app)  # Enable CORS
    # Talisman(app)  # Enforce HTTPS

    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app


# for local development and testing
if __name__ == '__main__':
    app = create_app()  # Initialize the Flask application
    app.run(debug=True)  # Run the app with debug mode enabled
