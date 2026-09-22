#!/usr/bin/env python3
"""Reproduce BeFree from the pinned approved template, changing content only.
Source: supplied portfolio-report(1).html, extracted 15-18 September 2026.
The report covers eight properties, not the entire BeLive business.
"""
import base64
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

source = Path(sys.argv[1] if len(sys.argv) > 1 else '_template')
public = Path('public')
if public.exists():
    shutil.rmtree(public)
# Font binaries stay at their original public source; do not redistribute them.
shutil.copytree(source / 'public', public, ignore=shutil.ignore_patterns('fonts'))
js_path = public / 'assets/index-CHKnvv48.js'
js = js_path.read_text(encoding='utf-8')
original_js_sha = hashlib.sha256(js_path.read_bytes()).hexdigest()
a = js.index('const J0=') + len('const J0=')
b = js.index(',I0=new Map', a)
rows = json.loads(js[a:b])
prefix, suffix = js[:a], js[b:]

# Rows replace the original English lookup key and both existing translations.
updates = {
  0: ['HIGHEST RECORDED MONTHLY UNIT RENT', '单个单位最高月租记录', 'SEWA BULANAN UNIT TERTINGGI DIREKODKAN'],
  2: ['The highest recorded unit income in this eight-property portfolio, from combined room rents.', '在这份八个项目的组合报告中，单个单位各房间合计租金的最高记录。', 'Pendapatan unit tertinggi dalam portfolio lapan hartanah ini, daripada gabungan sewa bilik.'],
  3: ['Gross contracted room rent before costs, from records extracted 15–18 September 2026. Excludes parking and other charges. An individual result, not a typical return or a guarantee.', '2026年9月15至18日提取的记录；为扣除成本前的房间合约租金，不含停车位及其他收费。这是个别单位成绩，并非一般回报或保证。', 'Sewa bilik berkontrak kasar sebelum kos, daripada rekod 15–18 September 2026. Tidak termasuk parkir dan caj lain. Hasil individu, bukan pulangan biasa atau jaminan.'],
  5: ['OUR PORTFOLIO. YOUR PERSPECTIVE.', '以组合成绩，了解管理实力。', 'PORTFOLIO KAMI. PERSPEKTIF ANDA.'],
  8: ['We put our people, technology and tenant network to work — so your property doesn’t become your second job. Here is the record across eight properties.', '让团队、科技与租客网络协同运作，不让物业成为您的第二份工作。以下是八个项目的管理记录。', 'Kami menggerakkan pasukan, teknologi dan rangkaian penyewa — supaya hartanah anda tidak menjadi pekerjaan kedua. Ini rekod daripada lapan hartanah.'],
  9: ['SEPTEMBER 2026 OCCUPANCY', '2026年9月入住率', 'PENGHUNIAN SEPTEMBER 2026'],
 10: ['Rental performance. Made visible.', '让出租表现，有据可查。', 'Prestasi sewaan. Jelas kelihatan.'],
 11: ['856 of 896 lettable rooms had a tenancy during September, across the eight properties in the report.', '报告中八个项目共896间可出租房间，856间在9月期间有租约。', '856 daripada 896 bilik boleh disewa mempunyai sewaan dalam bulan September, merentas lapan hartanah dalam laporan.'],
 12: ['A tenancy covering at least one day counts. September is still in progress.', '当月有至少一天租约即计为入住；9月尚未结束。', 'Sewaan sekurang-kurangnya satu hari dikira. September masih berjalan.'],
 13: ['2026 CONTRACT RENEWALS', '2026年合约续租率', 'PEMBAHARUAN KONTRAK 2026'],
 15: ['A reason to stay.', '让租客选择，继续住下去。', 'Sebab untuk terus menetap.'],
 16: ['57.3% of 1,019 contracts expiring in 2026 were renewed across the reported portfolio.', '报告组合中，2026年到期的1,019份合约，57.3%已续租。', '57.3% daripada 1,019 kontrak yang tamat pada 2026 diperbaharui dalam portfolio yang dilaporkan.'],
 17: ['Linked renewals or a new contract within 31 days; informal month-to-month stays excluded.', '包括关联续约或到期31天内的新合约；不含非正式逐月续住。', 'Pembaharuan berpaut atau kontrak baharu dalam 31 hari; sambungan bulanan tidak formal dikecualikan.'],
 18: ['PEOPLE WHO CALLED IT HOME', '曾经在这里，安家的租客', 'MEREKA YANG PERNAH MENGHUNINYA'],
 20: ['Real people. Real homes.', '真实的租客。真实的生活。', 'Penghuni sebenar. Kediaman sebenar.'],
 21: ['2,278 tenants housed across these buildings to date, as reported in the portfolio review.', '根据组合报告，这些项目至今累计接待2,278名租客。', '2,278 penyewa pernah ditempatkan di bangunan ini setakat laporan portfolio.'],
 22: ['Historical total across the eight properties, not the number currently in residence.', '八个项目的历史累计数字，并非现有在住人数。', 'Jumlah sejarah merentas lapan hartanah, bukan jumlah penghuni semasa.'],
 23: ['EIGHT PROPERTIES. ONE CONNECTED TEAM.', '八个项目。一个协同团队。', 'LAPAN HARTANAH. SATU PASUKAN BERHUBUNG.'],
 25: ['A portfolio. Professionally managed.', '专业管理，贯穿整个组合。', 'Satu portfolio. Diurus secara profesional.'],
 26: ['195 active units and 896 lettable rooms across eight properties in this portfolio review.', '这份组合报告涵盖八个项目、195个在管单位及896间可出租房间。', '195 unit aktif dan 896 bilik boleh disewa merentas lapan hartanah dalam laporan portfolio ini.'],
 28: ['Source: supplied eight-property portfolio report, records extracted 15–18 September 2026. These are portfolio results, not company-wide figures. September is in progress. Past performance is not a promise for your property.', '来源：所提供的八项目组合报告，记录提取于2026年9月15至18日。这些是该组合的成绩，并非全公司数据；9月尚未结束。过往表现不代表对您物业的承诺。', 'Sumber: laporan portfolio lapan hartanah yang dibekalkan, rekod 15–18 September 2026. Angka ini untuk portfolio tersebut, bukan seluruh syarikat. September masih berjalan. Prestasi lepas bukan janji untuk hartanah anda.'],
 35: ['This portfolio alone brings together 195 active units across eight properties — with systems, technology and people working together.', '仅这份组合，就涵盖八个项目、195个在管单位，由系统、科技与团队协同支持。', 'Portfolio ini sahaja merangkumi 195 unit aktif di lapan hartanah — disokong sistem, teknologi dan manusia yang bekerjasama.'],
 47: ['One property.', '一份物业投资。', 'Satu hartanah.'],
 48: ['A whole team behind it.', '背后有一整个团队。', 'Seluruh pasukan di belakangnya.'],
 50: ['Lettable rooms in this portfolio', '该组合的可出租房间', 'Bilik boleh disewa dalam portfolio ini'],
 51: ['Eight properties. A team for your property.', '八个项目的经验，支持您的物业。', 'Lapan hartanah. Pasukan untuk hartanah anda.'],
 52: ['Active units in this portfolio', '该组合的在管单位', 'Unit aktif dalam portfolio ini'],
 54: ['LIFE WITH BELIVE', '在 BELIVE 的生活', 'KEHIDUPAN BERSAMA BELIVE'],
 57: ['A tenant shares her BeLive experience', '租客分享她在 BeLive 的体验', 'Seorang penyewa berkongsi pengalaman BeLive'],
 58: ['BELIVE · TENANT STORY', 'BELIVE · 租客故事', 'BELIVE · KISAH PENYEWA'],
 60: ['BeLive experience.', 'BeLive 生活体验。', 'Pengalaman BeLive.'],
 61: ['Featured on BeLive’s official website: a tenant shares her experience of one of our managed homes.', '来自 BeLive 官网的租客故事，分享她在其中一个管理项目的居住体验。', 'Dipaparkan di laman rasmi BeLive: seorang penyewa berkongsi pengalaman di salah satu kediaman yang kami urus.'],
166: ['BEFREE BY BELIVE · FOR PROPERTY PARTNERS', 'BEFREE BY BELIVE · 为物业伙伴而设', 'BEFREE BY BELIVE · UNTUK RAKAN HARTANAH'],
193: ['EIGHT-PROPERTY PORTFOLIO', '八个项目的管理组合', 'PORTFOLIO LAPAN HARTANAH'],
202: ['Room and unit counts refer only to the supplied eight-property portfolio, extracted 15–18 September 2026. Google review figures are retained from the original BeLive website template and are not live. Logos represent selected BeLive collaborations, not endorsements of individual rental returns.', '房间与单位数量仅指所提供的八项目组合，记录提取于2026年9月15至18日。Google评价数字沿用原BeLive网站模板，并非实时数字。标志代表BeLive的部分合作关系，不代表对个别租金回报的背书。', 'Jumlah bilik dan unit merujuk hanya kepada portfolio lapan hartanah, rekod 15–18 September 2026. Angka ulasan Google dikekalkan daripada templat asal BeLive dan bukan angka langsung. Logo mewakili kerjasama terpilih BeLive, bukan pengesahan pulangan sewaan individu.'],
211: ['An individual owner’s story, not a promise of timing, occupancy or rental returns for every property.', '个别业主的故事，并非对每个物业出租时间、入住率或租金回报的保证。', 'Kisah pemilik individu, bukan jaminan tempoh, penghunian atau pulangan sewa bagi setiap hartanah.'],
234: ['for your property.', '为您的物业提供支持。', 'untuk hartanah anda.']
}
for index, new_row in updates.items():
    old = rows[index][0]
    prefix = prefix.replace(old, new_row[0])
    suffix = suffix.replace(old, new_row[0])
    rows[index] = new_row
