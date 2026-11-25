# Document & Expiry Tracker

**A Custom Odoo 19 Module for Document Management, Expiration Monitoring, and Renewal Workflows.**

## Overview

Companies manage a wide range of documents with different expiration dates, including:

- Employee passports
- Work permits
- Commercial registrations
- Insurance policies
- Licenses and certificates

Managing these documents manually can result in missed expiration dates, delayed renewals, and limited visibility.

**Document & Expiry Tracker** provides a centralized solution inside Odoo to manage company documents, monitor expiration dates, automate reminders, and control the renewal lifecycle.

## Key Features

### 1. Document Management
- Create and manage company document records.
- Organize documents using configurable document types.
- Assign responsible users.
- Upload and store document attachments.
- Track issue dates and expiration dates.
- Automatically calculate remaining days.

### 2. Expiration Monitoring & Notifications
- Automatically classify documents as Active, Expiring Soon, or Expired.
- Scheduled daily expiration checks.
- Automatic reminder activities for responsible users.
- Reminder tracking to avoid duplicate notifications.
- Reset notification flags when expiration dates change.

### 3. Renewal Workflow

Manage document renewal requests through a structured workflow:

`Draft → In Progress → Waiting Approval → Completed`

Additional state: `Cancelled`

Features include:
- Automatic renewal reference generation.
- Validation of new expiration dates.
- Prevention of duplicate open renewal requests.
- Protection against outdated renewal requests when the original document's expiration date changes.
- Automatic document expiration date update after completion.

### 4. Renewal History
- Maintain a permanent history of completed renewals.
- Track previous and updated expiration dates.
- Record the user responsible for completing the renewal.
- Access renewal history directly from the related document.

### 5. User Interface & Reporting
- Kanban, List, and Form views.
- Search and filtering capabilities.
- Document status monitoring.
- Dashboard and reporting views.
- Smart buttons for quick access to related records.

## Business Workflow

1. Create a document and assign its type and responsible user.
2. Enter its issue and expiration dates.
3. The system calculates the remaining days and determines its status.
4. Scheduled checks create reminder activities as expiration approaches.
5. A responsible user creates a renewal request.
6. The request moves through the renewal workflow.
7. Once completed, the document's expiration date is updated and a renewal history record is created.

## Technical Stack

| Component | Technology |
|---|---|
| ERP Platform | Odoo 19 |
| Programming Language | Python |
| User Interface | XML Views |
| Frontend | JavaScript, XML, SCSS |
| Database | PostgreSQL |
| Data Access | Odoo ORM |
| Automation | Scheduled Actions (Cron) |
| Notifications | Odoo Mail Activities |
| Communication | Mail Thread & Activity Mixin |

## Module Structure

```text
document_expiry_tracker/
├── models/
│   ├── document_tracker.py
│   ├── document_type.py
│   ├── document_renewal.py
│   ├── document_renewal_history.py
│   ├── document_tracker_notification.py
│   └── document_dashboard.py
├── views/
│   ├── document_tracker_views.xml
│   ├── document_type_views.xml
│   ├── document_renewal_views.xml
│   ├── document_renewal_history_views.xml
│   ├── document_tracker_search_views.xml
│   ├── document_tracker_report_views.xml
│   ├── document_renewal_report_views.xml
│   ├── document_dashboard_action.xml
│   ├── document_dashboard_menus.xml
│   ├── document_sequence.xml
│   └── document_cron.xml
├── security/
│   └── ir.model.access.csv
├── static/
│   └── src/
│       ├── js/
│       ├── scss/
│       └── xml/
├── __init__.py
├── __manifest__.py
└── README.md
```

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/amarelsalamty-7/odoo-document-expiry-tracker.git
   ```

2. Copy `document_expiry_tracker` into your custom addons directory.
3. Add the custom addons directory to your Odoo `addons_path`.
4. Restart the Odoo server.
5. Activate Developer Mode.
6. Update the Apps List.
7. Search for **Document & Expiry Tracker**.
8. Install the module.

## Project Status

**Development:** Core features implemented.

**Testing:** End-to-end testing pending.

**Security:** Access rights configuration and validation pending.

## Author

**Ammar Elsalamty**

GitHub: [@amarelsalamty-7](https://github.com/amarelsalamty-7)

