"""Rule-based scam category mapping; no untrained model is presented as AI."""
def classify(signals: list[str]) -> list[str]:
    s=set(signals); out=[]
    def add(cond, label):
        if cond and label not in out: out.append(label)
    add("financial_brand" in s and ("otp" in s or "credential" in s or "url" in s or "prize" in s), "Banking Scam")
    add("financial_brand" in s and ("otp" in s or "prize" in s or "credential" in s), "Mobile Wallet Scam")
    add("otp" in s, "OTP Theft"); add("credential" in s or "cnic" in s, "Credential Theft")
    add("prize" in s or "cash_reward" in s, "Prize Scam")
    add("government" in s and ("url" in s or "otp" in s or "credential" in s or "prize" in s), "Government Impersonation")
    add("job" in s, "Fake Job Scam"); add("investment" in s, "Investment Scam")
    add("loan" in s, "Loan Scam")
    add("delivery" in s, "Delivery Scam"); add("threat" in s, "Account Suspension Scam")
    add("money_request" in s and "investment" not in s, "Financial Phishing")
    add("url" in s, "Suspicious Link")
    if not out and ("urgent" in s or "verify" in s): out.append("Social Engineering")
    return out or ["Unknown / Other"]
