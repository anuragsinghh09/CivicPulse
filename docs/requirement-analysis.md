# CivicPulse — Requirement Analysis

**Project title:** Smart Civic Issue Reporting, Prioritization & Resolution System
**Phase:** 2 — Requirement Analysis
**Status:** Complete

## 1. Project Overview

CivicPulse is a web application for reporting and managing civic issues such as potholes, garbage accumulation, water leakage, damaged street lights, and drainage problems. Citizens submit and track their own complaints. Administrators review those complaints, verify or reject them, assign a priority and department, progress the complaint through a controlled resolution workflow, and review feedback submitted after resolution.

The application is intended to demonstrate a realistic civic-service workflow using Flask, MySQL, authentication, role-based access, relational data, and maintainable web-development practices suitable for a BCA academic project.

## 2. Problem Statement

Citizens often lack a simple and transparent way to report local civic issues and follow their resolution. Authorities need a structured record of complaints, priorities, department assignments, and status updates to manage work consistently. CivicPulse addresses this gap by providing a single web-based process that records each complaint from submission to resolution while allowing citizens to see its current progress.

## 3. Functional Requirements

| ID | Requirement | Testable result |
|---|---|---|
| FR-01 | The system shall allow a citizen to register using name, email, phone, and password. | A valid registration creates one citizen account; duplicate emails are rejected. |
| FR-02 | The system shall allow registered citizens and seeded administrators to log in and log out. | Valid credentials create a session; logout ends it. |
| FR-03 | The system shall allow a logged-in citizen to view and update permitted profile details. | The citizen can view and save their own permitted profile data. |
| FR-04 | The system shall allow a citizen to submit a complaint with a category, location, description, and optional images. | A valid submission creates a complaint with initial status `Submitted`. |
| FR-05 | The system shall obtain complaint categories from maintained category records. | The submission form lists configured categories: Road, Garbage, Water, Street Light, Drainage, and Other. |
| FR-06 | The system shall store a separate location record for each complaint. | Each complaint contains area, city, and pincode; latitude and longitude are optional. |
| FR-07 | The system shall permit a maximum of three validated image uploads per complaint. | A fourth image or an invalid image file is rejected. |
| FR-08 | The system shall allow a citizen to view only their submitted complaints and their current statuses. | A citizen cannot access another citizen's complaint list or details. |
| FR-09 | The system shall show a citizen the details, images, assignment information where appropriate, current status, and status history of their own complaint. | The complaint detail view displays the stored complaint data and history. |
| FR-10 | The system shall show a citizen dashboard with total, pending, and resolved complaint counts, recent complaints, and current statuses. | Dashboard figures are calculated only from the logged-in citizen's complaints. |
| FR-11 | The system shall allow the complaint owner to submit one rating and comment after the complaint is resolved. | Feedback is accepted once only for a resolved complaint owned by the logged-in citizen. |
| FR-12 | The system shall show an administrator dashboard with complaint counts by status and high/critical priority counts. | Dashboard totals reflect all complaints visible to administrators. |
| FR-13 | The system shall allow an administrator to view all complaints, details, images, status history, assignment history, and feedback. | An administrator can access these records without being the complaint owner. |
| FR-14 | The system shall allow an administrator to verify a submitted complaint or reject it with a recorded reason or note. | The status changes only to `Verified` or `Rejected`, and history is recorded. |
| FR-15 | The system shall allow an administrator to set or change a complaint priority: Low, Medium, High, or Critical. | Only these four values can be saved. |
| FR-16 | The system shall allow an administrator to assign a verified complaint to a configured department and enter an `assigned_to` person/authority value. | Assignment is recorded with complaint, department, assigned_to, and assignment date. |
| FR-17 | The system shall enforce the approved controlled complaint workflow. | Unsupported status jumps, reversals, or changes from terminal statuses are rejected. |
| FR-18 | The system shall record every status change in complaint status history. | Each change stores the complaint, resulting status, timestamp, and user who made the change. |
| FR-19 | The system shall allow authorized administrators to manage category and department records if this administrative screen is included. | Changes are available only to administrators and are reflected in future selections. |

## 4. Non-Functional Requirements

