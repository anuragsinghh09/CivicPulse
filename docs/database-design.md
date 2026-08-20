# CivicPulse — Database Design

**Phase:** 3 — Database Design
**Database name:** `civicpulse`
**DBMS:** MySQL 8.0.16 or later
**Database type:** Relational Database Management System (RDBMS)

## 1. Database Overview

The CivicPulse database stores citizen and administrator accounts, complaint records, configured categories and departments, complaint-specific locations, assignments, image references, status history, and one possible feedback record per complaint. The design uses InnoDB tables, primary keys, foreign keys, unique constraints, checks, and focused indexes to preserve referential integrity and support the approved civic-complaint workflow.

The executable SQL design is provided in [schema.sql](../database/schema.sql), with fictional development data in [seed.sql](../database/seed.sql). The editable relationship diagram is [database-er-diagram.md](diagrams/database-er-diagram.md).

## 2. Table List and Purpose

| Table | Purpose |
|---|---|
| `users` | Stores citizens and seed-created administrators. |
| `categories` | Stores selectable civic complaint categories. |
| `departments` | Stores departments that receive complaint assignments. |
| `locations` | Stores one location context for each complaint. |
| `complaints` | Central record containing complaint ownership, category, location, current status, priority, and timestamps. |
| `assignments` | Preserves department and `assigned_to` assignment history. |
| `complaint_images` | Stores up to three image file references per complaint, not binary image data. |
| `status_history` | Immutable audit-trail records for the initial submission and later status changes. |
| `feedback` | Stores one citizen rating and comment for a resolved complaint. |

No separate staff/authority, notifications, maps, payments, messaging, analytics, or social-feature tables are included.

## 3. Detailed Table Structures

### 3.1 `users`

| Column | MySQL type | Null | Key / constraint | Description |
|---|---|---|---|---|
| `user_id` | `BIGINT UNSIGNED` | No | PK, auto increment | User identifier. |
| `full_name` | `VARCHAR(100)` | No | — | Citizen or administrator name. |
| `email` | `VARCHAR(255)` | No | UNIQUE | Login identity; must be unique. |
| `phone` | `VARCHAR(20)` | No | — | Contact number. |
| `password_hash` | `VARCHAR(255)` | No | — | Secure password hash only; never a plain-text password. |
| `role` | `ENUM('Citizen','Admin')` | No | Default `Citizen` | Access-control role. |
| `created_at` | `DATETIME` | No | Default current time | Account creation time. |
| `updated_at` | `DATETIME` | No | Auto-updated current time | Last permitted account update. |

Administrators are created through seed data/database administration only. There is no public administrator-registration mechanism.

### 3.2 `categories`

| Column | MySQL type | Null | Key / constraint | Description |
|---|---|---|---|---|
| `category_id` | `SMALLINT UNSIGNED` | No | PK, auto increment | Category identifier. |
| `name` | `VARCHAR(50)` | No | UNIQUE | Category name. |
| `description` | `VARCHAR(255)` | Yes | — | Short category explanation. |
| `is_active` | `BOOLEAN` | No | Default `TRUE` | Indicates whether it is available for selection. |
| `created_at` | `DATETIME` | No | Default current time | Record creation time. |
| `updated_at` | `DATETIME` | No | Auto-updated current time | Last maintenance time. |

Initial values: Road, Garbage, Water, Street Light, Drainage, and Other.

### 3.3 `departments`

| Column | MySQL type | Null | Key / constraint | Description |
|---|---|---|---|---|
| `department_id` | `SMALLINT UNSIGNED` | No | PK, auto increment | Department identifier. |
| `name` | `VARCHAR(100)` | No | UNIQUE | Department name. |
| `description` | `VARCHAR(255)` | Yes | — | Department responsibility. |
| `is_active` | `BOOLEAN` | No | Default `TRUE` | Indicates whether it is available for assignment. |
| `created_at` | `DATETIME` | No | Default current time | Record creation time. |
| `updated_at` | `DATETIME` | No | Auto-updated current time | Last maintenance time. |

