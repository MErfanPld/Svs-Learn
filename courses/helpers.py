import time
from django.utils.text import slugify
import random
import string


def upload_courses_category_image(instance, filename):
    path = 'uploads/category/courses/' + slugify(instance.name, allow_unicode=True)
    safe_name = slugify(instance.name, allow_unicode=True)
    name = f"{int(time.time())}-{safe_name}-{filename}"
    return f"{path}/{name}"


def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
