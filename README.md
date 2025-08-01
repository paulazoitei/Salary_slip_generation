# Flask Salary Slip Generation – Automated PDF/Excel Delivery API with Monitoring

This Python microservice is built with **Flask** and designed to:

- Generate personalized salary slips in **PDF** for each employee
- Generate aggregated **Excel** reports for managers
- Send documents via **email**, based on employee role
- Automatically archive all sent files (PDF & Excel) for audit purposes
- Monitor application performance via **Flask-MonitoringDashboard**

---

## Features

- Modular architecture with `controllers/`, `services/`, `models/`
- Salary data stored and retrieved from **PostgreSQL**
- PDF generation using **ReportLab**
- Excel file generation using **Pandas**
- Email delivery via **smtplib** (SMTP-based)
- Archiving mechanism based on file-based "flags"
- Real-time route monitoring via **Flask-MonitoringDashboard**
- Configuration handled through external `config.cfg` (ignored by Git)

---

## Application Flow

1. **PDFs are generated and sent** to all employees with role `EMPLOYEE`
2. **An Excel report is created and sent** to the manager (`role = MANAGER`)
3. **Archiving logic is triggered automatically** once both types of files are confirmed as sent
4. All files are copied to the `/archive/pdf/YYYY-MM/` and `/archive/excel/YYYY-MM/` folders

---

## API Endpoints

| Method | Endpoint                        | Description                                                                |
|--------|----------------------------------|----------------------------------------------------------------------------|
| POST   | `/createAggregatedEmployeeData` | Generates an Excel report for selected employee IDs                        |
| POST   | `/sendAggregatedEmployeeData`   | Sends the generated Excel report via email to the manager                  |
| POST   | `/createPdfForEmployees`        | Generates individual PDF salary slips for all employees                    |
| POST   | `/sendPdfToEmployees`           | Sends each employee their personalized PDF salary slip via email           |

---

## Monitoring Dashboard

Visit: `http://localhost:8081/dashboard`

- Requires login (credentials defined in `config.cfg`)
- Tracks request durations, outliers, route-specific metrics
- Integration via `flask_monitoringdashboard`

---

## Technologies Used

- **Python 3.11**
- **Flask**
- **SQLAlchemy + Alembic** (ORM + migrations)
- **PostgreSQL**
- **ReportLab** (PDF generation)
- **Pandas** (Excel file generation)
- **smtplib + email.message** (Email sending)
- **Flask-MonitoringDashboard** (Monitoring)

---

## Notes

- `config.cfg` and `.env` are **excluded from Git** (see `.gitignore`)
- Archive folders are dynamically created and organized by month
- Flags are stored in `temp_flags/` to synchronize PDF + Excel workflows

---

## Future Improvements

- Add file download endpoints (PDF/Excel) for manager access
- Add frontend dashboard to view report history
- Switch to background tasks with Celery for email delivery
- Add file integrity checks or encryption on archive