Initial values: Road Department, Sanitation Department, Water Department, Electricity Department, Drainage Department, and General Department.

### 3.4 `locations`

| Column | MySQL type | Null | Key / constraint | Description |
|---|---|---|---|---|
| `location_id` | `BIGINT UNSIGNED` | No | PK, auto increment | Location identifier. |
| `area` | `VARCHAR(120)` | No | — | Local area or landmark. |
| `city` | `VARCHAR(120)` | No | — | City. |
| `pincode` | `CHAR(6)` | No | CHECK six digits | Indian pincode. |
| `latitude` | `DECIMAL(9,6)` | Yes | CHECK -90 to 90 | Optional latitude. |
| `longitude` | `DECIMAL(9,6)` | Yes | CHECK -180 to 180 | Optional longitude. |
| `created_at` | `DATETIME` | No | Default current time | Location-record creation time. |

The unique `complaints.location_id` constraint makes this a one-to-one relationship: one complaint has one location, and each location record belongs to one complaint context.

### 3.5 `complaints`

| Column | MySQL type | Null | Key / constraint | Description |
|---|---|---|---|---|
| `complaint_id` | `BIGINT UNSIGNED` | No | PK, auto increment | Complaint identifier. |
| `citizen_id` | `BIGINT UNSIGNED` | No | FK → `users.user_id` | Citizen who submitted the complaint. |
| `category_id` | `SMALLINT UNSIGNED` | No | FK → `categories.category_id` | Selected civic category. |
| `location_id` | `BIGINT UNSIGNED` | No | FK + UNIQUE → `locations.location_id` | Complaint-specific location. |
| `description` | `TEXT` | No | — | Required complaint details. |
| `priority` | priority `ENUM` | No | Default `Medium` | Current priority. |
| `status` | status `ENUM` | No | Default `Submitted` | Current workflow status. |
| `created_at` | `DATETIME` | No | Default current time | Submission time. |
| `updated_at` | `DATETIME` | No | Auto-updated current time | Last record update. |
| `resolved_at` | `DATETIME` | Yes | CHECK matches resolved status | Resolution time, only when status is `Resolved`. |

No separate title field is stored because the approved requirements require a description, not a title or short summary.

### 3.6 `assignments`

| Column | MySQL type | Null | Key / constraint | Description |
|---|---|---|---|---|
| `assignment_id` | `BIGINT UNSIGNED` | No | PK, auto increment | Assignment identifier. |
| `complaint_id` | `BIGINT UNSIGNED` | No | FK → `complaints.complaint_id` | Assigned complaint. |
| `department_id` | `SMALLINT UNSIGNED` | No | FK → `departments.department_id` | Responsible department. |
| `assigned_to` | `VARCHAR(120)` | No | — | Person/authority text value. |
| `assigned_by` | `BIGINT UNSIGNED` | No | FK → `users.user_id` | Administrator who made the assignment. |
| `assigned_at` | `DATETIME` | No | Default current time | Assignment timestamp. |

Reassignment adds a new row and never overwrites old assignment records.

### 3.7 `complaint_images`

| Column | MySQL type | Null | Key / constraint | Description |
|---|---|---|---|---|
| `image_id` | `BIGINT UNSIGNED` | No | PK, auto increment | Image-reference identifier. |
| `complaint_id` | `BIGINT UNSIGNED` | No | FK → `complaints.complaint_id` | Owning complaint. |
| `stored_filename` | `VARCHAR(255)` | No | — | Safely generated server filename. |
| `file_path` | `VARCHAR(500)` | No | UNIQUE | Validated relative storage path/reference. |
| `image_order` | `TINYINT UNSIGNED` | No | CHECK 1–3; unique with complaint | Display position and count guard. |
| `created_at` | `DATETIME` | No | Default current time | Reference creation time. |

The application/service layer must still validate image type, file size, ownership, and count. The `image_order` check plus unique `(complaint_id, image_order)` provides an additional database guard against more than three image rows for one complaint.

