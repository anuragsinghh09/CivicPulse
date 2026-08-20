# CivicPulse Database ER Diagram

```mermaid
erDiagram
    USERS ||--o{ COMPLAINTS : submits
    CATEGORIES ||--o{ COMPLAINTS : classifies
    LOCATIONS ||--|| COMPLAINTS : identifies
    COMPLAINTS ||--o{ ASSIGNMENTS : has
    DEPARTMENTS ||--o{ ASSIGNMENTS : receives
    USERS ||--o{ ASSIGNMENTS : assigns
    COMPLAINTS ||--o{ COMPLAINT_IMAGES : contains
    COMPLAINTS ||--o{ STATUS_HISTORY : records
    USERS ||--o{ STATUS_HISTORY : changes
    COMPLAINTS ||--o| FEEDBACK : receives

    USERS {
        bigint user_id PK
        varchar full_name
        varchar email UK
        varchar phone
        varchar password_hash
        enum role
    }

    CATEGORIES {
        smallint category_id PK
        varchar name UK
        boolean is_active
    }

    DEPARTMENTS {
        smallint department_id PK
        varchar name UK
        boolean is_active
    }

    LOCATIONS {
        bigint location_id PK
        varchar area
        varchar city
        char pincode
        decimal latitude
        decimal longitude
    }

    COMPLAINTS {
        bigint complaint_id PK
        bigint citizen_id FK
        smallint category_id FK
        bigint location_id FK_UK
        text description
        enum priority
        enum status
        datetime resolved_at
    }

    ASSIGNMENTS {
        bigint assignment_id PK
        bigint complaint_id FK
        smallint department_id FK
        varchar assigned_to
        bigint assigned_by FK
    }

    COMPLAINT_IMAGES {
        bigint image_id PK
        bigint complaint_id FK
        varchar stored_filename
        varchar file_path UK
        tinyint image_order
    }

    STATUS_HISTORY {
        bigint status_history_id PK
        bigint complaint_id FK
        enum previous_status
        enum new_status
        bigint changed_by FK
        text note
    }

    FEEDBACK {
        bigint feedback_id PK
        bigint complaint_id FK_UK
        tinyint rating
        text comment
    }
```

`FK_UK` indicates a foreign key with a unique constraint. It makes the `locations` to `complaints` relationship one-to-one and the `complaints` to `feedback` relationship zero-or-one.
