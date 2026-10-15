#!/usr/bin/env python3
"""Check generated content and local links; no third-party dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=set();self.images=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if attrs.get('id'):
            assert attrs['id'] not in self.ids, f'Duplicate id: {attrs["id"]}'
            self.ids.add(attrs['id'])
        for key in ('href','src','data-video'):
            if attrs.get(key):self.links.append(attrs[key])
        if tag=='img':assert attrs.get('alt'), 'Missing image alternative text'
        if 'data-en' in attrs:assert attrs.get('data-zh'), 'Missing Chinese translation'
for path in (ROOT/'index.html',):
    page=Page();page.feed(path.read_text())
    for link in page.links:
        parsed=urlsplit(link)
        if parsed.scheme or parsed.netloc:continue
        if parsed.path:
            target=(path.parent/unquote(parsed.path)).resolve()
            assert target.is_relative_to(ROOT), f'Link escapes root: {link}'
            assert target.exists(), f'Missing file: {link}'
        elif parsed.fragment:assert parsed.fragment in page.ids, f'Broken anchor: {link}'
    print(f'{path.name}: {len(page.links)} local/external references checked')
d=json.loads((ROOT/'data/content.json').read_text())
assert len(d['papers'])==6
assert sum(p['first'] for p in d['papers'])==1
assert any('Han Lyu' in p['authors'] and p.get('alias') for p in d['papers'])
print('Content checks passed: 6 papers, 1 first-author paper, alias disclosure present.')

assert {p['id'] for p in d['papers']} == {'elhplan', 'aecnav', 'ucsbench', 'exploration', 'tgpt', 'distillation'}, 'Only approved publications may be published'

assert not (ROOT/"cv.html").exists(), "Public CV must not be included"
assert "cv.html" not in (ROOT/"index.html").read_text(), "Public CV link must not be included"
