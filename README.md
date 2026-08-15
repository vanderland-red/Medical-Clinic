# 🏥 Medical Clinic Management System

یک وب‌سایت مدیریت و نوبت‌دهی کلینیک پزشکی که با استفاده از **Python و Flask** توسعه داده شده است.

این پروژه امکان مدیریت پزشکان، برنامه کاری، کاربران، نوبت‌ها و پرداخت‌ها را فراهم می‌کند.

## امکانات

* 👨‍⚕️ مدیریت پزشکان و اطلاعات آن‌ها
* 📅 ایجاد و مدیریت برنامه کاری پزشکان
* 🩺 سیستم نوبت‌دهی آنلاین
* 👤 ثبت‌نام و ورود کاربران
* 🔐 احراز هویت با OTP
* 💳 سیستم پرداخت و ثبت تراکنش
* 📊 داشبورد کاربر و مدیریت نوبت‌ها
* 🔎 جستجوی پزشکان بر اساس نام و تخصص
* 🛠️ پنل مدیریت
* 📱 طراحی Responsive برای موبایل و دسکتاپ

## تکنولوژی‌ها

**Backend**

* Python
* Flask
* SQLAlchemy
* Flask-Migrate
* Flask-Login

**Frontend**

* HTML5
* CSS3
* JavaScript
* Jinja2

**Database**

* MySQL

## 📦 Dependencies

تمام کتابخانه‌های موردنیاز پروژه در فایل `requirements.txt` قرار دارند.

برای نصب آن‌ها:

```bash
pip install -r requirements.txt
```

## ⚙️ اجرای پروژه

ابتدا Repository را Clone کنید:

```bash
git clone https://github.com/USERNAME/clinic-project.git
cd clinic-project
```

ایجاد محیط مجازی:

```bash
python -m venv venv
```

فعال‌سازی در Windows:

```bash
venv\Scripts\activate
```

نصب Dependencies:

```bash
pip install -r requirements.txt
```

اجرای Migration:

```bash
flask db upgrade
```

اجرای پروژه:

```bash
python app.py
```

سپس وارد آدرس زیر شوید:

```text
http://127.0.0.1:5000
```

## هدف پروژه

هدف این پروژه، پیاده‌سازی یک سیستم واقعی نوبت‌دهی پزشکی و تمرین عملی مفاهیم **Backend Development با Flask**، طراحی دیتابیس، Authentication، CRUD، مدیریت Session، Migration و ارتباط بین بخش‌های مختلف یک وب‌سایت است.

## قابلیت‌های آینده

* اتصال به درگاه پرداخت واقعی
* ارسال OTP از طریق SMS
* پنل اختصاصی پزشک
* سیستم امتیازدهی و نظرات
* یادآوری نوبت از طریق SMS
* توسعه API و نسخه React

## Developed with Python & Flask
Medical Clinic