### 3.8 `status_history`

| Column | MySQL type | Null | Key / constraint | Description |
|---|---|---|---|---|
| `status_history_id` | `BIGINT UNSIGNED` | No | PK, auto increment | Audit-entry identifier. |
| `complaint_id` | `BIGINT UNSIGNED` | No | FK → `complaints.complaint_id` | Related complaint. |
| `previous_status` | status `ENUM` | Yes | — | Prior status; null for initial submission. |
| `new_status` | status `ENUM` | No | — | Status after the recorded action. |
| `changed_by` | `BIGINT UNSIGNED` | No | FK → `users.user_id` | Citizen or administrator who caused the change. |
| `note` | `TEXT` | Yes | — | Optional verification, rejection, or update note. |
| `changed_at` | `DATETIME` | No | Default current time | Change time. |

Rows are audit records. Normal application workflows must insert new entries rather than update or delete existing ones.

### 3.9 `feedback`

| Column | MySQL type | Null | Key / constraint | Description |
|---|---|---|---|---|
| `feedback_id` | `BIGINT UNSIGNED` | No | PK, auto increment | Feedback identifier. |
| `complaint_id` | `BIGINT UNSIGNED` | No | FK + UNIQUE → `complaints.complaint_id` | Resolved complaint receiving feedback. |
| `rating` | `TINYINT UNSIGNED` | No | CHECK 1–5 | Citizen rating. |
| `comment` | `TEXT` | No | — | Citizen feedback comment. |
| `created_at` | `DATETIME` | No | Default current time | Feedback submission time. |

Feedback ownership is derived from `complaints.citizen_id`. The application must verify that the authenticated citizen owns the complaint and that it is resolved before inserting feedback. The unique complaint key enforces one feedback row per complaint.

## 4. Primary Keys and Foreign Keys

Every table uses a surrogate numeric primary key. Foreign keys are intentionally `RESTRICT` on update and delete: historic civic records must not be removed or reassigned accidentally through reference-table changes.

| Child table / column | Parent table / column | Purpose |
|---|---|---|
| `complaints.citizen_id` | `users.user_id` | Complaint ownership. |
| `complaints.category_id` | `categories.category_id` | Complaint category. |
| `complaints.location_id` | `locations.location_id` | Complaint location. |
| `assignments.complaint_id` | `complaints.complaint_id` | Assignment history. |
| `assignments.department_id` | `departments.department_id` | Responsible department. |
| `assignments.assigned_by` | `users.user_id` | Assigning administrator. |
| `complaint_images.complaint_id` | `complaints.complaint_id` | Image ownership. |
| `status_history.complaint_id` | `complaints.complaint_id` | Status audit trail. |
| `status_history.changed_by` | `users.user_id` | User who made the recorded change. |
| `feedback.complaint_id` | `complaints.complaint_id` | One feedback record per complaint. |

## 5. Relationships and Cardinalities

| Relationship | Cardinality | Explanation |
|---|---|---|
| User → Complaints | One-to-many | One citizen can submit many complaints; each complaint has one owner. |
| Category → Complaints | One-to-many | One category can classify many complaints; each complaint selects one category. |
| Complaint ↔ Location | One-to-one | Each complaint has one dedicated location record. |
| Complaint → Assignments | One-to-many | A complaint can be assigned or reassigned many times. |
| Department → Assignments | One-to-many | A department can receive many assignments. |
| User → Assignments | One-to-many | One administrator can make many assignments. |
| Complaint → Complaint Images | One-to-many, maximum three | A complaint can have zero to three image references. |
| Complaint → Status History | One-to-many | A complaint has an initial status record and later status records. |
| User → Status History | One-to-many | A user can create or change many status-history records. |
| Complaint → Feedback | One-to-zero-or-one | A complaint has at most one feedback record. |

## 6. Status and Priority Values

### Complaint status

`Submitted`, `Verified`, `Assigned`, `In Progress`, `Resolved`, and `Rejected` are the only values accepted by the `complaints.status` and status-history fields.

