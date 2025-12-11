from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:doctor_id>/", views.doctor_detail, name="doctor_detail"),
    path("book/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
    path("dashboard/", views.my_appointments, name="dashboard"),
    path('register/', views.sign_up, name='sign_up'),
    path('login/', views.sign_in, name='sign_in'),
    path('logout/', views.sign_out, name='sign_out'),
    path('delete-appointment/<int:id>/', views.delete_appointment, name='delete_appointment'),
]
