import os
from datetime import datetime
from pathlib import Path

from flask import current_app
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import Complaint, ComplaintImage, Location, StatusHistory

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
ALLOWED_STATUS_FLOW = {
    'Submitted': {'Verified', 'Rejected'},
    'Verified': {'Assigned'},
    'Assigned': {'In Progress'},
    'In Progress': {'Resolved'},
    'Resolved': set(),
    'Rejected': set(),
}


class ComplaintValidationError(ValueError):
    pass


def allowed_transition(current_status, next_status):
    return next_status in ALLOWED_STATUS_FLOW.get(current_status, set())


def create_complaint(citizen_id, form_data, files):
    category_id = form_data.get('category_id') or form_data.get('category')
    area = (form_data.get('area') or '').strip()
    city = (form_data.get('city') or '').strip()
    pincode = (form_data.get('pincode') or '').strip()
    latitude = (form_data.get('latitude') or '').strip()
    longitude = (form_data.get('longitude') or '').strip()
    description = (form_data.get('description') or '').strip()

    from ..models import Category

    if not category_id or not area or not city or not pincode or not description:
        raise ComplaintValidationError('Category, area, city, pincode, and description are required.')

    try:
        category_id_int = int(category_id)
    except (TypeError, ValueError):
        category = Category.query.filter_by(name=str(category_id)).first()
        if category is None:
            raise ComplaintValidationError('Select a valid complaint category.')
        category_id_int = category.category_id

    if not Category.query.get(category_id_int):
        raise ComplaintValidationError('Select a valid complaint category.')

    if len(str(pincode)) != 6 or not pincode.isdigit():
        raise ComplaintValidationError('Pincode must contain exactly 6 digits.')

    if latitude:
        try:
            latitude_val = float(latitude)
            if latitude_val < -90 or latitude_val > 90:
                raise ComplaintValidationError('Latitude must be between -90 and 90.')
        except ValueError as error:
            if isinstance(error, ComplaintValidationError):
                raise
            raise ComplaintValidationError('Latitude must be a valid number.')
    else:
        latitude_val = None

    if longitude:
        try:
            longitude_val = float(longitude)
            if longitude_val < -180 or longitude_val > 180:
                raise ComplaintValidationError('Longitude must be between -180 and 180.')
        except ValueError as error:
            if isinstance(error, ComplaintValidationError):
                raise
            raise ComplaintValidationError('Longitude must be a valid number.')
    else:
        longitude_val = None

    upload_files = [file for file in files.getlist('images') if file and file.filename]
    if len(upload_files) > 3:
        raise ComplaintValidationError('You can upload a maximum of 3 images.')

    validated_files = []
    for file in upload_files:
        filename = secure_filename(file.filename)
        if not filename:
            raise ComplaintValidationError('One uploaded file has an invalid filename.')
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise ComplaintValidationError('Images must be JPG, JPEG, or PNG files.')
        if file.stream is not None:
            file.stream.seek(0, os.SEEK_END)
            size = file.stream.tell()
            file.stream.seek(0)
            if size > 5 * 1024 * 1024:
                raise ComplaintValidationError('Each image must be 5 MB or smaller.')
        validated_files.append((file, ext))

    location = Location(area=area, city=city, pincode=pincode, latitude=latitude_val, longitude=longitude_val)
    db.session.add(location)
    db.session.flush()

    complaint = Complaint(
        citizen_id=citizen_id,
        category_id=category_id_int,
        location_id=location.location_id,
        description=description,
        priority='Medium',
        status='Submitted',
    )
    db.session.add(complaint)
    db.session.flush()

    history = StatusHistory(
        complaint_id=complaint.complaint_id,
        previous_status=None,
        new_status='Submitted',
        changed_by=citizen_id,
        note='Complaint submitted by citizen.',
    )
    db.session.add(history)

    upload_dir = Path(current_app.config['UPLOAD_FOLDER'])
    upload_dir.mkdir(parents=True, exist_ok=True)

    for index, (file, ext) in enumerate(validated_files, start=1):
        saved_name = f"complaint_{complaint.complaint_id}_{index}{ext}"
        save_path = upload_dir / saved_name
        file.save(save_path)
        image = ComplaintImage(
            complaint_id=complaint.complaint_id,
            stored_filename=saved_name,
            file_path=f"uploads/{saved_name}",
            image_order=index,
        )
        db.session.add(image)

    db.session.commit()
    return complaint


def update_complaint_status(complaint, next_status, changed_by, note=''):
    if not allowed_transition(complaint.status, next_status):
        raise ValueError(f"Invalid status transition from {complaint.status} to {next_status}.")

    previous_status = complaint.status
    complaint.status = next_status
    complaint.updated_at = datetime.utcnow()
    if next_status == 'Resolved':
        complaint.resolved_at = datetime.utcnow()
    elif previous_status != 'Resolved' and complaint.resolved_at is not None:
        complaint.resolved_at = None

    db.session.add(StatusHistory(
        complaint_id=complaint.complaint_id,
        previous_status=previous_status,
        new_status=next_status,
        changed_by=changed_by,
        note=note or None,
    ))
    db.session.commit()
    return complaint
