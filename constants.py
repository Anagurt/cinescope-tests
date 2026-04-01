import os

from dotenv import load_dotenv

load_dotenv()


ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

BASE_AUTH_URL = "https://auth.dev-cinescope.coconutqa.ru"
BASE_MOVIES_URL = "https://api.dev-cinescope.coconutqa.ru"

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
MOVIES_ENDPOINT = "/movies"
USER_ENDPOINT = "/user"
