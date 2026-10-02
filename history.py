from datetime import datetime, timezone
import html

def add_entry(history, message, result):
    history=list(history or [])
    history.insert(0,{"time":datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M"),"preview":(message or "")[:100],"language":result["language"],"score":result["risk_score"],"level":result["risk_level"],"type":", ".join(result["scam_types"])})
    return history[:50]

def render_history(history, risk_filter="All levels", language_filter="All languages", type_filter="All types"):
    entries=history or []
    if risk_filter!="All levels": entries=[x for x in entries if x["level"]==risk_filter]
    if language_filter!="All languages": entries=[x for x in entries if x["language"]==language_filter]
    if type_filter!="All types": entries=[x for x in entries if type_filter in x["type"]]
    if not entries: return "<div class='empty-state'>No scans match these filters. Your history is kept only for this session.</div>"
    rows="".join(f"<tr><td>{html.escape(str(e['time']))}</td><td>{html.escape(str(e['preview']))}</td><td>{html.escape(str(e['language']))}</td><td><b>{int(e['score'])}/100</b></td><td>{html.escape(str(e['level']))}</td><td>{html.escape(str(e['type']))}</td></tr>" for e in entries)
    return f"<div class='table-wrap'><table><thead><tr><th>Date / time</th><th>Message preview</th><th>Language</th><th>Risk score</th><th>Risk level</th><th>Scam type</th></tr></thead><tbody>{rows}</tbody></table></div>"
