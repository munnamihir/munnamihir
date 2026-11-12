#!/usr/bin/env python3
"""Update language-donut.svg using GitHub language byte counts for a curated public repo sample.

Source: https://docs.github.com/en/rest/repos/repos#list-repository-languages
This is a sampled source-code-byte breakdown, not a measure of developer skill,
hours or contribution counts. Uses the default GitHub Linguist classifications.
"""
import html, json, math, os, urllib.request
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone

OWNER = 'munnamihir'
REPOS = [
  'cryptoscan-pqc','QuantumMail-v2','cipherguard','pneuma-db','aplomb',
  'fleetmind','shift-aware-scheduling','nemoclaw-community',
  'linkedin-fixer','orybit','Saas-radar',
]
ROOT=Path(__file__).resolve().parents[1]
AS=ROOT/'assets'
COLORS=['#40E1D5','#79BBFF','#B19DFF','#F0BC83','#E99FD4','#8FE2AD']
TOKEN=os.environ.get('GH_TOKEN','')


def get_languages(repo):
    req=urllib.request.Request(
       f'https://api.github.com/repos/{OWNER}/{repo}/languages',
       headers={'Accept':'application/vnd.github+json',
                'User-Agent':'mihir-profile-telemetry',
                **({'Authorization':f'Bearer {TOKEN}'} if TOKEN else {})},
    )
    with urllib.request.urlopen(req,timeout=15) as r:
        return json.load(r)


def txt(x,y,value,size,color='#EAF4FF',weight='600',anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{html.escape(str(value))}</text>'


def generate():
    totals=Counter()
    for repo in REPOS:
        for lang,bytes_ in get_languages(repo).items():
            totals[lang]+=int(bytes_)
    summed=sum(totals.values())
    if summed<=0:
        raise RuntimeError('Zero language bytes reported; leaving old graphic unchanged')
    top=totals.most_common(5)
    rest=summed-sum(v for _,v in top)
    if rest:top.append(('Other',rest))
    r=112; cx=215;cy=231;circ=2*math.pi*r; offset=0
    body=[]
    body.append('<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#080F1F"/><stop offset="1" stop-color="#11172B"/></linearGradient><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#506890" stroke-opacity=".12"/></pattern></defs>')
    body.extend(['<rect width="1200" height="419" rx="20" fill="url(#bg)" stroke="#32506C"/>','<rect width="1200" height="419" rx="20" fill="url(#grid)"/>'])
    body.append(txt(38,46,'// GITHUB LANGUAGE FINGERPRINT',15,'#60E6D8','800'))
    body.append(txt(38,79,'Source-code bytes · selected public repositories',21,'#ECF6FE','700'))
    body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#2A3851" stroke-width="38"/>')
    for i,(lang,bytes_) in enumerate(top):
        seg=circ*bytes_/summed
        length=max(0,seg-6)
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{COLORS[i]}" stroke-width="38" stroke-dasharray="{length:.2f} {circ-length:.2f}" stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 {cx} {cy})"/>')
        offset+=seg
    body.append(txt(cx,225,str(len(REPOS)),45,'#EBF6FF','800','middle'))
    body.append(txt(cx,247,'REPOSITORIES',12,'#78DEDA','800','middle'))
    for i,(lang,bytes_) in enumerate(top):
        x=421+(i//3)*381;y=152+(i%3)*70
        body.append(f'<rect x="{x}" y="{y-16}" width="14" height="14" rx="4" fill="{COLORS[i]}"/>')
        body.append(txt(x+25,y-2,lang,15,'#E7F0FC','700'))
        body.append(txt(x+25,y+22,f'{bytes_/summed*100:.1f}% of reported bytes',12,'#A3B8D1','500'))
    timestamp=datetime.now(timezone.utc).strftime('%Y-%m-%d UTC')
    body.append(txt(40,398,f'LAST SYNC  {timestamp}   //   GitHub Linguist API   //   ~{summed:,} language bytes',12,'#91ABC6','500'))
    body.append('</svg>')
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="419" viewBox="0 0 1200 419">'+''.join(body)
    AS.mkdir(parents=True,exist_ok=True)
    (AS/'language-donut.svg').write_text(svg,encoding='utf-8')
    (AS/'language-telemetry.json').write_text(json.dumps({
        'updated_utc':timestamp,'owner':OWNER,'repositories':REPOS,
        'raw_language_bytes':dict(totals.most_common()),'total_language_bytes':summed,
    },indent=2)+'\n',encoding='utf-8')
    print('Updated language-donut.svg from actual GitHub language byte counts.')

if __name__ == '__main__':
    generate()
