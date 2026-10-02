import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from explanation_engine import explain

def test_high_risk_combinations():
    assert explain("You won a prize. Send your OTP now.")["risk_score"] >= 80
    assert explain("JazzCash OTP bhejo warna account band")["risk_score"] >= 60
    assert explain("Your account suspended urgently click http://fake.example")["risk_score"] >= 80

def test_isolated_names_are_not_critical():
    assert explain("BISP office is open today")["risk_score"] < 30
    assert explain("JazzCash is a digital wallet service")["risk_score"] < 30

def test_multilingual_safe_examples():
    assert explain("Assalam o Alaikum kal class 10 baje start hogi")["risk_score"] < 30
    assert explain("Your parcel has arrived at reception")["risk_score"] < 30
    assert explain("آپ کی کتابیں استقبالیہ پر رکھ دی گئی ہیں")["risk_score"] < 30

def test_sensitive_and_scam_patterns():
    assert explain("Apna CNIC bhejein")["risk_score"] >= 20
    assert explain("Pay registration fee to secure this job")["risk_score"] >= 30
    assert explain("Invest now for guaranteed returns")["risk_score"] >= 15
    assert "Loan Scam" in explain("Instant loan approved, pay processing fee")["scam_types"]
    assert explain("Pay delivery fee via http://parcel.example")["risk_score"] >= 30
