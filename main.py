from asyncio import run
from web_socket_client.socketClient import WebSocketClient
from web_socket_client.utils import custom_handle_message
from web_socket_client.settings import authenticate

async def main():
    jsessionid, ws_key = await authenticate()
    if jsessionid and ws_key:
        websocket_client = WebSocketClient(jsessionid, ws_key)
        await websocket_client.connect(handle_message=custom_handle_message)

if __name__ == "__main__":
    run(main())
