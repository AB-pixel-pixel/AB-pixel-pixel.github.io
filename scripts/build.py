#!/usr/bin/env python3
"""Generate dependency-free bilingual pages from data/content.json."""
import json
from html import escape as e
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT / 'data/content.json').read_text())
def t(value, tag='span', cls=''):
    if isinstance(value,str): return e(value)
    return f'<{tag} class="{cls}" data-en="{e(value["en"],quote=True)}" data-zh="{e(value["zh"],quote=True)}">{e(value["en"])}</{tag}>'
def bi(en,zh,tag='span',cls=''): return t({'en':en,'zh':zh},tag,cls)
def links(items):
    result=[]
    labels={'Paper':'论文','Project':'项目主页','Code & data':'代码与数据','Demo':'演示视频'}
    for x in items:
        label=bi(x['label'],labels[x['label']])
        if 'video' in x: result.append(f'<button class="text-link" data-video="{x["video"]}" data-title="{e(x.get("title","Research demo"))}"><span aria-hidden="true">▷</span> {label}</button>')
        else: result.append(f'<a class="text-link" href="{e(x["url"])}" target="_blank" rel="noopener noreferrer">{label} <span aria-hidden="true">↗</span></a>')
    return '<div class="paper-links">'+''.join(result)+'</div>'
def authors(p):
    return ', '.join(f'<strong>{e(a)}</strong>' if a in ('Shaobin Ling','Han Lyu') else e(a) for a in p['authors'])
def papers():
    result=[]
    for p in d['papers']:
        status=t(p['status'],'span','status') if p['status'] else ''
        first=bi('First author','第一作者','span','first-author') if p['first'] else ''
        alias=t(p['alias'],'span','alias') if p.get('alias') else ''
        img=f'<a class="paper-image" href="assets/images/{p["image"]}" target="_blank" rel="noopener" aria-label="{e(p["alt"]["en"])}"><img src="assets/images/{p["image"]}" alt="{e(p["alt"]["en"])}" loading="lazy" width="520" height="320"><span>{e(p["short"])} <span aria-hidden="true">↗</span></span></a>' if p['image'] else f'<div class="paper-index" aria-hidden="true">{p["year"]}<span>{"Graph learning" if p["id"]=="tgpt" else "Visual learning"}</span></div>'
        highlight=t(p['highlight'],'p','finding') if p.get('highlight') else ''
        result.append(f'''<article class="paper {'compact' if not p['image'] else ''}" id="{p['id']}" data-first="{str(p['first']).lower()}">{img}<div class="paper-body"><div class="paper-meta"><span class="venue">{e(p['venue'])}</span>{status}{first}</div><h3>{e(p['title'])}</h3><p class="authors">{authors(p)}</p>{alias}{t(p['summary'],'p','paper-summary')}{highlight}<details><summary>{bi('My contribution','我的贡献')}</summary>{t(p['contribution'],'p')}</details>{links(p['links'])}</div></article>''')
    return ''.join(result)
def timeline(key):
    return ''.join(f'<article class="timeline-item">{t(x["date"],"p","date")}{t(x["role"],"h3")}{t(x["org"],"p","organization")}{t(x["detail"],"p","timeline-detail")}</article>' for x in d[key])
