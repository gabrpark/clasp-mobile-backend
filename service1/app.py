from flask import Flask
from flask_cors import CORS
# from flask_talisman import Talisman
from flask_restful import Api
from api.routes import api_bp

# Create Flask app
app = Flask(__name__)  # Create Flask app
# api = Api(app)  # Create API
CORS(app)  # Enable CORS
# Talisman(app)  # Enforce HTTPS

app.register_blueprint(api_bp, url_prefix='/api')

# Start app
if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)  # Run app
