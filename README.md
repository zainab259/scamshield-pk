---
title: ScamShield PK
emoji: ðŸ›¡ï¸
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
- Explainable local pattern and contextual-combination scoring (0â€“100; not a probability).
- OTP, credential, CNIC, link, urgency, prize, payment, government, job, investment, delivery and account-threat signals.
- Structured categories, safety recommendations and per-session scan history.
- Demo messages with balanced fictional scam and legitimate examples.
- Responsive Gradio UI, Product Details documentation and Safety Center.
- Runs on CPU with no secrets, model download, paid API or database server.

## Screenshots

Add screenshots of the Home, Scan Message result and Product Details pages here after launching the app.

## Supported languages

English Â· Urdu (Unicode) Â· Roman Urdu Â· mixed-language messages. Language identification is a lightweight heuristic and may be uncertain on very short text.

## Architecture

```text
Gradio UI â†’ Unicode-safe preprocessing â†’ language detection
          â†’ signal extraction â†’ contextual risk fusion
          â†’ category classification â†’ explanation + safety action
```

The current MVP uses transparent rules and vocabulary heuristics. No trained transformer scam model is currently active. Product Details explains the implemented and planned components.

## Project structure

```text
scamshield-pk/
â”œâ”€â”€ app.py
â”œâ”€â”€ config.py
â”œâ”€â”€ preprocessing.py
â”œâ”€â”€ language_engine.py
â”œâ”€â”€ risk_engine.py
â”œâ”€â”€ classifier.py
â”œâ”€â”€ explanation_engine.py
â”œâ”€â”€ history.py
â”œâ”€â”€ ui_components.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ render.yaml
â”œâ”€â”€ README.md
â”œâ”€â”€ assets/style.css
â”œâ”€â”€ data/demo_messages.json
â””â”€â”€ tests/test_scoring.py
```

## Risk scoring

Signals contribute transparent points (for example OTP request +30, credential request +30, CNIC +20, URL +20, prize +15, urgency +10, financial brand +5). Context combinations add weight, such as prize + OTP, financial brand + OTP, government name + link, and threat + urgency + link. The result is capped at 100 and mapped to Low Risk (0â€“29), Suspicious (30â€“59), High Risk (60â€“79), or Critical Scam Risk (80â€“100). An isolated brand or government name does not trigger a high score. These are advisory risk points, not a calibrated probability.

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

## Free public deployment on Vercel

The project exposes its existing Gradio interface as a FastAPI ASGI application for Vercel's Python runtime. The scan engine, visual interface, and session-based history are unchanged. No Docker, GPU, paid API, or secrets are required.

1. Push this repository to GitHub.
2. Sign in to [Vercel](https://vercel.com/) and select **Add New**, then **Project**.
3. Import `zainab259/scamshield-pk` (or your fork) and select the **Hobby** plan for personal, non-commercial use.
4. Keep the detected Python/FastAPI settings and select **Deploy**. No build command or environment variables are needed.
5. Once deployment finishes, use the generated `*.vercel.app` URL and test a safe and a demonstration message.

Vercel's Python runtime is currently in Beta. The Hobby plan is intended for personal, non-commercial projects and has usage limits. Scan history remains session-based and ephemeral.

## Other deployment targets

`python app.py` still runs the original Gradio server locally. `render.yaml` is retained for users who prefer Render, and the Hugging Face Space metadata remains available for eligible Spaces accounts.

## Demonstration messages

- Scam: `Congratulations! Apko JazzCash ki taraf se Rs 50,000 inaam mila hai. Apna OTP aur CNIC bhejein.`
- Scam: `Your account will be suspended today. Verify immediately by clicking http://example-login.com`
- Scam: `Ø¢Ù¾ Ú©Ùˆ 25000 Ø±ÙˆÙ¾Û’ Ø§Ù†Ø¹Ø§Ù… Ù…Ù„Ø§ ÛÛ’Û” Ø±Ù‚Ù… Ø­Ø§ØµÙ„ Ú©Ø±Ù†Û’ Ú©Û’ Ù„ÛŒÛ’ Ø§Ù¾Ù†Ø§ Ø§Ùˆ Ù¹ÛŒ Ù¾ÛŒ Ø¨Ú¾ÛŒØ¬ÛŒÚºÛ”`
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
