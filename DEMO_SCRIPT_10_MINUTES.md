# SOURCEWELL #110426 — RECORDED PLATFORM DEMONSTRATION
## Presenter-ready, 9 min 45 sec target / 10 min maximum

**Required by Sourcewell RFP Table 6 (as clarified in Addendum 2):** record a video **not exceeding 10 minutes**. Host it at a reviewer-accessible, **non-password-protected** URL and enter that URL in the appropriate portal Table 6 field. The offline demonstration application and this script are **not** themselves a hosted recording or a portal submission.

### Prior to pressing Record (not part of video)

1. Run `START_DEMO_WINDOWS.bat` or `python -m http.server 8765`, and browse to `http://localhost:8765` at **1440×900** or **1920×1080**.
2. Log in as **Platform Administrator**, open **Audit & exports**, press **Reset all demo data**, confirm, and then use top-right **Switch persona**.
3. Prepare the following order details: **Item** `Letter copy paper · 10 reams`; **Quantity** `3`; **Cost center** `DEP-100 — Facilities & Administration`; **Purpose** `Office replenishment — Sourcewell 110426 walkthrough`; **Supplier carrier** `Sample Delivery`; **Tracking** `DEMO-SHIP-110426`; **Freight** `12.00 CAD`. These are deliberately fictional.
4. Turn off auto-updates, OS notifications, external tabs and bookmarks. Use one browser profile for all persona switches; saved data automatically follows the next role.
5. Do **not** show any real credentials or confidential customer information. Do not suggest a live Sourcewell award, confirmed goods sellers, verified tax exemption or successful external ERP/SSO integration.
6. Record in 1080p, 30 fps. Prefer a single continuous take. If editing, ensure every visible result corresponds to what the app actually did. Reserve a ~15-second margin under 10 minutes.

### 00:00–00:35 | Buyer context and simulated SSO

**On-screen:** Login / six persona tiles. Show the official Sourcewell seal taken from the buyer-provided RFP; briefly point to the **Corporate SSO — simulated** option. Click **Continue with demo SSO**, then choose **Department Requester — Amelia Brooks**.

**Narration:** “This is PCL One's Oracle-style interactive procurement demonstration aligned to Sourcewell solicitation 110426. We will follow one public-agency purchase across self-service, departmental approvals, procurement, supplier collaboration and financial control. Six separate role workspaces share one interactive set of demonstration data. Corporate single sign-on is represented here as a local simulation.”

**Visible proof:** Role-specific landing page and sidebar; not a static slide.

### 00:35–01:35 | Four required operational goods categories and catalog discovery

**On-screen:** Requester → **Shopping catalog**. Show drop-down categories one at a time: **Office supplies**, **Janitorial & facilities**, **Safety & PPE**, **Technology accessories**. Return to **Office supplies**, search `paper`, identify `Letter copy paper · 10 reams`, click **+ Add**.

**Narration:** “The requested platform experience spans the four operational-goods categories identified in Section II.B: office consumables, facility supplies, safety and PPE, and technology accessories. Users can filter a shared catalog and see an item, seller, unit of measure and illustrative price. The items shown are fictional demonstration records, not evidence of approved seller inventory or actual orderability.”

**Visible proof:** Functional filters and search; sample SKU, seller, price and product selection.

### 01:35–02:20 | Requisition and financial coding

**On-screen:** Click **My basket**. Change quantity to **3**, tab away; point to instant line total **CAD 126.00**. Click **Create purchase requisition**; choose **DEP-100**, enter purpose `Office replenishment — Sourcewell 110426 walkthrough`; submit. Show new **REQ** row with **Pending approval**.

**Narration:** “Updating a quantity immediately recalculates the request. The requester assigns a cost center, describes business need and submits. A unique requisition is created, persisted locally and routed to the responsible approver rather than bypassing policy controls.”

**Visible proof:** Basket arithmetic changes, request ID, department, status and live persistence.

### 02:20–03:05 | Role-based manager approvals

