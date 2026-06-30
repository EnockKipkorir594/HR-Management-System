from fastapi import APIRouter, HTTPException, Depends
from app.db import PAYROLL, EMPLOYEES
from app.auth_utils import get_current_user

router = APIRouter()


@router.get("/{employee_id}")
def get_payslip(employee_id: int, month: str, user=Depends(get_current_user)):
    # Employees can only view their own payslip
    if user["role"] == "employee" and user["employee_id"] != employee_id:
        raise HTTPException(403, "You can only view your own payslip")

    record = next((p for p in PAYROLL if p["employee_id"] == employee_id and p["month"] == month), None)
    if not record:
        raise HTTPException(404, "No payslip found for this employee and period")

    emp = next((e for e in EMPLOYEES if e["id"] == employee_id), None)
    if not emp:
        raise HTTPException(404, "Employee not found")

    # Split allowances into house + transport for display
    house_allowance     = 5000
    transport_allowance = max(0, record["allowances"] - house_allowance)

    return {
        "reference":             f"PS-{month}-{str(employee_id).zfill(3)}",
        "pay_period":            month,
        "employee_id":           employee_id,
        "employee_name":         emp["name"],
        "job_title":             emp["job_title"],
        "department":            emp["department"],
        "email":                 emp["email"],
        "basic_salary":          record["basic_salary"],
        "house_allowance":       house_allowance,
        "transport_allowance":   transport_allowance,
        "gross_pay":             record["gross_pay"],
        "paye":                  record["paye"],
        "nhif":                  record["nhif"],
        "nssf":                  record["nssf"],
        "total_deductions":      record["paye"] + record["nhif"] + record["nssf"],
        "net_pay":               record["net_pay"],
        "payment_method":        "Bank transfer",
        "status":                record["status"],
    }