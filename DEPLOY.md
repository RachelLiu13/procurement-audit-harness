# Deployment guide (Part B)

When you finish, you will have a URL like `https://<name>.streamlit.app` that you can submit for Part B.
There are four steps: get an API key → push the code to GitHub → deploy on Streamlit Community Cloud → run the workflow once.

---

## Step 1: Get an Anthropic API key

The website calls Claude from the server, which needs an API key. A Claude.ai Pro or Max subscription does **not** include API usage. You have to set up the API separately.

1. Go to <https://platform.claude.com> (the Claude Console) and sign up or log in.
2. Open **Billing**, add a card and buy prepaid credits (the minimum is about US$5).
3. Recommended: under **Limits**, set a monthly spend limit such as $20, so you can't overspend by accident.
4. Open **API Keys** → **Create Key**, give it a name (for example `audit-planner`), and copy the key. It starts with `sk-ant-`.
   **The key is shown only once.** Save it in a password manager.
5. The key goes only into the Streamlit Secrets in Step 3. Never paste it into code, commit it to GitHub or share it.

> **Cost.** The default model is `claude-opus-5-5`. A demo run with "Reuse Part A's Phase 1 outputs" ticked typically costs a few dollars. A full run costs more, depending on how many turns the agents take. To spend less, add `CLAUDE_MODEL = "claude-sonnet-5-5"` to the Secrets. The app shows live token usage for each run.

## Step 2: Push the code to GitHub

1. On GitHub, click **+ → New repository**.
   - Repository name: `procurement-audit-harness`
   - Visibility: **Public**
   - Do **not** add a README. Leave the repository empty.
   - Click **Create repository**.
2. In a terminal opened in this project folder, run these commands. Replace `<your-username>` with your GitHub username:

```bash
git remote add origin https://github.com/<your-username>/procurement-audit-harness.git
```

```bash
git push -u origin main
```

   If Git asks you to log in, use your GitHub username. For the password, use a **Personal Access Token**, not your account password. To create one, go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token, and tick the `repo` scope.
   Alternative: in GitHub Desktop, choose File → Add local repository, pick this folder and click **Publish repository**.

## Step 3: Deploy on Streamlit Community Cloud (free)

1. Go to <https://share.streamlit.io>, click **Continue with GitHub**, and authorize access to your repositories.
2. Click **Create app** → **Deploy a public app from GitHub**.
3. Fill in:
   - Repository: `<your-username>/procurement-audit-harness`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: choose a name, for example `wbc-audit-planner`
4. Open **Advanced settings**:
   - Python version: **3.12**
   - In **Secrets**, paste the following and put in your key from Step 1:

```toml
ANTHROPIC_API_KEY = "sk-ant-paste-your-key-here"
APP_PASSWORD = "choose-an-access-password"
```

   `APP_PASSWORD` is optional but recommended: only people who know it can use the site and spend your API credits. When you submit, give the grader both the URL and the password.
5. Click **Deploy**. The first build takes about 3–5 minutes. It installs the Python packages in `requirements.txt` and `pdftotext` and `jq` from `packages.txt`.

To change the key later, open the app's **Settings → Secrets**, edit and save. The app restarts automatically.

## Step 4: Check the full workflow

1. Open `https://<your-name>.streamlit.app` and enter the access password.
2. The sidebar shows the model name. If you see a red "ANTHROPIC_API_KEY is not set" message, the Secrets are wrong.
3. For the first demonstration, tick **Reuse Part A's Phase 1 outputs**, then click **New run** → **Start the agents**.
   - The **Agent activity** tab shows each agent's tool calls, messages and reports live.
   - You can close the page and come back with the `?run=<id>` link. The run keeps going.
4. At **Gate 1**, choose Approve, Amend or Reject for each risk and submit. The harness then runs the risk-assessor revision, the approval gate, the planner + challenger + qa-reviewer team and the lead report.
5. At **Gate 2**, read the planning memo and review in the **Outputs** tab, then enter your name and sign off.
6. Click **Download all outputs (.zip)** to get the complete audit planning pack.
7. If time and budget allow, run the full pipeline once with Reuse unticked (rules → analytics/history → … → sign-off).

## Notes

- Free Streamlit apps go to sleep after a few days without visitors. Opening the URL and clicking "Yes, get this app back up" wakes the app. Open it yourself shortly before you submit.
- Each redeploy or restart clears the runs stored on the server (`/tmp`). Download the zip of anything you want to keep.
- **Part A example run** in the sidebar shows Part A's complete, signed-off outputs. Viewing it needs no API key.
