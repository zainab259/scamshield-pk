"""Explainable rule scoring. Scores are advisory risk points, not probabilities."""
from __future__ import annotations
import re
from preprocessing import PreparedMessage, preprocess

PATTERNS = {
 "otp": (r"\botp\b|one[- ]time password|verification code|\bcode\b.{0,20}(?:send|share|bhej)|(?:او ٹی پی|otp)", 30, "Requests an OTP or verification code"),
 "credential": (r"\b(?:password|passcode|pin|cvv|card number|login details)\b|پن|پاس ورڈ", 30, "Requests a password, PIN or payment credential"),
 "cnic": (r"\bcnic\b|identity card|شناختی کارڈ", 20, "Requests CNIC or identity details"),
 "url": (r"https?://|www\.", 20, "Contains an unsolicited link"),
 "short_url": (r"\b(?:bit\.ly|tinyurl\.com|t\.co|goo\.gl|cutt\.ly|rb\.gy)/?", 15, "Uses a shortened link that hides its destination"),
 "prize": (r"\b(?:winner|won|prize|reward|congratulations|claim your|free gift)\b|\b(?:inaam|mubarak|jeet|jeeta|jeeti)\b|انعام|مبارک", 15, "Claims an unexpected prize or reward"),
 "urgent": (r"\b(?:urgent|urgently|immediately|right now|today|expires?|limited time|hurry|jaldi|foran|abhi|warna)\b|فوری", 10, "Creates urgency or time pressure"),
 "threat": (r"\b(?:suspend|suspended|blocked|block|terminate|close your account|account band|band ho)\b|بند", 15, "Threatens account suspension or access loss"),
 "financial_brand": (r"\b(?:jazzcash|easypaisa|bank|hbl|ubl|meezan|nayapay|sadapay)\b", 5, "Mentions a financial institution or wallet"),
 "government": (r"\b(?:bisp|ehsaas|nadra|pta|fbr|government|govt)\b|حکومت", 5, "Mentions a government service or program"),
 "money_request": (r"\b(?:send|transfer|pay|deposit|fee|payment)\b.{0,35}\b(?:money|cash|rupees?|rs\.?|pkr|fee)\b|\b(?:pay|deposit)\b.{0,18}\b(?:fee|charges)\b|پیسے.{0,12}(?:بھیج|جمع)", 20, "Requests a payment or money transfer"),
 "investment": (r"\b(?:invest|investment|double your money|guaranteed returns?|profit daily|crypto returns?)\b|منافع", 15, "Promises unusually high or guaranteed investment returns"),
 "job": (r"\b(?:job|hiring|vacancy|employment)\b.{0,50}\b(?:fee|registration|deposit|processing)\b|\b(?:fee|registration fee)\b.{0,40}\b(?:job|work|vacancy)\b", 20, "Pairs a job offer with an upfront fee"),
 "delivery": (r"\b(?:parcel|delivery|courier)\b.{0,60}\b(?:pay|payment|fee|customs|click|link)\b", 15, "Requests action or payment about a delivery"),
 "verify": (r"\b(?:verify|verification|confirm your|tasdeeq|تصدیق)\b", 15, "Requests account or identity verification"),
 "loan": (r"\b(?:instant loan|loan approved|easy loan|loan offer|loan available)\b|\bloan\b.{0,35}\b(?:fee|deposit|processing|advance)\b", 15, "Promotes an unexpected loan or upfront loan fee"),
 "cash_reward": (r"(?:\brs\.?\s?[\d,]+|\b\d[\d,]*\s?(?:pkr|rupees?)\b|₨\s?[\d,]+).{0,35}(?:prize|reward|won|inaam|ملا|انعام)|(?:prize|reward|won|inaam|انعام).{0,50}(?:\brs\.?\s?[\d,]+|\b\d[\d,]*\s?(?:pkr|rupees?)\b|₨\s?[\d,]+)", 15, "Offers an unexpected monetary reward"),
}

def analyze_signals(message: str | PreparedMessage) -> dict:
    prepared = message if isinstance(message, PreparedMessage) else preprocess(message)
    text = prepared.normalized
    found = {k: (points, label) for k, (pattern, points, label) in PATTERNS.items() if re.search(pattern, text, re.I)}
    score = sum(v[0] for v in found.values())
    keys = found.keys()
    # Contextual combinations guard against high scores from benign brand mentions.
    if "otp" in keys and "prize" in keys: score += 35
    if "otp" in keys and "financial_brand" in keys: score += 20
    if "government" in keys and "url" in keys: score += 20
    if "threat" in keys and "urgent" in keys and "url" in keys: score += 35
    if "url" in keys and ("credential" in keys or "verify" in keys): score += 12
    if "job" in keys and "money_request" in keys: score += 15
    return {"score": min(100, score), "signals": list(found), "signal_labels": [v[1] for v in found.values()], "signal_points": {k:v[0] for k,v in found.items()}, "prepared": prepared}

def risk_level(score: int) -> str:
    return "Low Risk" if score < 30 else "Suspicious" if score < 60 else "High Risk" if score < 80 else "Critical Scam Risk"
