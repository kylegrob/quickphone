// Uses the bundled Node runtime, Playwright/Edge and pdf-lib.
const {chromium}=require('playwright');
const {PDFDocument}=require('pdf-lib');
const fs=require('fs/promises'),path=require('path'),{pathToFileURL}=require('url');
const root=path.resolve(__dirname,'../..'),src=__dirname;
const out=path.join(root,'.planning-review');
async function saveImage(source,target){
 try {await fs.writeFile(target,await fs.readFile(source));}
 catch(error){
  // Some managed Windows folders reject Node overwrite while permitting Python.
  const py=process.env.QP_BUNDLED_PYTHON||path.resolve(path.dirname(process.execPath),'../../python/python.exe');
  require('child_process').execFileSync(py,['-c','from pathlib import Path; import sys; Path(sys.argv[2]).write_bytes(Path(sys.argv[1]).read_bytes())',source,target]);
 }
}

(async()=>{
 await fs.mkdir(out,{recursive:true});
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});
 async function render(file,query,name,pdf){
  const errs=[];const err=e=>errs.push(e.message);page.on('pageerror',err);
  await page.goto(pathToFileURL(path.join(src,file)).href+'?'+query);
  await page.waitForFunction(()=>document.title==='done'||document.querySelector('pre'));
  if(errs.length||await page.locator('pre').count())throw Error(name+': '+errs.join(' ')+await page.locator('body').innerText());
  const svg=page.locator('svg');const box=await svg.boundingBox();
  await page.setViewportSize({width:Math.ceil(box.width),height:Math.ceil(box.height)});
  await svg.screenshot({path:path.join(out,name+'.png')});
  // Detect text outside the SVG canvas before exporting.
  const clips=await page.evaluate(()=>{const s=document.querySelector('svg'),v=s.getBoundingClientRect();return [...s.querySelectorAll('text')].filter(t=>{const b=t.getBoundingClientRect();return b.right>v.right+2||b.bottom>v.bottom+2||b.left<v.left-2||b.top<v.top-2}).map(t=>t.textContent)});
  if(clips.length) console.log(name+' text outside canvas: '+JSON.stringify(clips));
  if(pdf){const bytes=await page.pdf({preferCSSPageSize:true,printBackground:true,timeout:20000});const d=await PDFDocument.load(bytes);for(const p of await pdf.copyPages(d,d.getPageIndices()))pdf.addPage(p);}
  page.off('pageerror',err);console.log('Rendered '+name);return path.join(out,name+'.png');
 }
 const dfdKeys=['context','level0','l0a','l0b','l0c','l0d','l1_1','l1_2','l1_3','l1_4','l1_5','l1_6','l1_7','l1_9'];
 for(const [v,label] of [['log','logical'],['phys','physical']]){
  const d=await PDFDocument.create();
  for(const key of [...dfdKeys,...(v==='phys'?['l1_9b']:[]),'security'])await render('dfd_slides.html',`v=${v}&d=${key}`,`${label}-dfd-${key}`,d);
  await fs.writeFile(path.join(root,`planning/diagrams/dfd/${label}-dfd-set.pdf`),await d.save());
  if(!process.argv.includes('--dfd-only')) { const e=await PDFDocument.create();
  for(const key of ['overview','full','1','2','3','4'])await render('erd_slides.html',`v=${v}&s=${key}`,`${label}-erd-${key}`,e);
  await fs.writeFile(path.join(root,`planning/diagrams/erd/${label}-erd.pdf`),await e.save()); }
 }
 if(process.argv.includes('--dfd-only')) { await browser.close();console.log('Rendered both DFD sets.');return; }
 const align=await render('dfd_slides.html','v=log&d=align','alignment');await saveImage(align,path.join(root,'planning/diagrams/dfd-erd-alignment.png'));
 const uc=await render('uc_diagram.html','','use-cases');await saveImage(uc,path.join(root,'planning/use-case-diagram.png'));
 await browser.close();console.log('Rendered four PDF sets and two PNG diagrams.');
})().catch(e=>{console.error(e);process.exit(1)});
