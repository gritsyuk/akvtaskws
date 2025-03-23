import logfire
from dotenv import dotenv_values
from base64 import b64encode

config = dotenv_values(".env")

USERNAME = config.get("LOGIN_TASK")
PASSWORD = config.get("PASSWORD_TASK")
LOGFIRE_WRITE_TOKEN = config.get("LOGFIRE_WRITE_TOKEN")

BOUNDARY = "----WebKitFormBoundaryTah2AbvUtGqBnnf1"

PROXIES = {"http": "http://192.168.141.2:26280", "https": "http://192.168.141.2:26280"}


def basic_auth(username: str, password: str) -> str:
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


headers_start = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Authorization": basic_auth(USERNAME, PASSWORD),
}

logfire.configure(token=LOGFIRE_WRITE_TOKEN)