rows.extend([
    ['tenants', '位租客', 'penyewa'],
    ['BeFree · Live more', 'BeFree · 生活更多可能', 'BeFree · Lebih masa untuk hidup'],
    ['© 2026 BeLive Ventures Sdn Bhd · BeFree', '© 2026 BeLive Ventures Sdn Bhd · BeFree', '© 2026 BeLive Ventures Sdn Bhd · BeFree']
])
js = prefix + json.dumps(rows, ensure_ascii=False, separators=(',', ':')) + suffix

# Numeric edits are restricted to the performance component, never React internals.
f, g = js.index('function F0()'), js.index('function $0()')
component = js[f:g]
number_edits = {
    'children:["≈95",c.jsx("span",{children:"%"})]': 'children:["95.5",c.jsx("span",{children:"%"})]',
    'children:["7",c.jsx("span",{children:" days"})]': 'children:["57.3",c.jsx("span",{children:"%"})]',
    'children:["1",c.jsx("span",{children:" month"})]': 'children:["2,278",c.jsx("span",{children:" tenants"})]',
    'children:["360",c.jsx("span",{children:" rooms"})]': 'children:["896",c.jsx("span",{children:" rooms"})]',
    'children:"RM4,300"': 'children:"RM5,750"'
}
for old, new in number_edits.items():
    assert component.count(old) == 1, f'Unexpected template structure: {old}'
    component = component.replace(old, new)
