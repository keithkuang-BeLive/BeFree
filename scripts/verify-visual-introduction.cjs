// Tests never send messages, submit enquiries or play testimonial videos.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.json':'application/json'};
const output=path.resolve('verification');fs.mkdirSync(output,{recursive:true});
const report={version:'visual-introduction-v2',status:'failed',checks:[],scenarios:[],messagesSent:0,videoPlaybackTested:false};
function check(name,pass,detail){report.checks.push({name,pass:!!pass,...(detail===undefined?{}:{detail})});}
function serve(){return new Promise(resolve=>{const server=http.createServer((req,res)=>{try{const url=new URL(req.url,'http://localhost');let f=path.resolve('.'+decodeURIComponent(url.pathname));if(!f.startsWith(process.cwd()+path.sep))throw Error('outside root');if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.writeHead(200,{'Content-Type':mime[path.extname(f)]||'application/octet-stream'});res.end(fs.readFileSync(f));}catch(e){res.writeHead(404);res.end('Not found');}}).listen(0,'127.0.0.1',()=>resolve({server,url:'http://127.0.0.1:'+server.address().port}));});}
async function main(){
 const ri=process.argv.indexOf('--remote'),remote=ri>=0?process.argv[ri+1]:null;let host=null,browser=null;
 try{
  if(!remote)host=await serve();browser=await chromium.launch({headless:true});
  const variants=remote?[['public-preview',remote]]:[['website',host.url+'/public/'],['single-file',host.url+'/index.html']];
  for(const [kind,base] of variants){
   const ctx=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
   await ctx.route(/youtube\.com|youtube-nocookie\.com/,r=>r.abort());
   await ctx.route(/wa\.me|api\.whatsapp\.com/,r=>r.abort());
   const page=await ctx.newPage(),errors=[],failures=[];
   page.on('pageerror',e=>errors.push(e.message));
   page.on('response',r=>{if(r.status()>=400&&r.url().startsWith(host?.url||new URL(base).origin))failures.push({url:r.url(),status:r.status()});});
   const target=new URL(base);target.searchParams.set('lang','en');
   const response=await page.goto(target.href,{waitUntil:'domcontentloaded',timeout:90000});
   check(kind+' HTTP response',response.ok(),response.status());
   if(remote&&(await page.title()).includes('External Content Notice')){report.firstVisitNotice=true;await page.getByText('Open the page',{exact:true}).click();}
   await page.locator('.bf-brand').waitFor({timeout:90000});
   if(remote){report.previewUrl=remote;report.openedUrl=page.url();}
   for(const width of [1440,390,320])for(const lang of ['en','zh','ms']){
    const label=`${kind}-${lang}-${width}`;await page.setViewportSize({width,height:900});
    await page.locator('.language-picker select').selectOption(lang);
    await page.waitForFunction(l=>document.querySelector('.site-shell')?.dataset.language===l,lang);
    await page.evaluate(()=>document.querySelectorAll('img').forEach(i=>i.loading='eager'));
    await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0),null,{timeout:45000});
    const text=await page.locator('body').innerText();
    check(label+' company rooms',text.includes('4,500'));
    check(label+' removed old promotional cards',!text.includes('2,278')&&!text.includes('195')&&await page.locator('.marketing-proof').count()===0);
    check(label+' exactly one company introduction',await page.locator('#why-belive').count()===1);
    check(label+' only three case-study cards',await page.locator('.bf-result').count()===3);
    check(label+' case-study metrics retained',['95.5','57.3','5,750'].every(x=>text.includes(x)));
    check(label+' no horizontal overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
    check(label+' all images load',await page.locator('img').evaluateAll(imgs=>imgs.every(i=>i.complete&&i.naturalWidth>0)),await page.locator('img').count());
    check(label+' Google original wordmark',await page.locator('img.bf-google-logo').evaluate(i=>i.alt==='Google'&&i.naturalWidth>0));
    check(label+' Google review destination',await page.locator('.bf-review-link').getAttribute('href')==='https://maps.app.goo.gl/Z5yyBCq8m8SkzWN36');
    check(label+' Google no decorative rating stars',!/[★☆⭐]/u.test(await page.locator('.bf-review-banner').innerText()));
    check(label+' review snapshot qualifier visible',await page.locator('.bf-review-numbers>small').isVisible());
    check(label+' case-study scope visible',await page.locator('.bf-study-scope').isVisible()&&await page.locator('.bf-result-note').isVisible());
    check(label+' fee qualification visible',await page.locator('.bf-fee-terms').isVisible());
    check(label+' method collapsed initially',!(await page.locator('.bf-basis').evaluate(d=>d.open)));
    await page.locator('.bf-basis summary').click();check(label+' method expandable',await page.locator('.bf-basis').evaluate(d=>d.open));await page.locator('.bf-basis summary').click();
    await page.locator('.bf-fee-details summary').click();check(label+' fee explanation expandable',await page.locator('.bf-fee-details').evaluate(d=>d.open));await page.locator('.bf-fee-details summary').click();
    const buttons=page.locator('.bf-role-grid button');let descriptions=new Set();
    for(let i=0;i<6;i++){await buttons.nth(i).click();await page.waitForTimeout(30);const d=await page.locator('#bf-role-description').innerText();descriptions.add(d);check(label+' role '+i,await buttons.nth(i).getAttribute('aria-pressed')==='true'&&!!d.trim());}
    check(label+' six different role descriptions',descriptions.size===6);await buttons.nth(1).click();
    const support=page.locator('.support-tabs button');for(let i=0;i<3;i++){await support.nth(i).click();check(label+' support tab '+i,await support.nth(i).getAttribute('aria-selected')==='true');}await support.nth(0).click();
    check(label+' all internal links resolve',await page.locator('a[href^="#"]').evaluateAll(as=>as.filter(a=>a.getAttribute('href').length>1).every(a=>document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1))))));
    check(label+' WhatsApp actions retain contact',await page.locator('a[href*="wa.me"]').evaluateAll(as=>as.length>=5&&as.every(a=>a.href.includes('601110854123'))));
    check(label+' no condo-specific visible text',!/(M Vertica|AraTre|Taman Maluri|Austin Regency|Nexus Residence)/i.test(text));
    if(width<700){const menu=page.locator('button.mobile-menu');await menu.click();check(label+' mobile menu opens',await menu.getAttribute('aria-expanded')==='true');await menu.click();check(label+' mobile menu closes',await menu.getAttribute('aria-expanded')==='false');}
    if(lang==='en'&&(width===1440||width===390)){
     await page.evaluate(()=>document.querySelectorAll('details').forEach(x=>x.open=false));
     await page.evaluate(()=>{for(const e of document.querySelectorAll('header,a.skip-link,.whatsapp-float,.mobile-sticky'))if(getComputedStyle(e).position==='fixed'||e.matches('a.skip-link'))e.dataset.screenshotHide='true';});
     const style=await page.addStyleTag({content:'[data-screenshot-hide="true"]{visibility:hidden!important}.reveal{opacity:1!important;transform:none!important}'});
     await page.locator('.bf-brand').screenshot({path:path.join(output,label+'-introduction.png'),animations:'disabled'});
     await page.locator('#performance').screenshot({path:path.join(output,label+'-results.png'),animations:'disabled'});
     await style.evaluate(e=>e.remove());
    }
    report.scenarios.push({label,images:await page.locator('img').count(),visibleWords:text.trim().split(/\s+/).length});
   }
   check(kind+' no JavaScript errors',errors.length===0,errors);check(kind+' no failed same-origin resources',failures.length===0,failures);await ctx.close();
  }
 }catch(e){check('verification completed',false,e.stack||e.message);}
 finally{if(browser)await browser.close();if(host)host.server.close();report.passed=report.checks.filter(c=>c.pass).length;report.failed=report.checks.filter(c=>!c.pass).length;report.status=report.failed===0?'passed':'failed';fs.writeFileSync(path.join(output,remote?'public-preview-v2.json':'browser-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,passed:report.passed,failed:report.failed,failures:report.checks.filter(c=>!c.pass),url:remote}));if(report.failed)process.exitCode=1;}
}
main();
