from pydantic import BaseModel
from typing import List, Optional
from src.parser.models.task_tm import Task_list, Approve_tm


class Page(BaseModel):
    is_cur: bool | None
    name: str | None
    is_gap: bool | None


class Pager(BaseModel):
    current: int | None
    total: int | None
    pages: List[Page]
    limit: int | None
    count: int | None


class Sorted(BaseModel):
    is_desc: bool | None
    column: str | None


class Reply(BaseModel):
    sorted: Sorted | None
    pager: Pager | None
    threads: List[Task_list]


class Response(BaseModel):
    result: int | None
    reply: Reply | None


class ApprovalResponse(BaseModel):
    result: int
    approve: Approve_tm