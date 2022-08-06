from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *
from django import forms
import re


# Форма для створення завдання
class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'to_do_date']
        widgets = {
            'title': forms.TextInput(attrs={"class": "input_field inp", "placeholder": "Введіть назву завдання..."}),
            'description': forms.Textarea(
                attrs={"class": "task_field inp", "placeholder": "Введіть суть завдання..."}),
            'to_do_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                              attrs={"class": "date_field inp", "placeholder": "DD.MM.YYYY hh:mm",
                                                     "type": "datetime-local"})
        }
        labels = {
            'title': "Назва завдання",
            'description': "Опис",
            'to_do_date': "Deadline"
        }


# Форма для реєстрації юзера
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Паролі не збігаються")
        return password2


# Форма для зміни інформації у профілі
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'first_name', 'last_name', 'bio', 'photo')
        labels = {
            'email': "Email:",
            'phone': "Номер телефону",
            'bio': "Біографія",
            'photo': "Завантажити нове фото"
        }
        widgets = {
            'email': forms.TextInput(attrs={"class": "profile-email", "placeholder": "Введіть email..."}),
            'first_name': forms.TextInput(attrs={"placeholder": "Введіть ваше ім'я..."}),
            'last_name': forms.TextInput(attrs={"placeholder": "Введіть ваше прізвище..."}),
            'phone': forms.TextInput(
                attrs={"class": "profile-phone", "placeholder": "Введіть номер телефону...", "type": "tel"}),
            'bio': forms.Textarea(
                attrs={"class": "profile-bio", "placeholder": "Введіть вашу біографію", "rows": 5, "columns": 15}),
            'photo': forms.FileInput(attrs={"class": "photo_input"})
        }

    # Валідатори. Перевіряє на наявність усього, окрім букв
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if re.search(r"\d", last_name) or re.search(r"\W", last_name) or re.search("_", last_name):
            raise ValidationError("Прізвище не має містити цифри і різні знаки...")
        return last_name

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if re.search(r"\d", first_name) or re.search(r"\W", first_name) or re.search("_", first_name):
            raise ValidationError("Ім'я не має містити цифри і різні знаки...")
        return first_name
