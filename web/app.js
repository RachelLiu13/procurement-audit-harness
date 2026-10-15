// Procurement Audit Planner: browser client for the harness API (server.py).
"use strict";

const API = (window.API_BASE || "").replace(/\/$/, "");
const $ = (sel, el = document) => el.querySelector(sel);

const STAGES = [
  ["1", "Extract rules", "skill · extract-rules", "rules.json", false],
  ["2", "Analyse spend & history", "spend-analyst ∥ findings-analyst", "analytics.json · history.json", false],
  ["3", "Rate risks", "risk-assessor + risk-assessment skill", "risk-register.md", false],
  ["G1", "Auditor decisions", "you (human gate)", "auditor-comments.md", true],
  ["4", "Revise register", "risk-assessor", "register revision", false],
  ["5", "Plan, challenge, QA", "agent team: planner · challenger · qa-reviewer", "planning pack · review.md", false],
  ["G2", "Auditor sign-off", "you (human gate)", "review.md signed", true],
];
const KEY_FILES = ["planning-memo.md", "risk-control-matrix.md", "audit-program.md", "challenges.md", "review.md",
  "risk-register.md", "auditor-comments.md", "rules.json", "analytics.json", "history.json"];
const ICON = { text: "💬", tool: "🔧", result: "↳", message: "✉️", report: "📄", stage: "▶️", status: "ℹ️",
  error: "⚠️", script: "🐍", decision: "🧑‍⚖️", thinking: "💭" };

