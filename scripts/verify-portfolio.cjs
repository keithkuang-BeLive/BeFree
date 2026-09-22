const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const root = path.resolve('.');
const mime = {'.html':'text/html','.js':'application/javascript','.css':'text/css','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.ttf':'font/ttf','.json':'application/json'};
const server = http.createServer((req,res) => {
  let pathname = decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  if(pathname.endsWith('/')) pathname += 'index.html';
  const filename = path.resolve(root, '.' + pathname);
  if(!filename.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
  fs.readFile(filename,(err,data)=> { if(err){res.writeHead(404).end('Not found');return;}res.writeHead(200,{'Content-Type':mime[path.extname(filename)] || 'application/octet-stream'}).end(data); });
});
(async()=>{
 await new Promise(r=>server.listen(4173,'127.0.0.1',r));
 const browser=await chromium.launch({headless:true});
 const report={status:'running',checks:[],scenarios:[],messagesSent:0,videoPlaybackTested:false};
 const check=(name,pass,detail)=>report.checks.push({name,pass:!!pass,detail});
 fs.mkdirSync('verification',{recursive:true});
 try {
  for(const standalone of [false,true]) for(const width of [390,1440]) for(const lang of ['en','zh','ms']) {
   const ctx=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
   // Video playback is excluded. No messages, forms or WhatsApp tabs are submitted.
   await ctx.route(/youtube\.com|youtube-nocookie\.com/,r=>r.abort());
   const page=await ctx.newPage(); const errors=[],localFailures=[];
   page.on('pageerror',e=>errors.push(e.message));
   page.on('response',r=>{if(r.url().startsWith('http://127.0.0.1')&&r.status()>=400)localFailures.push(r.url());});
   const label=`${standalone?'single-file':'website'}-${lang}-${width}`;
   await page.goto(`http://127.0.0.1:4173/${standalone?'index.html':'public/index.html'}?lang=${lang}`,{waitUntil:'domcontentloaded'});
   await page.locator('h1').waitFor();
   await page.evaluate(()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');});
   await page.waitForFunction(()=>[...document.images].every(i=>i.complete),null,{timeout:45000});
   const text=await page.locator('body').innerText();
   check(label+' title', (await page.title()).includes('BeFree'), await page.title());
   check(label+' no condo-specific visible text',!(/M Vertica|Taman Maluri|AraTre|Azure Residence|Rica Residence|Nexus Residence|Austin Regency|Bora Residence|Medini Signature/i.test(text)));
   check(label+' portfolio metrics', ['95.5','57.3','2,278','896','195','RM5,750'].every(s=>text.includes(s)));
   check(label+' no old performance numbers',!(/93\.9|97\.5|RM4,300|114 room|22 days|80 active/.test(await page.locator('#performance').innerText())));
   check(label+' no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   const images=await page.evaluate(()=>[...document.images].map(i=>({alt:i.alt,loaded:i.complete&&i.naturalWidth>0})));
   check(label+' all images load',images.every(i=>i.loaded),images.length);
   const anchors=await page.locator('a[href^="#"]').evaluateAll(a=>a.map(e=>({href:e.getAttribute('href'),exists:!!document.querySelector(e.getAttribute('href'))})));
   check(label+' all in-page links have targets',anchors.every(a=>a.exists));
   const wa=await page.locator('a[href*="wa.me"]').evaluateAll(a=>a.map(e=>e.href));
   check(label+' WhatsApp links use correct number and generic text',wa.length>=6&&wa.every(a=>a.startsWith('https://wa.me/601110854123?text=')&&!/M Vertica|Taman Maluri/i.test(decodeURIComponent(a))),wa.length);
   for(let i=0;i<3;i++){
    const tab=page.locator('.support-tabs [role="tab"]').nth(i);await tab.click();
    check(label+' support tab '+i,await tab.getAttribute('aria-selected')==='true');
   }
   const carousel=page.locator('.carousel-controls');
   if(await carousel.isVisible()){
    await carousel.locator('button').nth(1).click();
    check(label+' carousel next',(await carousel.innerText()).includes('02 / 02'));
    await carousel.locator('button').nth(0).click();
    check(label+' carousel previous',(await carousel.innerText()).includes('01 / 02'));
   }
   if(width===390){
    await page.evaluate(()=>window.scrollTo(0,0));await page.locator('.mobile-menu').click();
    check(label+' menu opens',await page.locator('.mobile-menu').getAttribute('aria-expanded')==='true');
    await page.locator('#site-navigation a[href="#performance"]').click();
    check(label+' menu closes after navigation',await page.locator('.mobile-menu').getAttribute('aria-expanded')==='false');
   }
   await page.locator('.language-picker select').selectOption(lang==='en'?'zh':'en');
   check(label+' language switch',await page.locator('.site-shell').getAttribute('data-language')===(lang==='en'?'zh':'en'));
   await page.locator('.language-picker select').selectOption(lang);
   check(label+' JavaScript errors',errors.length===0,errors);
   check(label+' local resource errors',localFailures.length===0,localFailures);
   await page.evaluate(()=>window.scrollTo(0,0));await page.waitForTimeout(300);
   await page.screenshot({path:`verification/${label}-hero.png`});
   await page.locator('#performance').screenshot({path:`verification/${label}-results.png`});
   if(lang==='en'&&!standalone)await page.screenshot({path:`verification/${label}-full.png`,fullPage:true});
   report.scenarios.push({label,images:images.length,whatsappLinks:wa.length,errors,localFailures});
   await ctx.close();
  }
 } finally {
  await browser.close();server.close();
  report.passed=report.checks.filter(c=>c.pass).length;report.failed=report.checks.filter(c=>!c.pass).length;report.status=report.failed?'failed':'passed';
  fs.writeFileSync('verification/browser-report.json',JSON.stringify(report,null,2));
  console.log(JSON.stringify({status:report.status,passed:report.passed,failed:report.failed,failures:report.checks.filter(c=>!c.pass)}));
 }
 if(report.failed)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
