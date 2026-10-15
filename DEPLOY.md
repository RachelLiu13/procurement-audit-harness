# Deployment guide (Part B)

When you finish, you will have a URL like `https://<name>.vercel.app` that you can submit for Part B.

The app has two parts, deployed from the same GitHub repository:

| Part | Where | Why |
| --- | --- | --- |
| Website (`web/`) | **Vercel** (free) | The link you submit. Serves the pages and forwards `/api/*` to the agent server |
| Agent server (`server.py`) | **Render** (free) | Runs the agents. A run lasts 30–60 minutes, longer than Vercel's functions allow |

There are six steps: get an API key → push to GitHub → deploy the agent server on Render → point the website at it → deploy on Vercel → run the workflow once.

---

## Step 1: Get an Anthropic API key

The agents call Claude from the server, which needs an API key. A Claude.ai Pro or Max subscription does **not** include API usage. You have to set up the API separately.

1. Go to <https://platform.claude.com> (the Claude Console) and sign up or log in.
2. Open **Billing**, add a card and buy prepaid credits (the minimum is about US$5).
3. Recommended: under **Limits**, set a monthly spend limit such as $20.
4. Open **API Keys** → **Create Key**, name it (for example `audit-planner`), and copy the key. It starts with `sk-ant-`. **The key is shown only once**, so save it in a password manager.
5. The key goes only into Render's environment settings in Step 3. Never put it in code, commit it to GitHub or share it.

> **Cost.** The default model is `claude-opus-5-5`. A demo run with "Reuse Part A's Phase 1 outputs" ticked typically costs a few dollars. A full run costs more, depending on how many turns the agents take. To spend less, set `CLAUDE_MODEL` to `claude-sonnet-5-5` on Render. The site shows live token usage for each run.

## Step 2: Push the code to GitHub

1. On GitHub, click **+ → New repository**. Name it `procurement-audit-harness`, choose **Public**, do **not** add a README, and click **Create repository**.
2. In a terminal opened in this project folder, run these commands. Replace `<your-username>` with your GitHub username:

```bash
git remote add origin https://github.com/<your-username>/procurement-audit-harness.git
```

```bash
git push -u origin main
```

   If Git asks you to log in, enter your GitHub username. For the password, use a **Personal Access Token**: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token, with the `repo` scope.
   Alternative: in GitHub Desktop, choose File → Add local repository, pick this folder and click **Publish repository**.

## Step 3: Deploy the agent server on Render

1. Go to <https://render.com> and sign up with **GitHub**.
2. Click **New +** → **Blueprint**, connect your GitHub account if asked, and select the `procurement-audit-harness` repository. Render reads `render.yaml` and proposes a free web service called `audit-planner-api`.
3. Render asks for the values that are not in the file:
   - `ANTHROPIC_API_KEY`: your key from Step 1
   - `APP_PASSWORD`: an access password you choose. Visitors must enter it, so strangers can't spend your credits. Give it to your grader with the URL.
4. Click **Apply**. The first build installs Python, `pdftotext` and the packages, and takes about 5–10 minutes.
5. When the service shows **Live**, copy its URL from the top of the service page, for example `https://audit-planner-api-xxxx.onrender.com`.
   Check it by opening `https://audit-planner-api-xxxx.onrender.com/api/health` in your browser. You should see `{"ok":true,"key_configured":true,...}`.

To change a setting later, go to the service → **Environment**, edit it and save. Render redeploys automatically.

## Step 4: Point the website at the agent server

1. On GitHub, open your repository, then `web/vercel.json`, and click the pencil icon (Edit).
2. Replace `https://REPLACE-WITH-YOUR-RENDER-URL.onrender.com` with your Render URL from Step 3. Keep `/api/:path*` at the end:

```json
{
  "rewrites": [
    { "source": "/api/:path*", "destination": "https://audit-planner-api-xxxx.onrender.com/api/:path*" }
  ]
}
```

3. Click **Commit changes**.

## Step 5: Deploy the website on Vercel

1. Go to <https://vercel.com> and sign up or log in with **GitHub**.
2. Click **Add New…** → **Project**, and **Import** `procurement-audit-harness`.
3. In the configuration screen:
   - **Root Directory**: click **Edit** and choose `web`
   - **Framework Preset**: `Other`
   - Leave the build and output settings empty. The site is plain HTML, CSS and JavaScript.
4. Click **Deploy**. It takes under a minute. Your URL is shown on the success page, for example `https://procurement-audit-harness.vercel.app`. **This is the URL you submit.**

After that, a push to `main` redeploys automatically, but not always both sides:

- **Vercel** redeploys the website on every push.
- **Render** redeploys the agent server only when the push changes something it runs. The
  `buildFilter` in `render.yaml` ignores changes to `web/**`, `tests/**` and Markdown files
  (`*.md`), so editing the website, the tests or the docs does not redeploy it. A Render redeploy
  restarts the server and stops any run that is working, so push server changes (`harness/`,
  `server.py`, `part-a/`, `saved-runs/`, `Dockerfile`, `requirements.txt`) only when no run is in
  progress.

## Step 6: Check the full workflow

1. Open your Vercel URL. The top-right badge says **server ready** once the Render server answers. On the free plan, the first visit after a quiet period can take up to a minute to wake the server; the badge shows "waking the server" until then.
2. Enter the access password.
3. For the first demonstration, tick **Reuse Part A's Phase 1 outputs**, then click **New run** → **Start the agents**.
   - **Agent activity** shows each agent's tool calls, messages and reports live.
   - You can close the page and come back with the run's link (`?run=<id>`). The run keeps going.
4. At **Gate 1**, choose Approve, Amend or Reject for each risk and submit. The server then runs the risk-assessor revision, the approval gate, the planner + challenger + qa-reviewer team and the lead report.
5. At **Gate 2**, read the planning memo and review under **Outputs**, enter your name and sign off.
6. Click **Download all outputs (.zip)** for the complete audit planning pack.
7. If time and budget allow, also run the full pipeline once with Reuse unticked (rules → analytics/history → … → sign-off).

## Notes

- **Render free plan.** The server sleeps after 15 minutes without requests and wakes on the next visit. While a run is working, the server pings itself to stay awake, but a run waiting at a gate is not kept awake. Restarts and redeploys clear runs that are not saved: a run in progress or waiting at a gate is lost, so finish the gates promptly and download the zip. Completed runs committed to `saved-runs/` (see `save_live_run.py`) are restored on every restart. For a guaranteed always-on server, upgrade the Render service to the Starter plan (about $7/month).
- **Before you submit,** open the site once yourself so the server is awake when the grader visits.
- **Part A example run** in the sidebar shows Part A's complete, signed-off outputs. Viewing it doesn't call Claude.
- **Troubleshooting.**
  - If the badge stays at "server unreachable", check the Render service is **Live** and that the URL in `web/vercel.json` is exactly right.
  - If the badge says "server: no API key", set `ANTHROPIC_API_KEY` on Render.
