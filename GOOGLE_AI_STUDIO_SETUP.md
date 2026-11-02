# How to bring this UI into Google AI Studio and publish

## Reliable supported route: GitHub import
1. Extract the ZIP. The folder contains `package.json`, `server.mjs`, `index.html`, `app.js`, `styles.css`, `assets`, and documentation.
2. Make a **private GitHub repository** for this project, keeping this source separate from your unrelated personal projects. Upload the project files to the repository root (not one folder deeper).
3. Visit https://aistudio.google.com/ and open **Build**.
4. In the prompt input, open the **Add files (+)** menu and choose **Import from GitHub**. Choose this new repository. Grant GitHub access only to the intended repository if the consent flow offers repository selection.
5. Prompt: `Use the existing imported Node.js Sourcewell UI as the source of truth. Preserve app.js data flows, existing persona menus, styling and assets. Do not regenerate or replace the user interface. Make the app run on the standard Node host and verify preview works. Use only assets/sourcewell_rfp_logo.jpg for organization branding, no Oracle/PCL/old logo. Do not add Gemini features or require any API key.`
6. Review the **Preview**. Confirm every persona works. Use **Publish** when satisfied; your account may require eligible Starter tier or Cloud billing.

## Direct ZIP attachment route (may vary by account)
You can try attaching the ZIP as project context in a new Build app, then asking AI Studio to extract/replace files, but **the official guide documents GitHub import, not guaranteed direct ZIP-to-project importing**. Prefer the GitHub route if it does not recognize the ZIP.

## Alternative: host as-is
This ZIP is also directly runnable and deployable without Google AI Studio. Run `npm start` and open http://localhost:8080. `Dockerfile` enables direct Cloud Run container deployment.

## Demo caveats
Users and orders are synthetic, stored separately in each browser. True SSO and shared cloud database are not included. The UI is an independent presentation and does not imply Sourcewell endorsement or award.
