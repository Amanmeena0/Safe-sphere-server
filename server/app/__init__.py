import logging
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.config import Config
from app.models import db
from app.utils.celery_app import celery

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    db.init_app(app)

    # Configure Celery
    celery.conf.update(app.config)

    # Enable CORS
 for the specific frontend origin
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    from app.routes.search_routes import search_bp
    from app.routes.hello_auth import hello_bp 
    from app.routes.sos_route.police_services import police_bp  
    from app.routes.sos_route.crime_data import crime_data_bp
    from app.routes.profile_route.user_registration import user_bp
    from app.routes.profile_route.profile import profile_bp
    from app.routes.app_bot.generate import bot_bp
    
    # FIR route imports
    from app.routes.fir_route_register.form.misisngPerson import missingPerson_bp
    from app.routes.fir_route_register.form.cyber_crime import cyber_crime_bp
    from app.routes.fir_route_register.form.Lost_item import lost_item_bp
    from app.routes.fir_route_register.form.domestic import domestic_bp
    from app.routes.fir_route_register.form.rapeCase import rapecase_bp
    from app.routes.fir_route_register.form.theftEfir import theft_bp
    from app.routes.fir_route_register.form.MVtheft import mvtheft_bp

    app.register_blueprint(hello_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(police_bp)  
    app.register_blueprint(crime_data_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(bot_bp)
    
    # Register FIR blueprints
    app.register_blueprint(missingPerson_bp)
    app.register_blueprint(cyber_crime_bp)
    app.register_blueprint(lost_item_bp)
    app.register_blueprint(domestic_bp)
    app.register_blueprint(rapecase_bp)
    app.register_blueprint(theft_bp)
    app.register_blueprint(mvtheft_bp)

    @app.errorhandler(400)
    def bad_request(error):
        return {"error": "Bad Request", "message": str(error)}, 400

    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not Found", "message": "The requested resource was not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal Server Error", "message": "An unexpected error occurred"}, 500

    # Create tables
    with app.app_context():
        from app import models  # Import models to ensure they're registered
        db.create_all()

    return app
