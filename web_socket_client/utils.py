from web_socket_client.settings import logfire
import json


async def custom_handle_message(data):
    """
    Пример пользовательской функции для обработки сообщений WebSocket.
    """
    logfire.info("\n------- Новое сообщение -------")
    if data.get("type") == "CHAT":
        logfire.info(f"Chat message: {data['reply']['msg']}")
    elif data.get("type") == "MSG":
        logfire.info(f"New message: {data['reply']['text']}")
    elif data.get("type") == "event":
        logfire.info(f"Event: {data['reply']['text']}")
    else:
        logfire.info(f"Unknown message type: {data}")
    logfire.info(f"Received data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    logfire.info("-----------------------------")
