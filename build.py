#!/usr/bin/env python3
"""
EPICUltra Site Builder
Reads content.md and regenerates all HTML pages.
Run: python3 build.py
"""

import re
import os

# ── Read content.md ──────────────────────────────────────────────────────────
with open("content.md", "r", encoding="utf-8") as f:
    RAW = f.read()

def extract_section(label):
    pattern = rf"## PAGE: {label}.*?(?=\n## PAGE:|\n## SHARED|\Z)"
    m = re.search(pattern, RAW, re.DOTALL)
    return m.group(0) if m else ""

def between(text, start, end=None):
    if end:
        m = re.search(rf"{re.escape(start)}(.*?){re.escape(end)}", text, re.DOTALL)
    else:
        m = re.search(rf"{re.escape(start)}(.*?)$", text, re.DOTALL)
    return m.group(1).strip() if m else ""

# ── Shared design tokens & components ────────────────────────────────────────
NAV_LINKS = [
    ("Home", "index.html"),
    ("Architecture", "architecture.html"),
    ("AI Agents", "agents.html"),
    ("Governance", "governance.html"),
    ("Use Cases", "usecases.html"),
    ("About", "about.html"),
    ("Resources", "resources.html"),
]

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">'

CSS = """
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --violet:#6c47ff;--violet-dim:#4f30d4;--violet-glow:rgba(108,71,255,0.35);
  --teal:#00b894;--teal-dim:#00966e;--teal-glow:rgba(0,184,148,0.25);
  --bg:#050810;--bg2:#080d18;--bg3:#0d1220;
  --surface:#111827;--surface2:#161e30;--surface3:#1c2540;
  --border:rgba(108,71,255,0.2);--border2:rgba(0,245,200,0.15);
  --text:#e4e8f5;--text2:#8892b0;--text3:#4a5268;
  --nav-bg:rgba(5,8,16,0.85);
  --font:'Sora',sans-serif;--mono:'DM Mono',monospace;
  --r:8px;--r2:14px;--r3:20px;
}

/* ── Light theme ── */
[data-theme="light"]{
  --violet:#5a35e8;--violet-dim:#4527c9;--violet-glow:rgba(90,53,232,0.2);
  --teal:#00896e;--teal-dim:#006e59;--teal-glow:rgba(0,137,110,0.15);
  --bg:#f4f6fb;--bg2:#eef0f8;--bg3:#e8ebf5;
  --surface:#ffffff;--surface2:#f0f2fa;--surface3:#e4e8f5;
  --border:rgba(90,53,232,0.15);--border2:rgba(0,137,110,0.15);
  --text:#0f1525;--text2:#4a5580;--text3:#8892b0;
  --nav-bg:rgba(244,246,251,0.92);
}
[data-theme="light"] body::before{opacity:.15}
[data-theme="light"] .hero-bg{background:radial-gradient(ellipse 70% 60% at 60% 40%,rgba(90,53,232,.08) 0%,transparent 70%),radial-gradient(ellipse 50% 40% at 20% 80%,rgba(0,137,110,.06) 0%,transparent 60%)}
[data-theme="light"] .hero-grid{opacity:.2}
[data-theme="light"] .manifesto{background:linear-gradient(135deg,#fff 0%,#f4f6fb 100%)}
[data-theme="light"] .card{box-shadow:0 2px 12px rgba(15,21,37,.06)}
[data-theme="light"] .card:hover{box-shadow:0 8px 32px rgba(90,53,232,.12)}
[data-theme="light"] .agent-card{box-shadow:0 2px 12px rgba(15,21,37,.06)}
[data-theme="light"] .cta-section{background:linear-gradient(135deg,#fff 0%,#f0f2fa 100%)}
[data-theme="light"] nav{box-shadow:0 1px 20px rgba(15,21,37,.08)}
[data-theme="light"] .arch-layer.al-1{background:rgba(90,53,232,.1)}
[data-theme="light"] .arch-layer.al-2{background:rgba(90,53,232,.07)}
[data-theme="light"] .arch-layer.al-3{background:rgba(0,137,110,.07)}
[data-theme="light"] .arch-layer.al-4{background:rgba(0,137,110,.1)}
[data-theme="light"] .arch-layer.al-5{background:rgba(0,137,110,.14)}
[data-theme="light"] .metric{background:#fff}
[data-theme="light"] .sec-stat{background:#fff}
[data-theme="light"] .compliance-item{background:#fff}
[data-theme="light"] .pillar{background:#fff}
[data-theme="light"] .resource-card{background:#fff}
[data-theme="light"] .webinar-card{background:#fff}
[data-theme="light"] .uc-item{background:#fff}
[data-theme="light"] .flow-num{background:#f0f2fa}
[data-theme="light"] .int-tag{background:#f0f2fa}

/* ── Theme toggle button ── */
.theme-toggle{width:40px;height:40px;border-radius:50%;border:1px solid var(--border);background:var(--surface2);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1rem;transition:border-color .2s,background .2s,transform .15s;flex-shrink:0}
.theme-toggle:hover{border-color:var(--violet);transform:rotate(20deg)}
.theme-toggle .icon-dark{display:block}
.theme-toggle .icon-light{display:none}
[data-theme="light"] .theme-toggle .icon-dark{display:none}
[data-theme="light"] .theme-toggle .icon-light{display:block}

html{scroll-behavior:smooth}
body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.65;overflow-x:hidden;-webkit-font-smoothing:antialiased;transition:background .3s,color .3s}

/* ── Noise texture overlay ── */
body::before{content:'';position:fixed;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");pointer-events:none;z-index:9999;opacity:.4}

/* ── Nav ── */
nav{position:fixed;top:0;left:0;right:0;z-index:1000;padding:0 2rem;height:64px;display:flex;align-items:center;justify-content:space-between;background:var(--nav-bg);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);transition:background .3s}
.nav-logo{font-size:1.15rem;font-weight:700;color:var(--text);text-decoration:none;letter-spacing:-.02em}
.nav-logo span{color:var(--violet)}
.nav-links{display:flex;gap:2rem;list-style:none}
.nav-links a{font-size:.82rem;font-weight:500;color:var(--text2);text-decoration:none;letter-spacing:.04em;text-transform:uppercase;transition:color .2s}
.nav-links a:hover,.nav-links a.active{color:var(--teal)}
.nav-cta{background:var(--violet);color:#fff;padding:.5rem 1.25rem;border-radius:var(--r);font-size:.82rem;font-weight:600;text-decoration:none;letter-spacing:.02em;transition:background .2s,box-shadow .2s}
.nav-cta:hover{background:var(--violet-dim);box-shadow:0 0 20px var(--violet-glow)}
.nav-hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;background:none;border:none;padding:4px}
.nav-hamburger span{display:block;width:22px;height:2px;background:var(--text);transition:.3s}
@media(max-width:900px){
  .nav-links{display:none;position:fixed;top:64px;left:0;right:0;background:var(--bg2);flex-direction:column;gap:0;border-bottom:1px solid var(--border);padding:1rem 0}
  .nav-links.open{display:flex}
  .nav-links a{padding:.75rem 2rem;font-size:.9rem}
  .nav-hamburger{display:flex}
}

/* ── Layout ── */
.wrap{max-width:1160px;margin:0 auto;padding:0 2rem}
section{padding:6rem 0}
section:first-of-type{padding-top:9rem}

/* ── Badges ── */
.badge{display:inline-flex;align-items:center;gap:.5rem;font-family:var(--mono);font-size:.72rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--teal);border:1px solid var(--border2);border-radius:100px;padding:.35rem .9rem;margin-bottom:1.5rem}
.badge::before{content:'';display:block;width:6px;height:6px;border-radius:50%;background:var(--teal);box-shadow:0 0 8px var(--teal)}

/* ── Hero ── */
.hero{min-height:100vh;display:flex;align-items:center;padding-top:64px;position:relative;overflow:hidden}
.hero-bg{position:absolute;inset:0;background:radial-gradient(ellipse 70% 60% at 60% 40%,rgba(108,71,255,.12) 0%,transparent 70%),radial-gradient(ellipse 50% 40% at 20% 80%,rgba(0,245,200,.07) 0%,transparent 60%);pointer-events:none}
.hero-grid{position:absolute;inset:0;background-image:linear-gradient(var(--border) 1px,transparent 1px),linear-gradient(90deg,var(--border) 1px,transparent 1px);background-size:60px 60px;opacity:.35;pointer-events:none;mask-image:radial-gradient(ellipse 80% 80% at 50% 50%,black 30%,transparent 100%)}
.hero-content{position:relative;z-index:1;max-width:1000px}
.hero h1{font-size:clamp(3rem,6.5vw,5.8rem);font-weight:800;line-height:1.06;letter-spacing:-.04em;margin-bottom:3rem}
.hero h1 .accent{color:var(--violet)}
.hero h1 .accent-teal{color:var(--teal)}
.hero-sub{font-size:1.2rem;color:var(--text2);max-width:760px;margin-bottom:.75rem;line-height:1.7}
.hero-support{font-size:.95rem;color:var(--text3);max-width:720px;margin-bottom:2.5rem;font-family:var(--mono)}
.hero-btns{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:4rem}
.btn-primary{background:var(--violet);color:#fff;padding:.85rem 2rem;border-radius:var(--r);font-size:.9rem;font-weight:600;text-decoration:none;border:none;cursor:pointer;transition:background .2s,box-shadow .2s,transform .15s;letter-spacing:.01em}
.btn-primary:hover{background:var(--violet-dim);box-shadow:0 0 30px var(--violet-glow);transform:translateY(-1px)}
.btn-secondary{background:transparent;color:var(--text);padding:.85rem 2rem;border-radius:var(--r);font-size:.9rem;font-weight:500;text-decoration:none;border:1px solid var(--border);cursor:pointer;transition:border-color .2s,color .2s,transform .15s}
.btn-secondary:hover{border-color:var(--teal);color:var(--teal);transform:translateY(-1px)}
.hero-stats{display:flex;gap:3rem;flex-wrap:wrap}
.stat{display:flex;flex-direction:column;gap:.3rem}
.stat-val{font-size:2rem;font-weight:800;color:var(--text);letter-spacing:-.04em;line-height:1}
.stat-val span{color:var(--violet)}
.stat-label{font-family:var(--mono);font-size:.72rem;color:var(--text3);letter-spacing:.08em;text-transform:uppercase}

/* ── Section headers ── */
.section-header{margin-bottom:3.5rem}
.section-header h2{font-size:clamp(2.2rem,4.5vw,3.4rem);font-weight:800;letter-spacing:-.04em;line-height:1.1;margin-bottom:1rem}
.section-header p{font-size:1.1rem;color:var(--text2);max-width:760px;line-height:1.7}
.accent{color:var(--violet)}
.accent-teal{color:var(--teal)}

/* ── Cards ── */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r2);padding:2rem;transition:border-color .25s,transform .2s,box-shadow .25s}
.card:hover{border-color:var(--violet);transform:translateY(-3px);box-shadow:0 8px 40px rgba(108,71,255,.15)}
.card-icon{font-size:1.8rem;margin-bottom:1rem}
.card h3{font-size:1.05rem;font-weight:700;letter-spacing:-.02em;margin-bottom:.6rem}
.card p{font-size:.9rem;color:var(--text2);line-height:1.65}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem}
.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:1.25rem}
@media(max-width:900px){.grid-3,.grid-4{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.grid-3,.grid-4,.grid-2{grid-template-columns:1fr}}

/* ── Layer blocks ── */
.layer-block{display:grid;grid-template-columns:280px 1fr;gap:3rem;align-items:start;padding:3rem 0;border-bottom:1px solid var(--border)}
.layer-block:last-child{border-bottom:none}
.layer-num{font-family:var(--mono);font-size:.72rem;color:var(--text3);letter-spacing:.12em;text-transform:uppercase;margin-bottom:.5rem}
.layer-title{font-size:1.5rem;font-weight:800;letter-spacing:-.03em;margin-bottom:.75rem}
.layer-desc{font-size:.95rem;color:var(--text2);line-height:1.7;margin-bottom:1.5rem}
.feature-list{list-style:none;display:flex;flex-direction:column;gap:.85rem}
.feature-list li{display:flex;align-items:flex-start;gap:.75rem;font-size:.9rem;color:var(--text2);line-height:1.5}
.feature-list li::before{content:'→';color:var(--teal);flex-shrink:0;margin-top:.05em}
.feature-list strong{color:var(--text)}
.tag-active,.tag-streaming,.tag-enforced,.tag-live{font-family:var(--mono);font-size:.65rem;font-weight:500;padding:.2rem .55rem;border-radius:4px;margin-left:.5rem;vertical-align:middle;letter-spacing:.06em}
.tag-active{background:rgba(0,245,200,.12);color:var(--teal);border:1px solid rgba(0,245,200,.2)}
.tag-streaming{background:rgba(108,71,255,.12);color:var(--violet);border:1px solid rgba(108,71,255,.2)}
.tag-enforced{background:rgba(255,80,80,.1);color:#ff6b6b;border:1px solid rgba(255,80,80,.2)}
.tag-live{background:rgba(0,245,200,.08);color:var(--teal-dim);border:1px solid rgba(0,245,200,.15)}
@media(max-width:800px){.layer-block{grid-template-columns:1fr}}

/* ── Agent cards ── */
.agent-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r2);padding:2rem;display:flex;flex-direction:column;gap:1rem;transition:border-color .25s,box-shadow .25s}
.agent-card:hover{border-color:var(--violet);box-shadow:0 8px 40px rgba(108,71,255,.12)}
.agent-role{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:.25rem}
.role-tag{font-family:var(--mono);font-size:.65rem;font-weight:500;letter-spacing:.08em;color:var(--teal);border:1px solid var(--border2);border-radius:4px;padding:.2rem .55rem}
.agent-card h3{font-size:1.1rem;font-weight:700;letter-spacing:-.02em}
.agent-detail{display:flex;flex-direction:column;gap:.5rem}
.agent-detail-row{font-size:.82rem;color:var(--text2);display:flex;gap:.5rem;line-height:1.5}
.agent-detail-row strong{color:var(--text3);font-family:var(--mono);font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;flex-shrink:0;min-width:70px}
.agent-integrations{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.5rem}
.int-tag{font-family:var(--mono);font-size:.65rem;color:var(--text3);border:1px solid var(--surface3);border-radius:4px;padding:.2rem .5rem}

/* ── Flow steps ── */
.flow{display:flex;flex-direction:column;gap:0}
.flow-step{display:flex;gap:1.25rem;align-items:flex-start;padding:1rem 0;position:relative}
.flow-step:not(:last-child)::after{content:'';position:absolute;left:15px;top:44px;bottom:-4px;width:1px;background:linear-gradient(var(--border),transparent)}
.flow-num{width:32px;height:32px;border-radius:50%;background:var(--surface2);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:.72rem;color:var(--violet);flex-shrink:0}
.flow-text strong{font-size:.9rem;font-weight:600;display:block;margin-bottom:.25rem}
.flow-text span{font-size:.82rem;color:var(--text2)}

/* ── Metrics grid ── */
.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:var(--r2);overflow:hidden;margin-top:2rem}
.metric{background:var(--surface);padding:1.25rem 1.5rem}
.metric-val{font-size:1.35rem;font-weight:700;color:var(--teal);letter-spacing:-.03em;margin-bottom:.3rem}
.metric-label{font-family:var(--mono);font-size:.7rem;color:var(--text3);letter-spacing:.08em;text-transform:uppercase}
@media(max-width:700px){.metrics{grid-template-columns:repeat(2,1fr)}}

/* ── Use case tabs ── */
.uc-tabs{display:flex;gap:.5rem;margin-bottom:2.5rem;flex-wrap:wrap}
.uc-tab{font-family:var(--mono);font-size:.75rem;font-weight:500;letter-spacing:.06em;text-transform:uppercase;padding:.5rem 1.25rem;border-radius:100px;border:1px solid var(--border);color:var(--text2);background:transparent;cursor:pointer;transition:.2s}
.uc-tab.active,.uc-tab:hover{background:var(--violet);border-color:var(--violet);color:#fff}
.uc-panel{display:none}
.uc-panel.active{display:block}
.uc-item{border-left:2px solid var(--border);padding:1.25rem 1.5rem;margin-bottom:1rem;background:var(--surface);border-radius:0 var(--r) var(--r) 0;transition:.2s}
.uc-item:hover{border-left-color:var(--violet)}
.uc-item h4{font-size:.95rem;font-weight:700;margin-bottom:.4rem}
.uc-item p{font-size:.88rem;color:var(--text2);line-height:1.6;margin-bottom:.5rem}
.uc-result{font-family:var(--mono);font-size:.75rem;color:var(--teal);letter-spacing:.04em}
.uc-agents{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1.5rem}
.uc-agent-tag{font-family:var(--mono);font-size:.68rem;color:var(--text3);border:1px solid var(--surface3);border-radius:4px;padding:.2rem .6rem}

/* ── Governance pillars ── */
.pillar{background:var(--surface);border:1px solid var(--border);border-radius:var(--r2);padding:2rem;transition:.25s}
.pillar:hover{border-color:var(--teal);box-shadow:0 4px 30px var(--teal-glow)}
.pillar-icon{font-size:2rem;margin-bottom:1rem}
.pillar h3{font-size:1rem;font-weight:700;letter-spacing:-.02em;margin-bottom:.6rem}
.pillar p{font-size:.88rem;color:var(--text2);line-height:1.65}

/* ── Compliance table ── */
.compliance-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:var(--r2);overflow:hidden}
.compliance-item{background:var(--surface);padding:1.5rem}
.compliance-name{font-size:.9rem;font-weight:600}
.compliance-status{font-family:var(--mono);font-size:.68rem;letter-spacing:.08em;padding:.25rem .65rem;border-radius:4px}
.status-progress{background:rgba(108,71,255,.12);color:var(--violet);border:1px solid rgba(108,71,255,.2)}
.status-compliant{background:rgba(0,245,200,.1);color:var(--teal);border:1px solid rgba(0,245,200,.2)}
.status-supported{background:rgba(255,200,50,.08);color:#ffc832;border:1px solid rgba(255,200,50,.2)}
.status-roadmap{background:rgba(255,255,255,.04);color:var(--text3);border:1px solid var(--border)}
@media(max-width:700px){.compliance-grid{grid-template-columns:1fr}}

/* ── Security stats ── */
.sec-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:var(--r2);overflow:hidden;margin-bottom:3rem}
.sec-stat{background:var(--surface);padding:1.75rem;text-align:center}
.sec-stat-val{font-size:1.5rem;font-weight:800;color:var(--violet);letter-spacing:-.04em;margin-bottom:.4rem}
.sec-stat-label{font-family:var(--mono);font-size:.68rem;color:var(--text3);letter-spacing:.08em;text-transform:uppercase;margin-bottom:.3rem}
.sec-stat-desc{font-size:.8rem;color:var(--text2)}
@media(max-width:700px){.sec-stats{grid-template-columns:repeat(2,1fr)}}

/* ── About tenets ── */
.tenet{padding:2.5rem 0;border-bottom:1px solid var(--border);display:grid;grid-template-columns:200px 1fr;gap:2.5rem;align-items:start}
.tenet:last-child{border-bottom:none}
.tenet-num{font-family:var(--mono);font-size:.72rem;color:var(--violet);letter-spacing:.12em;text-transform:uppercase}
.tenet-title{font-size:1.2rem;font-weight:700;letter-spacing:-.03em;margin-bottom:.75rem}
.tenet p{font-size:.95rem;color:var(--text2);line-height:1.75}
@media(max-width:700px){.tenet{grid-template-columns:1fr;gap:1rem}}

/* ── Quote ── */
.manifesto{background:linear-gradient(135deg,var(--surface) 0%,var(--surface2) 100%);border:1px solid var(--border);border-left:3px solid var(--violet);border-radius:var(--r2);padding:3rem;margin:3rem 0;position:relative;overflow:hidden}
.manifesto::before{content:'"';position:absolute;top:-1rem;left:1.5rem;font-size:8rem;color:rgba(108,71,255,.08);font-weight:800;line-height:1;pointer-events:none}
.manifesto p{font-size:1.35rem;font-weight:600;line-height:1.55;letter-spacing:-.02em;color:var(--text);position:relative}

/* ── Resources ── */
.resource-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r2);padding:1.75rem;transition:.25s}
.resource-card:hover{border-color:var(--violet);transform:translateX(4px)}
.resource-type{font-family:var(--mono);font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--text3);margin-bottom:.35rem}
.resource-title{font-size:.95rem;font-weight:600;margin-bottom:.3rem}
.resource-desc{font-size:.83rem;color:var(--text2)}
.resource-dl{flex-shrink:0;background:var(--surface2);border:1px solid var(--border);border-radius:var(--r);padding:.6rem 1.1rem;font-size:.8rem;color:var(--text2);text-decoration:none;cursor:pointer;transition:.2s;white-space:nowrap}
.resource-dl:hover{border-color:var(--violet);color:var(--violet)}
.webinar-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r2);padding:1.5rem;display:flex;justify-content:space-between;align-items:center;gap:1rem;transition:.25s}
.webinar-card:hover{border-color:var(--teal)}
.webinar-date{font-family:var(--mono);font-size:.72rem;color:var(--text3)}
.webinar-title{font-size:.92rem;font-weight:600;margin:.3rem 0}
.webinar-status{font-family:var(--mono);font-size:.68rem;padding:.25rem .65rem;border-radius:4px;flex-shrink:0}
.ws-available{background:rgba(0,245,200,.1);color:var(--teal);border:1px solid rgba(0,245,200,.2)}
.ws-register{background:rgba(108,71,255,.12);color:var(--violet);border:1px solid rgba(108,71,255,.2)}

/* ── CTA section ── */
.cta-section{background:linear-gradient(135deg,var(--surface) 0%,var(--surface2) 100%);border:1px solid var(--border);border-radius:var(--r3);padding:5rem 4rem;text-align:center;position:relative;overflow:hidden}
.cta-section::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 80% at 50% 50%,rgba(108,71,255,.08) 0%,transparent 70%);pointer-events:none}
.cta-section h2{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;letter-spacing:-.04em;margin-bottom:1rem;position:relative}
.cta-section p{font-size:1rem;color:var(--text2);max-width:480px;margin:0 auto 2.5rem;position:relative;line-height:1.7}
.cta-btns{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;position:relative}

/* ── Position statement ── */
.position-list{list-style:none;display:flex;flex-direction:column;gap:.6rem}
.position-list li{display:flex;align-items:center;gap:.75rem;font-size:.95rem;color:var(--text2)}
.position-list li::before{content:'';width:8px;height:8px;border-radius:50%;background:var(--teal);flex-shrink:0;box-shadow:0 0 8px var(--teal)}

/* ── About split grid ── */
.about-split{display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start}
@media(max-width:700px){.about-split{grid-template-columns:1fr;gap:2.5rem}}

/* ── How different ── */
.diff-item{padding:1.75rem 0;border-bottom:1px solid var(--border);display:grid;grid-template-columns:1fr 2fr;gap:2rem}
.diff-item:last-child{border-bottom:none}
.diff-title{font-size:1rem;font-weight:700;color:var(--text)}
.diff-desc{font-size:.92rem;color:var(--text2);line-height:1.7}
@media(max-width:700px){.diff-item{grid-template-columns:1fr}}

/* ── Architecture stack visual ── */
.arch-stack{display:flex;flex-direction:column;gap:2px;margin-top:2rem;border-radius:var(--r2);overflow:hidden;border:1px solid var(--border)}
.arch-layer{padding:1rem 1.5rem;display:flex;justify-content:space-between;align-items:center;font-size:.88rem;font-weight:500;transition:.2s}
.arch-layer:hover{filter:brightness(1.1)}
.arch-layer-label{font-family:var(--mono);font-size:.68rem;color:rgba(255,255,255,.5);letter-spacing:.08em}
.al-1{background:rgba(108,71,255,.25);border-bottom:1px solid rgba(108,71,255,.15)}
.al-2{background:rgba(108,71,255,.18)}
.al-3{background:rgba(0,245,200,.12)}
.al-4{background:rgba(0,245,200,.18)}
.al-5{background:rgba(0,245,200,.25)}

/* ── Footer ── */
footer{border-top:1px solid var(--border);padding:2.5rem 0;margin-top:2rem}
.footer-inner{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1.5rem}
.footer-logo{font-size:1rem;font-weight:700;color:var(--text);letter-spacing:-.02em}
.footer-logo span{color:var(--violet)}
.footer-tag{font-size:.82rem;color:var(--text3);margin-top:.25rem}
.footer-links{display:flex;gap:2rem;list-style:none;flex-wrap:wrap}
.footer-links a{font-size:.8rem;color:var(--text3);text-decoration:none;transition:color .2s}
.footer-links a:hover{color:var(--teal)}
.footer-copy{font-family:var(--mono);font-size:.7rem;color:var(--text3)}

/* ── Animations ── */
@keyframes fadeUp{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
.animate-up{animation:fadeUp .6s ease both}
.animate-up-2{animation:fadeUp .6s .15s ease both}
.animate-up-3{animation:fadeUp .6s .3s ease both}
.animate-up-4{animation:fadeUp .6s .45s ease both}

/* ── Misc ── */
.divider{height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:2rem 0}
.mono{font-family:var(--mono)}
.text2{color:var(--text2)}
.mt-1{margin-top:1rem}.mt-2{margin-top:2rem}.mt-3{margin-top:3rem}
.mb-1{margin-bottom:1rem}.mb-2{margin-bottom:2rem}

/* ── Hero architecture animation ── */
.hero-arch{margin-top:3rem;border:1px solid var(--border);border-radius:var(--r2);overflow:hidden;background:var(--surface)}
.hero-arch-layer{display:flex;align-items:center;gap:1rem;padding:.85rem 1.5rem;border-bottom:1px solid var(--border);transition:.3s;cursor:default}
.hero-arch-layer:last-child{border-bottom:none}
.hero-arch-layer:hover{background:var(--surface2)}
.hal-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.hal-label{font-size:.85rem;font-weight:500;flex:1}
.hal-tag{font-family:var(--mono);font-size:.65rem;color:var(--text3);letter-spacing:.06em}

/* ── Feature highlight cards (teal bold) ── */
.feat-item{background:rgba(0,184,148,.04);border:1px solid rgba(0,184,148,.15);border-left:3px solid var(--teal);border-radius:var(--r);padding:1rem 1.25rem}
.feat-item strong{color:var(--teal);font-weight:700;font-size:.9rem;display:block;margin-bottom:.3rem}
.feat-item span{font-size:.85rem;color:var(--text2);line-height:1.6;display:block}
[data-theme="light"] .feat-item{background:rgba(0,137,110,.04);border-color:rgba(0,137,110,.2)}

/* ── Horizontal flow steps ── */
.flow-h{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:var(--r2);overflow:hidden;margin:2rem 0}
.flow-h-step{background:var(--surface2);padding:1.25rem 1.5rem;position:relative}
.flow-h-step:not(:last-child)::after{content:'→';position:absolute;right:-.55rem;top:1.25rem;color:var(--text3);font-size:.85rem;z-index:1;background:var(--surface2);padding:.1rem 0}
.flow-h-num{font-family:var(--mono);font-size:.64rem;color:var(--teal);letter-spacing:.08em;text-transform:uppercase;margin-bottom:.4rem}
.flow-h-step strong{font-size:.88rem;font-weight:600;display:block;margin-bottom:.3rem}
.flow-h-step span{font-size:.78rem;color:var(--text2);line-height:1.5}
@media(max-width:700px){.flow-h{grid-template-columns:1fr 1fr}}

/* ── Compact agent cards ── */
.agc{background:var(--surface);border:1px solid var(--border);border-radius:var(--r2);padding:1.75rem;display:flex;flex-direction:column;gap:.7rem;transition:border-color .25s,transform .2s,box-shadow .25s;position:relative;overflow:hidden}
.agc::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--violet),rgba(108,71,255,0))}
.agc:hover{border-color:var(--violet);transform:translateY(-3px);box-shadow:0 8px 32px rgba(108,71,255,.14)}
.agc-num{position:absolute;top:1.25rem;right:1.5rem;font-family:var(--mono);font-size:.68rem;color:var(--text3);letter-spacing:.06em}
.agc-icon{font-size:2rem}
.agc-name{font-size:1rem;font-weight:700;letter-spacing:-.02em}
.agc-roles{display:flex;gap:.35rem;flex-wrap:wrap}
.agc-role{font-family:var(--mono);font-size:.6rem;font-weight:500;letter-spacing:.08em;color:var(--teal);border:1px solid rgba(0,184,148,.2);border-radius:3px;padding:.15rem .5rem}
.agc-desc{font-size:.875rem;color:var(--text2);line-height:1.6;flex:1}
.agc-ints{display:flex;flex-wrap:wrap;gap:.3rem;padding-top:.25rem;border-top:1px solid var(--border)}
.agc-int{font-family:var(--mono);font-size:.6rem;color:var(--text3);border:1px solid var(--surface3);border-radius:3px;padding:.15rem .45rem;background:var(--surface2)}
/* ── Mandate bar ── */
.mandate-bar{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:var(--r2);overflow:hidden;margin-bottom:3.5rem}
.mb-item{background:var(--surface2);padding:1.5rem;text-align:center}
.mb-icon{font-size:1.5rem;margin-bottom:.5rem}
.mb-title{font-size:.85rem;font-weight:700;letter-spacing:-.01em;margin-bottom:.25rem}
.mb-desc{font-family:var(--mono);font-size:.68rem;color:var(--text3);letter-spacing:.04em}
@media(max-width:700px){.mandate-bar{grid-template-columns:repeat(2,1fr)}}

/* ── Layer timeline (Four Layers section) ── */
.lt-wrap{position:relative;margin-top:2.5rem}
.lt-line{position:absolute;left:27px;top:28px;bottom:28px;width:2px;background:linear-gradient(180deg,var(--violet),var(--teal));opacity:.25;pointer-events:none}
.lt-item{display:grid;grid-template-columns:56px 1fr;gap:2rem;padding:2rem 0;position:relative;align-items:start}
.lt-item:not(:last-child)::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:var(--border)}
.lt-num{width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:.8rem;font-weight:700;color:#fff;flex-shrink:0;position:relative;z-index:1;letter-spacing:.02em}
.lt-n1{background:linear-gradient(135deg,#5a35e8,#6c47ff);box-shadow:0 0 24px rgba(108,71,255,.4)}
.lt-n2{background:linear-gradient(135deg,#6c47ff,#8060ff)}
.lt-n3{background:linear-gradient(135deg,#5050cc,#6060dd)}
.lt-n4{background:linear-gradient(135deg,#00966e,#00b894)}
.lt-n5{background:linear-gradient(135deg,#00b894,#00c8a0);box-shadow:0 0 24px rgba(0,184,148,.35)}
.lt-icon{font-size:1.5rem;margin-bottom:.5rem}
.lt-title{font-size:1.2rem;font-weight:700;letter-spacing:-.03em;margin-bottom:.35rem}
.lt-desc{font-size:.93rem;color:var(--text2);line-height:1.7;margin-bottom:.8rem}
.lt-tags{display:flex;flex-wrap:wrap;gap:.4rem}
.lt-tag{font-family:var(--mono);font-size:.64rem;color:var(--teal);border:1px solid rgba(0,184,148,.2);border-radius:4px;padding:.2rem .6rem;background:rgba(0,184,148,.04)}
@media(max-width:700px){.lt-item{grid-template-columns:1fr}.lt-line{display:none}.lt-num{width:44px;height:44px}}

/* ── Principles numbered list ── */
.principle{display:grid;grid-template-columns:90px 1fr;gap:2rem;padding:2.25rem 0;border-bottom:1px solid var(--border);align-items:start;transition:border-color .2s}
.principle:last-child{border-bottom:none}
.principle:hover{border-bottom-color:rgba(108,71,255,.3)}
.principle-num{font-size:4rem;font-weight:800;letter-spacing:-.06em;line-height:1;font-family:var(--mono);color:var(--surface3)}
[data-theme="light"] .principle-num{color:var(--border)}
.principle-icon{font-size:1.4rem;margin-bottom:.5rem}
.principle-title{font-size:1.08rem;font-weight:700;letter-spacing:-.02em;margin-bottom:.5rem}
.principle-text{font-size:.95rem;color:var(--text2);line-height:1.75}
@media(max-width:600px){.principle{grid-template-columns:1fr}}

/* ── Stats strip ── */
.stat-strip{background:linear-gradient(90deg,rgba(108,71,255,.06) 0%,rgba(0,184,148,.06) 100%);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:3rem 0}
.stat-strip-inner{display:grid;grid-template-columns:repeat(4,1fr)}
.strip-stat{padding:0 2rem;border-right:1px solid var(--border);text-align:center}
.strip-stat:last-child{border-right:none}
.strip-val{font-size:3rem;font-weight:800;letter-spacing:-.05em;line-height:1;margin-bottom:.4rem;background:linear-gradient(135deg,var(--violet),var(--teal));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.strip-label{font-family:var(--mono);font-size:.7rem;color:var(--text3);letter-spacing:.08em;text-transform:uppercase}
@media(max-width:700px){.stat-strip-inner{grid-template-columns:repeat(2,1fr)}.strip-stat{padding:1rem;border-right:none;border-bottom:1px solid var(--border)}.strip-stat:nth-child(3),.strip-stat:last-child{border-bottom:none}}

/* ── Industry cards ── */
.industry-card{border:1px solid var(--border);border-radius:var(--r2);padding:2rem;background:var(--surface);position:relative;overflow:hidden;transition:transform .25s,box-shadow .25s,border-color .25s}
.industry-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.industry-card.ic-v::before{background:linear-gradient(90deg,var(--violet),rgba(108,71,255,.2))}
.industry-card.ic-t::before{background:linear-gradient(90deg,var(--teal),rgba(0,184,148,.2))}
.industry-card:hover{transform:translateY(-4px);box-shadow:0 12px 40px rgba(108,71,255,.12)}
.ic-num{position:absolute;bottom:-1.5rem;right:1.5rem;font-size:6rem;font-weight:800;font-family:var(--mono);color:rgba(255,255,255,.025);letter-spacing:-.05em;line-height:1;pointer-events:none;user-select:none}
[data-theme="light"] .ic-num{color:rgba(0,0,0,.04)}
.ic-label{font-size:1.1rem;font-weight:700;letter-spacing:-.02em;margin-bottom:.75rem}
.ic-desc{font-size:.9rem;color:var(--text2);margin-bottom:1.25rem;line-height:1.65}
.ic-list{list-style:none;display:flex;flex-direction:column;gap:.45rem}
.ic-list li{font-size:.83rem;color:var(--text3);display:flex;align-items:center;gap:.6rem}
.ic-list li::before{content:'';width:5px;height:5px;border-radius:50%;flex-shrink:0}
.ic-list.iv li::before{background:var(--violet)}
.ic-list.it li::before{background:var(--teal)}
</style>
"""

