import logfire
import json
from aiohttp import ClientSession
from pydantic import ValidationError
from typing import AsyncGenerator
from .settings import headers
from .models.parser_response import (
    Response, 
    ApprovalResponse
    )
from .models.task_tm import (
    Task_list, 
    Approve_tm
    )
from .constants import UserStatusApproval
from .settings import (
    generate_payload, 
    generate_aprove_payload_id
    )
from .utils import parse_date


class TaskParser:
    def __init__(self) -> None:
        self.url = "https://akv.task-tm.com:30201"

    async def __aenter__(self):
        self.session = ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def get_tickets(self) -> AsyncGenerator[Task_list, None]:
        link = self.url + "/tm/action/?vx=form/thread/ticket/list"
        payload = generate_payload("ticket")
        try:
            async with self.session.post(
                url=link, data=payload, verify_ssl=False
            ) as res:
                byte_string = await res.read()

            decode_str = byte_string.decode("utf-8")
            tickets = Response.model_validate_json(decode_str)
            for thread in tickets.reply.threads:
                yield thread
        except Exception as e:
            logfire.error(e)

    async def get_approvals(self) -> AsyncGenerator[Task_list, None]:
        link = self.url + "/tm/action/?vx=form/thread/approval/list"
        payload = generate_payload("approval")
        try:
            async with self.session.post(
                url=link, data=payload, verify_ssl=False
            ) as res:
                byte_string = await res.read()

            decode_str = byte_string.decode("utf-8")
            response_obj = Response.model_validate_json(decode_str)
            for thread in response_obj.reply.threads:
                yield thread
        except Exception as e:
            logfire.error(e)

    async def get_approve_by_id(self, task_id) -> Approve_tm | None:
        link = self.url + "/tm/action/?vx=form/approving/approve/get"
        payload = generate_aprove_payload_id(task_id)
        try:
            async with self.session.post(
                url=link, data=payload, verify_ssl=False
            ) as res:
                byte_string = await res.read()

            decode_str = byte_string.decode("utf-8")
            response_obj = ApprovalResponse.model_validate_json(decode_str)

            return response_obj
        except ValidationError:
            logfire.error(f"ERROR: Pydantic ValidationError: {task_id}")
        except Exception as e:
            logfire.error(e)

        return None

    async def get_simplified_approval(self, task_id) -> dict | None:
        link = self.url + "/tm/action/?vx=form/approving/approve/get"
        payload = generate_aprove_payload_id(task_id)
        try:
            async with self.session.post(
                url=link, data=payload, verify_ssl=False
            ) as res:
                res_json = await res.read()
                data = json.loads(res_json.decode("utf-8"))

                if "approve" not in data:
                    logfire.error(f"No 'approve' field in response for task {task_id}")
                    return None

                approve_data = data["approve"]
                simplified_approvers = []
                not_marked_user_count = 0
                not_marked_user_names = []
                visor_names = []
                max_date = None
                created_date_str = approve_data.get("created")

                if "visor" in approve_data and approve_data["visor"] is not None:
                    for visor in approve_data["visor"]:
                        name = (
                            visor.get("short_name") if isinstance(visor, dict) else None
                        )
                        if name:  # Игнорируем None и пустые строки
                            visor_names.append(name)

                if "approvers" in approve_data:
                    for approver in approve_data["approvers"]:
                        user_name = approver.get("name")
                        approved_date_str = approver.get("approved_date")
                        user_approve_status = approver.get("status")

                        approved_date = (
                            parse_date(approved_date_str) if approved_date_str else None
                        )

                        if approved_date:
                            if max_date is None or approved_date > max_date:
                                max_date = approved_date

                        max_date_str = (
                            max_date.strftime("%d.%m.%Y %H:%M:%S")
                            if max_date
                            else created_date_str
                        )

                        if approver.get("status") == UserStatusApproval.NOT_MARKED:
                            not_marked_user_count += 1
                            not_marked_user_names.append(user_name)

                        simplified_approvers.append(
                            {
                                "name": user_name,
                                "approved_date": approved_date_str,
                                "status": user_approve_status,
                            }
                        )

                return {
                    "created": created_date_str,
                    "modified": max_date_str,
                    "status_name": approve_data.get("status_name"),
                    "not_marked_user_count": not_marked_user_count,
                    "not_marked_user_names": not_marked_user_names,
                    "approvers": simplified_approvers,
                    "subj": approve_data.get("subj"),
                    "author": approve_data.get("author").get("short_name"),
                    "visor": visor_names,
                }

        except ValidationError as e:
            logfire.error(f"Validation error for task {task_id}: {str(e)}")
        except KeyError as e:
            logfire.error(
                f"Missing expected field in response for task {task_id}: {str(e)}"
            )
        except Exception as e:
            logfire.error(f"Error fetching approval for task {task_id}: {str(e)}")

        return None
