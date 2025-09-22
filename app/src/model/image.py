# app/src/model/image.py
import os
from app import app, db
from werkzeug.utils import secure_filename

# Image handling for shopping centre photos
ALLOWED_EXTS = {"jpg", "jpeg", "png", "webp"}

# Directory for uploading centre images
def upload_dir() -> str:
    """Absolute path to the centre photo upload folder."""
    folder = os.path.join(app.root_path, "static", "uploads", "centre_photo")
    os.makedirs(folder, exist_ok=True)
    return folder

# Save or replace an image file for a centre
def save_or_replace_image(centre_id: int, new_name: str, file_storage) -> str | None:
    """Save a new image, delete old one if different, return new filename or None."""
    if not file_storage or not file_storage.filename:
        return None
    
    # Validate file extension
    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTS:
        raise ValueError("Unsupported image type. Allowed: jpg, jpeg, png, webp")
    
    # Construct new filename
    clean_name = new_name.strip().replace(' ', '')
    new_filename = f"{clean_name}_{centre_id}.{ext}"
    
    # Ensure upload directory exists
    folder = upload_dir()
    os.makedirs(folder, exist_ok=True)
    new_path = os.path.join(folder, new_filename)

    # fetch old filename
    with db.get_cursor() as cursor:
        cursor.execute("SELECT image_filename FROM shopping_centre WHERE id=%s", (centre_id,))
        row = cursor.fetchone()
        old_filename = row.get('image_filename') if row else None
    
    # Update DB with new filename
    if old_filename and old_filename != new_filename:
        old_path = os.path.join(folder, old_filename)
        if os.path.isfile(old_path):
            try:
                os.remove(old_path)
            except Exception as e:
                app.logger.warning(f"Could not delete old image {old_path}: {e}")
    
    # Save new file
    file_storage.save(new_path)
    return new_filename
