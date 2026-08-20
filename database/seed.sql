-- CivicPulse Phase 3 fictional development seed data.
-- All names, email addresses, phone values, locations, complaints, and file references are fictional.
-- password_hash values are scrypt hashes for a non-secret demo credential; no plain-text password is stored here.

USE civicpulse;

START TRANSACTION;

INSERT INTO users (user_id, full_name, email, phone, password_hash, role, created_at) VALUES
  (1, 'Asha Mehta', 'asha.mehta@example.com', '0000000001', 'scrypt:32768:8:1$civicpulse_demo$501af7e93fff10dcdb26bffe7b1f6d4aeeb726233b05dc2ed3f8e1a022e8fc1fd9eebf143890ef87e453a77abfea9da653dc724a2bbb30c8497a3edfdf4f41e5', 'Admin', '2026-01-01 09:00:00'),
  (2, 'Rohan Verma', 'rohan.verma@example.com', '0000000002', 'scrypt:32768:8:1$civicpulse_demo$501af7e93fff10dcdb26bffe7b1f6d4aeeb726233b05dc2ed3f8e1a022e8fc1fd9eebf143890ef87e453a77abfea9da653dc724a2bbb30c8497a3edfdf4f41e5', 'Citizen', '2026-01-02 10:00:00'),
  (3, 'Neha Kapoor', 'neha.kapoor@example.com', '0000000003', 'scrypt:32768:8:1$civicpulse_demo$501af7e93fff10dcdb26bffe7b1f6d4aeeb726233b05dc2ed3f8e1a022e8fc1fd9eebf143890ef87e453a77abfea9da653dc724a2bbb30c8497a3edfdf4f41e5', 'Citizen', '2026-01-03 11:00:00');

INSERT INTO categories (category_id, name, description) VALUES
  (1, 'Road', 'Potholes, damaged roads, and road-surface issues.'),
  (2, 'Garbage', 'Garbage accumulation and sanitation issues.'),
  (3, 'Water', 'Water leakage and water-supply issues.'),
  (4, 'Street Light', 'Broken or damaged public street lights.'),
  (5, 'Drainage', 'Drainage blockage and drainage-system issues.'),
  (6, 'Other', 'Other public infrastructure issues.');

INSERT INTO departments (department_id, name, description) VALUES
  (1, 'Road Department', 'Responsible for roads and pothole repairs.'),
  (2, 'Sanitation Department', 'Responsible for garbage collection and sanitation.'),
  (3, 'Water Department', 'Responsible for water supply and leakage issues.'),
  (4, 'Electricity Department', 'Responsible for street-light and public electricity issues.'),
  (5, 'Drainage Department', 'Responsible for drainage-system issues.'),
  (6, 'General Department', 'Responsible for uncategorized public infrastructure issues.');

INSERT INTO locations (location_id, area, city, pincode, latitude, longitude, created_at) VALUES
  (1, 'Green Park Sector 2', 'Nandipur', '110001', 28.613900, 77.209000, '2026-02-01 08:30:00'),
  (2, 'Lake View Road', 'Nandipur', '110002', 28.618000, 77.214500, '2026-02-03 09:15:00'),
  (3, 'Sunrise Colony', 'Nandipur', '110003', NULL, NULL, '2026-02-05 10:45:00');

INSERT INTO complaints (complaint_id, citizen_id, category_id, location_id, description, priority, status, created_at, updated_at, resolved_at) VALUES
  (1, 2, 1, 1, 'A deep pothole near the Green Park Sector 2 community entrance is creating a hazard for two-wheelers.', 'High', 'In Progress', '2026-02-01 08:30:00', '2026-02-02 14:00:00', NULL),
  (2, 3, 2, 2, 'Garbage has accumulated beside the public bin on Lake View Road for several days.', 'Medium', 'Resolved', '2026-02-03 09:15:00', '2026-02-05 16:20:00', '2026-02-05 16:20:00'),
  (3, 2, 3, 3, 'Water is leaking continuously from a public pipeline near Sunrise Colony.', 'Low', 'Submitted', '2026-02-05 10:45:00', '2026-02-05 10:45:00', NULL);

-- These are fictional file references for database demonstration only; no image files are included in Phase 3.
INSERT INTO complaint_images (image_id, complaint_id, stored_filename, file_path, image_order, created_at) VALUES
  (1, 1, 'demo-pothole-01.jpg', 'uploads/demo-pothole-01.jpg', 1, '2026-02-01 08:31:00'),
  (2, 1, 'demo-pothole-02.jpg', 'uploads/demo-pothole-02.jpg', 2, '2026-02-01 08:31:00'),
  (3, 2, 'demo-garbage-01.jpg', 'uploads/demo-garbage-01.jpg', 1, '2026-02-03 09:16:00');

INSERT INTO assignments (assignment_id, complaint_id, department_id, assigned_to, assigned_by, assigned_at) VALUES
  (1, 1, 1, 'Arun Rao, Road Repair Team', 1, '2026-02-01 13:30:00'),
  (2, 2, 2, 'Meera Shah, Sanitation Crew', 1, '2026-02-03 15:00:00');

INSERT INTO status_history (status_history_id, complaint_id, previous_status, new_status, changed_by, note, changed_at) VALUES
  (1, 1, NULL, 'Submitted', 2, 'Complaint submitted by citizen.', '2026-02-01 08:30:00'),
  (2, 1, 'Submitted', 'Verified', 1, 'Pothole verified from the submitted details.', '2026-02-01 11:00:00'),
  (3, 1, 'Verified', 'Assigned', 1, 'Assigned to Road Department.', '2026-02-01 13:30:00'),
  (4, 1, 'Assigned', 'In Progress', 1, 'Repair work has started.', '2026-02-02 14:00:00'),
  (5, 2, NULL, 'Submitted', 3, 'Complaint submitted by citizen.', '2026-02-03 09:15:00'),
  (6, 2, 'Submitted', 'Verified', 1, 'Garbage accumulation verified.', '2026-02-03 11:00:00'),
  (7, 2, 'Verified', 'Assigned', 1, 'Assigned to Sanitation Department.', '2026-02-03 15:00:00'),
  (8, 2, 'Assigned', 'In Progress', 1, 'Collection work has started.', '2026-02-04 09:30:00'),
  (9, 2, 'In Progress', 'Resolved', 1, 'Area cleaned and bin collection restored.', '2026-02-05 16:20:00'),
  (10, 3, NULL, 'Submitted', 2, 'Complaint submitted by citizen.', '2026-02-05 10:45:00');

INSERT INTO feedback (feedback_id, complaint_id, rating, comment, created_at) VALUES
  (1, 2, 4, 'The area was cleaned promptly after verification.', '2026-02-06 09:00:00');

COMMIT;
