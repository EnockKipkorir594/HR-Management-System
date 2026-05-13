# HR AND PAYROLL MANAGEMENT SYSTEM 
Web based HR Management system with a payroll calculator

## Key User Roles and Access Managemnt
To ensure security and separation of duties, the system must enforce strict Role Based Access Control(RBAC)
- **Employee**: The baseline user. Needs a self-service portal to view payslips, apply for time off, update
  personal information (next of kin, bank details), view company policies, and access the organizational chart.

- **Manager(Line Manager)**: Mid-level access. Needs to view their direct reports, approve or reject leave
  applications, view team attendance metrics, conduct performance appraisals, and initiate recruitment or
  offboarding requests for their team.
  
- **HR Admin**: Administrative access for human capital. Needs to onboard/offboard staff, manage organizational
  charts, maintain employee records, track disciplinary actions, manage company assets, and configure leave policies.

- **Payroll Officer**: Financial administrative access. Needs to run payroll batches, manage statutory and custom
  deductions/earnings, process salary advances, generate compliance reports (tax, pension, health), and trigger
  disbursements.

- **Super Admin**: IT/System level access. Needs to manage global system configurations, user roles, security
  policies, API integrations, and review system audit logs.

## 2 & 3. Care Modules and Feature Specifications.
### Module 1 : Core HR & Employee Data Management 
This module acts as single source of truth for all employee data.
- **Digital Onboarding Workflow**: Automated checklists for new hires (document collection, IT provisioning, contract signing).
- **Centralized Employee Directory**: Searchable database with comprehensive profiles (demographics, job history, contact info).
- **Document Vault**: Secure upload and storage of contracts, IDs, academic certificates, and compliance forms.
- **Asset Management**: Tracking of company property (laptops, phones, vehicles) assigned to employees.
- **Offboarding Management**: Automated checklists for clearance, asset recovery, and final exit interviews.
- **Disciplinary & Grievance Tracking**: Secure logging of warnings, PIPs (Performance Improvement Plans), and disciplinary hearings.
- **Dynamic Org Chart Genenaration**: Auto-updating visual hierarchy based on reporting lines.

### Module 2 : Time and Leave Management
Handles availability, absence and attendance tracking. 
- **Leave Application & Approval Workflow**: Multi-tier approval routing for annual, sick, maternity, and compassionate leave.
- **Automated Leave Accruals**: System-calculated leave balances based on tenure, carry-over rules, and company policy.
- **Public Holiday Calendar**: Configurable calendar for national and regional public holidays (e.g., Kenyan public holidays).
- **Timesheets & Attendance Tracking**: Daily or weekly time logging for hourly or shift-based workers.
- **Overtime Computation**: Rules engine to calculate 1.5x or 2.0x overtime rates automatically linked to payroll.
- **Biometric/Hardware Integration Engine**: APIs to pull clock-in/clock-out data from office fingerprint or RFID scanners.

### Module 3 : Payroll Processing & Compensation
The financial engine of the application. Requires high precision and auditability.
- **Dynamic Payroll Processing**: Support for weekly, bi-weekly, or monthly pay cycles with pre-run validation checks.
- **Custom Earnings & Deductions Builder**: Ability to create one-off or recurring allowances (e.g., transport) and deductions (e.g., loans).
- **Statutory Deductions Engine**: Automated, rule-based calculation of PAYE, Social Security, Health Insurance, and Housing Levies.
- **Loan & Salary Advance Management**: Amortization tracking that automatically deducts installments from subsequent payrolls.
- **Automated Payslip Generation**: PDF payslips automatically emailed to employees or published to their self-service portal (password protected).
- **Proration Engine**: Automatic salary calculation for employees joining or leaving mid-month.
- **Off-Cycle Payroll Runs**: Support for ad-hoc payments like annual bonuses, commissions, or severance packages.

