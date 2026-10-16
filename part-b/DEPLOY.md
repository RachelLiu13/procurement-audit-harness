# Deployment guide (Part B)

When you finish, you will have one URL like `https://procurement-audit-harness.fly.dev` that you submit for Part B.

The whole app runs on **Fly.io** as one service built from `part-b/Dockerfile`: `server.py` serves the website (`web/`) at `/` and the agent API at `/api`. There is no separate front-end host.

Why Fly.io: a run lasts 30–60 minutes and waits on the auditor at two gates, so it needs a server that stays on. `fly.toml` keeps one machine running (`auto_stop_machines = "off"`), gives it 2 GB of memory, and stores runs on a volume at `/data`, so runs survive restarts and redeploys.

There are five steps: get an API key → install flyctl and log in → create the app → set the secrets and deploy → run the workflow once.

---

## Step 1: Get an Anthropic API key

The agents call Claude from the server, which needs an API key. A Claude.ai Pro or Max subscription does **not** include API usage. You have to set up the API separately.

1. Go to <https://platform.claude.com> (the Claude Console) and sign up or log in.
2. Open **Billing**, add a card and buy prepaid credits (the minimum is about US$5).
3. Recommended: under **Limits**, set a monthly spend limit such as $20.
4. Open **API Keys** → **Create Key**, name it (for example `audit-planner`), and copy the key. It starts with `sk-ant-`. **The key is shown only once**, so save it in a password manager.
5. The key goes only into Fly.io's secrets in Step 4. Never put it in code, commit it to GitHub or share it.

> **Cost.** The default model is `claude-opus-5-5`. A demo run with "Reuse Part A's Phase 1 outputs" ticked typically costs a few dollars. A full run costs more, depending on how many turns the agents take. To spend less, set `CLAUDE_MODEL` to `claude-sonnet-5-5` in `fly.toml`. The site shows live token usage for each run.
>
> **Fly.io cost.** One always-on machine with 2 GB of memory plus a 1 GB volume costs roughly US$10–12 a month. Fly.io needs a card on file. Run `fly scale count 0` after grading to stop paying for the machine.

## Step 2: Install flyctl and log in

```bash
brew install flyctl          # macOS; other systems: https://fly.io/docs/flyctl/install/
fly auth login               # opens the browser; sign up or log in
```

## Step 3: Create the app

In a terminal opened in the repository root (where `fly.toml` is; the image is built from there so it holds `part-a/` and `part-b/`). Run every `fly` command below from the root:

```bash
fly launch --no-deploy
```

- When asked whether to copy the existing `fly.toml` configuration, answer **Yes**.
- Do not add a database or Redis.
- If the name `procurement-audit-harness` is already taken, choose another name. Fly writes it into `fly.toml`, and your URL becomes `https://<that-name>.fly.dev`. Use that URL wherever this guide and the README say `procurement-audit-harness.fly.dev`.

## Step 4: Set the secrets and deploy

```bash
fly secrets set ANTHROPIC_API_KEY=sk-ant-... APP_PASSWORD=choose-a-password
fly deploy
```

- `APP_PASSWORD` is the access password visitors must enter, so strangers can't spend your credits. Give it to your grader with the URL.
- The first deploy builds the image (Python, `pdftotext` and the packages) and creates the volume. It takes about 5–10 minutes.
- Check it: open `https://procurement-audit-harness.fly.dev/api/health`. You should see `{"ok":true,"key_configured":true,...}`.

To change a setting later, edit `[env]` in `fly.toml` and run `fly deploy`, or for secrets run `fly secrets set NAME=value` (Fly restarts the machine automatically). A deploy restarts the server and stops any run that is working, so deploy only when no run is in progress. Runs waiting at a gate and finished runs are kept on the volume.

## Step 5: Check the full workflow

1. Open `https://procurement-audit-harness.fly.dev`. The top-right badge says **server ready**.
2. Enter the access password.
3. For the first demonstration, tick **Reuse Part A's Phase 1 outputs**, then click **New run** → **Start the agents**.
   - **Agent activity** shows each agent's tool calls, messages and reports live.
   - You can close the page and come back with the run's link (`?run=<id>`). The run keeps going.
4. At **Gate 1**, choose Approve, Amend or Reject for each risk and submit. The server then runs the risk-assessor revision, the approval gate, the planner + challenger + qa-reviewer team and the lead report.
5. At **Gate 2**, read the planning memo and review under **Outputs**, enter your name and sign off.
6. Click **Download all outputs (.zip)** for the complete audit planning pack.
7. If time and budget allow, also run the full pipeline once with Reuse unticked (rules → analytics/history → … → sign-off).

## Notes

- **Saving a finished run into the repository.** `python part-b/save_live_run.py <run-id> https://procurement-audit-harness.fly.dev` writes it to `part-b/saved-runs/` (restored on every start) and `part-b/web/live-run/` (the read-only "Completed end-to-end run" page). Commit both, then `fly deploy` from the root.
- **Part A example run** in the sidebar shows Part A's complete, signed-off outputs. Viewing it doesn't call Claude.
- **Logs:** `fly logs`. **Status:** `fly status`.
- **Troubleshooting.**
  - If the deploy fails with out-of-memory errors, check `[[vm]] memory = "2gb"` in `fly.toml`.
  - If the badge says "server: no API key", run `fly secrets set ANTHROPIC_API_KEY=...`.
  - If `fly deploy` says the volume is missing, create it: `fly volumes create runs_data --size 1 --region lax`.
