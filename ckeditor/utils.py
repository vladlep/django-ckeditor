import mimetypes
import os.path
import random
import string

from django.core.files.storage import default_storage
from django.template.defaultfilters import slugify
from django.utils.module_loading import import_string


class NotAnImageException(Exception):
    pass


def slugify_filename(filename):
    """ Slugify filename """
    name, ext = os.path.splitext(filename)
    slugified = get_slugified_name(name)
    return slugified + ext


def get_slugified_name(filename):
    slugified = slugify(filename)
    return slugified or get_random_string()


def get_random_string():
    return ''.join(random.sample(string.ascii_lowercase*6, 6))


def get_thumb_filename(file_name):
    """
    Generate thumb filename by adding _thumb to end of
    filename before . (if present)
    """
    return u'{0}_thumb{1}'.format(*os.path.splitext(file_name))


def get_image_format(extension):
    mimetypes.init()
    return mimetypes.types_map[extension.lower()]


def get_storage():
    from django.conf import settings
    ckeditor_storage = getattr(settings, 'CKEDITOR_STORAGE_BACKEND', None)
    if ckeditor_storage:
        storage = import_string(ckeditor_storage)()
    else:
        storage = default_storage
    return storage


def get_media_url(path):
    """
    Determine system file's media URL.
    """
    storage = get_storage()
    return storage.url(path)    

