# Simplify Money – KuberAI Gold Assignment (Minimal Implementation)

This repo implements exactly what's asked:
1) **API 1**: Interact via LLM, identify if the user's question is about *gold investments*, reply with a concise fact, and nudge to purchase Digital Gold.
2) **API 2**: Process a Digital Gold **purchase** (values may be hard-coded), **write an entry** into a SQLite DB, and **return success**.

## Run locally

```bash
python -m venv venv
# Windows PowerShell
# .\venv\Scripts\Activate.ps1
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env  # then set OPENAI_API_KEY in .env
uvicorn app.main:app --reload
```

### Test

**API 1** (identify + answer + nudge):
```bash
curl -X POST http://127.0.0.1:8000/ask_gold   -H "Content-Type: application/json"   -d '{"user_id":"user123","message":"Should I invest in digital gold today?"}'
```

**API 2** (purchase ₹10 example):
```bash
curl -X POST http://127.0.0.1:8000/purchase_gold   -H "Content-Type: application/json"   -d '{"user_id":"user123","name":"Kumkum Maurya","phone":"+91-9000000000","amount_inr":10}'
```

A `gold_purchases.db` file will be created at the project root with your purchase.



