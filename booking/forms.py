from django import forms
from .models import Appointment, Doctor
from django.contrib.auth.models import User


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["date", "time", "note"]
        # HTML5 kalendari chiqishi uchun widgetlar qo'shamiz
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Shikoyatingizni qisqacha yozing...",
                }
            ),
        }


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["diagnosis", "prescription"]
        widgets = {
            "diagnosis": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Bemorga qanday tashxis qo'ydingiz?",
                }
            ),
            "prescription": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Dori-darmonlar va tavsiyalar ro'yxati...",
                }
            ),
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


# 2. FAQAT SHIFOKORLAR UCHUN (Rasm, Narx, vaqt...)
class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "speciality",
            "bio",
            "image",
            "price",
            "work_start_time",
            "work_end_time",
            "telephone",
        ]
        # DIQQAT: widgets Meta klassining ichida, fields bilan bir qatorda turishi shart!
        widgets = {
            "speciality": forms.Select(attrs={"class": "form-select"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "work_start_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "work_end_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
        }