JS = """
<script>
// ── Apply saved theme immediately (before paint) ──
(function(){
  const t = localStorage.getItem('eu-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', t);
})();

document.addEventListener('DOMContentLoaded',()=>{
  // ── Theme toggle ──
  const toggle = document.getElementById('themeToggle');
  const applyTheme = (t) => {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('eu-theme', t);
  };
  if(toggle){
    toggle.addEventListener('click',()=>{
      const current = document.documentElement.getAttribute('data-theme');
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  // ── Nav hamburger ──
  const ham = document.getElementById('hamburger');
  const links = document.getElementById('navLinks');
  if(ham) ham.addEventListener('click',()=>links.classList.toggle('open'));

  // ── Active nav link ──
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a=>{
    if(a.getAttribute('href')===path) a.classList.add('active');
  });

  // ── Use case tabs ──
  document.querySelectorAll('.uc-tab').forEach(tab=>{
    tab.addEventListener('click',()=>{
      document.querySelectorAll('.uc-tab').forEach(t=>t.classList.remove('active'));
      document.querySelectorAll('.uc-panel').forEach(p=>p.classList.remove('active'));
      tab.classList.add('active');
      const panel = document.getElementById(tab.dataset.panel);
      if(panel) panel.classList.add('active');
    });
  });
});
</script>
"""

