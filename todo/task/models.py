from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.text import slugify

# todo: write all comments in english

# Розширений юзер
class CustomUser(AbstractUser):
    # Валідатор для номеру телефона
    # todo: that's cool, but there is also a phone field in django exists
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="False number. Example: +380000000000")
    phone = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    score = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    # todo: its better to set constant in setting like `settings.MEDIA_ROOT`
    photo = models.ImageField(upload_to='UserIcon/%Y/%m/%d', blank=True)
    slug = models.SlugField(blank=True)

    # Для слагів
    def save(self, *args, **kwargs):
        # todo: check pre_save signal, it's not better for real, but it's a good practice
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)


# Модель завдання
# todo: for class its better to use tripple quotes, like this:
class Task(models.Model):
    """Save task details in db."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # todo: boolean fields has own naming rules
    #  (https://stackoverflow.com/questions/47996388/python-boolean-methods-naming-convention)
    complete = models.BooleanField(default=False)
    creation_data = models.DateTimeField(auto_now_add=True)
    to_do_date = models.DateTimeField()

    def __str__(self):
        return f"{self.title}"

    # Для адмінки
    class Meta:
        verbose_name = 'Завдання'
        verbose_name_plural = "Завдання"
        ordering = ['to_do_date', 'title']


# Модель для фото на головне меню
class SiteImages(models.Model):
    caption = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to="SitePhotos")
