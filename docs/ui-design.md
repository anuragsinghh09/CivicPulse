# CivicPulse UI Design

## 1. UI Objectives

The UI design for CivicPulse is intended to reflect a professional civic-service portal, with a clear distinction between public, citizen, and administrator views. The interface should help users perform complaint actions quickly while keeping the workflow understandable and consistent.

The design focuses on:

- Simple complaint submission for citizens
- Transparent status tracking from submission to resolution
- Clear admin review and assignment workflows
- Controlled navigation between public and authenticated areas
- Responsive use across desktop, tablet, and mobile screens
- Accessible labels, structure, buttons, and form feedback

## 2. Design Style

The visual language follows a modern civic/government portal aesthetic.

- Primary color: deep blue, representing trust and public service
- Accent color: warm gold for highlights and indicators
- Clean white and light gray surfaces for readability
- Rounded cards and soft shadows to keep the interface modern but clean
- Bootstrap 5 components used consistently for layout, navigation, forms, and tables

## 3. Navigation

### Public navigation

- Home
- About
- Login
- Register

### Citizen navigation

- Dashboard
- Submit Complaint
- My Complaints
- Profile
- Logout

### Admin navigation

- Dashboard
- Complaints
- Categories
- Departments
- Logout

The navigation is designed to be clear, compact, and mobile-friendly using the Bootstrap collapsible nav pattern.

## 4. Public Pages

### Home page

The landing page introduces CivicPulse, explains the civic problem it solves, and highlights the complaint lifecycle. It also provides calls to action for logging in or registering.

### About page

The about page explains the purpose of CivicPulse and the value of a structured civic complaint system.

### Login page

The login page uses a clean two-panel layout with a branded left panel and a form on the right. It is designed for clarity and quick access.

### Citizen registration page

The registration page includes the required fields for a citizen account and is styled consistently with the rest of the app.

## 5. Citizen Pages

### Citizen dashboard

The dashboard contains summary cards for complaint totals and status counts. It also provides quick access to recent complaints and repetitive actions.

### Submit complaint

The complaint form includes only the approved fields:

- Category
- Area
- City
- Pincode
- Optional latitude
- Optional longitude
- Description
- Up to 3 images

This form intentionally avoids a title/summary field and includes validation-ready structure and image preview support.

### My complaints

The complaints list gives a clear table view with complaint ID, category, location, status, priority, submitted date, and action links.

### Complaint details

The complaint details page includes description, location, current status, priority, department, assigned person, images, status history, and feedback where applicable. Status and priority badges are visually distinct.

### Citizen profile

The citizen profile page allows viewing and editing permitted profile details with a minimal, professional form layout.

### Feedback UI

The feedback page is available only for a resolved complaint and includes a rating dropdown and comment field. The UI reflects the rule that feedback is only relevant after resolution.

## 6. Admin Pages

### Admin dashboard

The admin dashboard focuses on complaint operations and counts. It includes complaint totals and priority overview cards without becoming a BI dashboard.

### All complaints

The admin complaints page presents all complaints in a review-friendly list with complaint information and quick links to detailed review.

### Complaint details

The admin complaint detail page includes status, priority, department, assignment, images, history, and management controls. It supports admin actions such as verify/reject, assign department, update priority, and change status.

### Category management

The category management page presents a simple admin list for maintaining complaint categories.

### Department management

The department page allows admin control over complaint departments and assignment routing.

## 7. Forms

All forms use semantic HTML and consistent form-control styling. Validation is prepared at the client side with visible required fields and helpful alerts, even though no backend logic is implemented in this Phase 4 UI design.

### Complaint-form specifics

The complaint form clearly displays: “Maximum 3 images” and includes file input with preview support. The form is specifically designed to avoid title or summary fields.

## 8. Status and Priority Indicators

### Status badges

- Submitted
- Verified
- Assigned
- In Progress
- Resolved
- Rejected

### Priority badges

- Low
- Medium
- High
- Critical

Each status and priority uses a distinct color treatment so users can identify complaint conditions quickly.

## 9. Responsive Design

The layout is structured using Bootstrap grid systems and stacked cards to remain readable on mobile screens. The forms, tables, and nav elements collapse or reflow appropriately for smaller viewports, ensuring usability on desktop, tablet, and mobile devices.

## 10. Accessibility

Accessibility practices used include:

- Semantic HTML sections and headings
- Proper form labels
- Clear button labels
- Meaningful alt text for relevant images
- Keyboard-friendly controls through standard HTML elements and Bootstrap components
- Readable contrast and spacing in the design system

## 11. Template Structure

Templates are organized in a modular structure as follows:

- backend/app/templates/base.html
- backend/app/templates/public/
- backend/app/templates/auth/
- backend/app/templates/citizen/
- backend/app/templates/admin/

Static assets are organized under:

- backend/app/static/css/
- backend/app/static/js/
- backend/app/static/images/

## 12. UI State Coverage

The design includes mock states for:

- Empty or populated complaint listings
- Form validation feedback
- Warning and success states
- Rejected and resolved complaints
- Unsubmitted or submitted feedback states
- Missing assignment history or status history

These states are represented visually, without implementing actual backend or database logic.
