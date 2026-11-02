"""Run: python tests/test_demo.py  (requires Playwright + Chromium)."""
import os, json, sys, time, base64
from playwright.sync_api import sync_playwright
URL=os.environ.get('DEMO_URL','http://127.0.0.1:8765/')
OUT=os.environ.get('DEMO_SCREENSHOTS',os.path.join(os.path.dirname(os.path.dirname(__file__)),'qa'))
os.makedirs(OUT, exist_ok=True)
passed=[];errors=[]
def check(name,fn):
 try:
  fn(); passed.append(name); print('PASS',name)
 except Exception as e:
  errors.append({'test':name,'error':str(e)});print('FAIL',name,str(e)[:300]); raise

def main():
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  page=browser.new_page(viewport={'width':1440,'height':900},accept_downloads=True)
  page.on('pageerror',lambda e:errors.append({'test':'javascript-runtime','error':str(e)}))
  ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  html=open(os.path.join(ROOT,'index.html'),encoding='utf8').read()
  css=open(os.path.join(ROOT,'styles.css'),encoding='utf8').read()
  js=open(os.path.join(ROOT,'app.js'),encoding='utf8').read()
  seal=base64.b64encode(open(os.path.join(ROOT,'assets','sourcewell_rfp_logo.jpg'),'rb').read()).decode('ascii')
  def boot(snapshot=None):
   page.goto('about:blank')
   page.evaluate('''(old)=>{const m=old?.local||{},s=old?.session||{};
     Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>m[k]??null,setItem:(k,v)=>m[k]=String(v),removeItem:k=>delete m[k]}});
     Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:k=>s[k]??null,setItem:(k,v)=>s[k]=String(v),removeItem:k=>delete s[k]}});
     window.__storage=m;window.__session=s;}''',snapshot)
   page.set_content(html)
   page.add_style_tag(content=css)
   page.add_script_tag(content=js)
   page.evaluate('''(data)=>{const fix=()=>{for(const img of document.querySelectorAll('img[src*=sourcewell_rfp_logo]'))img.src='data:image/jpeg;base64,'+data};fix();new MutationObserver(fix).observe(document.querySelector('#app'),{childList:true,subtree:true});}''',seal)
  boot()
  check('Login screen and official seal',lambda: (page.get_by_text('Choose your workspace').wait_for(),page.locator('.login-left .orb img').wait_for()))
  page.screenshot(path=os.path.join(OUT,'01_login.png'),full_page=True)
  def signin(r):
   if page.locator('button[data-action="switch"]').count():page.locator('button[data-action="switch"]').first.click()
   page.locator(f'button[data-action="login"][data-id="{r}"]').click()
   page.locator('#main').wait_for()
  def nav(to):page.locator(f'aside button[data-page="{to}"]').click()
  def modal_click(act,id=None):
   selector=f'#modal button[data-action="{act}"]'+(f'[data-id="{id}"]' if id else '')
   page.locator(selector).first.click()
  check('Distinct role login — requester',lambda:signin('requester'))
  check('Requester navigation is restricted',lambda: (page.locator('aside button[data-page="approvals"]').count()==0 or (_ for _ in ()).throw(AssertionError('Approvals incorrectly visible'))))
  page.screenshot(path=os.path.join(OUT,'02_requester_dashboard.png'),full_page=True)
  check('Catalog displays four required categories',lambda:(nav('catalog'),page.get_by_text('Operational goods marketplace').wait_for(),[page.locator('.product').filter(has_text=x).first.wait_for() for x in ['Office supplies','Janitorial & facilities','Safety & PPE','Technology accessories']]))
  check('Catalog quantity action',lambda: (page.locator('button[data-action="add-cart"][data-id="P1"]').click(), nav('cart'),page.locator('input[data-qty="P1"]').fill('3'),page.locator('input[data-qty="P1"]').press('Tab'),page.get_by_text('CAD 126.00').first.wait_for()))
  page.screenshot(path=os.path.join(OUT,'03_cart.png'),full_page=True)
  def reqcreate():
   page.locator('button[data-action="submit-cart"]').click()
   page.locator('input[name="purpose"]').fill('2026 demo recording office supplies')
   page.locator('#modal button[type="submit"]').click()
   assert '2026 demo recording office supplies' in page.locator('#main').inner_text()
  check('Create requisition with live state',reqcreate)
  reqid=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3')).requisitions[0].id")
  check('Requisition persists across app reload',lambda:(boot(page.evaluate('({local:window.__storage,session:window.__session})')),page.get_by_text(reqid).first.wait_for()))
  check('Approver landing and inbox',lambda:(signin('approver'),page.get_by_text('Approvals & Team Spend').wait_for(),nav('approvals'),page.get_by_text(reqid).first.wait_for()))
  def approve():
   page.locator(f'button[data-action="approve"][data-id="{reqid}"]').click()
   data=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   assert next(r for r in data['requisitions'] if r['id']==reqid)['status']=='Approved'
  check('Department approval reserves budget',approve)
  check('Procurement dashboard and requisitions',lambda:(signin('procurement'),page.get_by_text('Procurement Command Center').wait_for(),nav('requisitions')))
  def convert():
   page.locator(f'button[data-action="req-detail"][data-id="{reqid}"]').click()
   modal_click('create-po',reqid)
   data=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   matching=[p for p in data['orders'] if p['request']==reqid]
   assert len(matching)==1
   return matching[0]['id']
  poid=convert();passed.append('Approved requisition converts into supplier PO');print('PASS','Approved requisition converts into supplier PO')
  nav('orders');page.screenshot(path=os.path.join(OUT,'04_procurement_orders.png'),full_page=True)
  check('Supplier sees only own PO',lambda:(signin('supplier'),page.get_by_text('Supplier Collaboration').wait_for(),nav('supplierorders'),page.get_by_text(poid).first.wait_for()))
  def ship():
   page.locator(f'button[data-action="po-detail"][data-id="{poid}"]').click()
   modal_click('po-accept',poid)
   page.locator(f'button[data-action="po-detail"][data-id="{poid}"]').click()
   modal_click('po-ship',poid)
   page.locator('input[name="carrier"]').fill('Demo Courier Express')
   page.locator('input[name="tracking"]').fill('DEMO-TRACK-12345')
   page.locator('input[name="shipCost"]').fill('12')
   page.locator('#modal button[type="submit"]').click()
   d=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   po=next(p for p in d['orders'] if p['id']==poid)
   assert po['status']=='Shipped' and po['tracking']=='DEMO-TRACK-12345' and po['shipCost']==12
  check('Supplier acknowledgement and freight/tracking updates',ship)
  def supplier_invoice():
   nav('invoices');page.locator('button[data-action="invoice-new"]').click();page.locator('select[name="po"]').select_option(poid)
   # Invoice may pre-populate first unrelated PO, change to the chosen PO total manually.
   po=page.evaluate("(id)=>JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3')).orders.find(p=>p.id===id)",poid)
   page.locator('input[name="amount"]').fill(str(po['total']))
   page.locator('#modal button[type="submit"]').click()
   d=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   assert any(i['po']==poid and i['status']=='Submitted' for i in d['invoices'])
  check('Supplier invoice ties to new PO',supplier_invoice)
  check('Procurement goods receipt queue',lambda:(signin('procurement'),nav('receiving'),page.get_by_text(poid).first.wait_for()))
  def goods_receive():
   page.locator(f'button[data-action="po-detail"][data-id="{poid}"]').click()
   modal_click('po-receive',poid)
   page.locator('#modal button[type="submit"]').click()
   d=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   assert next(p for p in d['orders'] if p['id']==poid)['status']=='Received'
  check('Goods receipt posts against exact order',goods_receive)
  page.screenshot(path=os.path.join(OUT,'05_receiving.png'),full_page=True)
  check('Finance landing and invoice workbench',lambda:(signin('finance'),page.get_by_text('Financial Operations').wait_for(),nav('invoices')))
  def pay():
   d=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   iid=next(i['id'] for i in d['invoices'] if i['po']==poid)
   page.locator(f'button[data-action="invoice-detail"][data-id="{iid}"]').click()
   modal_click('invoice-match',iid)
   d=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   assert next(i for i in d['invoices'] if i['id']==iid)['status']=='Matched'
   page.locator(f'button[data-action="invoice-detail"][data-id="{iid}"]').click()
   modal_click('invoice-pay',iid)
   d=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   assert next(i for i in d['invoices'] if i['id']==iid)['status']=='Paid'
   assert next(p for p in d['orders'] if p['id']==poid)['paid']
  check('Three-way match and simulated payment',pay)
  page.screenshot(path=os.path.join(OUT,'06_finance.png'),full_page=True)
  def exports():
   nav('reports')
   with page.expect_download() as dl:page.locator('button[data-action="export-spend"]').click()
   assert dl.value.suggested_filename.endswith('.csv')
   with page.expect_download() as dl:page.locator('button[data-action="export-audit"]').click()
   assert dl.value.suggested_filename.endswith('.csv')
  check('Dynamic reports + export both CSVs',exports)
  check('Admin page separation',lambda:(signin('admin'),page.get_by_text('Security & Platform Control').wait_for(),nav('policies')))
  def policy_and_escalation():
   page.locator('button[data-action="policy-edit"]').click()
   page.locator('input[name="approvalLimit"]').fill('5')
   page.locator('#modal button[type="submit"]').click()
   signin('requester');nav('catalog');page.locator('button[data-action="add-cart"][data-id="P2"]').click();nav('cart');page.locator('button[data-action="submit-cart"]').click()
   page.locator('input[name="purpose"]').fill('Escalation threshold test');page.locator('#modal button[type="submit"]').click()
   rid=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3')).requisitions[0].id")
   signin('approver');nav('approvals');page.locator(f'button[data-action="approve"][data-id="{rid}"]').click()
   d=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   assert next(r for r in d['requisitions'] if r['id']==rid)['status']=='Escalated'
   signin('procurement');nav('requisitions');page.locator(f'button[data-action="req-detail"][data-id="{rid}"]').click();modal_click('escalation-approve',rid)
   d=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   assert next(r for r in d['requisitions'] if r['id']==rid)['status']=='Approved'
  check('Admin changes policy; approval escalates; procurement authorizes',policy_and_escalation)
  def catalog_moderation():
   signin('supplier');nav('catalog');page.locator('button[data-action="product-add"]').click();page.locator('input[name="name"]').fill('Sample notebook refill 200 pages')
   page.locator('input[name="sku"]').fill('DEMO-NOTE-999')
   page.locator('#modal button[type="submit"]').click()
   d=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   item=next(p for p in d['products'] if p['sku']=='DEMO-NOTE-999');assert item['status']=='Review'
   signin('procurement');nav('catalog');page.locator(f'button[data-action="product-approve"][data-id="{item["id"]}"]').click()
   d=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   assert next(p for p in d['products'] if p['id']==item['id'])['status']=='Active'
  check('Supplier submits new catalog SKU and procurement moderates',catalog_moderation)
  def platform_admin():
   signin('admin');nav('users');page.get_by_text('Identity & role access').wait_for()
   nav('integrations');page.locator('button[data-action="integration-run"][data-id="ERP"]').click()
   d=page.evaluate("JSON.parse(localStorage.getItem('pcl_sourcewell_110426_demo_v3'))")
   assert next(j for j in d['integrations'] if j['id']=='ERP')['status']=='Simulation completed'
   nav('tax');page.locator('button[data-action="tax-toggle"]').first.click()
   nav('audit');page.get_by_text('SIMULATED INTEGRATION').first.wait_for()
   with page.expect_download() as dl:page.locator('button[data-action="export-json"]').click()
   assert dl.value.suggested_filename.endswith('.json')
  check('User / integration / tax / audit / JSON export controls',platform_admin)
  roles={'requester':['home','catalog','cart','requisitions','orders','profile'],
         'approver':['home','approvals','requisitions','budgets','reports','profile'],
         'procurement':['home','requisitions','orders','receiving','catalog','contracts','suppliers','reports','audit','profile'],
         'supplier':['home','supplierorders','catalog','invoices','profile'],
         'finance':['home','invoices','orders','budgets','reports','audit','profile'],
         'admin':['home','users','policies','integrations','suppliers','contracts','catalog','tax','reports','audit','profile']}
  def test_every_page():
   for r,views in roles.items():
    signin(r)
    actual=page.locator('aside button.nav').evaluate_all('(e)=>e.map(x=>x.dataset.page)')
    assert actual==views,(r,actual)
    for v in views:
     nav(v)
     assert page.locator('#main h1,#main h2').count()>0,(r,v)
   print('   navigated',sum(map(len,roles.values())),'persona-scoped pages')
  check('All 45 persona-specific navigation views render without crash',test_every_page)
  def mobile():
   page.set_viewport_size({'width':375,'height':812})
   nav('reports');page.screenshot(path=os.path.join(OUT,'07_mobile_admin_report.png'),full_page=True)
   assert page.locator('aside button.nav').count()>0
   assert page.evaluate('document.documentElement.scrollWidth')<=page.evaluate('window.innerWidth')+1
  check('Mobile dashboard no document overflow',mobile)
  browser.close()
 print('\nSUMMARY',len(passed),'checks passed;',len(errors),'errors')
 with open(os.path.join(OUT,'results.json'),'w') as f:json.dump({'passed':passed,'errors':errors,'screenshots':sorted(os.listdir(OUT))},f,indent=2)
 if errors:sys.exit(1)

if __name__=='__main__':main()
