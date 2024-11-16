import os
import secrets

from PIL import Image
from configs import Config


def save_profile_upload(file):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(file.filename)
    file_name = random_hex + file_extension
    file_path = os.path.join(Config.UPLOAD_FOLDER, file_name)

    preferred_size = (500, 650)
    image = Image.open(file)
    image.thumbnail(preferred_size)

    image.save(file_path)

    return file_name


def delete_previous_profile(file_name):

    file = os.path.join('src', 'static', 'assets', 'users', file_name)

    if os.path.exists(file):
        os.remove(file)


def is_file_type_allowed(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

    if '.' not in filename:
        return False

    # Split the filename at the last period to get the extension
    file_extension = filename.rsplit('.', 1)[1].lower()

    if file_extension in ALLOWED_EXTENSIONS:
        return True
    else:
        return False
