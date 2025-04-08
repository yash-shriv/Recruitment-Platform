# JobSphere - Recruitment Portal

![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=flat&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)

A full-featured recruitment platform built with Django that connects employers with job seekers through intelligent matching and automated workflows.

## Key Features

### 🛠️ Role-Based Portal
- **Recruiters** can post jobs, filter applicants, and send automated updates
- **Job Seekers** can search listings, apply, and track application status
- Secure authentication with custom user models and role-based access control

### 🔍 Smart Search System
- Dynamic job/applicant matching using Django ORM
- Case-insensitive keyword search with Q-objects
- Multi-field filtering (skills, titles, companies)

### ⚡ Automated Workflows
- Real-time email notifications (Celery + Redis)
- Account verification & password resets
- Application status updates via Gmail SMTP

### 🗂️ File Management
- Resume upload/download functionality
- Paginated job listings and applications
- Role-based post-login redirection

## Technical Implementation
- **Backend**: Django with custom user models
- **Database**: MySQL with optimized queries
- **Async Tasks**: Celery + Redis for email processing
- **Search**: Django Q-objects with `icontains` filters
- **Security**: Role-based access control (RBAC)

## Why This Stands Out
This project demonstrates:
- Full-stack development with complex workflows
- Database design and query optimization
- Asynchronous task handling
- Secure authentication patterns
- User experience considerations

*Note: This was developed as a portfolio project to showcase Django expertise and web design capabilities.*