js = js[:f] + component + js[g:]
for old, new in {
    'M Vertica · Taman Maluri': 'BeFree · Live more',
    'Hi Keith, I own a unit at M Vertica.': 'Hi Keith, I own a property.',
    'Keith 您好，我在 M Vertica 有一个单位。': 'Keith 您好，我想了解我的物业可以获得什么管理支持。',
    'Hai Keith, saya memiliki unit di M Vertica.': 'Hai Keith, saya memiliki sebuah hartanah.',
    'BeLive M Vertica｜': 'BeFree by BeLive｜',
    'BeLive M Vertica |': 'BeFree by BeLive |',
    '© 2026 BeLive Ventures Sdn Bhd · M Vertica, Taman Maluri': '© 2026 BeLive Ventures Sdn Bhd · BeFree',
    'id:"m-vertica-story"': 'id:"tenant-story"',
    'children:"4,500"': 'children:"896"',
    'children:"~1,000"': 'children:"195"',
    'const Se="/assets/"': 'const Se="./assets/"',
    'V.src="/analytics.js"': 'V.src="./analytics.js"',
    'belive-language': 'befree-language'
}.items():
    assert old in js, f'Missing expected template content: {old}'
    js = js.replace(old, new)
js_path.write_text(js, encoding='utf-8')

css_path = public / 'assets/index-BU1YTRwW.css'
css = css_path.read_text(encoding='utf-8')
font_base = 'https://rawcdn.githack.com/keithkuang-BeLive/BeFree-MVertica/3d0fe6d7ea613508f2d23261bbbb34e714a46c62/public/fonts/'
css = css.replace('url(/fonts/', 'url(' + font_base)
css_path.write_text(css, encoding='utf-8')
html_path = public / 'index.html'
html = html_path.read_text(encoding='utf-8')
html = html.replace('Your Property. Your Freedom. | BeLive M Vertica', 'BeFree by BeLive | More Time for Life')
html = html.replace('your M Vertica property', 'your property')
html = html.replace('href="/assets/', 'href="./assets/').replace('src="/assets/', 'src="./assets/')
html = html.replace('<meta name="theme-color"', '<meta name="robots" content="noindex,nofollow"><meta name="theme-color"')
html_path.write_text(html, encoding='utf-8')

# A single-file preview: same React application, images/JS/CSS embedded.
# Existing public typeface URLs are preserved rather than redistributing fonts.
assets = {}
for p in sorted((public / 'assets').iterdir()):
    if p.suffix.lower() in {'.png', '.webp', '.jpg', '.jpeg'}:
        mime = {'.png':'image/png', '.webp':'image/webp', '.jpg':'image/jpeg', '.jpeg':'image/jpeg'}[p.suffix.lower()]
        assets['./assets/' + p.name] = 'data:' + mime + ';base64,' + base64.b64encode(p.read_bytes()).decode()
