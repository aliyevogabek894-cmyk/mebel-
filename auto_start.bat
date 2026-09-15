@echo off
:: Kompyuter yonganda avtomatik ishga tushadi - terminal ko'rinmaydi
cd /d "C:\Users\Teacher\Pictures\yangi loyha"

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist "env\Scripts\activate.bat" (
    call env\Scripts\activate.bat
)

start /min "" python manage.py runserver 127.0.0.1:8000
