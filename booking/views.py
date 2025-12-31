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
from django.db.models import Q
from .forms import MedicalRecordForm, AppointmentForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .forms import DoctorUpdateForm, UserUpdateForm


# --- MAXSUS TEKSHIRUV FUNKSIYASI ---
# Bu funksiya userning "Superuser" (Admin) ekanligini tekshiradi
def is_admin(user):
    return user.is_superuser


# --- SHAXSIY ADMIN PANEL ---
@login_required
@user_passes_test(is_admin)  # <-- Bu "qulf": Faqat admin kira oladi
def admin_dashboard(request):
    # 1. Statistikalar
    total_doctors = Doctor.objects.count()
    total_patients = User.objects.filter(
        is_superuser=False
    ).count()  # Admin bo'lmaganlar
    total_appointments = Appointment.objects.count()

    # 2. Ro'yxatlar (Oxirgi 10 tasi)
    appointments = Appointment.objects.all().order_by("-date", "-time")[:10]
    doctors = Doctor.objects.all()

    context = {
        "total_doctors": total_doctors,
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "appointments": appointments,
        "doctors": doctors,
    }
    return render(request, "booking/admin_dashboard.html", context)


def home(request):
    doctors = Doctor.objects.all()
    search_query = request.GET.get("q")
    if search_query:
        doctors = doctors.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(speciality__icontains=search_query)
        )
    spec_filter = request.GET.get("spec")
    if spec_filter:
        doctors = doctors.filter(speciality=spec_filter)
    count = doctors.count()

    context = {"doctors": doctors, "search_query": search_query, "count": count}
    return render(request, "booking/index.html", context)


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
                appointment.save()
                messages.success(
                    request, f"Tabriklaymiz! {doctor.last_name} qabuliga yozildingiz."
                )
                return redirect("dashboard")
            except IntegrityError:
                messages.error(
                    request,
                    "Uzr, bu vaqt allaqachon band qilingan! Iltimos, boshqa vaqtni tanlang.",
                )
    else:
        form = AppointmentForm()

    context = {"doctor": doctor, "form": form}
    return render(request, "booking/booking_form.html", context)


@login_required
def my_appointments(request):
    # 1. Tekshiramiz: Bu foydalanuvchi Shifokormi?
    # (hasattr - user ichida 'doctor' degan bog'lanish bormi yo'qmi tekshiradi)
    if hasattr(request.user, "doctor"):
        # --- SHIFOKOR UCHUN ---
        doctor = request.user.doctor
        # Faqat SHU shifokorga kelgan qabullarni olamiz
        appointments = Appointment.objects.filter(doctor=doctor).order_by(
            "-date", "time"
        )
        return render(
            request, "booking/doctor_dashboard.html", {"appointments": appointments}
        )

    else:
        # --- BEMOR UCHUN (Eski kod) ---
        appointments = Appointment.objects.filter(patient=request.user).order_by(
            "-date", "-time"
        )
        return render(request, "booking/dashboard.html", {"appointments": appointments})


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

            # --- TO'G'RILANGAN QISM ---
            if hasattr(user, "doctor"):
                # Diqqat: 'doctor_dashboard' EMAS, 'dashboard' deb yozamiz.
                # Chunki urls.py da name='dashboard' deb nomlaganmiz.
                # my_appointments funksiyasi o'zi shifokorligini bilib,
                # kerakli HTMLni ochib beradi.
                return redirect("dashboard")
            else:
                # Bemorlarni bosh sahifaga yo'naltiramiz
                return redirect("home")
            # --------------------------

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

    if request.method == "POST":
        # Qabulni bazadan o'chirib tashlaymiz
        appointment.delete()
        messages.warning(request, "Qabul muvaffaqiyatli bekor qilindi.")
        return redirect("dashboard")

    # Agar adashib kirib qolsa, dashboardga qaytarib yuboramiz
    return redirect("dashboard")


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    context = {"doctor": doctor}
    return render(request, "booking/doctor_detail.html", context)


@login_required
def update_status(request, appointment_id, new_status):
    # Faqat SHU shifokorga tegishli qabulni topamiz
    # Agar user shifokor bo'lmasa yoki qabul uniki bo'lmasa -> 404 xato beradi
    if not hasattr(request.user, "doctor"):
        return redirect("home")

    appointment = get_object_or_404(
        Appointment, id=appointment_id, doctor=request.user.doctor
    )

    # Statusni o'zgartiramiz
    appointment.status = new_status
    appointment.save()

    # Xabar beramiz
    messages.success(request, f"Status o'zgartirildi: {appointment.status}.")

    return redirect("dashboard")


@login_required
def add_medical_record(request, appointment_id):
    # Faqat shu shifokorga tegishli qabul ekanligini tekshiramiz
    if not hasattr(request.user, "doctor"):
        return redirect("home")

    appointment = get_object_or_404(
        Appointment, id=appointment_id, doctor=request.user.doctor
    )

    if request.method == "POST":
        form = MedicalRecordForm(request.POST, instance=appointment)
        if form.is_valid():
            # 1. Ma'lumotlarni (tashxis/retsept) saqlaymiz lekin bazaga yozmay turamiz
            record = form.save(commit=False)
            # 2. Statusni avtomatik "Yakunlandi" qilamiz
            record.status = "completed"
            # 3. Endi hammasini saqlaymiz
            record.save()
            messages.success(request, "Tashxis va retsept muvaffaqiyatli saqlandi!")
            return redirect("dashboard")
    else:
        # Agar ma'lumot bor bo'lsa, uni formaga yuklab beramiz (tahrirlash uchun)
        form = MedicalRecordForm(instance=appointment)

    return render(
        request, "booking/medical_form.html", {"form": form, "appointment": appointment}
    )


@login_required
def edit_profile(request):
    # 1. Userni aniqlaymiz
    user = request.user
    is_doctor = hasattr(user, "doctor")  # Shifokormi?

    if request.method == "POST":
        # User formasi (ism, email) hamma uchun
        u_form = UserUpdateForm(request.POST, instance=user)

        # Agar shifokor bo'lsa, uning formasini ham olamiz
        d_form = (
            DoctorUpdateForm(request.POST, request.FILES, instance=user.doctor)
            if is_doctor
            else None
        )

        # Tekshiramiz va saqlaymiz
        if u_form.is_valid():
            if is_doctor and d_form is not None and d_form.is_valid():
                u_form.save()
                d_form.save()  # Shifokor ma'lumotlari
                messages.success(request, "Profilingiz (Shifokor) yangilandi!")
            elif not is_doctor:
                u_form.save()  # Bemor ma'lumotlari
                messages.success(request, "Profilingiz yangilandi!")

            return redirect("dashboard")  # Saqlagandan keyin kabinetga qaytadi

    else:
        # GET so'rov (sahifa endi ochilganda)
        u_form = UserUpdateForm(instance=user)
        d_form = DoctorUpdateForm(instance=user.doctor) if is_doctor else None

    context = {"u_form": u_form, "d_form": d_form, "is_doctor": is_doctor}
    return render(request, "booking/edit_profile.html", context)
