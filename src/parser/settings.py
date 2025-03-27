import os
from base64 import b64encode
from dotenv import load_dotenv

load_dotenv()


USERNAME = os.getenv('LOGIN_TASK')
PASSWORD = os.getenv('PASSWORD_TASK')
BOUNDARY = "----WebKitFormBoundaryTah2AbvUtGqBnnf1"


PROXIES = {
    "http": "http://192.168.141.2:26280",
    "https": "http://192.168.141.2:26280"
    }  

def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": f"multipart/form-data; boundary={BOUNDARY}",
        "cookie": "JSESSIONID=C6FF36219A1DBB247C8EE8D9BE287B0B",
        "Authorization": basic_auth(USERNAME, PASSWORD),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

def generate_payload(name_param: str) -> str:
    payload = (
        f'--{BOUNDARY}\r\n'
        f'Content-Disposition: form-data; name="type"\r\n\r\n'
        f'form\r\n'
        f'--{BOUNDARY}\r\n'
        f'Content-Disposition: form-data; name="realm"\r\n\r\n'
        f'thread\r\n'
        f'--{BOUNDARY}\r\n'
        f'Content-Disposition: form-data; name="name"\r\n\r\n'
        f'{name_param}\r\n'
        f'--{BOUNDARY}\r\n'
        f'Content-Disposition: form-data; name="action"\r\n\r\n'
        f'list\r\n'
        f'--{BOUNDARY}\r\n'
        f'Content-Disposition: form-data; name="object"\r\n\r\n'
        f'{{"building_id":0,"contacts":[],"cdate_from":"","cdate_to":"","astatus_id":0,"search":"","page":0,"limit":0,"sort_column":"","sort_desc":"false","view_page":"all"}}\r\n'
        f'--{BOUNDARY}--\r\n'
    )
    return payload


def generate_aprove_payload_id(id: int) -> str:
    data = (
        f"--{BOUNDARY}\r\n"
        f"Content-Disposition: form-data; name=\"type\"\r\n\r\nform\r\n"
        f"--{BOUNDARY}\r\n"
        f"Content-Disposition: form-data; name=\"realm\"\r\n\r\napproving\r\n"
        f"--{BOUNDARY}\r\n"
        f"Content-Disposition: form-data; name=\"name\"\r\n\r\napprove\r\n"
        f"--{BOUNDARY}\r\n"
        f"Content-Disposition: form-data; name=\"action\"\r\n\r\nget\r\n"
        f"--{BOUNDARY}\r\n"
        f"Content-Disposition: form-data; name=\"object\"\r\n\r\n{{\"id\":{id}}}\r\n"
        f"--{BOUNDARY}--"
    )
    return data

