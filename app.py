"""ScamShield PK — explainable multilingual scam message analysis."""
from pathlib import Path
import json
import os
import gradio as gr
from config import APP_NAME, MAX_MESSAGE_LENGTH, DISCLAIMER
from explanation_engine import explain
from history import add_entry, render_history
from ui_components import result_html

BASE=Path(__file__).parent
CSS=(BASE/"assets"/"style.css").read_text(encoding="utf-8")
DEMO=json.loads((BASE/"data"/"demo_messages.json").read_text(encoding="utf-8"))
DEMO_MAP={x["id"]:x for x in DEMO}

def scan_message(message, source, history):
    if not message or not message.strip(): return "<div class='empty-state'>Enter a message to begin your analysis.</div>", history or [], "Please paste a message first."
    if len(message)>MAX_MESSAGE_LENGTH: return "<div class='empty-state'>This message is too long to scan. Please keep it under 12,000 characters.</div>", history or [], "Message exceeds the 12,000 character limit."
    try:
        result=explain(message); result["source"]=source
        return result_html(result), add_entry(history,message,result), "Analysis complete — review the signals and actions below."
    except Exception:
        return "<div class='empty-state'>We could not analyze this message. Please try a shorter message or different text.</div>", history or [], "Analysis could not be completed."

def load_demo(choice):
    demo=DEMO_MAP.get(choice)
    return demo["message"] if demo else ""

def home_html():
    return """<main class='home-page'>
      <section class='hero'>
        <div class='hero-copy'><div class='kicker'><span class='live-dot'></span> DIGITAL SAFETY, BUILT FOR PAKISTAN</div>
          <h1>Confidence starts<br>with a second look.</h1>
          <p class='hero-lede'>AI-powered protection from digital scams</p>
          <p>Check suspicious SMS, WhatsApp, email and social messages in English, Urdu or Roman Urdu. See the signals, understand the risk, and know what to do next.</p>
          <div class='hero-proof'><span>EN&nbsp; English</span><i></i><span>ع&nbsp; Urdu</span><i></i><span>RU&nbsp; Roman Urdu</span></div>
          <div class='hero-actions'><a class='hero-primary' href='#' onclick="const t=[...document.querySelectorAll('#main-navigation [role=tab],#main-navigation .tab-nav button')].find(x=>x.textContent.trim()==='Scan');if(t)t.click();return false;">Check a message <span>→</span></a><a class='hero-secondary' href='#how-it-works'>How it works</a></div>
        </div>
        <div class='hero-visual' aria-hidden='true'><div class='orbit orbit-one'></div><div class='orbit orbit-two'></div><div class='shield-tile'><span class='shield-icon'>✓</span></div><div class='floating-card'><span class='float-check'>✓</span><div><b>Clear, explainable results</b><small>Signals · context · next steps</small></div></div><div class='hero-caption'><span class='live-dot'></span> PRIVATE BY DESIGN <span>·</span> NO ACCOUNT REQUIRED</div></div>
      </section>
      <div class='trust-ribbon'><span class='trust-mark'>✳</span><span><b>Made for the messages people receive here.</b> Locally relevant patterns for wallets, banks, public programs and more.</span></div>
      <section class='content-section'><div class='section-heading'><div><div class='eyebrow-dark'>A SAFER WAY TO CHECK</div><h2 class='section-title'>Built for Pakistan</h2></div><p class='section-copy'>Useful context. Clear explanations.<br>No false certainty.</p></div>
        <div class='feature-grid'><article class='feature'><span class='feature-icon icon-language'>ع</span><h3>Urdu support</h3><p>Unicode Urdu messages stay intact through analysis.</p></article><article class='feature'><span class='feature-icon icon-roman'>RU</span><h3>Roman Urdu</h3><p>Recognizes common Roman Urdu scam language.</p></article><article class='feature'><span class='feature-icon icon-english'>EN</span><h3>English</h3><p>Checks familiar phishing and pressure patterns.</p></article><article class='feature'><span class='feature-icon'>◎</span><h3>Explainable results</h3><p>See the signals behind every advisory score.</p></article><article class='feature'><span class='feature-icon'>◇</span><h3>Privacy focused</h3><p>No account required. Scan history stays in your session.</p></article><article class='feature'><span class='feature-icon'>↗</span><h3>Lightweight by design</h3><p>Runs on CPU without a paid API or model download.</p></article></div>
      </section>
      <section class='content-section how-section' id='how-it-works'><div class='eyebrow-dark'>A CLEAR FOUR-STEP CHECK</div><h2 class='section-title'>From message to next step.</h2><div class='steps'><article class='step'><span class='step-num'>01</span><div><b>PASTE</b><h3>Bring the message</h3><p>SMS, email, chat or social post.</p></div></article><article class='step'><span class='step-num'>02</span><div><b>ANALYZE</b><h3>Check the context</h3><p>Language, links and risk signals.</p></div></article><article class='step'><span class='step-num'>03</span><div><b>UNDERSTAND</b><h3>Review the risk</h3><p>A score with reasons you can follow.</p></div></article><article class='step'><span class='step-num'>04</span><div><b>ACT</b><h3>Choose a safer next step</h3><p>Practical guidance, without guesswork.</p></div></article></div></section>
      <section class='content-section categories-section'><div class='eyebrow-dark'>LOCAL SCAM PATTERNS</div><h2 class='section-title'>Common tactics, easier to spot.</h2><div class='category-grid'><div class='category'><span>01</span>Banking alerts</div><div class='category'><span>02</span>JazzCash / Easypaisa</div><div class='category'><span>03</span>BISP / Ehsaas</div><div class='category'><span>04</span>OTP theft</div><div class='category'><span>05</span>Fake jobs</div><div class='category'><span>06</span>Prize scams</div><div class='category'><span>07</span>Investment fraud</div></div></section>
    </main>"""

