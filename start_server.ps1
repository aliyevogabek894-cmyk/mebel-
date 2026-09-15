$env:PATH = "$HOME\.local\bin;" + $env:PATH
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   MEBEL ERP SERVERI ISHGA TUSHDI!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Brauzerda oching: http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "Admin panel:      http://127.0.0.1:8000/admin" -ForegroundColor Yellow
Write-Host ""
Write-Host "Login ma'lumotlari:" -ForegroundColor White
Write-Host "  Username: admin" -ForegroundColor Gray
Write-Host "  Parol:    admin123" -ForegroundColor Gray
Write-Host ""
Write-Host "To'xtatish uchun: Ctrl+C" -ForegroundColor Red
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

uv run python manage.py runserver 0.0.0.0:8000
