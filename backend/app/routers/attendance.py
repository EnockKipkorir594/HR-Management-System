from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from app.db import ATTENDANCE, EMPLOYEES
from app.auth_utils import get_current_user, require_admin
import calendar

router = APIRouter()

VALID_STATUSES = {"present", "absent", "leave", "off"}


class AttendanceRecord(BaseModel):
    employee_id: int
    month: str   # "YYYY-MM"
    day: int
    status: str


class AttendanceMark(BaseModel):
    status: str


@router.get("/")
def get_attendance(employee_id: int, month: str, _user=Depends(get_current_user)):
    year, mon = map(int, month.split("-"))
    days_in_month = calendar.monthrange(year, mon)[1]
    records = []
    for day in range(1, days_in_month + 1):
        status = ATTENDANCE.get((employee_id, month, day), "off")
        records.append({"employee_id": employee_id, "month": month, "day": day, "status": status})
    return records


@router.get("/summary")
def attendance_summary(employee_id: int, month: str, _user=Depends(get_current_user)):
    year, mon = map(int, month.split("-"))
    days_in_month = calendar.monthrange(year, mon)[1]
    counts = {"present": 0, "absent": 0, "leave": 0, "off": 0}
    for day in range(1, days_in_month + 1):
        s = ATTENDANCE.get((employee_id, month, day), "off")
        counts[s] = counts.get(s, 0) + 1
    return counts


@router.post("/mark", status_code=200)
def mark_attendance(payload: AttendanceRecord, _admin=Depends(require_admin)):
    if payload.status not in VALID_STATUSES:
        raise HTTPException(400, f"Status must be one of {VALID_STATUSES}")
    if not any(e["id"] == payload.employee_id for e in EMPLOYEES):
        raise HTTPException(404, "Employee not found")
    ATTENDANCE[(payload.employee_id, payload.month, payload.day)] = payload.status
    return {"employee_id": payload.employee_id, "month": payload.month,
            "day": payload.day, "status": payload.status}


@router.get("/all-employees-summary")
def all_employees_summary(month: str, _admin=Depends(require_admin)):
    result = []
    for emp in EMPLOYEES:
        if emp["status"] != "active":
            continue
        summary = attendance_summary.__wrapped__(emp["id"], month, None) if hasattr(attendance_summary, '__wrapped__') else None
        year, mon = map(int, month.split("-"))
        days_in_month = calendar.monthrange(year, mon)[1]
        counts = {"present": 0, "absent": 0, "leave": 0, "off": 0}
        for day in range(1, days_in_month + 1):
            s = ATTENDANCE.get((emp["id"], month, day), "off")
            counts[s] = counts.get(s, 0) + 1
        result.append({"employee_id": emp["id"], "name": emp["name"], "department": emp["department"], **counts})
    return result