def head(title):
    return f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="theme-color" content="#f8f9f6"><title>{title}</title><meta name="description" content="Shaobin Ling (凌绍彬), master's student at CUHK-Shenzhen. Research in embodied AI, multi-robot collaboration, and long-horizon task planning."><meta property="og:title" content="{title}"><meta property="og:description" content="Embodied AI · Multi-robot collaboration · Task planning"><meta property="og:type" content="website"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><script src="assets/main.js" defer></script></head>'''
nav=f'''<a class="skip-link" href="#main">{bi('Skip to content','跳至正文')}</a><header class="site-header"><div class="header-inner"><a class="wordmark" href="./" aria-label="Shaobin Ling home">SL<span class="brand-dot">.</span></a><nav aria-label="Main navigation"><a href="#about">{bi('About','关于')}</a><a href="#research">{bi('Research','研究')}</a><a href="#experience">{bi('Experience','经历')}</a><a href="#contact">{bi('Contact','联系')}</a></nav><button class="language-button" data-language aria-label="Switch to Chinese">中文 <span aria-hidden="true">↔</span></button></div></header>'''
hero=f'''<section class="hero" id="about"><div class="hero-copy"><p class="eyebrow">{bi('ROBOTICS · PLANNING · EMBODIED AI','机器人 · 任务规划 · 具身智能')}</p><h1>Shaobin Ling<span class="chinese-name">凌绍彬</span></h1><p class="role">{bi('Master’s student · CUHK-Shenzhen','香港中文大学（深圳） · 硕士在读')}</p>{t(d['intro'],'p','intro')}{t(d['researchIntro'],'p','research-intro')}<div class="hero-links"><a class="button primary" href="mailto:{d['email']}">{bi('Get in touch','邮件联系')} <span aria-hidden="true">↗</span></a><a class="button" href="{d['github']}" target="_blank" rel="noopener">GitHub <span aria-hidden="true">↗</span></a></div></div><figure class="portrait"><div class="portrait-frame"><img src="assets/images/portrait.webp" width="420" height="600" alt="Portrait of Shaobin Ling" fetchpriority="high"></div><figcaption><span class="location-dot" aria-hidden="true"></span>{bi('Shenzhen, China','中国 · 深圳')}<span>22.54° N · 114.06° E</span></figcaption></figure></section>'''
interests='<section class="interests" aria-label="Research interests">'+''.join(f'<div><span class="interest-number">0{i+1}</span>{t(x["title"],"h2")}{t(x["text"],"p")}</div>' for i,x in enumerate(d['interests']))+'</section>'
research=f'''<section class="research-section" id="research"><div class="section-heading"><div><p class="eyebrow">{bi('RESEARCH','研究成果')}</p><h2>{bi('Publications & preprints','论文与预印本')}</h2></div><div class="filters" role="group" aria-label="Filter publications"><button data-filter="all" aria-pressed="true">{bi('All work','全部')} <span>{len(d["papers"]):02d}</span></button><button data-filter="first" aria-pressed="false">{bi('First author','第一作者')} <span>{sum(p["first"] for p in d["papers"]):02d}</span></button></div></div><p class="section-note">{bi('From collaborative planning to navigation and spatial understanding.','从协同任务规划，到导航与空间理解。')}</p><div class="publication-list">{papers()}</div><p class="filter-status sr-only" aria-live="polite"></p></section>'''
field=f'''<section class="field-section"><div class="section-heading"><div><p class="eyebrow">{bi('BEYOND THE PAPER','研究现场')}</p><h2>{bi('From plans to the real world','从任务规划走向真实世界')}</h2></div></div><div class="field-grid"><a class="field-feature" href="https://basaermi.github.io/aecnav-website/" target="_blank" rel="noopener"><img src="assets/images/robot-demo.webp" loading="lazy" width="1100" height="619" alt="AECNav quadruped robot demonstration"><div><p class="eyebrow">AECNav</p><h3>{bi('Evidence-driven navigation, on a real robot.','在真实机器人上，验证证据驱动导航。')}</h3><span class="text-link">{bi('Explore the project','查看项目')} ↗</span></div></a><figure class="poster-feature"><a href="assets/images/poster.webp" target="_blank" rel="noopener"><img src="assets/images/poster.webp" loading="lazy" width="514" height="354" alt="ELHPlan research poster at IROS 2026"></a><figcaption><span class="eyebrow">ELHPlan · IROS 2026</span><p>{bi('Sharing research in multi-agent planning.','分享多智能体任务规划研究。')}</p></figcaption></figure></div></section>'''
experience=f'''<section class="experience-section" id="experience"><div class="section-heading"><div><p class="eyebrow">{bi('BACKGROUND','学习与研究经历')}</p><h2>{bi('Education & experience','教育与工作经历')}</h2></div></div><div class="experience-grid"><div><h3 class="column-title">{bi('Education','教育经历')}</h3>{timeline('education')}</div><div><h3 class="column-title">{bi('Research & teaching','研究与教学')}</h3>{timeline('experience')}</div></div><div class="awards"><h3>{bi('Selected honors','所获奖项')}</h3><ul>{''.join(t(x,'li') for x in d['awards'])}</ul></div></section>'''
footer=f'''<section class="contact" id="contact"><p class="eyebrow">{bi('LET’S CONNECT','保持联系')}</p><h2>{bi('Good research starts with a conversation.','让交流成为研究的起点。')}</h2><a class="email" href="mailto:{d['email']}">{d['email']} <span aria-hidden="true">↗</span></a><p>{bi('Interested in embodied AI, planning, or robot collaboration? I’d be glad to connect.','欢迎交流具身智能、任务规划与多机器人协同相关研究。')}</p></section><footer><span>© 2026 Shaobin Ling</span><span>{bi('Updated October 2026','更新于 2026 年 10 月')}</span><a href="#about">{bi('Back to top','返回顶部')} ↑</a></footer>'''
dialog=f'''<dialog id="video-dialog" aria-labelledby="video-title"><div class="dialog-heading"><h2 id="video-title">Research demo</h2><button class="dialog-close" aria-label="Close video">{bi('Close','关闭')} ×</button></div><video controls playsinline preload="none"></video><p>{bi('Research demonstration video.','研究演示视频。')}</p></dialog>'''
html=head('Shaobin Ling · Robotics & Embodied AI')+'<body>'+nav+'<main id="main" class="container">'+hero+interests+research+field+experience+footer+'</main>'+dialog+'</body></html>'
(ROOT/'index.html').write_text(html)
print(f'Generated index.html; {len(d["papers"])} papers, 2 languages.')
