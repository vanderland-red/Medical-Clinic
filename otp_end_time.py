from flask import session
from datetime import datetime


# این قسمت برای زمانی هستش که کد پیامکی تاریخ انقضاش تموم میشه

def is_otp_expired():
    expire = session.get("otp_expire")

    if not expire:
        return True

    # تبدیل زمان انقضا از رشته به فرمت زمانی پایتونی
    expire_time = datetime.fromisoformat(expire) 

    return datetime.utcnow() > expire_time