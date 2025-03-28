import json
from web_socket_client.settings import logfire
from src.parser.task import TaskParser
from src.email_akv.email_sender import EmailSender

def generate_approvers_html(approve_data):
    approvers_html = ""
    
    if "approvers" in approve_data:
        for approver in approve_data["approvers"]:
            approvers_html += f'<tr><td>{approver["name"]}</td><td>{approver["status"]}</td><td>{approver["approved_date"]}</td></tr>\n'
    
    return approvers_html


def process_string(input_string: str, num: int) -> str:
    if len(input_string) > num:
        return input_string[:num] + "..."
    else:
        return input_string

tehzak_email = EmailSender()

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
        if "полностью согласован" in approval_text.lower():
            url_task = f"https://akv.task-tm.com:30201/tm/approval/show/{approval_id}"
            
            async with TaskParser() as parser:
                task_info =  await parser.get_simplified_approval(approval_id)

            await tehzak_email.send_email(
                    html_table=f"""
            <html>
            <head>
                <style>
                    th {{
                        background-color: #005C8C;
                        color: #ffffff;
                    }}
                        th, td {{
                        font-size: 12px;
                        padding: 2px 10px;
                    }}
                </style>
            </head>
            <body>
                <p><a href="{url_task}/">{url_task}</a>'</p>
                <h1>{approval_text}<h2>
                <table border="0">
                    <tr>
                        <th>Ответсвенный</th>
                        <th>Согласовано?</th>
                        <th>Дата согласования</th>
                    </tr>
                    {generate_approvers_html(task_info.get('approvers'))}
                </table>
                <p></p>
                <p style='font-size: 12px; color: grey;' >Это письмо сформировано автоматически. Отвечать на него не нужно.</p>
            </body>
            </html>
            """,
                    email_subj=f"{approval_id} | Согласован | {process_string(task_info.get('subj')), 30}",
                    email_list=["gricyuk@group-akvilon.ru"]
                )
        logfire.info(f"{approval_text}")
        return

    if event == "event":
        logfire.info(f"EVENT: {event}")
        logfire.info(f"MESSAGE: {data['reply']['text']}")
        return

    else:
        logfire.error(f"UNKNOW EVENT TYPE:\n {data}")
        
    logfire.info("-----------------------------")
