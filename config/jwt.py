from authx import AuthX, AuthXConfig
from typing import Any
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


jwt_secret_key = os.getenv("JWT_SECRET_KEY")
if not jwt_secret_key:
    raise ValueError("JWT_SECRET_KEY is not set. Please configure it in the .env file.")


access_token_cookie_name = os.getenv("JWT_ACCESS_COOKIE_NAME")
if not access_token_cookie_name:
    raise ValueError("JWT_ACCESS_COOKIE_NAME is not set. Please configure it in the .env file.")

config = AuthXConfig()


config.JWT_SECRET_KEY = jwt_secret_key
config.JWT_ALGORITHM = "HS256"
config.JWT_ACCESS_COOKIE_NAME = access_token_cookie_name
config.JWT_TOKEN_LOCATION = ["cookies"]

config.JWT_ACCESS_COOKIE_PATH = "/"
config.JWT_REFRESH_COOKIE_PATH = "/"


config.JWT_COOKIE_CSRF_PROTECT = False
config.JWT_COOKIE_SECURE = False
config.JWT_COOKIE_SAMESITE = "lax"


security = AuthX[Any](config=config)