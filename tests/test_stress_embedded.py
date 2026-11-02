"""Deterministic browser-JS stress / negative-path assertions; no network calls.
Run python tests/test_stress.py (Playwright and Chromium required)."""
import os,json
from playwright.sync_api import sync_playwright
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
HTML=open(os.path.join(ROOT,'index.html'),encoding='utf8').read()
CSS=open(os.path.join(ROOT,'styles.css'),encoding='utf8').read()
JS=open(os.path.join(ROOT,'app.js'),encoding='utf8').read()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page()
 page.evaluate("""()=>{let m={},s={};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>m[k]??null,setItem:(k,v)=>m[k]=String(v),removeItem:k=>delete m[k]}});Object.defineProperty(window,'sessionStorage',{configurable:true,value:{getItem:k=>s[k]??null,setItem:(k,v)=>s[k]=String(v),removeItem:k=>delete s[k]}})}""")
 page.set_content(HTML);page.add_style_tag(content=CSS);page.add_script_tag(content=JS)
 errors=[]
 page.on('pageerror',lambda x:errors.append(str(x)))
 result=page.evaluate("""()=>{
    function as(r){role=r;sessionStorage.setItem(LOGIN,r);render()}
    function fd(o){let x=new FormData();Object.entries(o).forEach(([k,v])=>x.append(k,String(v)));return x}
    function assert(x,m){if(!x)throw Error(m)}
    const baseline={requests:db.requisitions.length,orders:db.orders.length,invoices:db.invoices.length};
    // Process 35 real UI-action requests, manager decisions, supplier-order generation.
    let ids=[];for(let i=0;i<35;i++){
      as('requester');db.cart=[{product:'P1',qty:1}];useForm('requisition-submit',fd({department:'DEP-100',purpose:'Stress procurement '+i,notes:'Automated stress scenario'}));
      let r=db.requisitions[0];assert(r.status==='Pending approval','request not submitted');ids.push(r.id);
      as('approver');run('approve',r.id);assert(r.status==='Approved','manager review failed');
      as('procurement');run('create-po',r.id);assert(r.status==='Ordered','PO issue failed');
    }
    assert(db.requisitions.length===baseline.requests+35,'request count');
    assert(db.orders.length===baseline.orders+35,'order count');
    let purchaseOrders=db.orders.filter(x=>ids.includes(x.request));
    for(let i=0;i<15;i++){
      let po=purchaseOrders[i];as('supplier');run('po-accept',po.id);assert(po.status==='Accepted','supplier acknowledgment');
      useForm('po-ship',fd({id:po.id,carrier:'Synthetic Carrier',tracking:'TRACK-STRESS-'+i,shipCost:0}));assert(po.status==='Shipped','shipment');
      as('procurement');useForm('po-receive',fd({id:po.id,qty:1,note:'Accepted'}));assert(po.status==='Received','goods receipt');
      as('supplier');useForm('invoice-new',fd({po:po.id,number:'STRESS-INV-'+i,amount:po.total}));
      let inv=db.invoices[0];assert(inv.po===po.id,'invoice link');
      as('finance');run('invoice-match',inv.id);assert(inv.status==='Matched','3-way match');run('invoice-pay',inv.id);assert(inv.status==='Paid'&&po.paid,'AP posting');
    }
    assert(db.invoices.length===baseline.invoices+15,'invoice count');
    const denial=db.requisitions.find(x=>x.id==='REQ-1001');as('requester');run('approve',denial.id);assert(denial.status==='Pending approval','requester unauthorized approve');
    const unauthorizedPo=purchaseOrders[15];as('finance');run('po-accept',unauthorizedPo.id);assert(unauthorizedPo.status==='Issued','finance unauthorized supplier action');
    // Invalid stock and value checks.
    as('requester');db.cart=[{product:'P1',qty:999}];let oldN=db.requisitions.length;useForm('requisition-submit',fd({department:'DEP-100',purpose:'Over budget'}));assert(db.requisitions.length===oldN,'overbudget was not blocked');
    // Wrong-price invoice must fail match; correcting it must be possible.
    let mismatched=purchaseOrders[16];as('supplier');run('po-accept',mismatched.id);useForm('po-ship',fd({id:mismatched.id,carrier:'Demo',tracking:'X-16',shipCost:0}));
    as('procurement');useForm('po-receive',fd({id:mismatched.id,qty:1,note:'Good'}));
    as('supplier');useForm('invoice-new',fd({po:mismatched.id,number:'BAD-INV',amount:mismatched.total+17}));let iv=db.invoices[0];
    as('finance');run('invoice-match',iv.id);assert(iv.status==='Mismatch','mismatch was not flagged');run('invoice-pay',iv.id);assert(iv.status==='Mismatch','mismatch invoice should not be paid');
    useForm('invoice-edit',fd({id:iv.id,number:'CORRECTED-INV',amount:mismatched.total}));run('invoice-match',iv.id);assert(iv.status==='Matched','correction not matched');
    // HTML injection is neutralized in rendered user data.
    as('procurement');useForm('product-add',fd({name:'<img id=evil src=x onerror=alert(1)>',sku:'INJECT-001',category:'Office supplies',supplier:'S1',price:2,unit:'each',stock:4}));
    assert(document.querySelector('#evil')===null,'unsafe HTML rendered in UI');
    // Product price changes do not rewrite past requisition or PO values.
    let historical=purchaseOrders[0],previous=historical.items[0].price;let first=db.products.find(x=>x.id==='P1');
    as('procurement');useForm('product-edit',fd({id:'P1',name:first.name,sku:first.sku,category:first.category,supplier:first.supplier,price:999,unit:first.unit,stock:20}));
    assert(historical.items[0].price===previous,'historical price snapshot mutated');
    // Supplier, contract, finance, tax and user controls.
    useForm('supplier-new',fd({name:'Stress Sample Seller',category:'Safety & PPE',region:'Fictional',contact:'stress@example.invalid',diversity:'Unverified'}));
    let lastSupplier=db.suppliers[0];assert(lastSupplier.status==='Pending','new seller must be reviewed');run('supplier-toggle',lastSupplier.id);assert(lastSupplier.status==='Approved','seller activation');
    useForm('contract-new',fd({name:'Stress Test Contract',supplier:lastSupplier.id,ceiling:15000,expires:'2028-12-31',status:'Active',terms:'Illustrative'}));assert(db.contracts[0].name==='Stress Test Contract','contract creation');
    as('finance');useForm('budget-edit',fd({id:'DEP-200',limit:82000,reason:'Stress test allocation'}));assert(byid('budgets','DEP-200').limit===82000,'budget update');
    as('admin');useForm('tax-new',fd({entity:'Sample',certificate:'DEMO-NEW-CERT',expiry:'2028-11-30'}));assert(db.tax[0].status==='Needs validation','certificate defaults unverified');
    run('user-toggle','supplier');assert(!byid('users','supplier').enabled,'disable user');as('admin');run('user-toggle','supplier');assert(byid('users','supplier').enabled,'restore user');
    const logs=db.audit.length,unique=new Set(db.audit.map(a=>a.id));assert(unique.size===logs,'duplicate audit IDs');
    return {created_requests:35,created_orders:35,completed_payments:15,rejected_mismatch:true,blocked_unauthorized:true,blocked_budget_excess:true,price_snapshot:true,html_escaped:true,unique_audit_events:logs,catalog_items:db.products.length,registered_suppliers:db.suppliers.length,contracts:db.contracts.length,invoice_count:db.invoices.length};
  }""")
 print(json.dumps(result,indent=2))
 assert not errors,errors
 os.makedirs(os.path.join(ROOT,'qa'),exist_ok=True)
 with open(os.path.join(ROOT,'qa','stress_results.json'),'w') as f:json.dump({'summary':result,'js_errors':errors},f,indent=2)
 browser.close()
