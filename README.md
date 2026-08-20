# CivicPulse

## Smart Civic Issue Reporting, Prioritization & Resolution System

CivicPulse is a Flask and MySQL web application that enables citizens to report civic issues and allows administrators to verify, assign, track, and resolve complaints.

## Technology Stack

- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Python
- Flask
- SQLAlchemy
- MySQL
- Flask-Login
- Git and GitHub

## User Roles

### Citizen

- Register, login and logout
- Manage profile
- Submit complaints
- Add category, location, description and up to 3 images
- View own complaints
- Track complaint status and history
- Submit one feedback after resolution

### Admin

- Login and logout
- View all complaints
- Verify or reject complaints
- Set priority
- Assign department and assigned_to person/authority
- Update permitted complaint statuses
- View complaint history
- View feedback
- Manage categories and departments

## Complaint Workflow

Submitted
↓
Verified
↓
Assigned
↓
In Progress
↓
Resolved

Alternative outcome:

Submitted → Rejected

## Priority Levels

- Low
- Medium
- High
- Critical

## Database

MySQL relational database.

Main entities:

- users
- complaints
- categories
- departments
- locations
- assignments
- complaint_images
- status_history
- feedback

## Development Phases

1. Planning — completed
2. GitHub Setup — completed
3. Requirement Analysis
4. Database Design
5. UI Design
6. Backend Development
7. Frontend Integration
8. Testing
9. Deployment
10. Documentation

## Project Boundaries

The project does NOT include:

- AI/ML
- Data Analytics
- GPS/live maps
- Notifications
- Chat/messaging
- Payments
- Mobile-native application
- Government-system integration
- Public complaint/social features
