from django.db import models
from django.contrib.auth.models import User
import datetime


class Speciality(models.TextChoices):
    DENTIST = "dentist", "Stomatolog"
    CARDIOLOGIST = "cardiologist", "Kardiolog"
    SURGEON = "surgeon", "Xirurg"
    DERMATOLOGIST = "dermatologist", "Dermatolog"
    PEDIATRICIAN = "pediatrician", "Pediatr"
    THERAPIST = "therapist", "Terapevt"


class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="doctor"
    )
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    telephone = models.CharField(max_length=15, verbose_name="Telefon raqam")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    SPECIALITY_CHOICES = [
        ("Stomatolog", "🦷 Stomatolog"),
        ("Kardiolog", "❤️ Kardiolog"),
        ("Xirurg", "🔪 Xirurg"),
        ("Dermatolog", "🧴 Dermatolog"),
        ("Pediatr", "👶 Pediatr"),
        ("Terapevt", "🩺 Terapevt"),
    ]

    speciality = models.CharField(
        max_length=50,
        choices=SPECIALITY_CHOICES,  # <--- choices= deb yozish SHART
        verbose_name="Mutaxassisligi",
    )

    bio = models.TextField(verbose_name="Shifokor haqida")
    image = models.ImageField(
        upload_to="doctors/", blank=True, null=True, verbose_name="Rasm"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Qabul narxi"
    )

    # --- 2. O'ZGARGAN JOYLAR ---
    # "09:00" o'rniga datetime.time(9, 0) ishlatamiz
    work_start_time = models.TimeField(
        default=datetime.time(9, 0), verbose_name="Ish boshlanish vaqti"
    )

    # "17:00" o'rniga datetime.time(17, 0) ishlatamiz
    work_end_time = models.TimeField(
        default=datetime.time(17, 0), verbose_name="Ish tugash vaqti"
    )
    # ---------------------------

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Shifokor"
        verbose_name_plural = "Shifokorlar"


# Appointment klassi o'zgarishsiz qoladi...
class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Kutilmoqda"),
        ("confirmed", "Tasdiqlandi"),
        ("cancelled", "Bekor qilindi"),
        ("completed", "Yakunlandi"),
    ]

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Bemor",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Shifokor",
    )

    date = models.DateField(verbose_name="Sana")
    time = models.TimeField(verbose_name="Vaqt")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True, verbose_name="Shikoyat")
    diagnosis = models.TextField(blank=True, null=True, verbose_name="Tashxis")
    prescription = models.TextField(blank=True, null=True, verbose_name="Retsept")

    def __str__(self):
        return f"{self.patient.username} -> {self.doctor.last_name} ({self.date})"

    class Meta:
        verbose_name = "Qabul"
        verbose_name_plural = "Qabullar"
        unique_together = ("doctor", "date", "time")
        ordering = ["-date", "-time"]
