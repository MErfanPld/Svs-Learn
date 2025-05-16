from django.core.management.base import BaseCommand
from faker import Faker
from courses.models import Course, CategoryCourse
from users.models import User 
from django.core.files.base import ContentFile
from django.utils.text import slugify
import random
import requests

class Command(BaseCommand):
    help = 'ساخت دیتای فیک برای دوره‌ها و دسته‌بندی‌ها'

    def handle(self, *args, **kwargs):
        fake = Faker('fa_IR')

        # اول چند دسته‌بندی بسازیم اگه خالیه
        if CategoryCourse.objects.count() == 0:
            for _ in range(5):
                name = fake.word()
                slug = slugify(name)
                CategoryCourse.objects.create(name=name, slug=slug)
            self.stdout.write(self.style.SUCCESS('دسته‌بندی‌های اولیه ساخته شد.'))

        categories = list(CategoryCourse.objects.all())

        # یه مدرس نمونه پیدا کن یا بساز
        instructor = User.objects.filter(is_staff=True).first()
        if not instructor:
            instructor = User.objects.create_user(
                phone_number=fake.phone_number(),
                email=fake.email(),
                password='test1234',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_staff=True
            )
            self.stdout.write(self.style.SUCCESS('مدرس تستی ساخته شد.'))

        # ساخت دوره‌ها
        for _ in range(10):
            title = fake.sentence(nb_words=4)
            slug = slugify(title)
            description = fake.paragraph(nb_sentences=4)
            course_type = random.choice(['in_person', 'online', 'offline'])
            price = random.randint(100_000, 1_000_000)
            duration = f"{random.randint(5, 40)} ساعت"
            meeting_link = fake.url() if course_type == 'online' else None
            schedule = fake.paragraph(nb_sentences=2)
            total_videos = random.randint(5, 30)
            total_downloads = random.randint(50, 500)

            # تصویر تستی با درخواست از اینترنت
            image_url = 'http://placekitten.com/600/400'
            image_response = requests.get(image_url)
            image_content = ContentFile(image_response.content)
            image_name = f"{slug}.png"

            course = Course.objects.create(
                title=title,
                slug=slug,
                description=description,
                instructor=instructor,
                category=random.choice(categories),
                course_type=course_type,
                price=price,
                duration=duration,
                meeting_link=meeting_link,
                schedule=schedule,
                total_videos=total_videos,
                total_downloads=total_downloads,
                is_active=True,
            )
            course.image.save(image_name, image_content, save=True)

            self.stdout.write(self.style.SUCCESS(f'دوره "{title}" ساخته شد.'))