def nav(active_page=""):
    links_html = ""
    for label, href in NAV_LINKS:
        active = 'class="active"' if href == active_page else ""
        links_html += f'<li><a href="{href}" {active}>{label}</a></li>'
    return f"""
<nav>
  <div style="display:flex;align-items:center;gap:3rem">
    <a href="index.html" class="nav-logo">EPIC<span>Ultra</span></a>
    <ul class="nav-links" id="navLinks">{links_html}</ul>
  </div>
  <div style="display:flex;align-items:center;gap:.75rem">
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme" title="Toggle light/dark mode">
      <span class="icon-dark">🌙</span>
      <span class="icon-light">☀️</span>
    </button>
    <a href="#contact" class="nav-cta">Request Briefing</a>
    <button class="nav-hamburger" id="hamburger" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>"""

def footer():
    return """
<footer>
  <div class="wrap">
    <div class="footer-inner">
      <div>
        <div class="footer-logo">EPIC<span>Ultra</span></div>
        <div class="footer-tag">Enterprise AI engineered for accountability.</div>
      </div>
      <ul class="footer-links">
        <li><a href="index.html">Home</a></li>
        <li><a href="architecture.html">Architecture</a></li>
        <li><a href="agents.html">AI Agents</a></li>
        <li><a href="governance.html">Governance</a></li>
        <li><a href="usecases.html">Use Cases</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="resources.html">Resources</a></li>
      </ul>
      <div class="footer-copy">© 2026 EPICUltra · epicultra.ai</div>
    </div>
  </div>
</footer>"""

