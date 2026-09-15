$env:PATH = "$HOME\.local\bin;" + $env:PATH
uv pip install --system-certs django djangorestframework
uv run django-admin startproject mebel_erp .
uv run python manage.py startapp production