| ID | Requirement | Testable result |
|---|---|---|
| NFR-01 | The interface shall be responsive and usable on desktop and mobile-sized screens. | Key pages remain readable and operable without horizontal page scrolling at common mobile widths. |
| NFR-02 | The interface shall use consistent navigation, labels, spacing, status badges, priority indicators, and success/error messages. | Equivalent controls are named and styled consistently across citizen and administrator areas. |
| NFR-03 | All forms shall have visible labels and clear validation feedback. | A user can identify required inputs and understand why invalid input was rejected. |
| NFR-04 | The system shall protect passwords, sessions, access-controlled pages, and uploaded files. | Security tests confirm the controls listed in Section 17. |
| NFR-05 | The database design shall preserve relational integrity through keys, constraints, and relationships. | Invalid foreign-key references and duplicate restricted records are prevented. |
| NFR-06 | Complaint history and assignment records shall be retained for auditability. | Existing history is displayed after later status or assignment updates. |
| NFR-07 | The codebase and documentation shall remain understandable for a BCA project. | Components are separated by concern and major rules can be explained from documentation. |
| NFR-08 | Normal list, detail, login, and complaint-submission actions shall provide a clear outcome without exposing technical error details. | The user receives a safe success or error message for valid and invalid actions. |

## 5. Citizen Requirements

A citizen shall be able to:

- Register, log in, and log out.
- View and update their profile.
- Submit a complaint with a database-backed category, per-complaint location, description, and up to three images.
- View a dashboard summarising only their own complaints.
- View a list of their complaints, each complaint's details, current status, and status history.
- Submit exactly one rating and comment after one of their complaints is resolved.

## 6. Admin Requirements

An administrator shall be able to:

- Log in and log out using a seeded administrator account; no public admin registration is required.
- View the administrator dashboard and all complaints.
- View a complaint's details, images, status history, assignment history, and citizen feedback.
- Verify or reject a submitted complaint.
- Set or change priority.
- Assign a department and record an `assigned_to` person/authority.
- Update a complaint only through the allowed workflow transitions.
- Manage categories and departments where the administrative management interface is included.

## 7. Authentication and Authorization Requirements

- Passwords shall be stored only as secure password hashes; plain-text passwords shall never be stored or returned.
- Login shall authenticate using an email and password.
- Logout shall invalidate the active authenticated session.
- Citizen-only pages shall require an authenticated citizen session.
- Administrator-only pages and actions shall require an authenticated administrator session.
- A citizen may access only their own profile, complaints, images, and feedback action.
- An administrator may access complaint-management actions and all complaint records.
- Direct URL access to a protected resource without the appropriate role shall be denied safely.
- Administrator accounts shall be established through seed data/database administration only; there shall be no administrator registration feature.

## 8. Complaint Submission Requirements

- A citizen shall be authenticated before submitting a complaint.
- The complaint shall include one valid category, location information, and a meaningful description.
- The system shall create the complaint in `Submitted` status and create the initial status-history record at the same time.
- The citizen shall be recorded as the complaint owner.
- Priority shall initially use the project-defined default selected by the design; an administrator can subsequently set or change it.
- The category selection shall use category records rather than duplicated hard-coded lists throughout the system.
- Each complaint submission shall have its own location entry; saved or reusable citizen locations are outside the first version.

## 9. Complaint Workflow and Status-Transition Rules

### Allowed transitions

| Current status | Allowed next status | Rule |
|---|---|---|
| New complaint | Submitted | Created by the authenticated citizen. |
| Submitted | Verified | Administrator confirms the complaint is suitable for action. |
| Submitted | Rejected | Administrator rejects an invalid, duplicate, or unsuitable complaint and records a note. |
| Verified | Assigned | Administrator records department and `assigned_to` assignment. |
| Assigned | In Progress | Administrator records that work has begun. |
| In Progress | Resolved | Administrator records that work has completed. |
| Rejected | None | Rejected is a terminal status in the initial version. |
| Resolved | None | Resolved is a terminal status in the initial version. |

### Workflow rules

- The system shall reject arbitrary status jumps, reverse transitions, and transitions from `Rejected` or `Resolved`.
- The `Assigned` transition shall not be permitted until a department and non-empty `assigned_to` value are supplied.
- Each valid transition shall update the current complaint status and add exactly one status-history entry.
- The status history shall remain available after the complaint reaches a terminal status.
- Citizen feedback becomes available only after `Resolved`.

## 10. Priority Requirements

