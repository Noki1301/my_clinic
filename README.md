# 🏥 MyClinic - Zamonaviy Tibbiy Klinika Tizimi

2025 yilning eng zamonaviy dizayni bilan yaratilgan Django-da yozilgan tibbiy klinika boshqaruv tizimi.

## ✨ Asosiy Xususiyatlar

### 🎨 Dizayn

- **Glass Morphism** - shaffof va zamonaviy card dizaynlar
- **Gradient Ranglar** - ko'z quvvatli gradient effectlar
- **Smooth Animations** - yumshoq fade-in va hover animatsiyalar
- **Responsive Dizayn** - barcha qurilmalarda mukammal ko'rinish
- **Modern UI/UX** - 2025 yilning eng yangi dizayn trendlari

### 👥 Foydalanuvchi Turlari

1. **Bemorlar** - qabul yozish, tibbiy yozuvlarni ko'rish
2. **Shifokorlar** - bemorlarni ko'rish, tibbiy yozuvlar kiritish
3. **Admin** - tizimni to'liq boshqarish

### 🔧 Funktsiyalar

- ✅ Shifokorlarni qidirish va filterlash
- ✅ Onlayn qabul yozish
- ✅ Tibbiy yozuvlar va retseptlar
- ✅ Qabullar statusi (Kutilmoqda, Tasdiqlandi, Yakunlandi)
- ✅ Admin dashboard - statistika va monitoring
- ✅ User dashboard - shaxsiy kabinet
- ✅ Shifokor profili - bio, rasm, narx, ish vaqti

## 🚀 O'rnatish

### 1. Repository klonlash

```bash
cd my_clinic
```

### 2. Virtual muhit yaratish

```bash
pipenv --python 3.13
pipenv shell
```

### 3. Dependensiyalarni o'rnatish

```bash
pipenv install
```

### 4. .env faylini sozlash

`.env` fayli yarating:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

SECRET_KEY generatsiya qilish:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Migratsiyalarni bajarish

```bash
python manage.py migrate
```

### 6. Superuser yaratish

```bash
python manage.py createsuperuser
```

### 7. Serverni ishga tushirish

```bash
python manage.py runserver 8080
```

Brauzerda oching: `http://127.0.0.1:8080/`

## 📁 Proyekt Tuzilishi

```
my_clinic/
├── booking/                # Asosiy app
│   ├── models.py          # Doctor, Appointment modellari
│   ├── views.py           # Barcha view funksiyalar
│   ├── forms.py           # Django forms
│   ├── urls.py            # URL routelari
│   └── admin.py           # Django admin sozlamalari
├── config/                # Proyekt sozlamalari
│   ├── settings.py        # Asosiy sozlamalar
│   ├── urls.py            # Root URLs
│   └── wsgi.py
├── templates/             # HTML shablon fayllar
│   ├── base.html          # Asosiy shablon
│   └── booking/           # Booking app shablonlari
│       ├── index.html             # Bosh sahifa
│       ├── login.html             # Kirish
│       ├── register.html          # Ro'yxatdan o'tish
│       ├── booking_form.html      # Qabul yozish
│       ├── dashboard.html         # User dashboard
│       ├── doctor_dashboard.html  # Shifokor dashboard
│       └── admin_dashboard.html   # Admin dashboard
├── static/                # Statik fayllar
│   └── css/
│       └── style.css      # Zamonaviy CSS dizayn
├── Pipfile               # Python dependensiyalar
└── manage.py
```

## 🎨 Dizayn Xususiyatlari

### CSS Variables

```css
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
--danger-gradient: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
--warning-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
```

### Asosiy Klasslar

- `.glass-card` - shaffof card effect
- `.btn-gradient-primary` - gradient tugma
- `.stat-card` - statistika kartochkasi
- `.badge-modern` - zamonaviy badge
- `.fade-in-up` - animatsiya

## 🔐 Xavfsizlik

- ✅ SECRET_KEY `.env` faylida
- ✅ DEBUG rejimi sozlanadi
- ✅ ALLOWED_HOSTS sozlamasi
- ✅ CSRF himoyasi
- ✅ Password validatsiya

## 📱 Responsive Dizayn

- **Desktop** - to'liq funksional
- **Tablet** - moslashtirilgan layout
- **Mobile** - optimallashtirilgan ko'rinish

## 🛠 Texnologiyalar

- **Backend**: Django 5.2.9
- **Frontend**: Bootstrap 5.3.0
- **Icons**: Bootstrap Icons 1.11.3
- **Fonts**: Google Fonts (Inter)
- **Database**: SQLite3 (Development)
- **Python**: 3.13

## 📞 Foydalanuvchi Rollari

### Bemor

- Shifokorlarni ko'rish va qidirish
- Qabul yozish
- O'z qabullarini ko'rish
- Tibbiy yozuvlarni ko'rish

### Shifokor

- O'z bemorlarini ko'rish
- Qabullarni tasdiqlash
- Tibbiy yozuvlar kiritish (tashxis, retsept)
- Profil sozlash

### Admin

- Barcha statistikani ko'rish
- Qabullarni boshqarish
- Shifokorlarni ko'rish
- Tizimni to'liq nazorat qilish

## 🎯 Keyingi Qadamlar

- [ ] Email bildirishnomalar
- [ ] SMS xabarnomalar
- [ ] Online to'lov tizimi
- [ ] Video konsultatsiya
- [ ] Chat funksiyasi
- [ ] Mobile app (React Native / Flutter)

## 📝 Litsenziya

MIT License - Erkin foydalanish uchun ochiq.

## 👨‍💻 Muallif

MyClinic - 2025 yilning zamonaviy tibbiy tizimi

---

**Eslatma**: Bu loyihani ishlatishdan oldin `.env` faylini to'g'ri sozlang va `http://` protokolidan foydalaning (HTTPS emas!).
