import asyncio
import websockets
import json
import ssl
from typing import Callable
from web_socket_client.settings import logfire


class WebSocketClient:
    def __init__(self, jsessionid: str, ws_key: str):
        self.jsessionid = jsessionid
        self.ws_key = ws_key
        self.url = "wss://akv.task-tm.com:30201/tm/tmws"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Origin": "https://akv.task-tm.com:30201",
            "Cookie": f"JSESSIONID={jsessionid}; WS_KEY={ws_key}",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Upgrade": "websocket",
        }
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def connect(self, handle_message: Callable[[dict], None]):
        """
        Устанавливает WebSocket соединение и вызывает _listen для обработки сообщений.
        :param handle_message: Функция для обработки полученных данных.
        """
        while True:
            try:
                logfire.info("Подключаемся к WebSocket серверу...")
                async with websockets.connect(
                        self.url, additional_headers=self.headers, ssl=self.ssl_context
                ) as websocket:
                    logfire.info("Соединение установлено.")
                    await self._listen(websocket, handle_message)
            except (websockets.exceptions.ConnectionClosed, websockets.exceptions.InvalidStatusCode) as e:
                logfire.error(f"Ошибка соединения: {e}. Повторная попытка...")
                await asyncio.sleep(5)  # Пауза перед повторной попыткой
            except Exception as e:
                logfire.error(f"Неожиданная ошибка: {e}")
                await asyncio.sleep(5)

    async def _listen(self, websocket, handle_message: Callable[[dict], None]):
        """
        Внутренний метод, который слушает сообщения от WebSocket-сервера и передает их на обработку.
        :param websocket: активное WebSocket-соединение.
        :param handle_message: Функция для обработки сообщений от WebSocket.
        """
        # Отправляем команду подписки
        subscribe_message = {
            "command": "SUBSCRIBE",
            "arguments": {"realm": "approval", "id": 0},
        }
        await websocket.send(json.dumps(subscribe_message))
        logfire.info(f"Отправлено сообщение: {json.dumps(subscribe_message, indent=2, ensure_ascii=False)}")

        # Ожидаем ответ от сервера
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                await handle_message(data)  # Используем переданную функцию для обработки сообщения
            except websockets.exceptions.ConnectionClosed as e:
                logfire.error(f"Соединение с сервером было закрыто: {e}")
                break