### Module 4 : Repoarting & Analytics
Empowers management with actionable data and ensures statutory compliance 
- **Statutory Export Files**: Auto-generated CSV/Excel formats for KRA (P10, P9 forms), NSSF, and Health Fund portals.
- **Payroll Variance Reports**: Month-over-month comparison highlighting significant changes in the wage bill.
- **Custom Report Builder**: Drag-and-drop interface to generate ad-hoc reports across any HR or payroll data points.
- **Headcount & Attrition Dashboard**: Visual charts tracking employee turnover, diversity, and department growth.
- **Bank/Disbursement Export**: Standardized EFT (Electronic Funds Transfer) files formatted for local banks.
- **Comprehensive Audit Trails**: Unalterable logs tracking who changed what data and when (critical for financial security).

## 4. Recommended Technology Stack 
- **Frontend (User Interface)**: React.js or Next.js using TypeScript. Paired with Tailwind CSS for styling and a component library like
  MUI (Material-UI) or Shadcn/ui for fast, accessible enterprise UI elements.
- **Backend (API & Business Logic)**: Python Flask will be used for the backend during development due to its easy learning curve and
  FASTAPI for production for scalability and its Asynchronous nature to handle multiple API requests and concurrency.
- **Database (Persistence)**: PostgreSQL. Do not use a NoSQL database for payroll; you need strict ACID compliance, relational integrity,
  and transaction rollbacks for financial data. Use Redis for session management and caching.
- **Authentication & Security**: Keycloak (open-source, self-hosted) or Auth0 (managed SaaS). These provide out-of-the-box SSO,
  MFA (Multi-Factor Authentication), and password policies.
- **File Storage**: AWS S3 or Azure Blob Storage. Ensure buckets are private and access to sensitive employee documents is governed by signed
   URLs generated by the backend.

## 5. Potential Integrations
To make the system a true enterprise hub, plan for the following integrations:
- **Payment Gateways (Kenya Specific)**:
      - **MPESA B2C API**: For instant disbursement of wages, casual worker pay, or salary advances directly to mobile wallets.
      - **Pesalink/Bank APIs**: Direct integration with banks (e.g., Equity, KCB, NCBA) for automated bulk salary transfers via host-to-host
         (H2H) connections.
- **Accounting/ERP Systems**: Bi-directional sync with Xero, QuickBooks Online, SAP, or Microsoft Dynamics to post payroll journals automatically.
    - **Identity Providers**: Google Workspace or Microsoft Entra ID (formerly Azure AD) so employees can log in using their existing company emails (SSO).
    - **Government Portals**: KRA iTax API (where available, or optimized file generation for manual upload) and eCitizen APIs for identity verification
        (e.g., verifying an employee's National ID during onboarding).

## 6. Key Compliance Requirements (Kenyan Context)
Designing for the Kenyan market requires strict adherence to local laws. Your system architecture must natively support the following rules as of 2026:
- **PAYE (Pay As You Earn)**: Dynamic tax bands. The system must easily update when the Finance Act changes tax brackets, personal relief, and 
      insurance relief.
- **NSSF (National Social Security Fund)**: Support for both Tier 1 and Tier 2 contributions, automatically capping based on the legally defines
      lower and upper earning limits.
- **SHIF (Social Health Insurance Fund)**: Note: SHIF replaced NHIF under the Social Health Authority (SHA). The system must calculate the 
      mandatory 2.75% gross salary deduction with no upper cap, replacing the old tiered NHIF system.
- **Affordable Housing Levy (AHL)**: Mandatory deduction of 1.5% of gross salary by the employee, matched by 1.5% from the employer.
- **NITA (National Industrial Training Authority)**: Tracking and generating the standard monthly employer contribution per employee.
- **Data Protection Act (DPA Kenya)**: The architecture must ensure Data Privacy by Design. This includes encrypting PII (Personally Identifiable
      Information) at rest, supporting "Right to be Forgotten" workflows, and registering the system as a data processor with the Office of the Data
      Protection Commissioner (ODPC).
- **Employment Act, 2007**: System logic must enforce statutory minimums (e.g., 21 days annual leave, 3 months maternity leave, 2 weeks paternity leave).
