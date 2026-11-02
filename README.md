# Sourcewell | Digital Procurement Experience

**An importable, publishable Node.js web-app source project** for Google AI Studio Build/GitHub import and standard Node/Cloud Run hosting.

## Start / publish

- Node.js 20+ installed. No external runtime packages.
- Run `npm start` (or `node server.mjs`).
- Open http://localhost:8080.
- On Cloud Run or an AI Studio compatible Node host, the app automatically listens on `0.0.0.0:$PORT`.
- `Dockerfile` is provided for portable container deployments.
- No Python launcher required. No API key required.

## Google AI Studio importing

AI Studio Build officially supports **Import from GitHub**. Extract this project, add these files to your private GitHub repository, then in Google AI Studio Build choose `+` -> `Import from GitHub`. Review in Preview, then Publish. In some account experiences, uploading a ZIP to the prompt can be used as source context but that is not a guaranteed one-click project import. Follow `GOOGLE_AI_STUDIO_SETUP.md` to avoid that problem.

## Branding

- Application header, login, title and favicon use **Sourcewell** branding.
- Logo `assets/sourcewell_rfp_logo.jpg` was directly extracted from Sourcewell's buyer RFP, not generated or repainted.
- No Oracle logo, PCL logo or Town of New Tecumseth logo in UI.
- Sourcewell name/logo is used to personalize an **independent, hypothetical vendor demonstration**, not to claim Sourcewell operated, approved, contracted or endorsed it.

## Interactive workflows

Six profiles: Requester, Department Approver, Procurement Officer, Supplier, Finance / Accounts Payable, Platform Admin. Each role receives different dashboard, side navigation and access controls. Synthetic request-to-pay sequence: cart -> requisition -> approval -> purchase order -> supplier acknowledgment/shipping -> goods receipt -> invoice -> three-way matching -> payment posting -> reporting. Contracts, catalog, sellers, budgets, policies, taxes, and exports are editable and connected.

## Data, security & limitations

- Browser localStorage persists data **on one browser and device**; other users/browsers do not share data.
- Role login and the SSO button are explicitly **simulated**. There is no backend identity provider or secure authenticated production role enforcement.
- ERP, shipping, payments, suppliers, prices and stock are fictional simulations only.
- It is a demo prototype, not a certified production procurement platform or evidence of commercial eligibility, authorized distributors, live catalogs, or awarded Sourcewell contracts.
- For production use add real auth, server database, secure authorization, integrations, accessible audit storage, verification and monitoring.
- For a clean walkthrough, switch to Administrator -> Audit & exports -> Reset demo data.

## Files

- `index.html`, `app.js`, `styles.css`: fully working browser UI
- `server.mjs`: zero-dependency Node server, supports Cloud Run `$PORT`
- `package.json`, `Dockerfile`: executable deploy project
- `GOOGLE_AI_STUDIO_SETUP.md`: supported import instructions
- `DEMO_SCRIPT_10_MINUTES.md`: short buyer demo talk track
- `tests/`, `qa/`: test harness and verification results
