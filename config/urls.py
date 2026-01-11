from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # <--- 1. BU BORMI?
from django.conf.urls.static import static  # <--- 2. BU BORMI?

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("booking.urls")),
    path("chat/", include("chat.urls")),
]

# --- 3. BU QISM TURLAR RO'YXATIDAN TASHQARIDA BO'LISHI SHART ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