The database enum prevents unknown values. The allowed transition order is enforced by future application/service logic:

```text
Submitted → Verified → Assigned → In Progress → Resolved
Submitted → Rejected
```

`Resolved` and `Rejected` are terminal in the approved initial workflow.

### Priority

`Low`, `Medium`, `High`, and `Critical` are the only accepted priority values. `Medium` is the schema default; administrators may later set or change priority through authorized application logic.

## 7. Constraints and Indexes

### Key constraints

- `users.email`, `categories.name`, and `departments.name` are unique.
- `complaints.location_id` is unique to enforce one location per complaint.
- `feedback.complaint_id` is unique to enforce at most one feedback record per complaint.
- `complaint_images.file_path` is unique, and `(complaint_id, image_order)` is unique with image order restricted to 1–3.
- Latitude, longitude, pincode, rating, image order, and resolved timestamp consistency use MySQL `CHECK` constraints.
- All dependent records use foreign keys to existing parent records.

### Supporting indexes

| Index | Reason |
|---|---|
| `users.email` | Unique login lookup. |
| `complaints.citizen_id` | Citizen dashboard and complaint-list lookup. |
| `complaints.category_id` | Category filtering and joins. |
| `complaints.status` | Administrator status views and dashboard counts. |
| `complaints.priority` | High/Critical monitoring and filtering. |
| `complaints.created_at` | Recent complaint ordering. |
| `assignments.complaint_id` | Assignment-history lookup. |
| `assignments.department_id` | Department assignment lookup. |
| `complaint_images.complaint_id` | Complaint image lookup. |
| `status_history.complaint_id` and `(complaint_id, changed_at)` | Chronological history retrieval. |
| `feedback.complaint_id` | Fast feedback lookup; also uniquely constrained. |

## 8. Normalization

The schema is normalized for the required academic scope:

- **First Normal Form:** Each table has a primary key; fields are atomic. Multiple images, assignments, and status changes are represented as separate rows rather than repeated columns.
- **Second Normal Form:** Non-key columns describe the table's own entity. For example, department data belongs in `departments`, not copied into `assignments`.
- **Third Normal Form:** Categories, departments, locations, and user data are separated from `complaints` to avoid repeated names and address values. Feedback ownership is derived through the complaint owner instead of duplicating `citizen_id` in `feedback`.

The current complaint status is deliberately retained in `complaints` for efficient display, while `status_history` preserves the complete audit trail. This controlled duplication has a clear operational purpose and must be updated together by the future service layer.

## 9. Seed Data Explanation

[seed.sql](../database/seed.sql) contains fictional development data only:

- One seeded administrator and two seeded citizens with `example.com` addresses and non-real phone values.
- The approved six complaint categories and six departments.
- Three example locations and three complaints in Submitted, In Progress, and Resolved states.
- Example image references, assignment records, chronological status-history records, and one feedback record on the resolved complaint.
- Password values are stored only as valid scrypt password hashes. The underlying demo credential is non-secret and must be replaced in any non-demo environment; it is not stored as plain text in the SQL file.

The referenced image paths are intentionally fictional database references; no binary image assets are part of this phase.

## 10. Database Design Assumptions

- MySQL 8.0.16+ is used so that declared `CHECK` constraints are enforced.
- The database is named `civicpulse`, uses `utf8mb4`, and uses InnoDB for foreign-key support.
- `pincode` is a six-digit value for the initial India-focused academic project.
- A complaint description is required; no title field is stored because it is not required by the approved analysis.
- `resolved_at` must be populated only when a complaint is `Resolved`.
- The future application layer will enforce user roles, allowed status transitions, feedback ownership/resolution eligibility, and image file validation. These business rules need authenticated request context and cannot all be expressed through single-row MySQL constraints.
- Database maintenance of categories and departments, if enabled later, must preserve referential integrity and not delete records that are already referenced.
- No GPS, maps, external services, cloud storage, separate staff table, automatic priority calculation, or arbitrary status transitions are part of this design.
