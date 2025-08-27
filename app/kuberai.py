import os
import json
from typing import Tuple
from openai import OpenAI

_client = None

def _client_safe() -> OpenAI | None:
    global _client
    if _client is not None:
        return _client
    try:
        _client = OpenAI()
        return _client
    except Exception:
        return None

def is_buy_intent(text: str) -> bool:
    text_l = text.lower()
    return any(k in text_l for k in [
        "buy", "purchase", "invest", "invest in",
        "kharid", "khareed", "kharidna", "khareedna",
        "lo", "lelo", "lena", "khareedna"
    ])

def answer_gold_question(message: str) -> Tuple[bool, str]:
    """
    Returns: (is_gold_related, answer)
    Uses OpenAI if key is present, else uses a lightweight fallback.
    """
    client = _client_safe()
    if client:
        try:
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                temperature=0.2,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are KuberAI, specialized in gold investments for Indian users. "
                            "Decide if the user's message is about gold investments (buy/sell, SIP, price, digital gold). "
                            "If yes, answer briefly (<=60 words) with one accurate fact or guidance, and add a gentle nudge to purchase Digital Gold. "
                            "Respond in English. Return strict JSON: "
                            '{"is_gold_related": true|false, "answer": "string"}'
                        )
                    },
                    {"role": "user", "content": message},
                ],
            )
            content = resp.choices[0].message.content
            data = json.loads(content)
            is_related = bool(data.get("is_gold_related", False))
            answer = str(data.get("answer", ""))
            return is_related, answer
        except Exception:
            pass

    msg = message.lower()
    gold_terms = [
        "gold", "digital gold", "sovereign gold bond", "sgb",
        "sona", "sone", "24k", "22k", "gram", "bullion", "sip"
    ]
    is_related = any(term in msg for term in gold_terms)
    if is_related:
        answer = (
            "Gold helps diversify your portfolio; many investors keep around 5–10% in gold. "
            "You can start with a small purchase of ₹10 worth of Digital Gold now."
        )
    else:
        answer = (
            "This assistant only answers questions related to gold investments. "
            "Please ask about digital gold, price per gram, or investment details."
        )
    return is_related, answer