**On-screen:** Top right **Switch persona** → **Department Approver — Jordan Ellis**. Show different landing cards and shorter sidebar. Click **Approval inbox**. Locate the new request (newest at top), show its cost center, total and authority status. Click **Approve**.

**Narration:** “This manager sees approvals and departmental budgets, not the requester’s shopping navigation. The request is evaluated against the configured authority limit and budget availability. This example is within the approval ceiling; approval reserves the sample budget and changes the same transaction into an approved purchasing request. Above the ceiling, it would escalate to Procurement instead.”

**Visible proof:** Different role menu, approval status change and budget impact.

### 03:05–03:55 | Procurement converts requisition into purchase order

**On-screen:** Switch to **Procurement Officer — Taylor Morgan**. Open **Requisitions**, click **View** on the newly approved request. Show item, cost center, budget and total. Click **Issue supplier POs**. Go to **Purchase orders**; locate newest **PO**, click **Open** to show linked requisition and seller. Close dialog.

**Narration:** “An approved request is converted into supplier-specific purchase orders while retaining item-level details and traceability back to the requisition. The system checks the sample seller's status and synthetic available stock, and places a purchase commitment against the configured department.”

**Visible proof:** Requisition-to-PO lineage, vendor, quantity, monetary record and status `Issued`.

### 03:55–04:55 | Supplier acknowledgment, shipment, and invoice

**On-screen:** Switch to **Supplier Partner — Casey Reed** → **Incoming orders**. Click **Open** for the new PO → **Acknowledge order**. Reopen it → **Create shipment**. Enter **Sample Delivery**, tracking **DEMO-SHIP-110426**, freight **12**, submit. Go to **My invoices** → **Create invoice**; choose this PO (the total autofills); set reference `DEMO-INVOICE-110426`, submit. Show `Submitted`.

**Narration:** “The seller's workspace is limited to assigned orders, supplier catalog proposals and invoices. The supplier can acknowledge the order, supply a delivery tracking reference and submit an invoice for the current PO total. These visible state changes are simulated transactions; no logistics provider, inventory feed or third-party invoice gateway is contacted.”

**Visible proof:** `Accepted` → `Shipped`, tracking value, updated freight and supplier invoice reference.

### 04:55–05:40 | Buyer receiving and quantity acceptance

**On-screen:** Switch back to **Procurement Officer** → **Goods receiving**. Locate shipped PO → **Receive / inspect** → **Record receipt**. Accept **3** units, note `All 3 cases inspected and accepted`, submit; show receipt register and PO `Received`.

**Narration:** “Receiving is controlled by the buyer, rather than self-certified by the supplier. Recording accepted quantity creates a goods-receipt reference tied to the purchase order. If only part of the shipment had arrived, the order would remain partly received and the invoice would not yet pass full matching.”

**Visible proof:** Goods receipt ID, accepted quantity, status and link to the original PO.

### 05:40–06:55 | Three-way matching and payment control

**On-screen:** Switch to **Finance & Accounts Payable — Morgan Lee**. Open **AP invoices**, click **Inspect** for the new invoice, show requested amount, PO amount and accepted units. Click **Run 3-way match**; status becomes `Matched`. Reopen invoice → **Post demo payment**; show `Paid`.

**Narration:** “Finance sees a purpose-built accounts payable workspace. The three-way check compares the purchase order, goods receipt and invoice amount and also considers seller approval. Only a matched invoice can progress to a payment posting. The payment event and resulting reports are local demonstration records; no actual money is transferred.”

**Visible proof:** `Submitted` → `Matched` → `Paid`, matching counts and transaction audit events.

### 06:55–07:40 | Contract governance and seller oversight

**On-screen:** Switch to **Procurement Officer** → **Enterprise contracts**; show sample contract ceiling, utilization progress, expiry and seller. Open **Supplier directory** and show categories, fictional geography, seller approval and diversity status `Unverified`. If time permits, show **Catalog** and its updated stock.

