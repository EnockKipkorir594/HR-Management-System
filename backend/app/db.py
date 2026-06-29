"""
db.py — in-memory store.
Replace with SQLAlchemy + Alembic + PostgreSQL when you're ready.
"""
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

USERS = [
    {"id": 1, "username": "enock_admin", "hashed_password": "$2b$12$7bgxbB2qFTfGt8sb4chAK.OzDWk8znAnwjdXZLd.512HgbizDMtW2",
     "name": "Enock Kipkorir", "initials": "EK", "role": "admin", "employee_id": 5},
    {"id": 2, "username": "alice_emp",   "hashed_password": "$2b$12$pIOk0Jr3bu8uoswg1NkyfeoKPZ.j5CASHiKLaeHAaDwDeucXrvalm",
     "name": "Alice Wanjiku",  "initials": "AW", "role": "employee", "employee_id": 1},
    {"id": 3, "username": "brian_emp",   "hashed_password": "$2b$12$pIOk0Jr3bu8uoswg1NkyfeoKPZ.j5CASHiKLaeHAaDwDeucXrvalm",
     "name": "Brian Otieno",   "initials": "BO", "role": "employee", "employee_id": 2},
]

EMPLOYEES = [
    {"id":1,  "name":"Alice Wanjiku",  "department":"Engineering","job_title":"Software Engineer",  "basic_salary":85000,"allowances":8000,"status":"active",  "role":"employee","email":"alice@company.co.ke"},
    {"id":2,  "name":"Brian Otieno",   "department":"HR",         "job_title":"HR Officer",         "basic_salary":52000,"allowances":5000,"status":"active",  "role":"employee","email":"brian@company.co.ke"},
    {"id":3,  "name":"Carol Muthoni",  "department":"Engineering","job_title":"Senior Engineer",     "basic_salary":91000,"allowances":8000,"status":"active",  "role":"employee","email":"carol@company.co.ke"},
    {"id":4,  "name":"David Kamau",    "department":"Finance",    "job_title":"Accountant",          "basic_salary":60000,"allowances":5000,"status":"inactive","role":"employee","email":"david@company.co.ke"},
    {"id":5,  "name":"Enock Kipkorir", "department":"Engineering","job_title":"Backend Engineer",    "basic_salary":90000,"allowances":8000,"status":"active",  "role":"admin",   "email":"enock@company.co.ke"},
    {"id":6,  "name":"Eve Akinyi",     "department":"HR",         "job_title":"Talent Acquisition",  "basic_salary":55000,"allowances":5000,"status":"active",  "role":"employee","email":"eve@company.co.ke"},
    {"id":7,  "name":"Faith Njoroge",  "department":"Finance",    "job_title":"Finance Analyst",     "basic_salary":65000,"allowances":6000,"status":"active",  "role":"employee","email":"faith@company.co.ke"},
    {"id":8,  "name":"George Ouma",    "department":"Engineering","job_title":"DevOps Engineer",     "basic_salary":88000,"allowances":8000,"status":"active",  "role":"employee","email":"george@company.co.ke"},
    {"id":9,  "name":"Hilda Waweru",   "department":"HR",         "job_title":"HR Manager",          "basic_salary":75000,"allowances":7000,"status":"active",  "role":"employee","email":"hilda@company.co.ke"},
    {"id":10, "name":"Ian Mutua",      "department":"Finance",    "job_title":"Finance Manager",     "basic_salary":80000,"allowances":7000,"status":"inactive","role":"employee","email":"ian@company.co.ke"},
]

# attendance: keyed (employee_id, month, day) -> status
ATTENDANCE = {}
_raw = [
    (1,"2025-04",1,"present"),(1,"2025-04",2,"present"),(1,"2025-04",3,"present"),
    (1,"2025-04",4,"absent"), (1,"2025-04",5,"present"),(1,"2025-04",6,"off"),
    (1,"2025-04",7,"off"),    (1,"2025-04",8,"present"),(1,"2025-04",9,"leave"),
    (1,"2025-04",10,"leave"), (1,"2025-04",11,"present"),(1,"2025-04",12,"present"),
    (1,"2025-04",13,"off"),   (1,"2025-04",14,"off"),   (1,"2025-04",15,"present"),
    (1,"2025-04",16,"present"),(1,"2025-04",17,"present"),(1,"2025-04",18,"present"),
    (1,"2025-04",19,"present"),(1,"2025-04",20,"off"),  (1,"2025-04",21,"off"),
    (1,"2025-04",22,"present"),(1,"2025-04",23,"present"),(1,"2025-04",24,"present"),
    (1,"2025-04",25,"absent"), (1,"2025-04",26,"present"),(1,"2025-04",27,"off"),
    (1,"2025-04",28,"off"),   (1,"2025-04",29,"present"),(1,"2025-04",30,"present"),
    (2,"2025-04",1,"present"),(2,"2025-04",2,"present"),(2,"2025-04",3,"leave"),
    (2,"2025-04",4,"leave"),  (2,"2025-04",5,"present"),(2,"2025-04",6,"off"),
    (2,"2025-04",7,"off"),    (2,"2025-04",8,"present"),(2,"2025-04",9,"present"),
    (2,"2025-04",10,"present"),(2,"2025-04",11,"present"),(2,"2025-04",12,"absent"),
    (2,"2025-04",13,"off"),   (2,"2025-04",14,"off"),   (2,"2025-04",15,"present"),
]
for eid, month, day, status in _raw:
    ATTENDANCE[(eid, month, day)] = status

PAYROLL = [
    {"id":1,"employee_id":1,"employee_name":"Alice Wanjiku", "month":"2025-04","basic_salary":85000,"allowances":8000,"gross_pay":93000,"paye":18820,"nhif":1700,"nssf":720,"net_pay":71760,"status":"processed"},
    {"id":2,"employee_id":2,"employee_name":"Brian Otieno",  "month":"2025-04","basic_salary":52000,"allowances":5000,"gross_pay":57000,"paye":9600, "nhif":1700,"nssf":720,"net_pay":44980,"status":"processed"},
    {"id":3,"employee_id":3,"employee_name":"Carol Muthoni", "month":"2025-04","basic_salary":91000,"allowances":8000,"gross_pay":99000,"paye":21900,"nhif":1700,"nssf":720,"net_pay":74680,"status":"processed"},
    {"id":4,"employee_id":5,"employee_name":"Enock Kipkorir","month":"2025-04","basic_salary":90000,"allowances":8000,"gross_pay":98000,"paye":21500,"nhif":1700,"nssf":720,"net_pay":74080,"status":"pending"},
    {"id":5,"employee_id":6,"employee_name":"Eve Akinyi",    "month":"2025-04","basic_salary":55000,"allowances":5000,"gross_pay":60000,"paye":10600,"nhif":1700,"nssf":720,"net_pay":46980,"status":"pending"},
    {"id":6,"employee_id":7,"employee_name":"Faith Njoroge", "month":"2025-04","basic_salary":65000,"allowances":6000,"gross_pay":71000,"paye":13200,"nhif":1700,"nssf":720,"net_pay":55380,"status":"pending"},
    {"id":7,"employee_id":8,"employee_name":"George Ouma",   "month":"2025-04","basic_salary":88000,"allowances":8000,"gross_pay":96000,"paye":20200,"nhif":1700,"nssf":720,"net_pay":73380,"status":"pending"},
    {"id":8,"employee_id":9,"employee_name":"Hilda Waweru",  "month":"2025-04","basic_salary":75000,"allowances":7000,"gross_pay":82000,"paye":16100,"nhif":1700,"nssf":720,"net_pay":63480,"status":"pending"},
]