from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.db import PAYROLL, EMPLOYEES
from app.auth_utils import get_current_user, require_admin

router = APIRouter()


# ── Kenya tax calculation (2024 KRA bands) ──────────────────────────────────

def calc_paye(gross: float) -> float:
    """KRA PAYE bands (monthly). Personal relief = KES 2,400."""
    bands = [
        (24000,  0.10),
        (8333,   0.25),
        (467667, 0.30),
    ]
    tax = 0.0
    remaining = gross
    for band_limit, rate in bands:
        if remaining <= 0:
            break
        taxable = min(remaining, band_limit)
        tax += taxable * rate
        remaining -= taxable
    if remaining > 0:
        tax += remaining * 0.35
    personal_relief = 2400
    return max(0, round(tax - personal_relief, 2))


def calc_nhif(gross: float) -> float:
    """NHIF deduction bands (2024)."""
    if gross <= 5999:     return 150
    if gross <= 7999:     return 300
    if gross <= 11999:    return 400
    if gross <= 14999:    return 500
    if gross <= 19999:    return 600
    if gross <= 24999:    return 750
    if gross <= 29999:    return 850
    if gross <= 34999:    return 900
    if gross <= 39999:    return 950
    if gross <= 44999:    return 1000
    if gross <= 49999:    return 1100
    if gross <= 59999:    return 1200
    if gross <= 69999:    return 1300
    if gross <= 79999:    return 1400
    if gross <= 89999:    return 1500
    if gross <= 99999:    return 1600
    return 1700


NSSF_TIER1_LIMIT  = 7000
NSSF_TIER2_LIMIT  = 36000
NSSF_RATE         = 0.06

def calc_nssf(gross: float) -> float:
    """NSSF (new rates) Tier I + Tier II."""
    tier1 = min(gross, NSSF_TIER1_LIMIT) * NSSF_RATE
    tier2 = max(0, min(gross, NSSF_TIER2_LIMIT) - NSSF_TIER1_LIMIT) * NSSF_RATE
    return round(tier1 + tier2, 2)


# ────────────────────────────────────────────────────────────────────────────

@router.get("/")
def list_payroll(month: str, _user=Depends(get_current_user)):
    return [p for p in PAYROLL if p["month"] == month]


@router.get("/summary")
def payroll_summary(month: str, _user=Depends(get_current_user)):
    records = [p for p in PAYROLL if p["month"] == month]
    return {
        "month": month,
        "headcount":   len(records),
        "total_gross": sum(r["gross_pay"] for r in records),
        "total_net":   sum(r["net_pay"]   for r in records),
        "total_paye":  sum(r["paye"]      for r in records),
        "total_nhif":  sum(r["nhif"]      for r in records),
        "total_nssf":  sum(r["nssf"]      for r in records),
        "pending":     sum(1 for r in records if r["status"] == "pending"),
        "processed":   sum(1 for r in records if r["status"] == "processed"),
    }


@router.post("/run")
def run_payroll(month: str, _admin=Depends(require_admin)):
    """
    Re-calculates PAYE/NHIF/NSSF for every active employee and marks them processed.
    Also inserts records for any active employee not yet in the payroll for this month.
    """
    existing_ids = {p["employee_id"] for p in PAYROLL if p["month"] == month}
    next_id = max((p["id"] for p in PAYROLL), default=0) + 1

    for emp in EMPLOYEES:
        if emp["status"] != "active":
            continue
        gross = emp["basic_salary"] + emp["allowances"]
        paye  = calc_paye(gross)
        nhif  = calc_nhif(gross)
        nssf  = calc_nssf(gross)
        net   = round(gross - paye - nhif - nssf, 2)

        if emp["id"] in existing_ids:
            record = next(p for p in PAYROLL if p["employee_id"] == emp["id"] and p["month"] == month)
            record.update({"gross_pay": gross, "paye": paye, "nhif": nhif,
                           "nssf": nssf, "net_pay": net, "status": "processed"})
        else:
            PAYROLL.append({
                "id": next_id, "employee_id": emp["id"],
                "employee_name": emp["name"], "month": month,
                "basic_salary": emp["basic_salary"], "allowances": emp["allowances"],
                "gross_pay": gross, "paye": paye, "nhif": nhif,
                "nssf": nssf, "net_pay": net, "status": "processed",
            })
            next_id += 1

    processed = [p for p in PAYROLL if p["month"] == month]
    return {"processed": len(processed), "month": month, "records": processed}


@router.get("/employee/{employee_id}")
def employee_payroll(employee_id: int, _user=Depends(get_current_user)):
    return [p for p in PAYROLL if p["employee_id"] == employee_id]