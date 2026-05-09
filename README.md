# Abduraufaka Panel (FastAPI + Admin UI)

Bu tayyor MVP:
- Telegram botdan kelgan hisobotlarni API orqali qabul qiladi
- PostgreSQL yoki SQLite ga saqlaydi
- Admin login sahifasi bor
- Dashboard, Reports list, Detail view bor
- Railway'ga tez deploy bo'ladi

## 1) Local ishga tushirish

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## 2) Railway
Variables:
- DATABASE_URL  -> Railway Postgres DATABASE_URL
- SECRET_KEY
- ADMIN_USERNAME
- ADMIN_PASSWORD
- APP_TITLE

Start command `railway.toml` ichida tayyor.

## 3) Login
- URL: `/login`
- Username/password: env dagi `ADMIN_USERNAME` va `ADMIN_PASSWORD`

## 4) Bot qayerga yuboradi
POST `/api/reports`

JSON body misoli:

```json
{
  "agent_name": "Хочиакбар",
  "agent_phone": "+998973524010",
  "address": "Sho'rchi",
  "landmark": "Maktab oldi",
  "client_code": "2418",
  "last_trade_agent_visit": "10-02-2026",
  "stand_code": "1",
  "client_comment": "dukondor ishlamas ekan",
  "conclusion": "dukondor ishlamas ekan",
  "created_at": "2026-05-06T21:42:00",
  "photos": [
    {
      "photo_type": "stand",
      "photo_link": "https://t.me/c/xxx/1"
    },
    {
      "photo_type": "product",
      "photo_link": "https://t.me/c/xxx/2"
    },
    {
      "photo_type": "outside",
      "photo_link": "https://t.me/c/xxx/3"
    }
  ]
}
```

## 5) Bot integratsiya qilish
Sizning botda Google Sheets o'rniga:
- `requests.post(PANEL_URL + "/api/reports", json=payload)` qiling

Keyingi bosqichda mavjud botingizni shu API bilan to'liq ulab berish mumkin.