**Narration:** “Procurement can maintain contract ceilings, supplier identities, category records, order history and seller governance together. The interface deliberately distinguishes demo-approved records from independently verified supplier authority or diversity certificates, which must be evidenced separately for the real bid.”

**Visible proof:** Contract portfolio utilization and responsible sourcing fields.

### 07:40–08:25 | Controls, tax certificates and integrations

**On-screen:** Switch to **Platform Administrator — Alex Grant**. Open **Approval policies** and show editable manager ceiling, tax simulation rate and invoice tolerance. Open **Tax exemptions** and show certificate status `Needs validation`. Open **ERP & punchout** and click **Run simulated sync** on Finance ERP connector.

**Narration:** “Administrators have a different control menu. Approval limits, financial tolerance and certificate registers are configurable, and integration jobs produce a traceable demonstration event. Corporate SSO, ERP export and punchout connectors here are simulated; production interface testing would require authorized external endpoints.”

**Visible proof:** Administrative role isolation, configurable policy and explicit simulated sync state.

### 08:25–09:20 | Analytics, audit, reporting and accountability

**On-screen:** Administrator → **Analytics**. Show committed PO value, four category coverage, category spend graph, supplier participation and locally recorded audit-event totals. Click **Export spend CSV** to trigger download. Open **Audit & exports**; show approval, PO issuance, shipment, receipt, match and payment entries; click **Export audit CSV**.

**Narration:** “As real demo entries change, analytics recalculate. The sample dashboard covers purchase commitments, category spend and seller activity. The audit trail captures who changed which demonstration record and when, while machine-readable exports can support procurement review and compliance discussions. Production data retention and regulatory compliance require independent system verification.”

**Visible proof:** Dynamic totals, current event references and actual CSV download actions.

### 09:20–09:45 | Close / handoff (leave 15-second recording margin)

**On-screen:** Return to Administrator home or Analytics and keep the Sourcewell RFP identity clearly visible. Do not open personal tabs.

**Narration:** “This end-to-end illustration connects the five proposed modules: procurement self-service, procurement management, enterprise contracts, supplier collaboration and financial management. The workflow, state transitions, controls and reports shown are interactive. For production adoption, seller authorization, real catalogs, fulfillment, certified security, tax validation and external integrations require verification through the implementation process. Thank you for reviewing our Sourcewell 110426 submission.”

**End before 09:50.** Never submit a video exceeding the buyer's 10-minute limit.

---

## Shot-list and recording QA

| Key proof | Expected visible result | If something went wrong |
|---|---|---|
| Role switch | A different landing page **and** restricted sidebar | Switch back and reselect the intended persona |
| Requisition submit | New `REQ-*` row with `Pending approval` | Check basket not empty and department budget enough |
| Approver action | `Approved` (or `Escalated` if admin threshold changed) | Use Admin → Approval policies; restore ceiling 5000; reset demo if needed |
| PO issue | New `PO-*` with same request reference | Check seller approved, stock sufficient and request already approved |
| Supplier order | Same PO visible to Sample Office Supply Co. | Make sure cart item belonged to sample seller S1 / Office supplies |
| Shipment | `Shipped`, carrier and tracking displayed | PO must be `Accepted` first and freight must fit budget |
| Receiving | `Received`, a `GR-*` record, quantity 3 | Shipment required; accept quantity no greater than outstanding |
| Invoice match | `Matched`, then `Paid` | Invoice should equal PO total including sample tax and freight; all goods must be received |
| Export | A new CSV file downloads | Check browser downloads permission; do not claim real compliance certificate |

## Short legal/presenter boundaries

Say **“Sourcewell RFP #110426”**, not **“Sourcewell-awarded contract”**. Say **“illustrative supplier”**, not **“verified goods supplier”**. Say **“simulated SSO / ERP / freight / payment”**, not **“production-integrated”**. Never imply the fictionally priced sample items are the CAD subscription/implementation pricing in the bid workbook.
