import time
from django.utils.text import slugify

def upload_courses_category_image(instance, filename):
    path = 'uploads/' + 'category/' + 'courses' + \
        slugify(instance.name, allow_unicode=True)
    name = str(time.time()) + '-' + str(instance.name) + '-' + filename
    return path + '/' + name

