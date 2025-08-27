import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
from .db import init_db, insert_purchase
from .kuberai import answer_gold_question, is_buy_intent

load_dotenv()

app = FastAPI(title="Simplify Money – KuberAI Gold Assignment")

# Initialize DB
init_db()

PRICE_PER_GRAM = float(os.getenv("GOLD_PRICE_PER_GRAM_INR", "7000"))

class AskRequest(BaseModel):
    user_id: str = Field(..., description="Stable identifier for the user (email or phone).")
    message: str

class CTA(BaseModel):
    suggest_purchase: bool
    purchase_url: Optional[str] = None

class AskResponse(BaseModel):
    is_gold_related: bool
    answer: str
    cta: CTA

class PurchaseRequest(BaseModel):
    user_id: str
    name: str
    phone: str
    amount_inr: float = Field(..., ge=1)

class PurchaseResponse(BaseModel):
    status: str
    transaction_id: int
    user_id: str
    amount_inr: float
    grams: float
    price_per_gram_inr: float
    timestamp_utc: str

@app.post("/ask_gold", response_model=AskResponse)
def ask_gold(req: AskRequest):
    is_related, answer = answer_gold_question(req.message)
    suggest = bool(is_related and is_buy_intent(req.message))
    purchase_url = "/purchase_gold" if is_related else None
    return AskResponse(
        is_gold_related=is_related,
        answer=answer,
        cta=CTA(suggest_purchase=suggest, purchase_url=purchase_url)
    )

@app.post("/purchase_gold", response_model=PurchaseResponse)
def purchase_gold(req: PurchaseRequest):
    grams = round(req.amount_inr / PRICE_PER_GRAM, 4)
    txn_id, ts = insert_purchase(
        user_id=req.user_id,
        name=req.name,
        phone=req.phone,
        amount_inr=float(req.amount_inr),
        grams=grams,
        price_per_gram_inr=PRICE_PER_GRAM,
    )
    return PurchaseResponse(
        status="SUCCESS",
        transaction_id=txn_id,
        user_id=req.user_id,
        amount_inr=req.amount_inr,
        grams=grams,
        price_per_gram_inr=PRICE_PER_GRAM,
        timestamp_utc=ts,
    )

@app.get("/")
def root():
    return {"message": "KuberAI Gold API is running", "endpoints": ["/ask_gold", "/purchase_gold", "/docs"]}

