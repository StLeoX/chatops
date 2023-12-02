from flask_cors import CORS

CORS_ORIGINS = "*"

cors = CORS(resources={r"/v1/*": {"origins": CORS_ORIGINS}})
