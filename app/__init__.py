# Flask modules
from flask import Flask
from flasgger import Swagger

# Other modules
import os
import redis

the_chat_manager = None
the_redis = None


def create_app(debug: bool = False):
    # Check if debug environment variable was passed
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", True)
    if FLASK_DEBUG:
        debug = FLASK_DEBUG

    # Create the Flask application instance
    app = Flask(
        __name__
    )

    # flasgger
    swagger = Swagger(app)

    # Set current_app context
    app.app_context().push()

    if debug:
        from app.config.dev import DevConfig

        app.config.from_object(DevConfig)
    else:
        from app.config.prod import ProdConfig

        app.config.from_object(ProdConfig)

    # Uncomment to enable logger
    # from app.utils.logger import setup_flask_logger
    # setup_flask_logger()

    # Initialize extensions
    from app.extensions import cors, cache, bcrypt, limiter, login_manager

    cors.init_app(app)
    cache.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)

    # 初始化 redis 配置
    global the_redis
    the_redis = redis.from_url(app.config.get('REDIS_URL'))
    # 设定初始值
    the_redis['aid'] = 1
    the_redis['eid'] = 1
    the_redis['fid'] = 1
    the_redis['rid'] = 1

    # Import all models and Create database tables
    from app import models

    # Register blueprints or routes
    from app.routes import api_bp, pages_bp, auth_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)

    # Global Ratelimit Checker
    # this is used because auto_check is set to 'False'
    app.before_request(lambda: limiter.check())

    return app
