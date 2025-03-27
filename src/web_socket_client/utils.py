import json
from web_socket_client.settings import logfire
from src.parser.task import TaskParser



async def custom_handle_message(data):
    """
    {
    "success": true,
    "type": "MSG",
        "reply": {
            "tm": "17:43:07.711",
            "mid": 1742827387,
            "realm": "ticket",
            "id": 27178,
            "text": "Добавлен файл в \\"Претензионный порядок с ООО СК Вира \\"\\nhttps://akv.task-tm.com:30201/tm/ticket/show/27178/",
            "type": "msg"
        }
    }
    """
    logfire.info("\n------- Новое сообщение -------")
    logfire.info(f"Received data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    event = data.get("type")
    task_type = data.get('reply').get('realm') # ["approval", "ticket", "АСК"]

    if event == "ACK" and data.get("success"):
        logfire.info(f"EVENT: {event}")    
        logfire.info("Subscription -> socket connection success")       
        return

    if event == "CHAT":
        logfire.info(f"EVENT: {event}")
        logfire.info(f"MESSAGE: {data.get('reply').get('text')}")
        return

    if event == "MSG" and task_type == "ticket":
        logfire.info(f"EVENT: {event}")
        logfire.info(f"MESSAGE: {data.get('reply').get('text')}")
        return

    if event == "MSG" and task_type == "approval":
        approval_id = data.get('reply').get('id')
        approval_text = data.get('reply').get('text')
        logfire.info(f"EVENT: {event}")
        logfire.info(f"ID: {approval_id}")
        # logfire.info(f"MESSAGE: {approval_text}")
        async with TaskParser() as parser:
            task_info =  await parser.get_simplified_approval(approval_id)
        logfire.info(f"{task_info}")
        return

    if event == "event":
        logfire.info(f"EVENT: {event}")
        logfire.info(f"MESSAGE: {data['reply']['text']}")
        return

    else:
        logfire.error(f"UNKNOW EVENT TYPE:\n {data}")
        
    logfire.info("-----------------------------")