- Each complaint shall have one priority value: Low, Medium, High, or Critical.
- An administrator shall be able to set and change priority while the complaint is active.
- The citizen shall be able to see the current priority on their complaint details where shown by the interface.
- The administrator dashboard shall identify the count of High and Critical complaints.
- No automatic, predictive, AI, or machine-learning priority calculation is included.

## 11. Department Assignment Requirements

- Departments shall be maintained as records, initially including Road Department, Sanitation Department, Water Department, Electricity Department, Drainage Department, and General Department.
- An assignment shall record the complaint, selected department, `assigned_to` text value, and assignment date.
- The first version shall not use a separate staff or authority table.
- Reassignment shall retain prior assignment information as history rather than replacing it without a record.
- A verified complaint must receive a valid assignment before moving to `Assigned` status.

## 12. Location Requirements

- A location shall be created separately for each complaint.
- Area, city, and pincode shall be collected and validated for each submitted complaint.
- Latitude and longitude may be stored when provided, but are optional.
- The first version shall not include GPS capture, live maps, geocoding, route planning, or map APIs.

## 13. Image-Upload Requirements

- A complaint may have zero to three images.
- The server shall accept only JPEG or PNG images and reject other file types.
- The server shall reject an image file larger than 5 MB before storing it.
- Uploaded files shall be stored on the application server; the database shall store only the validated file reference/path and related metadata.
- Stored filenames shall be generated safely so that a user-supplied filename cannot overwrite another upload.
- An uploaded image shall be accessible only through an authorized complaint view.
- The system shall not store large image binary data directly in MySQL for this version.

## 14. Status-History Requirements

- The initial `Submitted` status shall be recorded when a complaint is created.
- Every later valid status change shall create a new immutable history entry.
- A history entry shall contain the complaint reference, status, change timestamp, user who made the change, and an optional note when applicable.
- The complaint detail page shall display status history in chronological order.
- History entries shall not be editable or deletable through normal citizen or administrator workflows.

## 15. Feedback Requirements

- Feedback shall be available only to the citizen who owns a resolved complaint.
- One complaint shall have at most one feedback record.
- Feedback shall contain a rating, comment, and submission date.
- The rating shall be validated as an integer from 1 through 5.
- An administrator shall be able to view feedback associated with a complaint.
- Feedback shall not be available for submitted, verified, assigned, in-progress, or rejected complaints.

## 16. Validation Rules

| Area | Validation rule |
|---|---|
| Registration | Name, email, phone, and password are required; email must be valid and unique; password must contain at least 8 characters. |
| Login | Email and password are required; invalid credentials return a generic error without identifying which field failed. |
| Profile | Citizen may update only allowed fields; email uniqueness is rechecked if email can be changed. |
| Complaint | Category, area, city, pincode, and description are required; submitted category must exist; description must not be blank. |
| Location | Pincode must contain exactly 6 digits; optional coordinates must be numeric and within valid latitude/longitude ranges when supplied. |
| Images | At most three files; each must be JPEG or PNG and no larger than 5 MB. |
| Priority | Value must be exactly Low, Medium, High, or Critical. |
| Assignment | Department must exist and `assigned_to` must be non-empty before `Assigned` is allowed. |
| Status | The requested transition must appear in the allowed transition table in Section 9. |
| Feedback | Complaint must be resolved and owned by the current citizen; rating is an integer from 1 to 5; one feedback record maximum. |

## 17. Security Requirements

- Use secure password hashing and never store or display plain-text passwords.
- Use authenticated server-side sessions with a protected secret configuration.
- Enforce role-based authorization on every protected server route and action.
- Validate all form input on the server; client-side validation may improve usability but shall not replace it.
- Use SQLAlchemy ORM or parameterized database operations to protect against SQL injection.
- Validate file extensions, content type where possible, size, file count, and generated storage filenames for uploads.
- Restrict uploaded-file access to authorized users and avoid executing uploaded content.
- Do not expose passwords, database credentials, secret keys, stack traces, or internal error details in user responses.
- Store environment-specific secrets outside version control; `.env.example` contains placeholders only.
- Apply CSRF protection to state-changing forms when the Flask implementation is introduced.

## 18. System Modules

