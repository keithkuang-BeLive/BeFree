#!/usr/bin/env python3
"""Visual-first BeFree revision. Run after create-portfolio.py.
Company scale is explicitly user supplied, separate from eight-property results.
"""
from pathlib import Path
import base64, json, re, urllib.request
root=Path(__file__).resolve().parents[1]
public=root/'public'
js_path=public/'assets/index-CHKnvv48.js'
css_path=public/'assets/index-BU1YTRwW.css'
js=js_path.read_text()
marker='/* BEFREE_VISUAL_INTRO_V2 */'
if marker not in js:
    a=js.index('const J0=')+len('const J0=');b=js.index(',I0=new Map',a)
    rows=json.loads(js[a:b]);prefix,suffix=js[:a],js[b:]
    updates={
      33:['A whole team behind your property. No percentage-based management fee.','整个团队为您的物业服务，不抽取百分比管理费。','Satu pasukan untuk hartanah anda. Tanpa yuran pengurusan berasaskan peratusan.'],
      39:['Marketing, cleaning and system services are priced separately in your quotation.','营销、清洁及系统服务在报价中独立列明。','Pemasaran, pembersihan dan sistem dicaj berasingan dalam sebut harga.'],
      41:['AI follows up. Spacify connects the records. Our people take action.','AI跟进咨询，Spacify连接记录，团队落实行动。','AI membuat susulan. Spacify menghubungkan rekod. Pasukan kami bertindak.'],
      43:['Tenant finding, property care and owner support. Working together.','招租、物业照护与业主服务，协同运作。','Pencarian penyewa, penjagaan hartanah dan sokongan pemilik. Bersama-sama.'],
      114:['One system. People who follow through.','一个系统，一群负责到底的人。','Satu sistem. Pasukan yang membuat susulan.'],
      115:['','',''],
      122:['Tenancies, rental records and reports. Together in Spacify.','租约、租金记录与报告，集中在Spacify。','Sewaan, rekod sewa dan laporan. Semuanya dalam Spacify.'],
      128:['Cleaning and repairs, with tracked tickets and team follow-up.','清洁与维修，以工单追踪、由团队跟进。','Pembersihan dan pembaikan, dengan tiket serta susulan pasukan.'],
      134:['Smart locks and meters, connected to tenancy management.','智能门锁与电表，连接租务管理。','Kunci dan meter pintar, berhubung dengan pengurusan sewaan.'],
      170:['Family time. Quieter weekends. That trip you keep postponing.','陪伴家人，享受周末，出发去那场一再推迟的旅行。','Masa keluarga. Hujung minggu tenang. Percutian yang sering tertangguh.'],
      180:['Family holidays. Quieter weekends. More choices.','家庭旅行，悠闲周末，更多选择。','Percutian keluarga. Hujung minggu tenang. Lebih pilihan.'],
      181:['','',''],182:['','',''],
      184:['Your property.','您的物业。','Hartanah anda.'],
      185:['Not your second job.','不该是第二份工作。','Bukan pekerjaan kedua anda.'],
      186:['','',''],187:['','',''],
      210:['A completed home. Tenant interest already coming in.','房子准备就绪，租客兴趣已到。','Rumah siap. Minat penyewa mula masuk.'],
      211:['One owner’s experience. Individual results vary.','个别业主体验，实际结果因物业而异。','Pengalaman seorang pemilik. Hasil individu berbeza.'],
      61:['Hear it from someone who lives with BeLive.','听听住在BeLive的租客怎么说。','Dengar daripada penghuni BeLive sendiri.'],
      62:['One tenant’s experience.','一位租客的真实体验。','Pengalaman seorang penyewa.'],
      214:['Owner confidence.','业主安心。','Keyakinan pemilik.'],
      215:['Tenant comfort.','租客舒心。','Keselesaan penyewa.'],
      216:['','',''],217:['','',''],
      233:['A whole team.','一个完整的团队。','Seluruh pasukan.'],
      234:['On your side.','站在您这一边。','Di sisi anda.']
    }
    for i,new in updates.items():
        old=rows[i][0]
        prefix=prefix.replace(json.dumps(old,ensure_ascii=False),json.dumps(new[0],ensure_ascii=False))
        suffix=suffix.replace(json.dumps(old,ensure_ascii=False),json.dumps(new[0],ensure_ascii=False))
        suffix=suffix.replace(json.dumps(' '+old,ensure_ascii=False),json.dumps(' '+new[0],ensure_ascii=False))
        rows[i]=new
    rows.extend([
      ['THIS IS BELIVE','这就是 BELIVE','INILAH BELIVE'],
      ['rooms under management','间房间在管','bilik di bawah pengurusan'],
      ['One complete team.','一个完整的专业团队。','Satu pasukan lengkap.'],
      ['You own the property. We take care of the everyday.','您拥有物业，日常交给我们。','Anda memiliki hartanah. Kami uruskan keperluan harian.'],
      ['Your team, behind the scenes.','在幕后，为您负责的团队。','Pasukan anda di sebalik tabir.'],
      ['Marketing','营销招租','Pemasaran'],['Operations','营运管理','Operasi'],
      ['Housekeeping','清洁保养','Pembersihan'],['Maintenance','维修支持','Penyelenggaraan'],
      ['Owner support','业主服务','Sokongan pemilik'],['Spacify & AI','Spacify 与 AI','Spacify & AI'],
      ['Enquiries, viewings and tenant acquisition.','咨询、带看与租客招募。','Pertanyaan, lawatan dan pencarian penyewa.'],
      ['Move-ins, inspections and day-to-day coordination.','入住、巡检与日常协调。','Kemasukan, pemeriksaan dan penyelarasan harian.'],
      ['Scheduled cleaning and reports you can follow.','定期清洁，记录可追踪。','Pembersihan berjadual dan laporan yang boleh disemak.'],
      ['Repair requests, tracked and followed through.','维修需求，追踪并落实。','Permintaan pembaikan, dijejak dan disusuli.'],
      ['A point of contact for your property.','您的物业，有人对接。','Satu saluran untuk urusan hartanah anda.'],
      ['Tenancy, billing and service records, connected.','租约、账单与服务记录，一体连接。','Rekod sewaan, bil dan perkhidmatan, berhubung.'],
      ['Explore your team','了解您的团队','Kenali pasukan anda'],
      ['Select a team function','选择团队职能','Pilih fungsi pasukan'],
      ['Reviews on Google','Google 上的评价','Ulasan di Google'],
      ['Real experiences.','真实体验。','Pengalaman sebenar.'],
      ['Read them for yourself.','亲自看看，他们怎么说。','Baca sendiri.'],
      ['Read reviews','阅读评价','Baca ulasan'],['reviews','条评价','ulasan'],
      ['Company-profile snapshot · not live','公司简介快照 · 非实时','Petikan profil syarikat · bukan langsung'],
      ['SELECTED COLLABORATIONS','部分合作伙伴','KERJASAMA TERPILIH'],
      ['Our network. Your advantage.','我们的网络，您的优势。','Rangkaian kami. Kelebihan anda.'],
      ['About the numbers','数字说明','Tentang angka ini'],
      ['4,500 rooms is BeLive’s company-wide management figure supplied by Keith on 22 September 2026. The case-study figures below cover only eight properties. The 4.7/5 and 2,000+ review figures are retained from BeLive’s original company-profile template; their original verification date was not supplied. Check Google for the latest. Collaboration logos do not imply endorsement of rental returns.','4,500间为Keith于2026年9月22日提供的BeLive全公司在管房间数。下方案例数据仅涵盖八个项目。4.7/5及2,000+评价沿用原公司简介模板，未提供原核实日期；最新信息请以Google为准。合作标志不代表对租金回报的背书。','4,500 bilik ialah angka pengurusan seluruh BeLive yang dibekalkan Keith pada 22 September 2026. Kajian kes di bawah meliputi lapan hartanah sahaja. Angka 4.7/5 dan 2,000+ ulasan dikekalkan daripada profil asal; tarikh pengesahan asal tidak dibekalkan. Semak Google untuk angka terkini. Logo kerjasama bukan pengesahan pulangan sewaan.'],
      ['The work.','实际执行。','Hasil kerja.'],['In numbers.','用数字说话。','Dalam angka.'],
      ['Eight-property case study · 15–18 Sep 2026','八个项目案例 · 2026年9月15–18日','Kajian kes lapan hartanah · 15–18 Sep 2026'],
      ['Sep occupancy*','9月入住率*','Penghunian Sep*'],
      ['2026 renewals','2026年续租','Pembaharuan 2026'],
      ['Highest monthly unit rent','单位最高月租','Sewa unit bulanan tertinggi'],
      ['Monthly tenancy coverage','当月租约覆盖率','Liputan sewaan bulanan'],
      ['Of contracts expiring in 2026','2026年到期合约','Daripada kontrak tamat pada 2026'],
      ['Gross, before costs. Individual maximum.','毛租金，未扣成本。个别最高记录。','Kasar, sebelum kos. Maksimum individu.'],
      ['Not a typical or guaranteed return.','非一般或保证回报。','Bukan pulangan biasa atau dijamin.'],
      ['*September is partial. Tenancy coverage, not occupied nights. Case study only, not all 4,500 rooms.','*9月尚未结束。按当月租约覆盖计算，非实际入住晚数。仅限案例，不代表全公司4,500间房。','*September belum lengkap. Liputan sewaan, bukan malam dihuni. Kajian kes sahaja, bukan semua 4,500 bilik.'],
      ['See the basis','查看计算方式','Lihat asas pengiraan'],
      ['Source: portfolio report, 15–18 September 2026. Occupancy: 856/896 rooms with a tenancy covering at least one day in September. Renewals: 57.3% of 1,019 expiring contracts, using linked renewals or a new contract within 31 days. Highest unit rent: RM5,750 in combined contracted monthly room rents, before costs, excluding parking and other charges. Results vary by property.','来源：2026年9月15–18日组合报告。入住率：896间中856间在9月至少一天有租约。续租率：1,019份到期合约中57.3%已续约，计入关联续租或到期31天内的新合约。单位最高月租：房间合约月租合计RM5,750，未扣成本，不含停车位及其他收费。实际表现因物业而异。','Sumber: laporan portfolio, 15–18 September 2026. Penghunian: 856/896 bilik dengan sewaan sekurang-kurangnya sehari dalam September. Pembaharuan: 57.3% daripada 1,019 kontrak tamat, melalui pembaharuan berpaut atau kontrak baharu dalam 31 hari. Sewa unit tertinggi: RM5,750 gabungan sewa bilik bulanan berkontrak, sebelum kos, tidak termasuk parkir dan caj lain. Hasil berbeza mengikut hartanah.'],
      ['What could your property do?','您的物业，有多少可能？','Apa potensi hartanah anda?'],
      ['How 0% works','0%如何运作','Bagaimana 0% berfungsi'],
      ['Other service charges and package terms apply.','其他服务收费及配套条款适用。','Caj perkhidmatan lain dan terma pakej dikenakan.'],
      ['A clear service package.','清晰的服务配套。','Pakej perkhidmatan yang jelas.'],
      ['Technology does the repetitive work.','科技处理重复工作。','Teknologi mengurus kerja berulang.'],
      ['A real team follows through.','专业团队落实跟进。','Pasukan sebenar membuat susulan.']
    ])
    js=prefix+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+suffix
    brand=r'''/* BEFREE_VISUAL_INTRO_V2 */
function BeFreeTeamIcon({index:b}){const d=[
 ["M3 11v2a2 2 0 0 0 2 2h3l8 4V5l-8 4H5a2 2 0 0 0-2 2Z","M7 15l1 6h3l-2-6","M20 8v8"],
 ["M4 21V3h12v18","M16 9h4v12H2","M8 7h4M8 11h4M8 15h4M8 21v-3h4v3"],
 ["m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5Z","M20 2v4M18 4h4"],
 ["M14.7 6.3a4 4 0 0 0-5 5L3 18a2.1 2.1 0 0 0 3 3l6.7-6.7a4 4 0 0 0 5-5l-3 3-3-3 3-3Z"],
 ["M21 11.5a8.5 8.5 0 0 1-8.5 8.5H3l2-5a8.5 8.5 0 1 1 16-3.5Z","M8 10h8M8 14h5"],
 ["M7 7h10v10H7Z","M4 9h3M4 15h3M17 9h3M17 15h3M9 4v3M15 4v3M9 17v3M15 17v3","M10 10h4v4h-4Z"]
][b];return c.jsx("svg",{viewBox:"0 0 24 24",width:23,height:23,fill:"none",stroke:"currentColor",strokeWidth:1.5,strokeLinecap:"round",strokeLinejoin:"round","aria-hidden":true,children:d.map((p,i)=>c.jsx("path",{d:p},i))})}
function BeFreeBrand(){const [active,setActive]=Na.useState(1);const roles=[
["Marketing","Enquiries, viewings and tenant acquisition."],
["Operations","Move-ins, inspections and day-to-day coordination."],
["Housekeeping","Scheduled cleaning and reports you can follow."],
["Maintenance","Repair requests, tracked and followed through."],
["Owner support","A point of contact for your property."],
["Spacify & AI","Tenancy, billing and service records, connected."]
];return El(c.jsx("section",{id:"why-belive",className:"why-section section-light bf-brand",children:c.jsxs("div",{className:"container",children:[
c.jsxs("div",{className:"bf-brand-top",children:[c.jsx(ne,{children:"THIS IS BELIVE"}),c.jsx("img",{src:Se+"logo.webp",width:120,height:39,alt:"BeLive"})]}),
c.jsxs("div",{className:"bf-team-hero",children:[c.jsxs("div",{className:"bf-scale",children:[c.jsx("strong",{children:"4,500"}),c.jsx("span",{className:"bf-scale-label",children:"rooms under management"}),c.jsx("h2",{children:c.jsx("em",{children:"One complete team."})}),c.jsx("p",{children:"You own the property. We take care of the everyday."}),c.jsxs("a",{href:"#team-functions",className:"text-link",children:["Explore your team ",c.jsx(Cs,{size:18})]})]}),c.jsxs("figure",{className:"bf-team-photo",children:[c.jsx("img",{src:Se+"team.webp",alt:"The BeLive team at a company gathering",loading:"lazy",width:1200,height:800}),c.jsxs("figcaption",{children:[c.jsx("span",{className:"bf-photo-dot","aria-hidden":true}),"Your team, behind the scenes."]})]})]}),
c.jsxs("div",{id:"team-functions",className:"bf-team-functions",children:[c.jsx("div",{className:"bf-role-grid",role:"group","aria-label":"Select a team function",children:roles.map((r,i)=>c.jsxs("button",{type:"button","aria-pressed":active===i,"aria-controls":"bf-role-description",onClick:()=>setActive(i),children:[c.jsx(BeFreeTeamIcon,{index:i}),c.jsx("span",{children:r[0]})]},r[0]))}),c.jsxs("div",{id:"bf-role-description",className:"bf-role-description","aria-live":"polite",children:[c.jsx("strong",{children:roles[active][0]}),c.jsx("span",{children:roles[active][1]})]})]}),
c.jsxs("div",{className:"bf-review-banner",children:[c.jsxs("div",{className:"bf-google-source",children:[c.jsx("img",{className:"bf-google-logo",src:Se+"google-wordmark.png",alt:"Google",width:136,height:46,loading:"lazy"}),c.jsx("span",{children:"Reviews on Google"})]}),c.jsxs("div",{className:"bf-review-message",children:[c.jsx("h3",{children:"Real experiences."}),c.jsx("p",{children:"Read them for yourself."})]}),c.jsxs("div",{className:"bf-review-numbers",children:[c.jsxs("div",{children:[c.jsxs("strong",{children:["4.7",c.jsx("small",{children:"/5"})]}),c.jsxs("span",{children:["2,000+ ","reviews"]})]}),c.jsx("small",{children:"Company-profile snapshot · not live"})]}),c.jsxs("a",{href:"https://maps.app.goo.gl/Z5yyBCq8m8SkzWN36",target:"_blank",rel:"noopener noreferrer",className:"bf-review-link",children:["Read reviews",c.jsx(Ue,{size:18})]})]}),
c.jsxs("div",{className:"bf-partner-header",children:[c.jsx(ne,{children:"SELECTED COLLABORATIONS"}),c.jsx("h3",{children:"Our network. Your advantage."})]}),c.jsx("div",{className:"partner-grid bf-partner-grid",children:Q0.map(([p,n])=>c.jsx("div",{className:"partner-tile",children:c.jsx("img",{src:Se+p,alt:n+" logo",title:n,loading:"lazy"})},n))}),
c.jsxs("details",{className:"source-note bf-credentials",children:[c.jsxs("summary",{children:["About the numbers",c.jsx(w0,{size:16})]}),c.jsx("p",{children:"4,500 rooms is BeLive’s company-wide management figure supplied by Keith on 22 September 2026. The case-study figures below cover only eight properties. The 4.7/5 and 2,000+ review figures are retained from BeLive’s original company-profile template; their original verification date was not supplied. Check Google for the latest. Collaboration logos do not imply endorsement of rental returns."})]})
]})}))}
function F0(){return El(c.jsx("section",{id:"performance",className:"evidence section-light bf-evidence",children:c.jsxs("div",{className:"container",children:[
c.jsxs("div",{className:"bf-performance-heading",children:[c.jsxs("h2",{children:["The work. ",c.jsx("em",{children:"In numbers."})]}),c.jsx("p",{className:"bf-study-scope",children:"Eight-property case study · 15–18 Sep 2026"})]}),
c.jsxs("div",{className:"bf-results-grid",children:[
c.jsxs("article",{className:"bf-result bf-result-occupancy",children:[c.jsx("span",{className:"proof-label",children:"Sep occupancy*"}),c.jsxs("strong",{children:["95.5",c.jsx("span",{children:"%"})]}),c.jsx("p",{children:"Monthly tenancy coverage"})]}),
c.jsxs("article",{className:"bf-result",children:[c.jsx("span",{className:"proof-label",children:"2026 renewals"}),c.jsxs("strong",{children:["57.3",c.jsx("span",{children:"%"})]}),c.jsx("p",{children:"Of contracts expiring in 2026"})]}),
c.jsxs("article",{className:"bf-result bf-result-rent",children:[c.jsx("span",{className:"proof-label",children:"Highest monthly unit rent"}),c.jsxs("strong",{children:[c.jsx("span",{children:"RM"}),"5,750"]}),c.jsx("p",{children:"Gross, before costs. Individual maximum."}),c.jsx("small",{children:"Not a typical or guaranteed return."})]})]}),
c.jsx("p",{className:"bf-result-note",children:"*September is partial. Tenancy coverage, not occupied nights. Case study only, not all 4,500 rooms."}),
c.jsxs("details",{className:"source-note bf-basis",children:[c.jsxs("summary",{children:["See the basis",c.jsx(w0,{size:16})]}),c.jsx("p",{children:"Source: portfolio report, 15–18 September 2026. Occupancy: 856/896 rooms with a tenancy covering at least one day in September. Renewals: 57.3% of 1,019 expiring contracts, using linked renewals or a new contract within 31 days. Highest unit rent: RM5,750 in combined contracted monthly room rents, before costs, excluding parking and other charges. Results vary by property."})]}),c.jsxs($l,{className:"text-link bf-results-link",children:["What could your property do? ",c.jsx(Ue,{size:18})]})
]})}))}
function $0(){return El(c.jsx("section",{id:"zero-management-fee",className:"zero-fee bf-zero",children:c.jsxs("div",{className:"container",children:[c.jsxs("div",{className:"fee-grid",children:[c.jsxs("div",{className:"fee-number",children:["0",c.jsx("span",{children:"%"}),c.jsx("strong",{children:"Management fee."})]}),c.jsxs("div",{className:"fee-message",children:[c.jsxs("h2",{children:["More of your rental.",c.jsx("br",{}),c.jsx("em",{children:"More of your life."})]}),c.jsx("p",{children:"A whole team behind your property. No percentage-based management fee."}),c.jsxs($l,{className:"fee-button",children:["Show me the 0% management fee package ",c.jsx(Ue,{size:18})]}),c.jsx("small",{className:"bf-fee-terms",children:"Other service charges and package terms apply."})]})]}),c.jsxs("details",{id:"fee-explained",className:"bf-fee-details",children:[c.jsxs("summary",{children:["How 0% works",c.jsx(w0,{size:19})]}),c.jsx("div",{className:"fee-reasons",children:[
["01","A clear service package.","Marketing, cleaning and system services are priced separately in your quotation."],
["02","Technology does the repetitive work.","AI follows up. Spacify connects the records. Our people take action."],
["03","A real team follows through.","Tenant finding, property care and owner support. Working together."]
].map(([n,h,p])=>c.jsxs("article",{children:[c.jsx("span",{children:n}),c.jsx("h4",{children:h}),c.jsx("p",{children:p})]},n))})]})]})}))}
'''
    s=js.index('function F0()');e=js.index('function P0()',s)
    js=js[:s]+brand+js[e:]
    s=js.index('c.jsx("section",{id:"why-belive",className:"why-section section-light"');e=js.index(',c.jsx("section",{id:"owner-story"',s)
    js=js[:s]+js[e+1:]
    js=js.replace('c.jsx(F0,{}),c.jsx($0,{})','c.jsx(BeFreeBrand,{}),c.jsx(F0,{}),c.jsx($0,{})',1)
    js=js.replace('href:"#care-system",className:"round-link"','href:"#why-belive",className:"round-link"')
    js=js.replace('c.jsx("p",{className:"intro-last",children:""}),','')
    js=js.replace('c.jsxs("p",{children:["",c.jsx("br",{}),""]})','null')
    js=js.replace('c.jsx("p",{className:"intro-last",children:""})','null')
    js_path.write_text(js)
