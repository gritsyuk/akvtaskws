import asyncio
import aiohttp
import logfire
from typing import Optional, Tuple, Callable
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

async def authenticate() -> Tuple[Optional[str], Optional[str]]:
    url = "https://akv.task-tm.com:30201/tm/approval/all/"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers_start, ssl=False) as response:
                if response.status != 200:
                    raise aiohttp.ClientError(f"Ошибка статуса: {response.status}")

                cookies = response.cookies
                jsessionid = cookies.get("JSESSIONID").value if cookies.get("JSESSIONID") else None
                ws_key = cookies.get("WS_KEY").value if cookies.get("WS_KEY") else None

                if not jsessionid or not ws_key:
                    raise ValueError("Отсутствуют обязательные данные в ответе")

                logfire.info(f"JSESSIONID: {jsessionid}, WS_KEY: {ws_key}")
                return jsessionid, ws_key

    except aiohttp.ClientProxyConnectionError as e:
        logfire.error(f"Ошибка прокси: {e}")
        return None, None
    except aiohttp.ClientConnectionError as e:
        logfire.error(f"Ошибка подключения: {e}")
        return None, None
    except asyncio.TimeoutError as e:
        logfire.error(f"Таймаут запроса: {e}")
        return None, None
    except Exception as e:
        logfire.error(f"Неожиданная ошибка: {e}")
        return None, None
