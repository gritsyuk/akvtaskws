import asyncio
import httpx
import websockets
import json
import ssl
from typing import Optional, Tuple
from settings import headers_start
from settings import logfire
from redis_client import RedisClient

# Создаем глобальный экземпляр Redis клиента
redis_client = RedisClient()


async def authenticate() -> Tuple[Optional[str], Optional[str]]:
    url = "https://akv.task-tm.com:30201/tm/approval/all/"

    try:
        async with httpx.AsyncClient(
            verify=False,  # Отключаем проверку SSL для тестирования
            timeout=30.0,
            proxy=None,
        ) as client:
            response = await client.get(url, headers=headers_start)
            response.raise_for_status()  # Проверяем статус ответа

            jsessionid = response.cookies.get("JSESSIONID")
            ws_key = response.cookies.get("WS_KEY")

            if not jsessionid or not ws_key:
                raise ValueError("Отсутствуют обязательные данные в ответе")

            logfire.info(f"JSESSIONID: {jsessionid}, WS_KEY: {ws_key}")
            return jsessionid, ws_key

    except httpx.ProxyError as e:
        logfire.info(f"Ошибка прокси: {e}")
        return None, None
    except httpx.ConnectError as e:
        logfire.info(f"Ошибка подключения: {e}")
        return None, None
    except httpx.TimeoutException as e:
        logfire.info(f"Таймаут запроса: {e}")
        return None, None
    except Exception as e:
        logfire.info(f"Неожиданная ошибка: {e}")
        return None, None


async def listen(jsessionid: str, ws_key: str):
    url = "wss://akv.task-tm.com:30201/tm/tmws"

    # Заголовки для подключения
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Origin": "https://akv.task-tm.com:30201",
        "Cookie": f"JSESSIONID={jsessionid}; WS_KEY={ws_key}",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Upgrade": "websocket",
    }

    # Создаем SSL контекст без проверки сертификата
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    print("Подключаемся к WebSocket серверу...")

    try:
        async with websockets.connect(
            url, additional_headers=headers, ssl=ssl_context
        ) as websocket:
            logfire.info("Соединение установлено. Отправляем команду подписки...")

            # Отправляем команду подписки
            subscribe_message = {
                "command": "SUBSCRIBE",
                "arguments": {"realm": "approval", "id": 0},
            }
            await websocket.send(json.dumps(subscribe_message))
            logfire.info(
                f"Отправлено сообщение: {json.dumps(subscribe_message, indent=2, ensure_ascii=False)}"
            )

            # Ожидаем ответ от сервера
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                if data.get("type") == "ACK" and data.get("success"):
                    logfire.info("Подписка подтверждена (ACK).")
                else:
                    logfire.info("\n------- Новое сообщение -------")
                    if data.get("type") == "CHAT":
                        logfire.info(f"Chat message: {data['reply']['msg']}")
                    elif data.get("type") == "MSG":
                        logfire.info(f"New message: {data['reply']['text']}")
                    elif data.get("type") == "event":
                        logfire.info(f"Event: {data['reply']['text']}")
                        # Асинхронно сохраняем событие в Redis
                        asyncio.create_task(redis_client.save_event(data))
                    else:
                        logfire.info(f"Unknown message type: {data}")
                    logfire.info(json.dumps(data, indent=2, ensure_ascii=False))
                    logfire.info("-----------------------------")

    except Exception as e:
        logfire.info(f"Ошибка подключения или получения данных: {e}")


async def main():
    logfire.info("Start!")
    jsessionid, ws_key = await authenticate()

    if jsessionid and ws_key:
        logfire.info("Аутентификация успешна")
        await listen(jsessionid, ws_key)
    else:
        logfire.info("Ошибка аутентификации")


if __name__ == "__main__":
    asyncio.run(main())
