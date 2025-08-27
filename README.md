# Simplify Money – KuberAI Gold Assignment (Minimal Implementation)

This repo implements exactly what's asked:
1) **API 1**: Interact via LLM, identify if the user's question is about *gold investments*, reply with a concise fact, and nudge to purchase Digital Gold.
2) **API 2**: Process a Digital Gold **purchase** (values may be hard-coded), **write an entry** into a SQLite DB, and **return success**.

No extra features are added beyond this flow.

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

## Deploy (Render – quick)

1. Push this folder to a new GitHub repo.
2. Create a new **Web Service** on Render and connect the repo.
3. Set **Start Command** to:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. Add environment variables: `OPENAI_API_KEY`, optional `OPENAI_MODEL`, `GOLD_PRICE_PER_GRAM_INR`.
5. Deploy. After it’s live, use the public URL with the same POST requests shown above.
```

