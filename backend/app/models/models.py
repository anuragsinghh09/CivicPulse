from flask_login import UserMixin
from sqlalchemy.orm import relationship

from ..extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('Citizen', 'Admin', name='user_role'), nullable=False, default='Citizen')
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    complaints = relationship('Complaint', back_populates='citizen', foreign_keys='Complaint.citizen_id')
    assignments = relationship('Assignment', back_populates='assigned_by_user', foreign_keys='Assignment.assigned_by')
    status_history = relationship('StatusHistory', back_populates='changed_by_user', foreign_keys='StatusHistory.changed_by')

    @property
    def is_admin(self):
        return self.role == 'Admin'

    @property
    def is_citizen(self):
        return self.role == 'Citizen'

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f'<User {self.user_id}: {self.email}>'


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    complaints = relationship('Complaint', back_populates='category')


class Department(db.Model):
    __tablename__ = 'departments'

    department_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    assignments = relationship('Assignment', back_populates='department')


class Location(db.Model):
    __tablename__ = 'locations'

    location_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    area = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    latitude = db.Column(db.Numeric(9, 6), nullable=True)
    longitude = db.Column(db.Numeric(9, 6), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    complaint = relationship('Complaint', back_populates='location', uselist=False)


class Complaint(db.Model):
    __tablename__ = 'complaints'

    complaint_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    citizen_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.SmallInteger, db.ForeignKey('categories.category_id'), nullable=False)
    location_id = db.Column(db.BigInteger, db.ForeignKey('locations.location_id'), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Enum('Low', 'Medium', 'High', 'Critical', name='complaint_priority'), nullable=False, default='Medium')
    status = db.Column(
        db.Enum('Submitted', 'Verified', 'Assigned', 'In Progress', 'Resolved', 'Rejected', name='complaint_status'),
        nullable=False,
        default='Submitted',
    )
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
    resolved_at = db.Column(db.DateTime, nullable=True)

    citizen = relationship('User', back_populates='complaints', foreign_keys=[citizen_id])
    category = relationship('Category', back_populates='complaints')
    location = relationship('Location', back_populates='complaint')
    images = relationship('ComplaintImage', back_populates='complaint', cascade='all, delete-orphan')
    assignments = relationship('Assignment', back_populates='complaint', cascade='all, delete-orphan')
    status_history = relationship('StatusHistory', back_populates='complaint', cascade='all, delete-orphan')
    feedback = relationship('Feedback', back_populates='complaint', uselist=False, cascade='all, delete-orphan')


class Assignment(db.Model):
    __tablename__ = 'assignments'

    assignment_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.BigInteger, db.ForeignKey('complaints.complaint_id'), nullable=False)
    department_id = db.Column(db.SmallInteger, db.ForeignKey('departments.department_id'), nullable=False)
    assigned_to = db.Column(db.String(120), nullable=False)
    assigned_by = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    assigned_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    complaint = relationship('Complaint', back_populates='assignments')
    department = relationship('Department', back_populates='assignments')
    assigned_by_user = relationship('User', back_populates='assignments', foreign_keys=[assigned_by])


class ComplaintImage(db.Model):
    __tablename__ = 'complaint_images'

    image_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.BigInteger, db.ForeignKey('complaints.complaint_id'), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), unique=True, nullable=False)
    image_order = db.Column(db.SmallInteger, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    complaint = relationship('Complaint', back_populates='images')


class StatusHistory(db.Model):
    __tablename__ = 'status_history'

    status_history_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.BigInteger, db.ForeignKey('complaints.complaint_id'), nullable=False)
    previous_status = db.Column(db.Enum('Submitted', 'Verified', 'Assigned', 'In Progress', 'Resolved', 'Rejected', name='status_history_previous_status'), nullable=True)
    new_status = db.Column(db.Enum('Submitted', 'Verified', 'Assigned', 'In Progress', 'Resolved', 'Rejected', name='status_history_new_status'), nullable=False)
    changed_by = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    note = db.Column(db.Text, nullable=True)
    changed_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    complaint = relationship('Complaint', back_populates='status_history')
    changed_by_user = relationship('User', back_populates='status_history', foreign_keys=[changed_by])


class Feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.BigInteger, db.ForeignKey('complaints.complaint_id'), unique=True, nullable=False)
    rating = db.Column(db.SmallInteger, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    complaint = relationship('Complaint', back_populates='feedback')