def safety_html():
    return """<h1 class='section-title'>Stay Safe Online</h1><p class='section-copy'>A few habits can stop many common social-engineering attempts.</p><div class='doc-grid'><article class='doc-card'><h3>Never share</h3><p>OTP codes · PINs · passwords · verification codes · card CVV</p><p>Legitimate support should not ask you to send these secrets in chat.</p></article><article class='doc-card'><h3>Verify independently</h3><p>Open the official app manually, type a known official website address, or call a verified number. Avoid using contact details or links supplied in the suspicious message.</p></article><article class='doc-card'><h3>Common warning signs</h3><p>Urgency · unexpected prizes · threats · requests for money · OTP requests · suspicious URLs · unusually attractive offers</p></article><article class='doc-card'><h3>If you already responded</h3><ol><li>Change exposed passwords from a trusted device.</li><li>Contact your bank or wallet using official channels.</li><li>Block cards or account access where appropriate.</li><li>Review recent transactions and report suspicious activity.</li><li>Stop communicating with the suspicious sender.</li></ol></article></div>"""

def details_html():
    return """<h1 class='section-title'>Product Details</h1><p class='section-copy'>How ScamShield PK works — current behavior, design choices and limitations.</p><div class='doc-grid'><article class='doc-card'><h3>Product vision</h3><p>Make scam detection accessible to ordinary users through multilingual, explainable risk analysis adapted to Pakistan's digital communication environment.</p></article><article class='doc-card'><h3>The problem</h3><p>Scams exploit financial brands, mobile wallets, government programs, fake rewards, OTP requests, job seekers, urgency and fear. It can be hard to distinguish these messages from genuine communication.</p></article><article class='doc-card'><h3>The solution</h3><p>Users paste suspicious text. The system checks language, patterns, scam indicators, contextual combinations, URLs and credential requests, then returns a risk score, categories, reasons and safety recommendations.</p></article><article class='doc-card'><h3>Target users</h3><p>Everyday Pakistani users, students, job seekers, older adults, online shoppers, mobile wallet users, small businesses and digital banking customers.</p></article><article class='doc-card'><h3>Supported languages</h3><p>English, Urdu, Roman Urdu and mixed-language messages. Language detection uses transparent Unicode and vocabulary heuristics and may be imperfect for short text.</p></article><article class='doc-card'><h3>How AI is used today</h3><p>This MVP implements language-aware preprocessing and explainable pattern scoring. No fine-tuned transformer or scam model is currently active. A future version can add a carefully evaluated XLM-RoBERTa model.</p></article><article class='doc-card'><h3>Why a hybrid design</h3><p>Rule signals are interpretable for OTP requests, links, urgency and identity details. A future multilingual model may improve contextual understanding while keeping visible explanations and human-readable factors.</p></article><article class='doc-card'><h3>Technology</h3><p>Python · Gradio · regular expressions · Hugging Face Spaces · standard library. XLM-RoBERTa is a future model option only; Transformers and scikit-learn are not required to run this MVP.</p></article></div><h2 class='section-title'>Architecture</h2><div class='pipeline'>User message → Gradio interface → Unicode-safe preprocessing → Language detection<br>Language-aware pattern signals → Contextual risk fusion → Category classification<br>Explanation and recommended action → Structured result in the interface</div><h2 class='section-title'>Processing pipeline</h2><div class='steps'><div class='step'><b>01</b><p>Message input</p></div><div class='step'><b>02</b><p>Normalization</p></div><div class='step'><b>03</b><p>Language detection</p></div><div class='step'><b>04</b><p>Signal extraction</p></div><div class='step'><b>05</b><p>Risk fusion</p></div><div class='step'><b>06</b><p>Classification</p></div><div class='step'><b>07</b><p>Explanation</p></div><div class='step'><b>08</b><p>Safety guidance</p></div></div><div class='doc-grid'><article class='doc-card'><h3>Risk scoring methodology</h3><p>Risk points are assigned for indicators such as credential requests, urgency, links, financial context, impersonation, prizes, money requests and threats. Combinations raise risk when context supports it, such as OTP plus prize. Scores cap at 100 and are not statistically calibrated probabilities.</p></article><article class='doc-card'><h3>URL analysis</h3><p>URLs and common shorteners are detected locally. A link is treated as a risk indicator; no external reputation service or live domain lookup is used. A URL alone is not proof that a message is malicious.</p></article><article class='doc-card'><h3>Privacy</h3><p>No account or personal information is required. Scan history is held in Gradio session state and is not intentionally persisted. Remove sensitive details before scanning; the MVP does not intentionally store OTPs, passwords, PINs, full CNICs or card details.</p></article><article class='doc-card'><h3>Limitations</h3><p>False positives can occur; legitimate messages may contain suspicious words; new scam styles may not be recognized; short messages can be hard to classify. The score is advisory. Independently verify important financial messages.</p></article></div><h2 class='section-title'>Roadmap</h2><div class='roadmap'><div class='phase'><b>Phase 1 · MVP</b><p>Multilingual analysis, risk scoring, explanations and recommendations.</p></div><div class='phase'><b>Phase 2 · AI model</b><p>Build a labeled dataset, fine-tune XLM-RoBERTa, measure precision, recall and F1.</p></div><div class='phase'><b>Phase 3 · Threat intel</b><p>Reputation checks for malicious URLs and domains.</p></div><div class='phase'><b>Phase 4 · Expansion</b><p>Browser extension, Android app, WhatsApp and Telegram integrations.</p></div><div class='phase'><b>Phase 5 · Community</b><p>Anonymous reports and emerging scam trend detection.</p></div></div>"""

