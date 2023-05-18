from flask import Flask, request
from flask_cors import CORS
from logging_helper import init_logger
from main import voter_validation_api
import os
from logging_helper import init_logger
from flask import Flask, request
from main_1 import get_details_api2
from get_captcha import search_by_epic
from verify_captcha import verify_captcha
from get_details import get_details
logger = init_logger("VOTER")

server = os.getenv("SERVER")
port = os.getenv("API_VERSION_PORT")
db = os.getenv("DB")


app = Flask(__name__)
cors = CORS(app)

logger = init_logger("voter_validation")

@app.route("/get_captcha", methods=["POST", "GET"])
def login_api():
    return search_by_epic(request)

@app.route("/verify_captcha", methods=["POST", "GET"])
def verify_api():
    return verify_captcha(request)

@app.route("/get_results", methods=["POST", "GET"])
def details_api():
    return get_details(request)

@app.route("/eci", methods=["POST"])
def voter_validation():
    logger.info("hit request voter-validation")
    return voter_validation_api(request)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
