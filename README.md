# HRMS Customization (ERPNext v15)

This app extends **ERPNext HRMS v15** with features in **Recruitment, Employee Lifecycle, Payroll, and Taxation**.  
It is built as a **separate app** to keep ERPNext core clean and upgrade-safe.

---

## 🚀 Features

### 🔹 Recruitment
- **Custom Recruitment Workflow**  
  `Job Opening → Application → Screening → Interview → Offer → Hired`
  <img width="1919" height="974" alt="image" src="https://github.com/user-attachments/assets/79ab7964-5a10-4a10-82e2-a8ba2d1fe393" />

- Role-based permissions for **HR Manager, Interviewer, Hiring Manager**
- Added custom field in **Job Applicant** → *Source of Application* (LinkedIn, Referral, Job Portal, etc.)
- <img width="1191" height="895" alt="image" src="https://github.com/user-attachments/assets/dee0063d-48e7-4100-b2e9-e645f607b134" />

- Dashboard + Report → **Applicants by Source**
- <img width="1916" height="968" alt="image" src="https://github.com/user-attachments/assets/aba39181-db24-4105-9faf-f4ab0b79fc8c" />


### 🔹 Employee Lifecycle
- Configure stages: **Joining → Probation → Confirmation → Exit**
- Automation:
  - On **Confirmation** → Employee status auto-updated
  - On **Exit** → System generates **Experience Letter PDF**
  - <img width="1919" height="1030" alt="image" src="https://github.com/user-attachments/assets/67ec1499-bac5-4f1c-8993-66d8c0f38521" />


### 🔹 Salary & Payroll
- Salary Structure includes:
  - **Basic, HRA, Special Allowance, PF, Professional Tax**
  - Earnings & Deductions
- Payroll Entry for multiple employees
- Custom **Payroll Slip Print Format** with branding

### 🔹 Tax Regime Support
- Support for **Old & New Tax Regimes**
- Added custom field in **Employee** → *Tax Regime Preference*
- <img width="1914" height="1026" alt="image" src="https://github.com/user-attachments/assets/4750cf20-be52-4ddc-a5d1-7cd9295ff262" />
<img width="1739" height="967" alt="image" src="https://github.com/user-attachments/assets/1830e645-8d76-4270-830c-fe0048eb3c50" />


- On payroll run → correct salary structure auto-picked
- <img width="1919" height="971" alt="image" src="https://github.com/user-attachments/assets/b42e9610-37b1-4012-b0cc-90cdb73c87ae" />
<img width="1919" height="970" alt="image" src="https://github.com/user-attachments/assets/5d2000ed-bc08-46f5-a96a-9553d7aac329" />



### 🔹 Customization
- New Doctype: **Employee Investment Declaration** with fields:
  - Section 80C (LIC, PPF, ELSS, etc.)
  - Section 80D (Medical Insurance)
  - Other Exemptions

---

## 🛠 Installation

```bash
# create app
bench new-app hrms_customization

# install app on site
bench --site <yoursite> install-app hrms_customization

# migrate & restart
bench --site <yoursite> migrate
bench restart
