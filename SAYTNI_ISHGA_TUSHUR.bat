@echo off
title Wood Timbero - Ishga tushirilmoqda...
color 0A
echo.
echo  ================================================
echo    WOOD TIMBERO - Ishlab chiqarish tizimi
echo  ================================================
echo.
echo  [*] Server ishga tushirilmoqda...
echo.

cd /d "C:\Users\Teacher\Pictures\yangi loyha"

:: Virtual environment bormi tekshir
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist "env\Scripts\activate.bat" (
    call env\Scripts\activate.bat
)

:: Brauzer ochish (3 soniyadan keyin)
start /min cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:8000"

echo  [*] Brauzer 3 soniyada ochiladi...
echo  [*] Saytni yopish uchun bu oynani yoping
echo.
echo  ================================================
echo.

:: Django serverni ishga tushur
python manage.py runserver 127.0.0.1:8000

pause
