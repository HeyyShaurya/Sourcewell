# Sourcewell interactive UI — QA evidence

## Results (November 2, 2026)

- JavaScript syntax: `npm run check` **PASS** (`app.js`, `server.mjs`).
- Standalone Node server: **PASS** (HTTP 200 for `/`, `/app.js`, `/assets/sourcewell_rfp_logo.jpg`; `/healthz` returns `ok`).
- Interactive Chromium harness: **25 / 25 assertions PASS**, no JavaScript runtime errors. Includes role-based navigation, 45 role-scoped screens, cart, request, manager approval, PO creation, supplier shipment, receiving, invoicing, three-way matching, payment simulation, reports and exports, admin settings, product moderation, and mobile view.
- Stress and negative scenarios: **PASS**. 35 requisitions and POs, 15 paid demo invoices, unauthorized actions denied by demo client-side role checks, budget excess rejected, invoice mismatch blocked, historical PO prices retained, inserted HTML escaped.
- Branding: RFP-extracted Sourcewell logo on login and header; no old-organization or Oracle logo present in application UI. Screenshots `01_login.png` and `02_requester_dashboard.png` reviewed.

## Verification boundaries

The container browser has a restriction blocking direct localhost navigation, so Chromium application workflow tests used an isolated HTML/CSS/JS harness; separate HTTP endpoint checks verified the Node host and its static assets. This is **not** proof of a Google AI Studio publishing run or of a live deployment. Imported GitHub repository preview and Publish must be tested in the user's own AI Studio workspace. Real SSO, ERP/finance connectors, shared database, supplier identity and delivery are outside this sample app's scope.

## Repeat tests

From the project folder:

- `npm run check`
- `npm start` (or set `PORT=8766 node server.mjs`)
- `python tests/test_demo_embedded.py` and `python tests/test_stress_embedded.py` if Python Playwright and Chromium are installed.

Python is for optional test execution only; it is **not** used to run or publish the app.
