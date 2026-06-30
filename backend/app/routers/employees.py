from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.db import EMPLOYEES
from app.auth_utils import get_current_user, require_admin

router = APIRouter()


class EmployeeOut(BaseModel):
    id: int
    name: str
    department: str
    job_title: str
    basic_salary: float
    allowances: float
    status: str
    role: str
    email: str


class EmployeeCreate(BaseModel):
    name: str
    department: str
    job_title: str
    basic_salary: float
    allowances: float
    status: str = "active"
    role: str = "employee"
    email: str


@router.get("/", response_model=List[EmployeeOut])
def list_employees(
    status: Optional[str] = None,
    department: Optional[str] = None,
    search: Optional[str] = None,
    _user=Depends(get_current_user),
):
    result = EMPLOYEES[:]
    if status:
        result = [e for e in result if e["status"] == status]
    if department:
        result = [e for e in result if e["department"].lower() == department.lower()]
    if search:
        q = search.lower()
        result = [e for e in result if q in e["name"].lower()
                  or q in e["department"].lower()
                  or q in e["job_title"].lower()]
    return result


@router.get("/stats")
def stats(_user=Depends(get_current_user)):
    total   = len(EMPLOYEES)
    active  = sum(1 for e in EMPLOYEES if e["status"] == "active")
    depts   = {}
    for e in EMPLOYEES:
        depts[e["department"]] = depts.get(e["department"], 0) + 1
    return {"total": total, "active": active, "inactive": total - active, "by_department": depts}


@router.get("/{eid}", response_model=EmployeeOut)
def get_employee(eid: int, _user=Depends(get_current_user)):
    emp = next((e for e in EMPLOYEES if e["id"] == eid), None)
    if not emp:
        raise HTTPException(404, "Employee not found")
    return emp


@router.post("/", response_model=EmployeeOut, status_code=201)
def create_employee(payload: EmployeeCreate, _admin=Depends(require_admin)):
    # Check duplicate email
    if any(e["email"].lower() == payload.email.lower() for e in EMPLOYEES):
        raise HTTPException(400, "An employee with this email already exists")
    new_id = max(e["id"] for e in EMPLOYEES) + 1
    emp = {"id": new_id, **payload.model_dump()}
    EMPLOYEES.append(emp)
    return emp


@router.put("/{eid}", response_model=EmployeeOut)
def update_employee(eid: int, payload: EmployeeCreate, _admin=Depends(require_admin)):
    emp = next((e for e in EMPLOYEES if e["id"] == eid), None)
    if not emp:
        raise HTTPException(404, "Employee not found")
    emp.update(payload.model_dump())
    return emp


@router.patch("/{eid}/status")
def toggle_status(eid: int, _admin=Depends(require_admin)):
    emp = next((e for e in EMPLOYEES if e["id"] == eid), None)
    if not emp:
        raise HTTPException(404, "Employee not found")
    emp["status"] = "inactive" if emp["status"] == "active" else "active"
    return {"id": eid, "status": emp["status"]}


@router.delete("/{eid}")
def delete_employee(eid: int, _admin=Depends(require_admin)):
    global EMPLOYEES
    if not any(e["id"] == eid for e in EMPLOYEES):
        raise HTTPException(404, "Employee not found")
    EMPLOYEES = [e for e in EMPLOYEES if e["id"] != eid]
    return {"deleted": eid}