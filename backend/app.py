import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config_by_name
from database.init_db import init_db

# Import Blueprints
from blueprints.pages import pages_bp
from blueprints.api import api_bp
from blueprints.lessons import lessons_bp
from blueprints.videos import videos_bp
from blueprints.games import games_bp
from blueprints.computer_skills import computer_skills_bp
from blueprints.daily_routine import daily_routine_bp

def create_app(config_name=None):
    """Application factory for MindVerse — Inclusive Learning Lab."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development").lower()

    app = Flask(__name__)
    config_class = config_by_name.get(config_name, config_by_name["default"])
    app.config.from_object(config_class)

    # Configure CORS with strict or configurable origins
    origins = app.config.get("CORS_ORIGINS", "*")
    CORS(
        app,
        resources={r"/api/*": {"origins": origins}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    # Initialize Database safely on application start
    try:
        init_db(app.config.get("DATABASE"))
    except Exception as e:
        app.logger.error(f"Database initialization warning: {e}")

    # Register Blueprints
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(lessons_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(computer_skills_bp)
    app.register_blueprint(daily_routine_bp)

    # Consistent Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": "Bad request. Please check your parameters and JSON payload.",
            "status_code": 400
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "The requested resource was not found.",
            "status_code": 404
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": "HTTP method not allowed for this route.",
            "status_code": 405
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": "An internal server error occurred. Please try again later.",
            "status_code": 500
        }), 500

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    print(f"MindVerse Backend running on http://{host}:{port}")
    app.run(host=host, port=port, debug=app.config.get("DEBUG", True))
