# Мерч ТГУ «САС 101/102»

Лендинг мерча выпускников переподготовки Томского государственного университета по специальности «Системный аналитик».

---

## Что изменить перед первым запуском

Перед первым запуском обязательно проверьте и измените:

1. **`.env`**
   - Скопируйте `.env.example` → `.env`
   - Заполните SMTP-креды Yandex
   - Укажите email получателя заявок (`ORDER_EMAIL_TO`)

2. **SMTP**
   - `SMTP_USER` — ваш email на Yandex
   - `SMTP_PASSWORD` — app password (не основной пароль!)

3. **Email получателя**
   - `ORDER_EMAIL_TO` — куда будут приходить уведомления о заказах

4. **IP / домен**
   - `APP_DOMAIN` — оставьте пустым для работы по IP

5. **Товары**
   - Данные товаров находятся в `backend/services/catalog.py`

6. **Цены**
   - Цены указаны в рублях как целые числа (`int`)

7. **Изображения**
   - Структура: `frontend/images/products/<product_key>/*.jpg`

8. **Сертификат**
   - Self-signed: `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout cert.key -out cert.crt -addext "subjectAltName=IP:ВАШ_IP" -subj "/CN=tsu-merch"`
   - Let's Encrypt: `certbot --nginx -d ваш-домен`

---

## Установка

### Требования
- Python 3.10+
- Ubuntu 22.04 (для production)

### Backend
```bash
cd backend
python -m venv ../venv
source ../venv/bin/activate
pip install -r ../requirements.txt
```

### Frontend
Открывается напрямую через Nginx или локально:
```bash
cd frontend
npx serve  # или любой static server
```

---

## Локальный запуск

```bash
# Backend
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API документация: http://127.0.0.1:8000/docs

---

## API Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/products` | Каталог товаров (источник истины) |
| GET | `/api/health` | Проверка доступности |

---

## Товары

- Данные товаров: `backend/services/catalog.py` — `get_catalog()`
- Цены: `int` в рублях
- Цвета: список hex-кодов
- Параметры: список объектов `{"name": "Пол", "options": ["Мужская", "Женская"]}`
- Изображения: `frontend/images/products/<product_key>/*.jpg`

---

## Production

- Ubuntu 22.04
- Nginx (reverse proxy + static frontend)
- Uvicorn + Systemd
- HTTPS (self-signed для IP → Let's Encrypt для домена)

Подробности в соответствующих секциях выше.