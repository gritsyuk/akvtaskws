from typing import Any, List, Optional

from pydantic import BaseModel, Field, field_validator


class Author_tm(BaseModel):
    gid: int | None
    can_delete: bool | None
    short_name: str | None
    id: int | None

class Author_item_tm(BaseModel):
    author: Optional[str]
    date: Optional[str]
    text: Optional[str]

class VisorItem_tm(BaseModel):
    gid: int | None
    can_delete: bool | None
    short_name: str | None
    id: int | None


class ApproveItem_tm(BaseModel):
    gid: int | None
    can_delete: bool | None
    short_name: str | None
    id: int | None

class Approver_tm(BaseModel):
    till: str
    declined: bool
    department_id: int
    name: str
    can_approve: bool
    responsib_id: int
    id: int
    approved_full: bool
    approved_part: bool
    department: str
    approved_date: str
    status: int


class File_tm(BaseModel):
    sequence: int | None
    vlink: str | None
    cdate: str | None
    can_view: bool | None
    size: int | None
    is_picture: bool | None
    can_delete: bool | None
    name: str | None
    link: str | None
    id: int | None
    can_add: bool | None
    msg_id: int | None


class Avatar_tm(BaseModel):
    path: str | None
    uid: int | None


class Status_tm(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None
    title: Optional[str] = None


class Message_tm(BaseModel):
    is_private: bool | None
    is_system: bool | None
    author: str | None
    created: str | None
    can_edit: bool | None
    avatar: Avatar_tm | None
    is_telegram: bool | None
    is_author: bool | None
    can_delete: bool | None
    files: List[File_tm] | None
    html: str | None
    id: int | None
    to: str | None
    author_id: int | None
    status: Optional[Status_tm] | None


class ExecItem(BaseModel):
    gid: int | None
    can_delete: bool | None
    short_name: str | None
    id: int | None



class Approve_tm(BaseModel):
    building_id: Optional[int] = None
    parent: Optional[int] = None
    df_exported: Optional[bool] = None
    df_exporting: Optional[bool] = None
    coexec: Optional[List] = None
    program_id: Optional[int] = None
    approvers: Optional[List[Approver_tm]] = None
    can_cancel: Optional[bool] = None
    type: Optional[str] = None
    building: Optional[str] = None
    building_allio: Optional[str] = None
    is_author: Optional[bool] = None
    can_delete: Optional[bool] = None
    id: Optional[int] = None
    subj: Optional[str] = None
    hiprio: Optional[bool] = None
    sep: Optional[bool] = None
    is_closed: Optional[bool] = None
    building_name: Optional[str] = None
    approve_msg: Optional[Any] = None
    can_write: Optional[bool] = None
    created: Optional[str] = None
    author: Author_tm | dict
    status_name: Optional[str] = None
    contract_name: Optional[str] = None
    pre_exp_days: Optional[int] = None
    can_docflow_export: Optional[bool] = None
    xdate: Optional[str] = None
    tags: Optional[List[str]] = None
    xnotify: Optional[int] = None
    cancel_reason: Optional[str] = None
    visor: Optional[List[VisorItem_tm]] = None
    is_archived: Optional[bool] = None
    approve: Optional[List[ApproveItem_tm]] = None
    is_unread: Optional[bool] = None
    files: Optional[List[File_tm]] = None
    messages: Optional[List[Message_tm]] = None
    realm: Optional[int] = None
    nosms: Optional[bool] = None
    template_id: Optional[int] = None
    fields: Optional[List[dict]] = None
    exec: Optional[List[ExecItem]] = None
    status: Status_tm | None


class Task_list(BaseModel):
    msg: Optional[Author_item_tm] = None
    approve_xdate: Optional[str] = None
    approve_expired: Optional[bool] = None
    files_count: Optional[int] = None
    is_new: Optional[bool] = None
    created: Optional[str] = None
    link: Optional[str] = None
    to_me: Optional[bool] = None
    building: Optional[str] = None
    xdate: Optional[str] = None
    is_expired: Optional[bool] = None
    to_count: Optional[int] = None
    modified: Optional[str] = None
    working: Optional[int] = None
    from_: str = Field(..., alias='from', default_factory=str)
    id: Optional[int] = None
    to: Optional[str] = None
    subj: Optional[str] = None
    hiprio: Optional[bool] = None
    from_me: Optional[bool] = None
    status: Status_tm | None

    @field_validator('msg', mode='before')
    @classmethod
    def check_msg(cls, value):
        if value == {}:
            return None
        return value