| Module | Responsibility |
|---|---|
| Public and Authentication | Home page, registration, login, logout, sessions, and role checks. |
| Citizen Profile | Citizen profile viewing and permitted updates. |
| Complaint Reporting | Complaint form, category selection, per-complaint location, description, and image validation. |
| Citizen Complaint Tracking | Dashboard, complaint list, complaint details, current status, and history. |
| Administrator Complaint Management | All-complaint view, detail review, verification, rejection, priority, assignment, and permitted status updates. |
| Category and Department Management | Administrator maintenance of configured categories and departments if included. |
| Feedback | One post-resolution citizen feedback record and administrator feedback viewing. |
| History and Audit | Status and assignment record retention and display. |

## 19. Use Cases

| ID | Use case | Primary actor |
|---|---|---|
| UC-01 | Register citizen account | Visitor |
| UC-02 | Log in and log out | Citizen or Admin |
| UC-03 | Manage citizen profile | Citizen |
| UC-04 | Submit complaint | Citizen |
| UC-05 | View and track own complaint | Citizen |
| UC-06 | Submit resolved-complaint feedback | Citizen |
| UC-07 | Review complaint | Admin |
| UC-08 | Verify or reject complaint | Admin |
| UC-09 | Set priority and assign department | Admin |
| UC-10 | Update complaint workflow status | Admin |
| UC-11 | View feedback and history | Admin |
| UC-12 | Manage categories and departments | Admin |

## 20. Use-Case Descriptions

### UC-01 — Register Citizen Account

- **Actor:** Visitor
- **Preconditions:** The visitor is not logged in.
- **Main flow:** The visitor enters name, unique email, phone, and password. The system validates the data, hashes the password, and creates a citizen account.
- **Outcome:** The account is available for citizen login.
- **Failure conditions:** Missing, invalid, or duplicate data is rejected with a clear message.

### UC-02 — Log In and Log Out

- **Actor:** Citizen or Admin
- **Preconditions:** A valid account exists; administrator accounts are seeded.
- **Main flow:** The user supplies email and password. The system verifies the password hash, creates a role-specific session, and allows logout.
- **Outcome:** The user reaches their permitted area; logout ends the session.
- **Failure conditions:** Invalid credentials produce a generic error; protected areas remain unavailable.

### UC-03 — Manage Citizen Profile

- **Actor:** Citizen
- **Preconditions:** Citizen is authenticated.
- **Main flow:** The citizen views their profile, changes permitted data, and submits the form. The system validates and saves allowed fields.
- **Outcome:** Updated profile data is shown to the same citizen.

### UC-04 — Submit Complaint

- **Actor:** Citizen
- **Preconditions:** Citizen is authenticated.
- **Main flow:** The citizen selects a category, enters location and description, optionally attaches up to three valid images, and submits. The system validates all values, stores the complaint and location, and records `Submitted` history.
- **Outcome:** The citizen receives confirmation and can track the new complaint.
- **Failure conditions:** Invalid data, unknown category, invalid upload, or more than three images prevents submission.

### UC-05 — View and Track Own Complaint

- **Actor:** Citizen
- **Preconditions:** Citizen is authenticated and owns the complaint.
- **Main flow:** The citizen opens their dashboard, complaint list, or complaint details. The system displays current status, priority where shown, images, and chronological status history.
- **Outcome:** The citizen can see the complaint's progress.
- **Failure conditions:** Attempts to access another citizen's complaint are denied.

### UC-06 — Submit Resolved-Complaint Feedback

- **Actor:** Citizen
- **Preconditions:** Citizen owns the complaint; status is `Resolved`; no feedback exists.
- **Main flow:** The citizen provides a rating from 1 to 5 and a comment. The system validates ownership, status, and one-feedback limit before saving.
- **Outcome:** One feedback record is linked to the complaint.

### UC-07 — Review Complaint

- **Actor:** Admin
- **Preconditions:** Admin is authenticated.
- **Main flow:** The admin views dashboard totals, all complaints, and a selected complaint's details, images, location, current status, assignments, history, and feedback if present.
- **Outcome:** The admin has the information needed to take an allowed management action.

### UC-08 — Verify or Reject Complaint

- **Actor:** Admin
- **Preconditions:** Admin is authenticated; complaint status is `Submitted`.
- **Main flow:** The admin verifies the complaint or rejects it with a note. The system validates the transition and records the status-history event.
- **Outcome:** Complaint becomes `Verified` or terminal `Rejected`.

### UC-09 — Set Priority and Assign Department

