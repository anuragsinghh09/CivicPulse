-- CivicPulse Phase 3 database schema
-- Target DBMS: MySQL 8.0.16 or later

CREATE DATABASE IF NOT EXISTS civicpulse
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE civicpulse;

CREATE TABLE users (
  user_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  full_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('Citizen', 'Admin') NOT NULL DEFAULT 'Citizen',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT pk_users PRIMARY KEY (user_id),
  CONSTRAINT uq_users_email UNIQUE (email)
) ENGINE=InnoDB;

CREATE TABLE categories (
  category_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(255) NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT pk_categories PRIMARY KEY (category_id),
  CONSTRAINT uq_categories_name UNIQUE (name)
) ENGINE=InnoDB;

CREATE TABLE departments (
  department_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255) NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT pk_departments PRIMARY KEY (department_id),
  CONSTRAINT uq_departments_name UNIQUE (name)
) ENGINE=InnoDB;

CREATE TABLE locations (
  location_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  area VARCHAR(120) NOT NULL,
  city VARCHAR(120) NOT NULL,
  pincode CHAR(6) NOT NULL,
  latitude DECIMAL(9,6) NULL,
  longitude DECIMAL(9,6) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_locations PRIMARY KEY (location_id),
  CONSTRAINT chk_locations_pincode CHECK (pincode REGEXP '^[0-9]{6}$'),
  CONSTRAINT chk_locations_latitude CHECK (latitude IS NULL OR latitude BETWEEN -90.000000 AND 90.000000),
  CONSTRAINT chk_locations_longitude CHECK (longitude IS NULL OR longitude BETWEEN -180.000000 AND 180.000000)
) ENGINE=InnoDB;

CREATE TABLE complaints (
  complaint_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  citizen_id BIGINT UNSIGNED NOT NULL,
  category_id SMALLINT UNSIGNED NOT NULL,
  location_id BIGINT UNSIGNED NOT NULL,
  description TEXT NOT NULL,
  priority ENUM('Low', 'Medium', 'High', 'Critical') NOT NULL DEFAULT 'Medium',
  status ENUM('Submitted', 'Verified', 'Assigned', 'In Progress', 'Resolved', 'Rejected') NOT NULL DEFAULT 'Submitted',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  resolved_at DATETIME NULL,
  CONSTRAINT pk_complaints PRIMARY KEY (complaint_id),
  CONSTRAINT uq_complaints_location_id UNIQUE (location_id),
  CONSTRAINT fk_complaints_citizen
    FOREIGN KEY (citizen_id) REFERENCES users (user_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_complaints_category
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_complaints_location
    FOREIGN KEY (location_id) REFERENCES locations (location_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT chk_complaints_resolved_at
    CHECK ((status = 'Resolved' AND resolved_at IS NOT NULL) OR (status <> 'Resolved' AND resolved_at IS NULL)),
  INDEX idx_complaints_citizen_id (citizen_id),
  INDEX idx_complaints_category_id (category_id),
  INDEX idx_complaints_status (status),
  INDEX idx_complaints_priority (priority),
  INDEX idx_complaints_created_at (created_at)
) ENGINE=InnoDB;

CREATE TABLE assignments (
  assignment_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  complaint_id BIGINT UNSIGNED NOT NULL,
  department_id SMALLINT UNSIGNED NOT NULL,
  assigned_to VARCHAR(120) NOT NULL,
  assigned_by BIGINT UNSIGNED NOT NULL,
  assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_assignments PRIMARY KEY (assignment_id),
  CONSTRAINT fk_assignments_complaint
    FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_assignments_department
    FOREIGN KEY (department_id) REFERENCES departments (department_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_assignments_assigned_by
    FOREIGN KEY (assigned_by) REFERENCES users (user_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  INDEX idx_assignments_complaint_id (complaint_id),
  INDEX idx_assignments_department_id (department_id)
) ENGINE=InnoDB;

CREATE TABLE complaint_images (
  image_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  complaint_id BIGINT UNSIGNED NOT NULL,
  stored_filename VARCHAR(255) NOT NULL,
  file_path VARCHAR(500) NOT NULL,
  image_order TINYINT UNSIGNED NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_complaint_images PRIMARY KEY (image_id),
  CONSTRAINT uq_complaint_images_file_path UNIQUE (file_path),
  CONSTRAINT uq_complaint_images_order UNIQUE (complaint_id, image_order),
  CONSTRAINT fk_complaint_images_complaint
    FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT chk_complaint_images_order CHECK (image_order BETWEEN 1 AND 3),
  INDEX idx_complaint_images_complaint_id (complaint_id)
) ENGINE=InnoDB;

CREATE TABLE status_history (
  status_history_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  complaint_id BIGINT UNSIGNED NOT NULL,
  previous_status ENUM('Submitted', 'Verified', 'Assigned', 'In Progress', 'Resolved', 'Rejected') NULL,
  new_status ENUM('Submitted', 'Verified', 'Assigned', 'In Progress', 'Resolved', 'Rejected') NOT NULL,
  changed_by BIGINT UNSIGNED NOT NULL,
  note TEXT NULL,
  changed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_status_history PRIMARY KEY (status_history_id),
  CONSTRAINT fk_status_history_complaint
    FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_status_history_changed_by
    FOREIGN KEY (changed_by) REFERENCES users (user_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  INDEX idx_status_history_complaint_id (complaint_id),
  INDEX idx_status_history_complaint_changed_at (complaint_id, changed_at)
) ENGINE=InnoDB;

CREATE TABLE feedback (
  feedback_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  complaint_id BIGINT UNSIGNED NOT NULL,
  rating TINYINT UNSIGNED NOT NULL,
  comment TEXT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_feedback PRIMARY KEY (feedback_id),
  CONSTRAINT uq_feedback_complaint_id UNIQUE (complaint_id),
  CONSTRAINT fk_feedback_complaint
    FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT chk_feedback_rating CHECK (rating BETWEEN 1 AND 5),
  INDEX idx_feedback_complaint_id (complaint_id)
) ENGINE=InnoDB;