def cta_section():
    return """
<section id="contact">
  <div class="wrap">
    <div class="cta-section">
      <h2>Enterprise AI Engineered for <span class="accent">Accountability</span></h2>
      <p>No SDRs, no sales funnels. We engage directly with CROs, CIOs, and enterprise architects.</p>
      <div class="cta-btns">
        <a href="mailto:hello@epicultra.ai" class="btn-primary">Request Executive Briefing</a>
        <a href="architecture.html" class="btn-secondary">Explore Architecture</a>
      </div>
    </div>
  </div>
</section>"""

def page(title, active, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — EPICUltra</title>
<meta name="description" content="EPICUltra: Enterprise AI architecture engineered for accountability, governance, and mandate-controlled execution.">
<script>document.documentElement.setAttribute('data-theme',localStorage.getItem('eu-theme')||'dark')</script>
{FONTS}
{CSS}
</head>
<body>
{nav(active)}
{body}
{cta_section()}
{footer()}
{JS}
</body>
</html>"""


# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════
home_body = """
<section class="hero">
  <div class="hero-bg"></div>
  <div class="hero-grid"></div>
  <div class="wrap" style="width:100%">
    <div class="hero-content">
      <div class="badge animate-up">AI-Native Enterprise Architecture</div>
      <h1 class="animate-up-2">Enterprise AI Needs<br><span class="accent">Architecture.</span><br><span class="accent-teal">Not Just Models</span></h1>
      <p class="hero-sub animate-up-3">EPICUltra provides the risk-grade foundation required to deploy AI safely across complex enterprise workflows.</p>
      <p class="hero-support animate-up-3">Deploy AI with confidence across trading, risk, and finance workflows without compromising control, compliance, or operational integrity.</p>
      <div class="hero-btns animate-up-4">
        <a href="#contact" class="btn-primary">Request Executive Briefing</a>
        <a href="architecture.html" class="btn-secondary">Explore the Architecture →</a>
      </div>
      <div class="hero-stats animate-up-4">
        <div class="stat"><div class="stat-val">7<span>+</span></div><div class="stat-label">Production Agents</div></div>
        <div class="stat"><div class="stat-val">100<span>%</span></div><div class="stat-label">Decision Traceability</div></div>
        <div class="stat"><div class="stat-val">&lt;15<span>ms</span></div><div class="stat-label">Execution Latency</div></div>
      </div>
    </div>
  </div>
</section>

<section style="padding:5rem 0">
  <div class="wrap">
    <div class="badge">The Challenge</div>
    <div class="section-header">
      <h2>AI in <span class="accent">High-Risk</span> Environments</h2>
      <p>Energy trading organizations operate in a world of accelerating volatility, fragmented systems, and exponential data growth. AI promises automation — but deployed without architecture, it amplifies weaknesses.</p>
    </div>
    <div class="grid-3">
      <div class="card">
        <div class="card-icon">⚖️</div>
        <h3>No Governance Layer</h3>
        <p>Off-the-shelf AI lacks mandate controls, role-based limits, and financial guardrails — creating unacceptable risk at every decision point.</p>
      </div>
      <div class="card">
        <div class="card-icon">👁️</div>
        <h3>Black-Box Decisions</h3>
        <p>When AI journals an entry or flags a position, you need a full audit trail. Opaque models cannot survive regulatory scrutiny.</p>
      </div>
      <div class="card">
        <div class="card-icon">🌀</div>
        <h3>Hallucination at Scale</h3>
        <p>Unstructured retrieval causes confabulation. In margin calculations and risk reports, one wrong number creates systemic exposure.</p>
      </div>
      <div class="card">
        <div class="card-icon">🧩</div>
        <h3>Fragmented Systems</h3>
        <p>Fragmented ETRM, ERP, and settlement systems create inconsistent data across operational platforms with no single source of truth.</p>
      </div>
      <div class="card">
        <div class="card-icon">💥</div>
        <h3>Amplified Errors</h3>
        <p>Market volatility increases exposure sensitivity. Operational automation deployed without controls amplifies errors at scale.</p>
      </div>
      <div class="card" style="background:linear-gradient(135deg,var(--surface2),var(--surface));border-color:var(--border2)">
        <div class="card-icon">🎯</div>
        <h3>The Solution</h3>
        <p>Modern enterprises need more than AI tools. They need <strong style="color:var(--teal)">AI architecture built for controlled execution.</strong></p>
      </div>
    </div>
  </div>
</section>

<div class="stat-strip">
  <div class="wrap">
    <div class="stat-strip-inner">
      <div class="strip-stat"><div class="strip-val">9+</div><div class="strip-label">Production Agents</div></div>
      <div class="strip-stat"><div class="strip-val">100%</div><div class="strip-label">Decision Traceability</div></div>
      <div class="strip-stat"><div class="strip-val">&lt;15ms</div><div class="strip-label">Execution Latency</div></div>
      <div class="strip-stat"><div class="strip-val">7yr</div><div class="strip-label">Audit Log Retention</div></div>
    </div>
  </div>
</div>

<section style="padding:5rem 0;background:var(--bg2)">
  <div class="wrap">
    <div class="badge">Architecture</div>
    <div class="section-header">
      <h2>Four Layers. <span class="accent">Zero Compromise.</span></h2>
      <p>A purpose-built stack where governance, traceability, and mandate enforcement are structural — not add-ons.</p>
    </div>
    <div class="lt-wrap">
      <div class="lt-line"></div>
      <div class="lt-item">
        <div class="lt-num lt-n1">01</div>
        <div>
          <div class="lt-icon">⚙️</div>
          <div class="lt-title">Risk-Grade Data Engineering</div>
          <div class="lt-desc">Clean, curated data pipelines integrate ETRM, ERP, and market data sources into reconciled datasets with full lineage traceability. AI models operate on trusted enterprise data — not fragmented system extracts.</div>
          <div class="lt-tags"><span class="lt-tag">Reconciled</span><span class="lt-tag">Audit-ready</span><span class="lt-tag">Single source of truth</span><span class="lt-tag">Medallion architecture</span></div>
        </div>
      </div>
      <div class="lt-item">
        <div class="lt-num lt-n2">02</div>
        <div>
          <div class="lt-icon">🎯</div>
          <div class="lt-title">Context-Governed Intelligence</div>
          <div class="lt-desc">Structured retrieval anchors AI outputs in validated enterprise context. Dramatically reduces hallucinations and ensures decisions remain grounded in authoritative data sources only.</div>
          <div class="lt-tags"><span class="lt-tag">Structured retrieval</span><span class="lt-tag">Hallucination reduction</span><span class="lt-tag">Explainable outputs</span></div>
        </div>
      </div>
      <div class="lt-item">
        <div class="lt-num lt-n3">03</div>
        <div>
          <div class="lt-icon">📜</div>
          <div class="lt-title">Total Decision Traceability</div>
          <div class="lt-desc">Every AI recommendation and action is recorded with complete transparency — reasoning pathways, source data context, model versions, and policy constraints. A fully auditable record for risk committees and regulators.</div>
          <div class="lt-tags"><span class="lt-tag">Model logging</span><span class="lt-tag">Policy enforcement logs</span><span class="lt-tag">Regulator access</span><span class="lt-tag">Full replay</span></div>
        </div>
      </div>
      <div class="lt-item">
        <div class="lt-num lt-n4">04</div>
        <div>
          <div class="lt-icon">🔒</div>
          <div class="lt-title">Mandate-Defined Agent Execution</div>
          <div class="lt-desc">Agents operate within clearly defined authority boundaries. Each agent is limited to specific roles, decision scopes, and execution environments — preventing uncontrolled automation at every level.</div>
          <div class="lt-tags"><span class="lt-tag">Role-based limits</span><span class="lt-tag">Financial guardrails</span><span class="lt-tag">Isolated environments</span></div>
        </div>
      </div>
      <div class="lt-item">
        <div class="lt-num lt-n5">05</div>
        <div>
          <div class="lt-icon">🏗️</div>
          <div class="lt-title">Isolated &amp; Resilient Architecture</div>
          <div class="lt-desc">AI agents run within independently versioned container environments with rollback capabilities and kill-switch controls. Ensures operational containment and resilience across every deployment.</div>
          <div class="lt-tags"><span class="lt-tag">Versioned containers</span><span class="lt-tag">Kill-switch controls</span><span class="lt-tag">Rollback</span><span class="lt-tag">Zero cross-contamination</span></div>
        </div>
      </div>
    </div>
    <div style="text-align:center;margin-top:3rem">
      <a href="architecture.html" class="btn-primary">View Full Architecture →</a>
    </div>
  </div>
</section>

<section style="padding:5rem 0">
  <div class="wrap">
    <div class="badge">Design Principles</div>
    <div class="section-header">
      <h2>Risk-Grade AI, <span class="accent">By Design</span></h2>
    </div>
    <div>
      <div class="principle">
        <div class="principle-num">01</div>
        <div>
          <div class="principle-icon">🛡️</div>
          <div class="principle-title">Governance First</div>
          <div class="principle-text">Every agent operates within defined mandates. No action executes outside its authorized boundary — ever. Governance is not a feature layer added after the fact; it is the foundation everything else is built on top of.</div>
        </div>
      </div>
      <div class="principle">
        <div class="principle-num">02</div>
        <div>
          <div class="principle-icon">🔍</div>
          <div class="principle-title">Full Explainability</div>
          <div class="principle-text">Every output includes a complete reasoning chain, data context, and model lineage — audit-ready at any moment. When regulators ask why a decision was made, you have a complete, immutable answer.</div>
        </div>
      </div>
      <div class="principle">
        <div class="principle-num">03</div>
        <div>
          <div class="principle-icon">⚡</div>
          <div class="principle-title">Execution, Not Experimentation</div>
          <div class="principle-text">EPICUltra is not a pilot program. It's production architecture engineered for enterprise accountability from day one — built to operate in environments where the stakes are real and the margin for error is not.</div>
        </div>
      </div>
      <div class="principle">
        <div class="principle-num">04</div>
        <div>
          <div class="principle-icon">🔒</div>
          <div class="principle-title">True Isolation</div>
          <div class="principle-text">Deployment isolation ensures zero cross-contamination between agents, clients, or operational contexts. Every EPICUltra deployment is its own isolated environment with dedicated compute and no shared memory.</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section style="padding:5rem 0;background:var(--bg2)">
  <div class="wrap">
    <div class="badge">Agent Framework</div>
    <div class="section-header">
      <h2>Nine Agents. <span class="accent">One Mandate Engine.</span></h2>
    </div>
    <div class="grid-3">
      <div class="card"><div class="card-icon">📊</div><h3>Margin Analyst</h3><p class="text2" style="font-size:.78rem;font-family:var(--mono);margin-bottom:.5rem">MONITOR · DECIDE · ENFORCE</p><p>Real-time margin analysis with threshold alerts and mandate-controlled escalation.</p></div>
      <div class="card"><div class="card-icon">📡</div><h3>Exposure Monitor</h3><p class="text2" style="font-size:.78rem;font-family:var(--mono);margin-bottom:.5rem">AGGREGATE · ALERT</p><p>Continuous cross-platform exposure aggregation and real-time risk visibility.</p></div>
      <div class="card"><div class="card-icon">📝</div><h3>Journal Entry</h3><p class="text2" style="font-size:.78rem;font-family:var(--mono);margin-bottom:.5rem">EXTRACT · POST</p><p>Intelligent journal automation from bank statements. 80% straight-through rate.</p></div>
      <div class="card"><div class="card-icon">⚖️</div><h3>Reconciliation</h3><p class="text2" style="font-size:.78rem;font-family:var(--mono);margin-bottom:.5rem">VERIFY · RESOLVE</p><p>Automated balance reconciliation with 90%+ straight-through matching rate.</p></div>
      <div class="card"><div class="card-icon">⚡</div><h3>Close Accelerator</h3><p class="text2" style="font-size:.78rem;font-family:var(--mono);margin-bottom:.5rem">ORCHESTRATE · CLOSE</p><p>Month-end close reduced from 10 days to under 3.</p></div>
      <div class="card"><div class="card-icon">📋</div><h3>Regulatory Reporting</h3><p class="text2" style="font-size:.78rem;font-family:var(--mono);margin-bottom:.5rem">COMPILE · SUBMIT</p><p>Automated regulatory submission with full auditability.</p></div>
      <div class="card"><div class="card-icon">💧</div><h3>Liquidity Watch</h3><p class="text2" style="font-size:.78rem;font-family:var(--mono);margin-bottom:.5rem">MONITOR · FORECAST</p><p>Real-time liquidity monitoring with scenario-based stress forecasting.</p></div>
      <div class="card"><div class="card-icon">🧾</div><h3>Billing Validation</h3><p class="text2" style="font-size:.78rem;font-family:var(--mono);margin-bottom:.5rem">VALIDATE · AUDIT</p><p>AI-driven validation of complex billing calculations with full audit traceability.</p></div>
      <div class="card"><div class="card-icon">🤖</div><h3>JAQ – Junior Accountant</h3><p class="text2" style="font-size:.78rem;font-family:var(--mono);margin-bottom:.5rem">DETECT · EXPLAIN</p><p>AI-assisted detection of P&L anomalies with natural-language explanations.</p></div>
    </div>
    <div style="text-align:center;margin-top:2.5rem">
      <a href="agents.html" class="btn-primary">View All Agents →</a>
    </div>
  </div>
</section>

<section style="padding:5rem 0">
  <div class="wrap">
    <div class="badge">Industries Served</div>
    <div class="section-header">
      <h2>Built for <span class="accent">High-Stakes</span> Financial Operations</h2>
    </div>
    <div class="grid-3">
      <div class="industry-card ic-v">
        <div class="ic-num">01</div>
        <div class="ic-label">⚡ Energy Trading</div>
        <div class="ic-desc">Real-time exposure management and margin automation for commodity and derivatives trading desks.</div>
        <ul class="ic-list iv">
          <li>Intraday exposure monitoring</li>
          <li>Margin automation</li>
          <li>Limit breach detection</li>
          <li>Scenario simulation</li>
        </ul>
      </div>
      <div class="industry-card ic-t">
        <div class="ic-num">02</div>
        <div class="ic-label">🏦 Financial Operations</div>
        <div class="ic-desc">Continuous close, journal automation, and reconciliation intelligence for enterprise finance teams.</div>
        <ul class="ic-list it">
          <li>Journal automation</li>
          <li>Close acceleration</li>
          <li>Reconciliation intelligence</li>
          <li>Variance detection</li>
        </ul>
      </div>
      <div class="industry-card ic-v">
        <div class="ic-num">03</div>
        <div class="ic-label">🛡️ Enterprise Risk</div>
        <div class="ic-desc">Cross-platform exposure aggregation and live risk monitoring for CROs and risk management teams.</div>
        <ul class="ic-list iv">
          <li>Anomaly detection</li>
          <li>Counterparty exposure analysis</li>
          <li>Liquidity monitoring</li>
          <li>Policy enforcement</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section style="padding:5rem 0;background:var(--bg2)">
  <div class="wrap">
    <div class="badge">Why HOC + MidDel</div>
    <div class="section-header">
      <h2>The Expertise <span class="accent">Behind</span> EPICUltra</h2>
    </div>
    <div class="grid-3">
      <div class="card">
        <div class="card-icon">🏛️</div>
        <h3>Deep Domain Expertise</h3>
        <p>Decades of front-to-back energy trading lifecycle experience embedded into every workflow and agent mandate.</p>
      </div>
      <div class="card">
        <div class="card-icon">⚙️</div>
        <h3>Enterprise Engineering Discipline</h3>
        <p>Proven delivery of scalable data platforms in regulated environments, built for production from day one.</p>
      </div>
      <div class="card">
        <div class="card-icon">🤖</div>
        <h3>Structured AI Deployment</h3>
        <p>AI mapped to defined risk classes, controlled execution boundaries, and monitored model lifecycles.</p>
      </div>
    </div>
  </div>
</section>
"""

# ══════════════════════════════════════════════════════════════════════════════
# ARCHITECTURE PAGE
# ══════════════════════════════════════════════════════════════════════════════
arch_body = """
<section class="hero" style="min-height:50vh">
  <div class="hero-bg"></div>
  <div class="hero-grid"></div>
  <div class="wrap" style="width:100%">
    <div class="hero-content">
      <div class="badge animate-up">Technical Architecture</div>
      <h1 class="animate-up-2">Four Layers.<br><span class="accent">Zero Compromise.</span></h1>
      <p class="hero-sub animate-up-3">Purpose-built, not assembled. Governance, traceability, and mandate enforcement are structural — not bolted on.</p>
      <div class="hero-stats animate-up-4" style="margin-top:2.5rem">
        <div class="stat"><div class="stat-val">4</div><div class="stat-label">Interlocking Layers</div></div>
        <div class="stat"><div class="stat-val">100<span>%</span></div><div class="stat-label">Decision Traceability</div></div>
        <div class="stat"><div class="stat-val">SOC</div><div class="stat-label">Ready Posture</div></div>
        <div class="stat"><div class="stat-val">&lt;15<span>ms</span></div><div class="stat-label">Execution Latency</div></div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="layer-block" style="grid-template-columns:1fr">
      <div>
        <div class="layer-num">Layer 01 — Foundation</div>
        <div class="layer-title">Risk-Grade Data <span class="accent">Engineering</span></div>
        <div class="layer-desc" style="max-width:700px">The foundation of trustworthy AI is trustworthy data. EPICUltra establishes a reconciled, audit-ready data layer before any intelligence layer touches it. AI models operate on trusted enterprise data — not fragmented system extracts.</div>
      </div>
      <div class="flow-h">
        <div class="flow-h-step"><div class="flow-h-num">01</div><strong>Raw Ingestion</strong><span>Bank feeds · Trading systems · ERP</span></div>
        <div class="flow-h-step"><div class="flow-h-num">02</div><strong>Reconciliation Engine</strong><span>Balance checks · Discrepancy flags · Lineage</span></div>
        <div class="flow-h-step"><div class="flow-h-num">03</div><strong>Canonical Store</strong><span>Single version of truth · Versioned snapshots</span></div>
        <div class="flow-h-step"><div class="flow-h-num">04</div><strong>Verified Data</strong><span>Audit-ready · Agent-accessible · Policy-tagged</span></div>
      </div>
      <div class="grid-4" style="gap:.75rem">
        <div class="feat-item"><strong>⚖️ Reconciled Data Layer</strong><span>Positions, balances, and transactions verified before any processing occurs.</span></div>
        <div class="feat-item"><strong>◎ Single Version of Truth</strong><span>Canonical stores eliminate version conflicts across all operational functions.</span></div>
        <div class="feat-item"><strong>📋 Audit-Ready Ingestion</strong><span>Every data point timestamped, sourced, and versioned at ingestion.</span></div>
        <div class="feat-item"><strong>⟳ Medallion Architecture</strong><span>Bronze → Silver → Gold with enforced quality gates at each stage.</span></div>
      </div>
    </div>

    <div class="layer-block" style="grid-template-columns:1fr">
      <div>
        <div class="layer-num">Layer 02 — Intelligence</div>
        <div class="layer-title">Context-Governed <span class="accent">Intelligence</span></div>
        <div class="layer-desc" style="max-width:700px">Structured retrieval replaces unconstrained generation. Every response grounded in verified, policy-tagged context — making hallucination structurally impossible in critical paths.</div>
      </div>
      <div class="metrics">
        <div class="metric"><div class="metric-val">99.2%</div><div class="metric-label">Retrieval Precision</div></div>
        <div class="metric"><div class="metric-val">100%</div><div class="metric-label">Context Grounding</div></div>
        <div class="metric"><div class="metric-val">0</div><div class="metric-label">Hallucination Incidents (30d)</div></div>
        <div class="metric"><div class="metric-val">12ms</div><div class="metric-label">Avg Response Latency</div></div>
        <div class="metric"><div class="metric-val">FULL</div><div class="metric-label">Explainability Score</div></div>
        <div class="metric"><div class="metric-val">14</div><div class="metric-label">Policy Overrides Blocked Today</div></div>
      </div>
      <div class="grid-3" style="gap:.75rem;margin-top:1.5rem">
        <div class="feat-item"><strong>🎯 Structured Retrieval</strong><span>Context injected via verified, policy-scoped retrieval pipelines only.</span></div>
        <div class="feat-item"><strong>🛡️ Hallucination Reduction</strong><span>Guardrails at the context layer anchor every output to reconciled enterprise data.</span></div>
        <div class="feat-item"><strong>💬 Explainable Outputs</strong><span>Data source, reasoning chain, and confidence level included in every output.</span></div>
      </div>
    </div>

    <div class="layer-block" style="grid-template-columns:1fr">
      <div>
        <div class="layer-num">Layer 03 — Accountability</div>
        <div class="layer-title">Total Decision <span class="accent-teal">Traceability</span></div>
        <div class="layer-desc" style="max-width:700px">When regulators ask why a decision was made, you have a complete answer. Every AI action logged with model version, data context, and policy state at the moment of execution.</div>
      </div>
      <div class="flow-h">
        <div class="flow-h-step"><div class="flow-h-num">01</div><strong>Agent Decision Event</strong><span>Action triggered by market or schedule</span></div>
        <div class="flow-h-step"><div class="flow-h-num">02</div><strong>Trace Logger</strong><span>Model version · Data state · Policy check</span></div>
        <div class="flow-h-step"><div class="flow-h-num">03</div><strong>Immutable Audit Store</strong><span>Tamper-evident · Encrypted · Regulator access</span></div>
        <div class="flow-h-step"><div class="flow-h-num">04</div><strong>Audit Dashboard</strong><span>CRO / CIO / Regulator · Full replay</span></div>
      </div>
      <div class="grid-3" style="gap:.75rem">
        <div class="feat-item"><strong>📁 Model Logging</strong><span>Version, parameters, and decision weights — immutable, tamper-evident records preserved at every action.</span></div>
        <div class="feat-item"><strong>🗃️ Data Context Capture</strong><span>Exact data snapshot for each decision preserved alongside the output.</span></div>
        <div class="feat-item"><strong>📜 Policy Enforcement Logs</strong><span>Every mandate check and guardrail trigger recorded with actor and outcome.</span></div>
      </div>
    </div>

    <div class="layer-block" style="grid-template-columns:1fr">
      <div>
        <div class="layer-num">Layer 04 — Execution</div>
        <div class="layer-title">Mandate-Defined <span class="accent">Agent Execution</span></div>
        <div class="layer-desc" style="max-width:700px">Each agent operates within a precise mandate: defined roles, authorized actions, financial limits, and isolated environments. No agent exceeds its mandate — by architecture, not just policy.</div>
      </div>
      <div class="grid-3" style="gap:.75rem">
        <div class="feat-item"><strong>👤 Role-Based Limits</strong><span>Specific role with defined action scope. Cross-role actions blocked at runtime — no exceptions.</span></div>
        <div class="feat-item"><strong>💰 Financial Guardrails</strong><span>Hard limits on position sizes, journal values, and exposure thresholds enforced at every execution.</span></div>
        <div class="feat-item"><strong>🔒 Isolated Environments</strong><span>No shared memory, no cross-contamination, no lateral movement between agents or clients.</span></div>
      </div>
      <div class="flow-h" style="margin-top:1.5rem">
        <div class="flow-h-step"><div style="font-size:1.4rem;margin-bottom:.4rem">🛡️</div><strong>SOC-Ready</strong><span>SOC 2 Type II alignment from day one</span></div>
        <div class="flow-h-step"><div style="font-size:1.4rem;margin-bottom:.4rem">🔐</div><strong>AES-256</strong><span>End-to-end encryption at rest and in transit</span></div>
        <div class="flow-h-step"><div style="font-size:1.4rem;margin-bottom:.4rem">📋</div><strong>RBAC</strong><span>Role-based access control at every layer</span></div>
        <div class="flow-h-step"><div style="font-size:1.4rem;margin-bottom:.4rem">📊</div><strong>Audit Log</strong><span>7-year immutable retention</span></div>
      </div>
    </div>
  </div>
</section>
"""

# ══════════════════════════════════════════════════════════════════════════════
# AGENTS PAGE
# ══════════════════════════════════════════════════════════════════════════════
agents_data = [
    ("📊","01","Margin Analyst","MONITOR · ANALYZE · ALERT",
     "Real-time margin analysis with threshold alerts and mandate-controlled escalation."),
    ("📡","02","Exposure Monitor","AGGREGATE · REPORT · ALERT",
     "Continuous cross-platform exposure aggregation and real-time risk visibility."),
    ("📝","03","Journal Entry","EXTRACT · CLASSIFY · POST",
     "Intelligent GL automation from bank data. 80% straight-through processing rate."),
    ("⚖️","04","Reconciliation","VERIFY · MATCH · RESOLVE",
     "Automated ledger matching with 90%+ straight-through reconciliation rate."),
    ("⚡","05","Close Accelerator","ORCHESTRATE · VALIDATE · CLOSE",
     "Month-end close reduced from 10 days to under 3."),
    ("📋","06","Regulatory Reporting","COMPILE · VALIDATE · SUBMIT",
     "Automated regulatory submissions across CFTC, SEC, and FCA — fully auditable."),
    ("💧","07","Liquidity Watch","FORECAST · MONITOR · ALERT",
     "Real-time liquidity monitoring with scenario-based stress forecasting."),
    ("🧾","08","Billing Validation","VALIDATE · FLAG · AUDIT",
     "AI-driven billing calculation validation with full audit traceability."),
    ("🤖","09","JAQ – Junior Accountant","DETECT · ANALYZE · EXPLAIN",
     "AI detection of P&L anomalies with natural-language explanations for finance teams."),
]

agents_cards = ""
for icon, num, name, role, desc in agents_data:
    role_tags = "".join(f'<span class="agc-role">{r.strip()}</span>' for r in role.split("·"))
    agents_cards += f"""
    <div class="agc">
      <div class="agc-num">{num}</div>
      <div class="agc-icon">{icon}</div>
      <div class="agc-name">{name}</div>
      <div class="agc-roles">{role_tags}</div>
      <div class="agc-desc">{desc}</div>
    </div>"""

agents_body = f"""
<section class="hero" style="min-height:45vh">
  <div class="hero-bg"></div>
  <div class="hero-grid"></div>
  <div class="wrap" style="width:100%">
    <div class="hero-content">
      <div class="badge animate-up">Production-Ready</div>
      <h1 class="animate-up-2">Nine Agents.<br><span class="accent">One Mandate Engine.</span></h1>
      <p class="hero-sub animate-up-3">Each agent operates within a defined mandate — explicit controls on what it monitors, decides, and can execute.</p>
      <div class="hero-stats animate-up-4" style="margin-top:2.5rem">
        <div class="stat"><div class="stat-val">9<span>+</span></div><div class="stat-label">Production Agents</div></div>
        <div class="stat"><div class="stat-val">100<span>%</span></div><div class="stat-label">Mandate-Controlled</div></div>
        <div class="stat"><div class="stat-val">24/7</div><div class="stat-label">Active Monitoring</div></div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="mandate-bar">
      <div class="mb-item">
        <div class="mb-icon">🎯</div>
        <div class="mb-title">Defined Roles</div>
        <div class="mb-desc">Scoped action boundaries per agent</div>
      </div>
      <div class="mb-item">
        <div class="mb-icon">💰</div>
        <div class="mb-title">Financial Guardrails</div>
        <div class="mb-desc">Hard limits on values &amp; thresholds</div>
      </div>
      <div class="mb-item">
        <div class="mb-icon">🔒</div>
        <div class="mb-title">Isolated Environments</div>
        <div class="mb-desc">No shared memory, no lateral movement</div>
      </div>
      <div class="mb-item">
        <div class="mb-icon">📜</div>
        <div class="mb-title">Full Audit Trail</div>
        <div class="mb-desc">Every decision logged &amp; replayable</div>
      </div>
    </div>
    <div class="grid-3">{agents_cards}</div>
    <div style="text-align:center;margin-top:3rem">
      <a href="#contact" class="btn-primary">Schedule AI Use Case Mapping Session</a>
    </div>
  </div>
</section>
"""

# ══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE PAGE
# ══════════════════════════════════════════════════════════════════════════════
gov_body = """
<section class="hero" style="min-height:45vh">
  <div class="hero-bg"></div>
  <div class="hero-grid"></div>
  <div class="wrap" style="width:100%">
    <div class="hero-content">
      <div class="badge animate-up">For CROs &amp; CIOs</div>
      <h1 class="animate-up-2">Governance Built Into<br>the <span class="accent">Foundation</span></h1>
      <p class="hero-sub animate-up-3">EPICUltra treats governance as infrastructure, not afterthought. Every layer is designed to satisfy compliance officers, regulators, and enterprise security teams.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-stats">
      <div class="sec-stat"><div class="sec-stat-val">100%</div><div class="sec-stat-label">Audit Coverage</div><div class="sec-stat-desc">Every agent action logged</div></div>
      <div class="sec-stat"><div class="sec-stat-val">SOC 2</div><div class="sec-stat-label">Compliance Posture</div><div class="sec-stat-desc">Type II in progress</div></div>
      <div class="sec-stat"><div class="sec-stat-val">0</div><div class="sec-stat-label">Unauthorized Overrides</div><div class="sec-stat-desc">Architecture-enforced</div></div>
      <div class="sec-stat"><div class="sec-stat-val">E2E</div><div class="sec-stat-label">Encrypted</div><div class="sec-stat-desc">AES-256 at rest &amp; transit</div></div>
    </div>

    <div class="badge">Governance Pillars</div>
    <div class="section-header"><h2>Six Pillars of <span class="accent">Enterprise Governance</span></h2></div>
    <div class="grid-3">
      <div class="pillar"><div class="pillar-icon">🏛️</div><h3>Model Governance Framework</h3><p>Structured lifecycle management for every AI model. Versioning, approval workflows, rollback, drift monitoring, lineage documentation.</p></div>
      <div class="pillar"><div class="pillar-icon">🔑</div><h3>Access Controls</h3><p>RBAC with least-privilege enforcement. MFA, session logging, PAM integration, scoped third-party tokens.</p></div>
      <div class="pillar"><div class="pillar-icon">📜</div><h3>Audit Logging</h3><p>Tamper-evident append-only logs. 7-year retention, real-time SIEM streaming, regulator-accessible query interface, full decision replay.</p></div>
      <div class="pillar"><div class="pillar-icon">🏗️</div><h3>Deployment Isolation</h3><p>Dedicated VPC per client. Agent sandboxing, no cross-client data pathways, IaC with policy-gated deployments, penetration testing.</p></div>
      <div class="pillar"><div class="pillar-icon">🔒</div><h3>Data Privacy Posture</h3><p>AES-256 encryption. Data residency controls, PII masking, GDPR + CCPA compliance, data minimization by design.</p></div>
      <div class="pillar"><div class="pillar-icon">🛡️</div><h3>SOC / ISO Readiness</h3><p>SOC 2 Type II in progress. ISO 27001 mapping, annual third-party security assessments, board-level security reporting.</p></div>
    </div>

    <div style="margin-top:4rem">
      <div class="badge">Compliance Frameworks</div>
      <div class="section-header"><h2>Regulatory <span class="accent-teal">Coverage</span></h2></div>
      <div class="compliance-grid">
        <div class="compliance-item"><span class="compliance-name">SOC 2 Type II</span></div>
        <div class="compliance-item"><span class="compliance-name">ISO 27001</span></div>
        <div class="compliance-item"><span class="compliance-name">CFTC Compliance</span></div>
        <div class="compliance-item"><span class="compliance-name">GDPR</span></div>
        <div class="compliance-item"><span class="compliance-name">Basel III / IV</span></div>
        <div class="compliance-item"><span class="compliance-name">Internal Audit</span></div>
      </div>
      <div style="text-align:center;margin-top:2.5rem">
        <a href="#contact" class="btn-primary">Request Security &amp; Governance Overview</a>
      </div>
    </div>
  </div>
</section>
"""

# ══════════════════════════════════════════════════════════════════════════════
# USE CASES PAGE
# ══════════════════════════════════════════════════════════════════════════════
uc_body = """
<section class="hero" style="min-height:45vh">
  <div class="hero-bg"></div>
  <div class="hero-grid"></div>
  <div class="wrap" style="width:100%">
    <div class="hero-content">
      <div class="badge animate-up">Operational Use Cases</div>
      <h1 class="animate-up-2">Where EPICUltra<br><span class="accent">Delivers Results</span></h1>
      <p class="hero-sub animate-up-3">Organized by function. Each use case reflects a real operational problem EPICUltra solves — production-tested, not theoretical.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="uc-tabs">
      <button class="uc-tab active" data-panel="uc-energy">⚡ Energy Trading</button>
      <button class="uc-tab" data-panel="uc-risk">🛡️ Risk Management</button>
      <button class="uc-tab" data-panel="uc-finance">🏦 Financial Operations</button>
      <button class="uc-tab" data-panel="uc-compliance">📋 Compliance &amp; Reporting</button>
    </div>

    <div class="uc-panel active" id="uc-energy">
      <div class="uc-agents">
        <span style="font-family:var(--mono);font-size:.7rem;color:var(--text3);letter-spacing:.06em;text-transform:uppercase;margin-right:.25rem">Key Agents:</span>
        <span class="uc-agent-tag">Margin Analyst</span><span class="uc-agent-tag">Exposure Monitor</span><span class="uc-agent-tag">Liquidity Watch</span>
      </div>
      <div class="uc-item"><h4>Margin Automation</h4><p>Monitors real-time margin requirements, calculates calls automatically, routes collateral within mandate thresholds.</p><div class="uc-result">→ Reduced margin call processing time by 70%+</div></div>
      <div class="uc-item"><h4>Exposure Monitoring</h4><p>Continuous cross-platform aggregation of gross and net exposures. Alerts fire before concentration limits breach.</p><div class="uc-result">→ Real-time exposure visibility across all trading books</div></div>
      <div class="uc-item"><h4>Trade Reconciliation</h4><p>Automated matching of trade records across systems. Breaks classified and resolved within mandate.</p><div class="uc-result">→ 90%+ straight-through matching on standard trades</div></div>
      <div class="uc-item"><h4>Risk Visibility</h4><p>Board-level and desk-level risk dashboards from reconciled data, not end-of-day snapshots. Scenario simulations run against live positions.</p><div class="uc-result">→ Intraday risk reporting replacing T+1 manual processes</div></div>
    </div>

    <div class="uc-panel" id="uc-risk">
      <div class="uc-agents">
        <span style="font-family:var(--mono);font-size:.7rem;color:var(--text3);letter-spacing:.06em;text-transform:uppercase;margin-right:.25rem">Key Agents:</span>
        <span class="uc-agent-tag">Exposure Monitor</span><span class="uc-agent-tag">Liquidity Watch</span><span class="uc-agent-tag">Margin Analyst</span>
      </div>
      <div class="uc-item"><h4>Exposure Aggregation</h4><p>Aggregated exposure across all platforms, asset classes, and legal entities. Updated continuously from reconciled data.</p><div class="uc-result">→ Single source of truth, updated every 15 minutes</div></div>
      <div class="uc-item"><h4>Limit Monitoring</h4><p>Continuous monitoring of counterparty, sector, and regulatory limits. Alerts fire before breaches occur.</p><div class="uc-result">→ Real-time limit visibility replacing end-of-day manual checks</div></div>
      <div class="uc-item"><h4>Anomaly Detection</h4><p>AI-driven detection of P&L anomalies, regime shifts, and unusual exposure patterns. Natural-language explanations generated automatically.</p><div class="uc-result">→ Intraday anomaly detection replacing T+1 manual review</div></div>
      <div class="uc-item"><h4>Scenario Simulation</h4><p>Board-defined stress scenarios run automatically against live positions. Shows concentration vulnerability before markets move.</p><div class="uc-result">→ Continuous stress testing replacing quarterly manual exercises</div></div>
    </div>

    <div class="uc-panel" id="uc-finance">
      <div class="uc-agents">
        <span style="font-family:var(--mono);font-size:.7rem;color:var(--text3);letter-spacing:.06em;text-transform:uppercase;margin-right:.25rem">Key Agents:</span>
        <span class="uc-agent-tag">Journal Entry</span><span class="uc-agent-tag">Reconciliation</span><span class="uc-agent-tag">Close Accelerator</span><span class="uc-agent-tag">JAQ</span><span class="uc-agent-tag">Billing Validation</span>
      </div>
      <div class="uc-item"><h4>Continuous Close</h4><p>Accruals post automatically, inter-company eliminations run daily, close certification triggers when data is ready — not when the calendar says so.</p><div class="uc-result">→ Month-end close cycle reduced from 10 days to under 3</div></div>
      <div class="uc-item"><h4>Journal Automation</h4><p>Bank data extracted, classified, mapped to GL, and posted automatically. Exceptions routed for human review with context pre-populated.</p><div class="uc-result">→ 80% reduction in manual journal processing time</div></div>
      <div class="uc-item"><h4>Reconciliation Intelligence</h4><p>Matches internal ledgers against custodian statements, classifies breaks, auto-resolves known patterns.</p><div class="uc-result">→ 90%+ straight-through reconciliation rate on standard items</div></div>
      <div class="uc-item"><h4>Billing Validation</h4><p>Complex billing calculations validated automatically with full audit traceability. Anomalies flagged and routed for review.</p><div class="uc-result">→ Reduced billing errors and faster dispute resolution</div></div>
    </div>

    <div class="uc-panel" id="uc-compliance">
      <div class="uc-agents">
        <span style="font-family:var(--mono);font-size:.7rem;color:var(--text3);letter-spacing:.06em;text-transform:uppercase;margin-right:.25rem">Key Agents:</span>
        <span class="uc-agent-tag">Regulatory Reporting</span><span class="uc-agent-tag">Reconciliation</span><span class="uc-agent-tag">Journal Entry</span>
      </div>
      <div class="uc-item"><h4>Regulatory Reporting</h4><p>Automated submission with full auditability across CFTC, SEC, and FCA requirements.</p><div class="uc-result">→ On-time regulatory submissions with complete audit trail</div></div>
      <div class="uc-item"><h4>Audit Documentation</h4><p>Every AI action logged with model version, data context, and policy state. Regulator-accessible query interface with full decision replay.</p><div class="uc-result">→ Audit-ready documentation at any moment</div></div>
      <div class="uc-item"><h4>Policy Mapping</h4><p>AI-driven mapping of operational workflows to compliance policy requirements. Gaps flagged automatically.</p><div class="uc-result">→ Continuous compliance monitoring replacing periodic manual audits</div></div>
    </div>

    <div style="text-align:center;margin-top:3rem">
      <a href="#contact" class="btn-primary">See Live Use Case Walkthrough</a>
    </div>
  </div>
</section>
"""

# ══════════════════════════════════════════════════════════════════════════════
# ABOUT PAGE
# ══════════════════════════════════════════════════════════════════════════════
about_body = """
<section class="hero" style="min-height:45vh">
  <div class="hero-bg"></div>
  <div class="hero-grid"></div>
  <div class="wrap" style="width:100%">
    <div class="hero-content">
      <div class="badge animate-up">Philosophy</div>
      <h1 class="animate-up-2">Not Corporate Fluff.<br><span class="accent">A Point of View.</span></h1>
      <p class="hero-sub animate-up-3">EPICUltra exists because most enterprise AI is built for demos, not for financial operations where the cost of being wrong is measured in positions, not user experience.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="manifesto">
      <p>"Enterprise AI engineered for accountability — not experimentation, not aspiration. Accountability."</p>
    </div>

    <div class="badge" style="margin-top:3rem">Three Tenets</div>
    <div style="margin-top:2rem">
      <div class="tenet">
        <div><div class="tenet-num">Tenet 01</div></div>
        <div><div class="tenet-title">AI must be <span class="accent">architecture-first</span></div><p>The AI tools flooding enterprise markets are retrofitted — intelligence layered on top of systems that weren't designed for it. The result is governance as an afterthought. EPICUltra was designed the other way. Every architectural decision starts with: how do we prove what this AI did, and why?</p></div>
      </div>
      <div class="tenet">
        <div><div class="tenet-num">Tenet 02</div></div>
        <div><div class="tenet-title">Governance is <span class="accent">non-negotiable</span></div><p>In financial operations, an AI system without complete traceability is a liability. When a regulator asks why a position was held or a journal entry was posted — you need an answer that withstands scrutiny. EPICUltra can provide it. Every decision is logged with model state, data context, and policy check result at the moment of execution. Not reconstructed. Captured.</p></div>
      </div>
      <div class="tenet">
        <div><div class="tenet-num">Tenet 03</div></div>
        <div><div class="tenet-title">Execution over <span class="accent-teal">experimentation</span></div><p>The enterprise AI landscape is littered with pilots that never reached production. EPICUltra is not a pilot program. It's production architecture. Built to operate in environments where the stakes are real and the margin for error is not.</p></div>
      </div>
    </div>

    <div class="about-split" style="margin-top:4rem">
      <div>
        <div class="badge">Position Statement</div>
        <ul class="position-list" style="margin-top:1.5rem">
          <li>Architecture-first design</li>
          <li>Governance as infrastructure</li>
          <li>100% decision traceability</li>
          <li>Production from day one</li>
          <li>No black-box AI in financial operations</li>
          <li>Mandate controls are non-negotiable</li>
        </ul>
      </div>
      <div>
        <div class="badge">How We're Different</div>
        <div style="margin-top:1.5rem">
          <div class="diff-item">
            <div class="diff-title">Governance as Foundation</div>
            <div class="diff-desc">Most AI platforms add governance after building the core. EPICUltra's mandate engine is designed first — everything else is built on top of it.</div>
          </div>
          <div class="diff-item">
            <div class="diff-title">No Hallucination By Design</div>
            <div class="diff-desc">Standard RAG can retrieve unverified data. EPICUltra's context layer is scoped to reconciled, policy-tagged data only.</div>
          </div>
          <div class="diff-item">
            <div class="diff-title">True Isolation</div>
            <div class="diff-desc">Multi-tenant AI platforms create cross-client risk. Every EPICUltra deployment is its own isolated environment.</div>
          </div>
        </div>
      </div>
    </div>

  </div>
</section>
"""

# ══════════════════════════════════════════════════════════════════════════════
# RESOURCES PAGE
# ══════════════════════════════════════════════════════════════════════════════
resources_body = """
<section class="hero" style="min-height:40vh">
  <div class="hero-bg"></div>
  <div class="hero-grid"></div>
  <div class="wrap" style="width:100%">
    <div class="hero-content">
      <div class="badge animate-up">Knowledge Base</div>
      <h1 class="animate-up-2">Resources for<br><span class="accent">Enterprise Decision-Makers</span></h1>
      <p class="hero-sub animate-up-3">Whitepapers, architecture overviews, webinar recordings, and case studies for CROs, CIOs, and enterprise architects.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="badge">Downloads</div>
    <div class="section-header"><h2>Research &amp; <span class="accent">Documentation</span></h2></div>
    <div style="display:flex;flex-direction:column;gap:1rem;margin-bottom:4rem">
      <div class="resource-card"><div><div class="resource-type">Whitepaper</div><div class="resource-title">AI Governance Brief for Financial Operations</div><div class="resource-desc">18 pages — A framework for evaluating AI governance in trading, risk, and finance.</div></div></div>
      <div class="resource-card"><div><div class="resource-type">Whitepaper</div><div class="resource-title">The Governance Imperative for AI in Trading</div><div class="resource-desc">A strategic framework for CROs evaluating AI deployment risk.</div></div></div>
      <div class="resource-card"><div><div class="resource-type">Technical Overview</div><div class="resource-title">EPICUltra Architecture Overview</div><div class="resource-desc">32 pages — Detailed technical documentation of the four-layer architecture.</div></div></div>
      <div class="resource-card"><div><div class="resource-type">Security Brief</div><div class="resource-title">Security &amp; Compliance Posture</div><div class="resource-desc">24 pages — SOC 2 alignment, data privacy posture, access control framework.</div></div></div>
      <div class="resource-card"><div><div class="resource-type">Case Study</div><div class="resource-title">Energy Trading: Margin Automation</div><div class="resource-desc">12 pages — How a mid-market trading desk reduced margin processing time by 70%.</div></div></div>
      <div class="resource-card"><div><div class="resource-type">Case Study</div><div class="resource-title">Finance Team: Continuous Close</div><div class="resource-desc">10 pages — From 10-day close to under 3, with 90% straight-through journal processing.</div></div></div>
      <div class="resource-card"><div><div class="resource-type">Research Paper</div><div class="resource-title">The Hallucination Problem in Financial AI</div><div class="resource-desc">14 pages — Why standard LLM retrieval fails in financial operations.</div></div></div>
    </div>

    <div class="badge">Webinars</div>
    <div class="section-header"><h2>On-Demand &amp; <span class="accent-teal">Upcoming</span></h2></div>
    <div style="display:flex;flex-direction:column;gap:1rem">
      <div class="webinar-card"><div><div class="webinar-date">March 2026</div><div class="webinar-title">Architecture-First AI: Why Your AI Platform Is a Governance Problem</div></div><span class="webinar-status ws-available">Recording Available</span></div>
      <div class="webinar-card"><div><div class="webinar-date">February 2026</div><div class="webinar-title">Eliminating Hallucination in Financial AI</div></div><span class="webinar-status ws-available">Recording Available</span></div>
      <div class="webinar-card"><div><div class="webinar-date">April 15, 2026</div><div class="webinar-title">Continuous Close: AI-Powered Month-End Transformation</div></div><span class="webinar-status ws-register">Register Now</span></div>
      <div class="webinar-card"><div><div class="webinar-date">May 2026</div><div class="webinar-title">AI Agents for Energy Trading</div></div><span class="webinar-status ws-register">Register Now</span></div>
    </div>
    <div style="text-align:center;margin-top:2.5rem">
      <a href="#contact" class="btn-primary">Request Full Resource Library</a>
    </div>
  </div>
</section>
"""

# ══════════════════════════════════════════════════════════════════════════════
# WRITE ALL PAGES
# ══════════════════════════════════════════════════════════════════════════════
pages = [
    ("index.html",      "Home",               "index.html",        home_body),
    ("architecture.html","Architecture",       "architecture.html", arch_body),
    ("agents.html",     "AI Agents",          "agents.html",       agents_body),
    ("governance.html", "Governance",         "governance.html",   gov_body),
    ("usecases.html",   "Use Cases",          "usecases.html",     uc_body),
    ("about.html",      "About",              "about.html",        about_body),
    ("resources.html",  "Resources",          "resources.html",    resources_body),
]

for filename, title, active, body in pages:
    html = page(title, active, body)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] {filename}")

print("\nSite built successfully!")