ABOUT="""<h1 class='section-title'>About ScamShield PK</h1><div class='doc-card'><p>ScamShield PK is an AI-assisted prototype designed to improve digital scam awareness and explainable message screening for Pakistani users. It is an educational safety aid, not a replacement for official verification or professional advice.</p><p><b>Version</b> · MVP 1.0<br><b>Status</b> · Prototype<br><b>Deployment target</b> · Hugging Face Spaces<br><b>Runtime</b> · CPU friendly, no external API keys</p></div>"""

with gr.Blocks(title=APP_NAME, css=CSS, theme=gr.themes.Base(primary_hue="blue", secondary_hue="cyan"), elem_id="scamshield-app") as demo:
    history_state=gr.State([])
    gr.HTML("<header class='brandbar'><div class='brand'><span class='brand-mark'>S</span><span class='brand-type'>ScamShield <em>PK</em><small>AI-powered message safety</small></span></div><div class='header-assurance'><span class='assurance-dot'></span> PRIVATE SESSION <span class='header-divider'></span> BUILT FOR PAKISTAN</div></header>")
    with gr.Tabs(elem_id="main-navigation"):
        with gr.Tab("Overview", id="home"):
            gr.HTML(home_html())
        with gr.Tab("Scan", id="scan"):
            gr.HTML("<div class='page-intro'><div class='eyebrow-dark'>MESSAGE CHECK</div><h1>Take a closer look.</h1><p>Paste a suspicious message to see its risk signals and safer next steps.</p></div>")
            gr.HTML("<div class='privacy'><span class='privacy-symbol'>!</span><span><b>Protect your information</b><small>Remove passwords, OTPs, PINs, full CNIC numbers and card details before scanning.</small></span></div>")
            with gr.Row(elem_classes=["scan-layout"]):
                with gr.Column(scale=7, elem_classes=["scan-form-card"]):
                    gr.HTML("<div class='card-overline'>YOUR MESSAGE</div>")
                    message=gr.Textbox(label="Message to analyze", placeholder="Paste SMS, WhatsApp, email or social message here…", lines=8, max_lines=14, elem_id="message-input")
                    source=gr.Dropdown(["SMS","WhatsApp","Email","Telegram","Social Media","Other"],value="WhatsApp",label="Where did you receive it?", elem_id="message-source")
                    with gr.Row():
                        analyze=gr.Button("Analyze message",variant="primary",scale=3,elem_classes=["analyze-button"])
                        clear=gr.Button("Clear",scale=1,elem_classes=["quiet-button"])
                    status=gr.Markdown(elem_classes=["scan-status"])
                with gr.Column(scale=4, elem_classes=["demo-card"]):
                    gr.HTML("<div class='demo-card-heading'><span class='demo-spark'>✳</span><div><div class='card-overline'>EXPLORE A SAMPLE</div><h3>Try a demo message</h3></div></div><p class='demo-copy'>See how the analysis explains common messages. Examples are fictional.</p>")
                    chosen=gr.Dropdown([x["id"] for x in DEMO],label="Choose a message",elem_id="demo-picker")
                    load=gr.Button("Load selected sample",elem_classes=["demo-button"])
                    gr.HTML("<div class='demo-note'><span>i</span> Demo messages are examples for exploration, not training data.</div>")
            gr.HTML("<div class='report-heading'><div><div class='eyebrow-dark'>YOUR RESULTS</div><h2>Analysis report</h2></div><span class='report-private'>SESSION ONLY</span></div>")
            report=gr.HTML("<div class='empty-state'><span class='empty-icon'>⌕</span><b>Nothing to review yet</b><span>Paste a message above and select <strong>Analyze message</strong> to get an explainable report.</span></div>",elem_classes=["report-output"])
            analyze.click(scan_message,[message,source,history_state],[report,history_state,status])
            load.click(load_demo,chosen,message)
            clear.click(lambda: ("", "<div class='empty-state'>Your explainable scan report will appear here.</div>", ""),None,[message,report,status])
        with gr.Tab("History", id="history"):
            gr.HTML("<div class='page-intro'><div class='eyebrow-dark'>YOUR RECENT CHECKS</div><h1>Scan history</h1><p>Only visible in this session. Clear it any time.</p></div>")
            with gr.Row():
                rf=gr.Dropdown(["All levels","Low Risk","Suspicious","High Risk","Critical Scam Risk"],value="All levels",label="Risk level",scale=1)
                lf=gr.Dropdown(["All languages","English","Urdu","Roman Urdu","Mixed / Roman Urdu","Mixed / Urdu"],value="All languages",label="Language",scale=1)
                tf=gr.Dropdown(["All types","OTP Theft","Prize Scam","Mobile Wallet Scam","Banking Scam","Government Impersonation","Fake Job Scam","Loan Scam","Investment Scam","Delivery Scam","Suspicious Link"],value="All types",label="Scam type",scale=1)
                clear_hist=gr.Button("Clear history",elem_classes=["quiet-button"],scale=0)
            hist_table=gr.HTML("<div class='empty-state'><span class='empty-icon'>◷</span><b>No scans yet</b><span>Your session's message checks will appear here.</span></div>",elem_classes=["history-output"])
            for filt in (rf,lf,tf): filt.change(render_history,[history_state,rf,lf,tf],hist_table)
            analyze.click(render_history,[history_state,rf,lf,tf],hist_table)
            clear_hist.click(lambda: ([],"<div class='empty-state'>History cleared for this session.</div>"),None,[history_state,hist_table])
        with gr.Tab("Safety Center", id="safety"):
            gr.HTML(safety_html())
        with gr.Tab("Product Details", id="details"):
            gr.HTML(details_html())
        with gr.Tab("About", id="about"):
            gr.HTML(ABOUT)
    gr.HTML("<footer class='footer'><span class='footer-brand'>ScamShield <b>PK</b></span><span>Risk checks are advisory. Verify important messages independently.</span><span>SESSION-BASED · NO ACCOUNT NEEDED</span></footer>")

if __name__ == "__main__":
    demo.queue(default_concurrency_limit=8).launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
    )