- **Actor:** Admin
- **Preconditions:** Admin is authenticated; complaint is active; for assignment, status is `Verified`.
- **Main flow:** The admin selects a permitted priority. For assignment, the admin selects a department and supplies `assigned_to`; the system records the assignment and moves the complaint to `Assigned`.
- **Outcome:** Priority and assignment information are available in complaint details and history.

### UC-10 — Update Complaint Workflow Status

- **Actor:** Admin
- **Preconditions:** Admin is authenticated; requested transition is allowed.
- **Main flow:** The admin moves an assigned complaint to `In Progress`, or an in-progress complaint to `Resolved`. The system verifies the transition and appends status history.
- **Outcome:** The current status is updated and the citizen can see the new progress.
- **Failure conditions:** Skipped, reversed, or terminal-state transitions are rejected.

### UC-11 — View Feedback and History

- **Actor:** Admin
- **Preconditions:** Admin is authenticated.
- **Main flow:** The admin opens a complaint detail view and reviews status history, assignment history, and feedback if submitted.
- **Outcome:** The administrator can review the complete recorded lifecycle.

### UC-12 — Manage Categories and Departments

- **Actor:** Admin
- **Preconditions:** Admin is authenticated and the management interface is included.
- **Main flow:** The admin creates, updates, or otherwise maintains permitted category and department records.
- **Outcome:** Current records are available for future complaint and assignment selections.

## 21. Acceptance Criteria

| ID | Acceptance criterion |
|---|---|
| AC-01 | A visitor can create a citizen account using valid unique data, while a duplicate email is rejected. |
| AC-02 | A citizen and seeded admin can log in; logout prevents subsequent access to protected pages until login. |
| AC-03 | A citizen can submit a complaint with valid category, location, description, and zero to three valid images; it begins as `Submitted` with a history entry. |
| AC-04 | The system rejects a complaint with missing required fields, an invalid category, more than three images, or a disallowed upload. |
| AC-05 | A citizen can see only their own dashboard, complaint list, details, current status, and history. |
| AC-06 | An administrator can view all complaints and their associated images, histories, assignments, and feedback. |
| AC-07 | An administrator can change a submitted complaint only to `Verified` or `Rejected`; a rejection is terminal. |
| AC-08 | An administrator cannot move a complaint to `Assigned` without a valid department and non-empty `assigned_to` value. |
| AC-09 | The system permits only `Verified → Assigned`, `Assigned → In Progress`, and `In Progress → Resolved` after the initial decision; skips and reversals are rejected. |
| AC-10 | Every valid status change creates one chronological history record that identifies status, time, and actor. |
| AC-11 | An administrator can set only Low, Medium, High, or Critical priority; High and Critical counts appear on the admin dashboard. |
| AC-12 | The complaint owner can submit exactly one rating from 1 to 5 and comment only after the complaint is resolved. |
| AC-13 | Passwords are hashed, protected pages enforce authentication and role checks, and database actions use safe parameterized/ORM access. |
| AC-14 | No feature in this phase introduces AI/ML, analytics, maps, notifications, messaging, payments, mobile-native apps, government integrations, or public/social complaint features. |

## 22. Requirement Traceability Table

| Requirement area | Requirement IDs | Related use cases | Acceptance criteria |
|---|---|---|---|
| Citizen registration, login, profile | FR-01 to FR-03 | UC-01 to UC-03 | AC-01, AC-02 |
| Complaint submission, categories, locations, images | FR-04 to FR-07 | UC-04 | AC-03, AC-04 |
| Citizen dashboard and tracking | FR-08 to FR-10 | UC-05 | AC-05 |
| Feedback | FR-11 | UC-06 | AC-12 |
| Administrator review and dashboard | FR-12 to FR-13 | UC-07, UC-11 | AC-06 |
| Verification, priority, assignment, workflow | FR-14 to FR-17 | UC-08 to UC-10 | AC-07 to AC-11 |
| Status history | FR-18 | UC-05, UC-11 | AC-10 |
| Category and department administration | FR-19 | UC-12 | AC-08 |
| Quality, security, integrity, and boundaries | NFR-01 to NFR-08 | All use cases | AC-13, AC-14 |

## Approved Project Boundaries

This phase does not add or require AI/ML, data analytics, GPS or live maps, notifications, chat or messaging, payments, mobile-native applications, government-system integration, or public/social complaint features. It also does not introduce a staff/authority table, administrator self-registration, automated priority prediction, or arbitrary complaint status changes.
