# Document & Expiry Tracker

An Odoo 19 custom module for managing company documents, tracking expiration dates, handling renewal requests, and monitoring document renewal history.

## Project Overview

Companies manage many documents with different expiration dates, such as:

- Employee passports
- Work permits
- Commercial registrations
- Insurance documents
- Licenses and certificates

Tracking these documents manually can lead to missed expiration dates, delayed renewals, and poor visibility.

**Document & Expiry Tracker** helps organize document records, monitor expiration dates, and manage the renewal process directly inside Odoo.

## Key Features

### Document Management
- Create and manage document records.
- Classify documents using Document Types.
- Assign responsible users.
- Store document attachments.
- Track issue and expiration dates.

### Expiration Tracking
- Automatically calculate remaining days.
- Identify active, expiring, and expired documents.
- Scheduled expiration checks.
- Automatic reminder activities for responsible users.

### Renewal Management
- Create renewal requests.
- Automatic renewal reference sequence.
- Renewal workflow:
  - Draft
  - In Progress
  - Waiting Approval
  - Completed
  - Cancelled
- Validate renewal dates.
- Prevent duplicate open renewal requests.

### Renewal History
- Maintain a history of completed renewals.
- Track previous and new expiration dates.
- Record the user who completed the renewal.
- Access renewal history from the document.

### User Interface
- Kanban views.
- List and form views.
- Search and filters.
- Dashboard and reporting.

## Technical Information

| Item | Technology |
|---|---|
| ERP | Odoo 19 |
| Language | Python |
| Views | XML |
| Data Storage | PostgreSQL |
| ORM | Odoo ORM |
| Automation | Scheduled Actions |
| Notifications | Odoo Mail Activities |

## Module Structure

```text
document_expiry_tracker/
├── models/
│   ├── document_tracker.py
│   ├── document_type.py
│   ├── document_renewal.py
│   ├── document_renewal_history.py
│   └── document_tracker_notification.py
├── views/
├── data/
├── security/
├── static/
├── __init__.py
├── __manifest__.py
└── README.md
```

## Installation

1. Clone or download this repository.
2. Place the module inside an Odoo custom addons directory.
3. Add the custom addons directory to the Odoo addons path.
4. Restart the Odoo server.
5. Activate Developer Mode.
6. Update the Apps List.
7. Search for **Document & Expiry Tracker**.
8. Install the module.

## Project Status

Development completed. Final testing and security configuration are pending.

## Author

Ammar Elsalamty