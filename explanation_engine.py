"""Turns detector output into clear, actionable user guidance."""
from language_engine import detect_language
from risk_engine import analyze_signals, risk_level
from classifier import classify

def explain(message: str) -> dict:
    result=analyze_signals(message); score=result["score"]; signals=result["signals"]
    types=classify(signals); labels=result["signal_labels"]
    if not signals or score < 30:
        summary="No strong scam indicators were detected in this message. This automated check cannot guarantee that it is legitimate."
    else:
        parts=[]
        if "prize" in signals or "cash_reward" in signals: parts.append("it presents an unexpected prize or monetary reward")
        if "otp" in signals or "credential" in signals or "cnic" in signals: parts.append("it asks for sensitive verification or identity information")
        if "url" in signals: parts.append("it includes a link whose destination has not been independently verified")
        if "urgent" in signals or "threat" in signals: parts.append("it uses urgency or a threat to pressure a quick response")
        if "financial_brand" in signals or "government" in signals: parts.append("it invokes a financial or government service")
        summary="This message is concerning because " + ", and ".join(parts) + ". These patterns are commonly used in social-engineering attempts; verify the sender independently."
    actions=[]
    if "otp" in signals or "credential" in signals or "cnic" in signals: actions.append("Do not share OTPs, passwords, PINs, or identity details.")
    if "url" in signals: actions.append("Do not open the link; visit the official service directly instead.")
    actions.append("Contact the organization using a number or app you already trust.")
    if score >= 30: actions.append("Do not reply; block or report the sender if appropriate.")
    tip="Never share an OTP, PIN, or password with another person." if any(x in signals for x in ("otp","credential")) else "Automated analysis cannot guarantee legitimacy. Verify unexpected messages independently."
    return {"risk_score":score,"risk_level":risk_level(score),"language":detect_language(message),"scam_types":types if score>=30 else ["None Detected"],"signals":labels,"explanation":summary,"actions":actions,"safety_tip":tip,"signal_points":result["signal_points"],"analysis_method":"Explainable heuristic and language-aware risk detection","model_used":False}
