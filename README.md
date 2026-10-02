---
title: ScamShield PK
emoji: 🛡️
colorFrom: blue
colorTo: cyan
sdk: gradio
app_file: app.py
---

# ScamShield PK

**AI-powered multilingual scam detection for Pakistan.**

ScamShield PK is a CPU-friendly Gradio prototype for explainable screening of suspicious SMS, WhatsApp, email and social messages in English, Urdu and Roman Urdu. It returns an advisory risk score, possible scam categories, detected signals, a plain-language explanation and safe next steps.

> This is an MVP safety aid, not a guarantee that a message is safe or malicious. Verify important messages independently.

## Overview

Pakistani users receive social-engineering messages that impersonate banks, mobile wallets, government programs, delivery services and employers. ScamShield PK focuses on showing *why* a message may be suspicious rather than presenting an unexplained binary verdict.

### Features

- Language-aware analysis for English, Urdu, Roman Urdu and mixed messages.
- Explainable local pattern and contextual-combination scoring (0–100; not a probability).
- OTP, credential, CNIC, link, urgency, prize, payment, government, job, investment, delivery and account-threat signals.
- Structured categories, safety recommendations and per-session scan history.
- Demo messages with balanced fictional scam and legitimate examples.
- Responsive Gradio UI, Product Details documentation and Safety Center.
- Runs on CPU with no secrets, model download, paid API or database server.

## Screenshots

Add screenshots of the Home, Scan Message result and Product Details pages here after launching the app.

## Supported languages

English · Urdu (Unicode) · Roman Urdu · mixed-language messages. Language identification is a lightweight heuristic and may be uncertain on very short text.

## Architecture

```text
Gradio UI → Unicode-safe preprocessing → language detection
          → signal extraction → contextual risk fusion
          → category classification → explanation + safety action
```

The current MVP uses transparent rules and vocabulary heuristics. No trained transformer scam model is currently active. Product Details explains the implemented and planned components.

## Project structure

```text
scamshield-pk/
├── app.py
├── config.py
├── preprocessing.py
├── language_engine.py
├── risk_engine.py
├── classifier.py
├── explanation_engine.py
├── history.py
├── ui_components.py
├── requirements.txt
├── render.yaml
├── README.md
├── assets/style.css
├── data/demo_messages.json
└── tests/test_scoring.py
```

## Risk scoring

Signals contribute transparent points (for example OTP request +30, credential request +30, CNIC +20, URL +20, prize +15, urgency +10, financial brand +5). Context combinations add weight, such as prize + OTP, financial brand + OTP, government name + link, and threat + urgency + link. The result is capped at 100 and mapped to Low Risk (0–29), Suspicious (30–59), High Risk (60–79), or Critical Scam Risk (80–100). An isolated brand or government name does not trigger a high score. These are advisory risk points, not a calibrated probability.

## Install and run locally

Python 3.11+ is recommended.

```bash
cd scamshield-pk
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open `http://localhost:7860`.

## Free public deployment on Render

The Gradio library is open source. Hugging Face currently requires a paid plan to create a standard Gradio Space on compute, so this project includes a Render Blueprint for a free Python web service instead.

1. Push this project folder to a GitHub repository.
2. Sign in to Render and choose **New → Blueprint**.
3. Connect the GitHub repository and approve the `render.yaml` blueprint.
4. Confirm the `scamshield-pk` web service uses the **Free** plan, then deploy.
5. After the build succeeds, open the `onrender.com` URL and test one safe and one demonstration message.

Render free services spin down after 15 minutes without traffic and can take about a minute to wake up. The first visit after idle may therefore be slow. No Docker, GPU, paid API, or database is required. Session history is ephemeral.

## Hugging Face Spaces

You can still deploy to a Gradio Space if you have an eligible Hugging Face plan or ZeroGPU access. Standard Gradio Spaces on CPU Basic are no longer available to create from a free personal account. Check current Spaces account eligibility and pricing before choosing this route.

## Demonstration messages

- Scam: `Congratulations! Apko JazzCash ki taraf se Rs 50,000 inaam mila hai. Apna OTP aur CNIC bhejein.`
- Scam: `Your account will be suspended today. Verify immediately by clicking http://example-login.com`
- Scam: `آپ کو 25000 روپے انعام ملا ہے۔ رقم حاصل کرنے کے لیے اپنا او ٹی پی بھیجیں۔`
- Safe example: `Assalam o Alaikum, kal class 10 baje start hogi. Please time par aa jana.`
- Safe example: `Your parcel has arrived and is available at the reception desk.`

The 40 records in `data/demo_messages.json` are demonstration and testing examples, not a training dataset.

## Privacy and limitations

No account is required. The app keeps only a small scan history in the active Gradio session. Avoid pasting OTPs, passwords, PINs, full CNICs or card information. Text is processed by the local rule engine; the app does not check live URL reputation. Heuristic language detection and pattern rules can miss new scams or flag legitimate messages. Scores are advisory and are not statistically calibrated.

## Roadmap

1. MVP: multilingual heuristic analysis, explanations and recommendations.
2. AI model: curate a labeled multilingual dataset, fine-tune XLM-RoBERTa and report precision/recall/F1.
3. Threat intelligence: optional domain reputation and phishing feeds.
4. Expansion: browser extension and mobile/chat integrations.
5. Community: privacy-preserving reports and trend insights.

## Disclaimer

ScamShield PK is an educational prototype, not a financial institution, law-enforcement service or guarantee of safety. Do not use a low-risk result as proof that a message is legitimate. Contact the organization through independently verified channels.
