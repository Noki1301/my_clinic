from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Appointment
from .forms import AppointmentForm
from django.contrib.auth.decorators import (
    login_required,
)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.contrib import messages


def home(request):
    doctors = Doctor.objects.all()
    context = {"doctors": doctors}
    return render(request, "booking/index.html", context)


# --- YANGI QO'SHILGAN QISM ---
@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor

            try:
                # 1. Saqlashga urinamiz
                appointment.save()

                # 2. Agar o'xshasa, xabar berib Dashboardga yo'naltiramiz
                messages.success(
                    request, f"Tabriklaymiz! {doctor.last_name} qabuliga yozildingiz."
                )
                return redirect("dashboard")

            except IntegrityError:
                # 3. Agar band bo'lsa, xabar chiqaramiz
                messages.error(
                    request,
                    "Uzr, bu vaqt allaqachon band qilingan! Iltimos, boshqa vaqtni tanlang.",
                )
                # MUHIM: Bu yerda redirect QILMAYMIZ va qayta SAVE qilmaymiz!
                # Kod pastga tushib, formani xatolik xabari bilan qayta ko'rsatadi.

    else:
        form = AppointmentForm()

    context = {"doctor": doctor, "form": form}
    return render(request, "booking/booking_form.html", context)
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = (
                request.user
            )  # Kim kirgan bo'lsa, o'shani bemor deb olamiz
            appointment.doctor = doctor
            try:
                appointment.save()
                # Muvaffaqiyatli bo'lsa xabar beramiz
                messages.success(
                    request, f"Tabriklaymiz! {doctor.last_name} qabuliga yozildingiz."
                )
                return redirect("dashboard")
            except IntegrityError:
                # Agar band bo'lsa, xatolikni ushlaymiz va xabar beramiz
                messages.error(
                    request,
                    "Uzr, bu vaqt allaqachon band qilingan! Iltimos, boshqa vaqtni tanlang.",
                )  # URL dan kelgan shifokorni biriktiramiz
            appointment.save()
            return redirect("home")  # Muvaffaqiyatli bo'lsa, bosh sahifaga qaytadi
    else:
        form = AppointmentForm()

    context = {"doctor": doctor, "form": form}
    return render(request, "booking/booking_form.html", context)


@login_required
def my_appointments(request):
    # Faqat shu foydalanuvchiga tegishli qabullarni olamiz
    appointments = Appointment.objects.filter(patient=request.user).order_by(
        "-date", "-time"
    )

    context = {"appointments": appointments}
    return render(request, "booking/dashboard.html", context)


# 1. Ro'yxatdan o'tish
def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Ro'yxatdan o'tishi bilan tizimga kiritib yuboramiz
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "booking/register.html", {"form": form})


# 2. Tizimga kirish
def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "booking/login.html", {"form": form})


# 3. Tizimdan chiqish
def sign_out(request):
    logout(request)
    return redirect("sign_in")  # Chiqib ketgach, Login sahifasiga otamiz
@login_required
def delete_appointment(request, id):
    # Faqat shu userga tegishli (patient=request.user) qabulni qidiramiz
    appointment = get_object_or_404(Appointment, id=id, patient=request.user)
    
    if request.method == 'POST':
        # Qabulni bazadan o'chirib tashlaymiz
        appointment.delete()
        messages.warning(request, "Qabul muvaffaqiyatli bekor qilindi.")
        return redirect('dashboard')
        
    # Agar adashib kirib qolsa, dashboardga qaytarib yuboramiz
    return redirect('dashboard')
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    context = {"doctor": doctor}
    return render(request, "booking/doctor_detail.html", context)