inline_bridge = 'const __BEFREE_IMAGES=' + json.dumps(assets, separators=(',', ':')) + ';for(const key of ["jsx","jsxs"]){const render=c[key];c[key]=function(type,props,...args){if(props&&typeof props.src==="string"&&__BEFREE_IMAGES[props.src])props={...props,src:__BEFREE_IMAGES[props.src]};return render(type,props,...args)}};'
inline_js = js.replace('const J0=', inline_bridge + 'const J0=', 1)
analytics = (public / 'analytics.js').read_text(encoding='utf-8')
inline_js = inline_js.replace('V.src="./analytics.js"', 'V.text=' + json.dumps(analytics))
standalone = re.sub(r'<script type="module"[^>]*></script>', lambda _: '<script type="module">' + inline_js.replace('</script', '<\\/script') + '</script>', html)
standalone = re.sub(r'<link rel="stylesheet"[^>]*>', lambda _: '<style>' + css + '</style>', standalone)
standalone = standalone.replace('href="./assets/logo.webp"', 'href="' + assets['./assets/logo.webp'] + '"')
Path('index.html').write_text(standalone, encoding='utf-8')

Path('scripts').mkdir(exist_ok=True)
for name in ['build.mjs', 'serve.mjs']:
    shutil.copyfile(source / 'scripts' / name, Path('scripts') / name)
package = {'name':'befree-by-belive','version':'1.0.0','private':True,'type':'module','scripts':{'build':'node scripts/build.mjs','start':'node scripts/serve.mjs'}}
Path('package.json').write_text(json.dumps(package, indent=2) + '\n')
shutil.copyfile(source / 'vercel.json', 'vercel.json')
Path('.gitignore').write_text('node_modules/\ndist/\n_template/\n.vercel/\nverification/\n')
Path('docs').mkdir(exist_ok=True)
metrics = {'brand':'BeFree by BeLive','source':'User-supplied portfolio-report(1).html','scope':'Eight-property portfolio only; not company-wide','extracted':'15–18 September 2026','lettable_rooms':896,'active_units':195,'properties':8,'september_occupancy_percent':95.5,'rooms_with_tenancy_in_september':856,'renewal_percent_2026':57.3,'expiring_contracts_2026':1019,'tenants_housed_to_date_as_reported':2278,'highest_recorded_monthly_unit_room_rent_RM':5750,'occupancy_definition':'At least one day covered by a tenancy in the month; September is in progress','income_definition':'Current contracted room rents summed per unit, before costs; excludes car park and other charges. Individual maximum, not typical or guaranteed.','review_numbers':'Retained original-template figures, not live or derived from the portfolio report','template_commit':'3d0fe6d7ea613508f2d23261bbbb34e714a46c62','original_template_js_sha256':original_js_sha}
Path('docs/portfolio-data.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + '\n')
Path('README.md').write_text('''# BeFree by BeLive

Generic property-partner website based on the approved BeLive design. The original condo-specific repository remains untouched.

## Review the website

[Open the BeFree website preview](https://raw.githack.com/keithkuang-BeLive/BeFree/main/index.html)

This is a review preview, not a claimed Vercel production deployment.

## Deploy on Vercel

Import `keithkuang-BeLive/BeFree`, branch `main`. Framework: **Other**. Root: repository root. Build: `npm run build`. Output: `dist`. Configuration is included in `vercel.json`.

`public/` is the normal website. Root `index.html` is the same application as a single-file review preview (images, CSS and JS embedded; original public typefaces referenced). No secrets or private records are included.

## Data scope

The uploaded portfolio report covers eight properties, 896 lettable rooms and 195 active units. It reports 95.5% September occupancy (856/896 rooms), 57.3% renewals on 1,019 expiring contracts, and 2,278 tenants housed to date. September is incomplete. Occupancy means at least one tenancy-covered day in the month, not daily occupancy. Highest recorded unit rent is RM5,750 gross before costs, not a typical or guaranteed return. These are not company-wide totals.

Google review figures and selected collaboration logos are retained from the original approved template and are separately qualified on the page. No review numbers are represented as live. Services and the 0% fee model remain subject to package terms and other charges.

## Reproduce this version

`scripts/create-portfolio.py` applies the documented content changes to the pinned original compiled template. It does not claim to recover the original editable React/TypeScript source. Use the accompanying workflow to rebuild from that pinned reference. The supplied raw portfolio report is not published.

This is a draft and carries `noindex,nofollow` until approved for launch.
''', encoding='utf-8')
print(json.dumps({'status':'created','public_files':len(list(public.rglob('*'))),'standalone_bytes':len(standalone.encode()),'metrics':metrics}, ensure_ascii=False))
