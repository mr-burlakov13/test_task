# Media Files REST API Service

## Описание

Это REST API микросервис для приёма, обработки и управления медиафайлами. 
Он позволяет загружать файлы, сохранять их на локальном диске, отправлять копию в облачное хранилище и управлять файлами по уникальному идентификатору (UID).

## Технологический стек

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker & Docker Compose

## Редактирование crontab
запуск крон задания на сервере

crontab -e

Добавьте следующую строку, чтобы запускать скрипт каждую неделю в воскресенье в 00:00:

0 0 * * 0 /usr/bin/python3 /path/to/your/project/cleanup.py >> /path/to/your/project/cleanup.log 2>&1

Важно: Замените /path/to/your/project/ на фактический путь к вашему проекту и убедитесь, 
что путь к Python (/usr/bin/python3) соответствует установленной версии Python на вашем сервере.

На некоторых системах cron может быть не запущен по умолчанию. Чтобы запустить его:

sudo service cron start Или для систем с systemd: sudo systemctl start cron