// ------------------------------------------------------------------ storage (best effort)
const store = {
  get(k) { try { return sessionStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { sessionStorage.setItem(k, v); } catch { /* private mode */ } },
};

// ------------------------------------------------------------------ API
let health = null;

async function api(path, opts = {}) {
  const headers = { ...(opts.headers || {}) };
  const pw = store.get("pw");
  if (pw) headers["X-App-Password"] = pw;
  if (opts.json !== undefined) { headers["Content-Type"] = "application/json"; opts.body = JSON.stringify(opts.json); }
  const res = await fetch(API + path, { ...opts, headers });
  if (res.status === 401) { await login(); return api(path, opts); }
  if (!res.ok) {
    let msg = res.statusText;
    try { msg = (await res.json()).detail || msg; } catch { /* not json */ }
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  const type = res.headers.get("content-type") || "";
  return type.includes("json") ? res.json() : res.text();
}

function login() {
  return new Promise((resolve) => {
    const dlg = $("#login");
    $("#login-error").textContent = store.get("pw") ? "Wrong password." : "";
    dlg.showModal();
    $("#login-form").onsubmit = async (e) => {
      e.preventDefault();
      store.set("pw", $("#password").value);
      const r = await fetch(API + "/api/auth", { headers: { "X-App-Password": $("#password").value } });
      if (r.ok) { dlg.close(); resolve(); } else { $("#login-error").textContent = "Wrong password."; }
    };
  });
}

async function connect() {
  const pill = $("#server");
  for (let i = 0; i < 30; i++) {
    try {
      const r = await fetch(API + "/api/health");
      if (r.ok) {
        health = await r.json();
        pill.textContent = health.key_configured ? "server ready" : "server: no API key";
        pill.className = "pill " + (health.key_configured ? "ok" : "err");
        $("#model").textContent = `Model ${health.model} · effort ${health.effort}`;
        $("#new-run").disabled = !health.key_configured;
        return true;
      }
    } catch { /* still waking */ }
    pill.textContent = "waking the server (up to a minute)…";
    await sleep(4000);
  }
  pill.textContent = "server unreachable"; pill.className = "pill err";
  return false;
}

// ------------------------------------------------------------------ helpers
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const md = (s) => DOMPurify.sanitize(marked.parse(String(s ?? "")));
const runId = () => new URLSearchParams(location.search).get("run");

function stageIndex(s) {
  const status = s.status, stage = s.stage || "";
  if (status === "complete") return STAGES.length;
  if (status === "awaiting_signoff") return 6;
  if (status === "awaiting_decisions") return 3;
  if (stage.startsWith("1–2")) return 2;
  const i = STAGES.findIndex(([code]) => stage.startsWith(code + " "));
  return i < 0 ? 0 : i;
}

function usageLine(s) {
  const u = s.usage || {};
  if (!u.input_tokens) return "";
  const n = (x) => (x || 0).toLocaleString();
  return `Tokens: ${n(u.input_tokens)} input · ${n(u.cache_read)} cache read · ${n(u.output_tokens)} output · ${esc(s.model)}`;
}

// ------------------------------------------------------------------ sidebar
async function refreshRuns() {
  if (!health) return;
  try {
    const runs = await api("/api/runs");
    const cur = runId();
    $("#runs").innerHTML = runs.length ? runs.map((r) =>
      `<li><a href="?run=${esc(r.id)}" class="${r.id === cur ? "active" : ""}">${esc(r.id)}` +
      `<small>${esc(r.status_text || r.status)}${r.reuse_phase1 ? " · reuse" : ""}</small></a></li>`).join("")
      : '<li class="muted small">No runs yet.</li>';
  } catch (e) { $("#runs").innerHTML = `<li class="error small">${esc(e.message)}</li>`; }
}

$("#new-run").onclick = async () => {
  $("#new-run").disabled = true;
  try {
    const r = await api("/api/runs", { method: "POST", json: { reuse_phase1: $("#reuse").checked } });
    location.search = "?run=" + encodeURIComponent(r.id);
  } catch (e) { alert(e.message); $("#new-run").disabled = false; }
};

// ------------------------------------------------------------------ pages
function about() {
  $("#main").innerHTML = $("#about-tpl").innerHTML;
  $("#about-stages").innerHTML = STAGES.map(([c, t, w, o]) =>
    `<li><code>${c}</code> <b>${t}</b> — ${esc(w)} → <code>${esc(o)}</code></li>`).join("");
}

// "live" is the saved end-to-end run in web/live-run/ (static files, no server needed).
const LIVE = "live-run";
const listFiles = (id) => id === "live" ? fetch(`${LIVE}/files.json`).then((r) => r.json())
  : api(`/api/runs/${encodeURIComponent(id)}/files`);
const readFile = (id, f) => id === "live"
  ? fetch(`${LIVE}/outputs/${f.split("/").map(encodeURIComponent).join("/")}`).then((r) => r.text())
  : api(`/api/runs/${encodeURIComponent(id)}/file?path=${encodeURIComponent(f)}`);

async function filesBrowser(el, id) {
  let files = await listFiles(id);
  if (!files.length) { el.innerHTML = '<p class="muted">No outputs yet.</p>'; return; }
  const pack = KEY_FILES.filter((f) => files.includes(f));
  const rest = files.filter((f) => !KEY_FILES.includes(f));
  const groups = [["Audit planning pack", pack], ["Working files", rest.filter((f) => !f.includes("/"))]];
  for (const dir of [...new Set(rest.filter((f) => f.includes("/")).map((f) => f.slice(0, f.lastIndexOf("/"))))])
    groups.push([dir + "/", rest.filter((f) => f.slice(0, f.lastIndexOf("/")) === dir)]);
  const keep = el.dataset.file && files.includes(el.dataset.file) ? el.dataset.file : (pack[0] || files[0]);
  el.innerHTML = `<div class="filebrowser"><nav class="filelist">${groups.filter(([, fs]) => fs.length).map(([g, fs]) =>
    `<h4>${esc(g)}</h4>${fs.map((f) => `<button type="button" data-f="${esc(f)}">${esc(f.split("/").pop())}</button>`).join("")}`).join("")}</nav>
    <div class="fileview"><div class="filebar"><b class="fname"></b><a class="dl small" target="_blank" rel="noopener">download</a></div>
    <div class="view card md"></div></div></div>`;
  const show = async (f) => {
    el.dataset.file = f;
    el.querySelectorAll(".filelist button").forEach((b) => b.classList.toggle("on", b.dataset.f === f));
    $(".fname", el).textContent = f;
    const text = await readFile(id, f);
    const view = $(".view", el);
    if (f.endsWith(".md")) view.innerHTML = md(text);
    else if (f.endsWith(".json")) { let t = text; try { t = JSON.stringify(JSON.parse(text), null, 1); } catch { } view.innerHTML = `<pre>${esc(t)}</pre>`; }
    else if (f.endsWith(".csv")) view.innerHTML = `<div class="csv">${csvTable(text)}</div>`;
    else view.innerHTML = `<pre>${esc(text)}</pre>`;
    const blob = new Blob([text], { type: "text/plain" });
    const a = $(".dl", el); a.href = URL.createObjectURL(blob); a.download = f.split("/").pop();
  };
  el.querySelectorAll(".filelist button").forEach((b) => b.onclick = () => show(b.dataset.f));
  await show(keep);
}

function csvTable(text) {
  const rows = [];
  let row = [], cell = "", q = false;
  for (let i = 0; i < text.length && rows.length < 501; i++) {
    const c = text[i];
    if (q) { if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; } else if (c === '"') q = false; else cell += c; }
    else if (c === '"') q = true;
    else if (c === ",") { row.push(cell); cell = ""; }
    else if (c === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; }
    else if (c !== "\r") cell += c;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  const [head, ...body] = rows;
  return `<table><thead><tr>${(head || []).map((h) => `<th>${esc(h)}</th>`).join("")}</tr></thead><tbody>` +
    body.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join("")}</tr>`).join("") + "</tbody></table>" +
    (rows.length > 500 ? '<p class="muted small">First 500 rows shown; download for the rest.</p>' : "");
}

async function examplePage() {
  $("#main").innerHTML = `<h1>Part A example run</h1>
    <p class="muted">The complete outputs of the team's Claude Code run (Part A), signed off on 2026-10-14.
    Read-only; compare it with a live run.</p><div id="files"></div>`;
  await filesBrowser($("#files"), "example");
}

// ------------------------------------------------------------------ run page
let poll = null, lastStatus = null, evCount = 0;

async function runPage(id) {
  $("#main").innerHTML = `<h1>Run <code>${esc(id)}</code></h1>
    <div id="stepper" class="stepper"></div><div id="banner"></div><div id="usage" class="muted small"></div>
    <div id="action"></div>
    <div class="tabs"><button data-t="activity" class="on">Agent activity</button><button data-t="outputs">Outputs</button></div>
    <div id="t-activity"><div class="row small"><label><input type="checkbox" id="detail"> Show tool results and thinking</label></div><div id="events"></div></div>
    <div id="t-outputs" hidden></div>`;
  document.querySelectorAll(".tabs button").forEach((b) => b.onclick = () => {
    document.querySelectorAll(".tabs button").forEach((x) => x.classList.toggle("on", x === b));
    $("#t-activity").hidden = b.dataset.t !== "activity";
    $("#t-outputs").hidden = b.dataset.t !== "outputs";
    if (b.dataset.t === "outputs") filesBrowser($("#t-outputs"), id).catch((e) => $("#t-outputs").textContent = e.message);
  });
  $("#detail").onchange = () => { evCount = 0; $("#events").innerHTML = ""; tick(id); };
  lastStatus = null; evCount = 0;
  await tick(id);
}

async function tick(id) {
  clearTimeout(poll);
  let s;
  try { s = await api(`/api/runs/${encodeURIComponent(id)}`); }
  catch (e) { $("#main").innerHTML = `<div class="banner err">${esc(e.message)}</div>`; return; }
  renderHeader(s);
  if (s.status !== lastStatus) { lastStatus = s.status; await renderAction(id, s); refreshRuns(); }
  await loadEvents(id);
  // Keep polling at the gates too (more slowly): someone else may decide in another browser.
  // The gate forms are redrawn only when the status changes, so typing is not interrupted.
  if (s.status === "running" || s.status === "created") poll = setTimeout(() => tick(id), 4000);
  else if ((s.status || "").startsWith("awaiting")) poll = setTimeout(() => tick(id), 15000);
  else if (s.final_report_status === "writing") { lastStatus = null; poll = setTimeout(() => tick(id), 5000); }
}

function renderHeader(s) {
  const idx = stageIndex(s);
  $("#stepper").innerHTML = STAGES.map(([code, title, who, out, human], i) => {
    const cls = i < idx ? "done" : i === idx && s.status !== "complete" ? "now" : "";
    const mark = i < idx ? "✅" : i === idx && s.status === "running" ? "⏳" : i === idx && (s.status || "").startsWith("awaiting") ? "👤" : "○";
    return `<div class="step ${cls} ${human ? "human" : ""}"><b>${mark} ${title}</b><div class="who">${esc(who)}</div><div class="out">→ ${esc(out)}</div></div>`;
  }).join("");
  const st = s.status;
  let b = "";
  if (st === "running") b = `<div class="banner run">⏳ <b>${esc(s.status_text)}</b>: ${esc(s.stage)}. You can close this page; the run continues. Come back with this page's link.</div>`;
  else if (st === "awaiting_decisions" || st === "awaiting_signoff") b = `<div class="banner wait">👤 <b>${esc(s.status_text)}</b></div>`;
  else if (st === "complete") b = `<div class="banner ok">✅ The pack is signed off. Download it below or browse it under Outputs.</div>`;
  else if (["failed", "cancelled", "blocked"].includes(st)) b = `<div class="banner err"><b>${esc(s.status_text)}</b>. ${esc(s.error || "")}</div>`;
  $("#banner").innerHTML = b;
  $("#usage").innerHTML = usageLine(s);
}

// The lead writes its report before the auditor decides; once the pack is signed off (or
// returned) the report is history, so say so and point to the decision in review.md.
function leadCard(s) {
  if (!s.lead_report) return "";
  const decided = s.status === "complete" || (s.status === "blocked" && (s.stage || "").startsWith("Returned"));
  if (!decided) return `<div class="card"><h3>Lead's report</h3><div class="md">${md(s.lead_report)}</div></div>`;
  const final = s.final_report
    ? `<div class="card"><h3>Lead's report · after sign-off</h3><div class="md">${md(s.final_report)}</div></div>`
    : s.final_report_status === "writing"
      ? `<div class="banner run">⏳ The lead is writing its report on the auditor's decision…</div>`
      : `<div class="banner ok small">Final status: <b>${s.status === "complete" ? "Signed off" : "Returned to the team"}</b>.
         The decision and the auditor's comments are in <code>review.md</code> → Auditor sign-off (Outputs tab).</div>`;
  return final + `<div class="card"><details><summary><b>Lead's report · before sign-off</b>
    <span class="muted small">(historical: written before the auditor's decision, kept as it was)</span></summary>
    <div class="md">${md(s.lead_report)}</div></details></div>`;
}

async function renderAction(id, s) {
  const el = $("#action");
  const base = `/api/runs/${encodeURIComponent(id)}`;
  const zip = `<p><button id="zip">⬇ Download all outputs (.zip)</button></p>`;
  const lead = leadCard(s);
  if (s.status === "created") {
    el.innerHTML = `<p><button class="primary" id="go">▶ Start the agents</button></p>`;
    $("#go").onclick = async () => { $("#go").disabled = true; try { await api(base + "/start", { method: "POST" }); } catch (e) { alert(e.message); } tick(id); };
  } else if (s.status === "running") {
    el.innerHTML = `<p><button id="stop">Cancel run</button></p>`;
    $("#stop").onclick = async () => { if (confirm("Cancel this run? Agents stop after their current step.")) await api(base + "/cancel", { method: "POST" }); };
  } else if (s.status === "awaiting_decisions") {
    await decisionsForm(el, id, s);
  } else if (s.status === "awaiting_signoff") {
    el.innerHTML = lead + `<div class="card"><h2>Gate 2 · Sign off the audit planning pack</h2>
      <p class="muted small">Read the planning memo, risk-control matrix, audit program, challenges and QA review under Outputs before you sign.</p>
      <form id="so"><div class="row"><label><input type="radio" name="d" value="Sign off" checked> Sign off</label>
      <label><input type="radio" name="d" value="Return to the team"> Return to the team</label></div>
      <label class="f">Name</label><input type="text" name="name" required>
      <label class="f">Role</label><input type="text" name="role" value="Internal auditor">
      <label class="f">Comments</label><textarea name="comments"></textarea>
      <p><button class="primary">Record decision in review.md</button></p></form></div>` + zip;
    $("#so").onsubmit = async (e) => {
      e.preventDefault();
      const f = new FormData(e.target);
      try {
        await api(base + "/signoff", { method: "POST", json: { decision: f.get("d"), name: f.get("name"), role: f.get("role"), comments: f.get("comments") } });
        lastStatus = null; tick(id);
      } catch (err) { alert(err.message); }
    };
  } else if (["complete", "blocked"].includes(s.status)) {
    el.innerHTML = lead + zip;
  } else {
    el.innerHTML = `<p class="muted">Start a new run from the left to try again.</p>`;
  }
  const z = $("#zip");
  if (z) z.onclick = async () => {
    const pw = store.get("pw");
    const r = await fetch(API + base + "/zip", { headers: pw ? { "X-App-Password": pw } : {} });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(await r.blob()); a.download = `audit-pack-${id}.zip`; a.click();
  };
}

async function decisionsForm(el, id, s) {
  const base = `/api/runs/${encodeURIComponent(id)}`;
  const { rows, other, choices } = await api(base + "/decisions");
  const register = await api(base + "/file?path=risk-register.md").catch(() => "");
  const closed = s.gate_output && s.gate_output.includes("GATE CLOSED")
    ? `<div class="banner err">The approval gate is still closed:<pre>${esc(s.gate_output)}</pre></div>` : "";
  el.innerHTML = `<div class="card"><h2>Gate 1 · Your decisions on the risk register</h2>${closed}
    <details><summary>Risk register (risk-register.md)</summary><div class="md">${md(register)}</div></details>
    ${s.assessor_report ? `<details><summary>risk-assessor's report</summary><div class="md">${md(s.assessor_report)}</div></details>` : ""}
    <p class="muted small">Approve, Amend or Reject every risk. For Amend, say exactly what to change; give a reason for Reject.
    The risk-assessor then re-issues the register and the agent team starts.</p>
    <form id="dec">${rows.map((r) => {
      const cur = choices.includes(r.Decision) ? r.Decision : "Approve";
      return `<div class="risk"><div><b>${esc(r["Risk ID"])}</b> · ${esc(r.Risk)}
        <div class="meta">L${esc(r.L)} × I${esc(r.I)} = ${esc(r.Score)} · ${esc(r.Band)} · proposed scope: <i>${esc(r["Proposed scope"])}</i></div></div>
        <select name="d-${esc(r["Risk ID"])}">${choices.map((c) => `<option ${c === cur ? "selected" : ""}>${c}</option>`).join("")}</select>
        <input type="text" name="c-${esc(r["Risk ID"])}" value="${esc(r.Comment)}" placeholder="Comment (required for Amend/Reject)"></div>`;
    }).join("")}
    <label class="f">Other instructions (optional, e.g. "add a risk on …")</label><textarea name="other">${esc(other)}</textarea>
    <p><button class="primary">Submit decisions and start the agent team</button></p></form></div>`;
  $("#dec").onsubmit = async (e) => {
    e.preventDefault();
    const f = new FormData(e.target);
    const decisions = {};
    for (const r of rows) { const k = r["Risk ID"]; decisions[k] = [f.get("d-" + k), f.get("c-" + k) || ""]; }
    const missing = Object.entries(decisions).filter(([, [d, c]]) => d !== "Approve" && !c.trim()).map(([k]) => k);
    if (missing.length) { alert("Add a comment for: " + missing.join(", ")); return; }
    try {
      await api(base + "/decisions", { method: "POST", json: { decisions, other: f.get("other") || "" } });
      lastStatus = null; tick(id);
    } catch (err) { alert(err.message); }
  };
}

function eventsHtml(events, detail) {
  return events.filter((e) => detail || !["result", "thinking"].includes(e.kind)).map((e) => {
    const pre = ["tool", "result", "script", "error"].includes(e.kind);
    const long = e.text.length > 600 && !["report", "decision", "stage"].includes(e.kind);
    const body = pre ? `<pre>${esc(e.text.slice(0, 6000))}</pre>`
      : e.kind === "message" ? esc(e.text) : `<div class="md">${md(e.text)}</div>`;
    const head = `<span class="h">${ICON[e.kind] || "•"} <b>${esc(e.agent)}</b> · ${esc(e.kind)} · ${esc(e.t.slice(11))}</span>`;
    return `<div class="ev ${esc(e.kind)}">` + (long ? `<details><summary>${head} ${esc(e.text.slice(0, 90))}…</summary><div class="body">${body}</div></details>`
      : `${head}<div class="body">${body}</div>`) + "</div>";
  }).reverse().join("");
}

async function loadEvents(id) {
  const detail = $("#detail") && $("#detail").checked;
  const { total, events } = await api(`/api/runs/${encodeURIComponent(id)}/events?after=${evCount}`);
  evCount = total;
  const html = eventsHtml(events, detail);
  if (html) $("#events").insertAdjacentHTML("afterbegin", html);
  if (!$("#events").innerHTML) $("#events").innerHTML = '<p class="muted">No activity yet.</p>';
  else { const p = $("#events > p.muted"); if (p && $("#events").children.length > 1) p.remove(); }
}

// ------------------------------------------------------------------ saved live run
async function livePage() {
  const [s, ev] = await Promise.all([fetch(`${LIVE}/state.json`).then((r) => r.json()),
    fetch(`${LIVE}/events.json`).then((r) => r.json())]);
  const events = ev.events || ev;
  const first = events[0] ? events[0].t.replace("T", " ") : "", last = events.length ? events[events.length - 1].t.replace("T", " ") : "";
  $("#main").innerHTML = `<h1>Part B live run <code>${esc(s.id)}</code></h1>
    <p class="muted">A complete end-to-end run of this deployed harness, from the Contract Rules PDF to the auditor's
    sign-off, ${esc(first)} → ${esc(last)} (server time, UTC). Saved from the server so it stays visible after the
    free instance restarts. Read-only: start your own run from the left.</p>
    <div id="stepper" class="stepper"></div><div id="banner"></div><div id="usage" class="muted small"></div>
    <p><a class="btn" href="${API}/api/runs/${encodeURIComponent(s.id)}/zip">⬇ Download all outputs (.zip)</a></p>
    ${leadCard(s)}
    <div class="tabs"><button data-t="activity" class="on">Agent activity (${events.length} events)</button><button data-t="outputs">Outputs</button></div>
    <div id="t-activity"><div class="row small"><label><input type="checkbox" id="detail"> Show tool results and thinking</label></div><div id="events"></div></div>
    <div id="t-outputs" hidden></div>`;
  renderHeader(s);
  const draw = () => { $("#events").innerHTML = eventsHtml(events, $("#detail").checked); };
  $("#detail").onchange = draw; draw();
  document.querySelectorAll(".tabs button").forEach((b) => b.onclick = () => {
    document.querySelectorAll(".tabs button").forEach((x) => x.classList.toggle("on", x === b));
    $("#t-activity").hidden = b.dataset.t !== "activity";
    $("#t-outputs").hidden = b.dataset.t !== "outputs";
    if (b.dataset.t === "outputs" && !$("#t-outputs").innerHTML) filesBrowser($("#t-outputs"), "live");
  });
}

// ------------------------------------------------------------------ boot
(async function boot() {
  const id = runId();
  if (!id) about();
  if (id === "live") livePage().catch(() => $("#main").innerHTML = '<div class="banner err">The saved run is not available.</div>');
  if (!(await connect())) {
    if (id) $("#main").innerHTML = '<div class="banner err">The server cannot be reached. Try again in a minute.</div>';
    return;
  }
  if (health.password_required && !store.get("pw")) await login();
  refreshRuns();
  if (id === "example") examplePage().catch((e) => $("#main").textContent = e.message);
  else if (id && id !== "live") runPage(id);
})();