style=(root/'scripts/visual-introduction.css').read_text()
css=css_path.read_text()
if marker in css:css=css[:css.index(marker)]
css+='\n'+marker+'\n'+style
css_path.write_text(css)
logo=public/'assets/google-wordmark.png'
if not logo.exists():
    url='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
    request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    content=urllib.request.urlopen(request,timeout=30).read()
    if not content.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Invalid Google PNG asset')
    logo.write_bytes(content)
# Same React application in the normal and single-file previews. No font binaries.
js=js_path.read_text();html=(public/'index.html').read_text();assets={}
for p in sorted((public/'assets').iterdir()):
    mime={'.png':'image/png','.webp':'image/webp','.jpg':'image/jpeg','.jpeg':'image/jpeg'}.get(p.suffix.lower())
    if mime:assets['./assets/'+p.name]='data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
bridge='const __BEFREE_IMAGES='+json.dumps(assets,separators=(',',':'))+';for(const key of ["jsx","jsxs"]){const render=c[key];c[key]=function(type,props,...args){if(props&&typeof props.src==="string"&&__BEFREE_IMAGES[props.src])props={...props,src:__BEFREE_IMAGES[props.src]};return render(type,props,...args)}};'
inline=js.replace('const J0=',bridge+'const J0=',1)
inline=inline.replace('V.src="./analytics.js"','V.text='+json.dumps((public/'analytics.js').read_text()))
standalone=re.sub(r'<script type="module"[^>]*></script>',lambda _:'<script type="module">'+inline.replace('</script','<\\/script')+'</script>',html)
standalone=re.sub(r'<link rel="stylesheet"[^>]*>',lambda _:'<style>'+css+'</style>',standalone)
standalone=standalone.replace('href="./assets/logo.webp"','href="'+assets['./assets/logo.webp']+'"')
(root/'index.html').write_text(standalone)
meta={'version':'visual-introduction-v2','company_rooms_under_management':4500,'company_scale_source':'Explicit figure supplied by Keith on 22 September 2026; not inferred from the eight-property report','performance_scope':'Eight-property case study only, separate from company-wide scale','removed_cards':['2278 tenants','896 rooms'],'review_display':'Original company-profile snapshot, not live; source verification date unavailable','google_logo_source':'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png','google_usage_guidance':'https://partnermarketinghub.withgoogle.com/brands/google/use-cases/customer-reviews/','changes':['Real team photo and six interactive functions','Google wordmark linking to the existing Maps listing','Three compact results cards with visible scope','Expandable methodology and fee explanation','Shortened service, introduction and testimonial copy'],'original_MVertica_modified':False}
(root/'docs/visual-introduction-v2.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
readme=root/'README.md'
if readme.exists():
    text=readme.read_text()
    if '## Visual-first revision' not in text:readme.write_text(text+'\n\n## Visual-first revision\n\nThe introduction now shows **4,500 rooms under management**, a company-wide figure explicitly supplied by Keith on 22 September 2026. It is not derived from the eight-property report. The 2,278-tenants and 896-rooms promotional cards were removed. Case-study performance remains separately labelled. A real team photo, six interactive team functions and an unmodified Google wordmark replace text-heavy introductory blocks. Review figures remain an explicitly labelled non-live company-profile snapshot. Run `python scripts/refine-introduction.py` after `scripts/create-portfolio.py` to reproduce this revision.\n')
print(json.dumps({'status':'refined','version':2,'standalone_bytes':len(standalone.encode()),'company_rooms':4500}))
