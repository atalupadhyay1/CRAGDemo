const $ = (selector, root = document) => root.querySelector(selector);

const welcomeState = $("#welcomeState");
const messageList = $("#messageList");
const conversationScroll = $("#conversationScroll");
const queryForm = $("#queryForm");
const queryInput = $("#queryInput");
const sendButton = $("#sendButton");
const traceList = $("#traceList");
const traceEmpty = $("#traceEmpty");
const traceStatus = $("#traceStatus");
const traceFooter = $("#traceFooter");
const documentList = $("#documentList");
const documentInput = $("#documentInput");
const toastRegion = $("#toastRegion");

let isPending = false;
let latestHealth = null;

const AGENT_ICON = '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M16 3.7 27 10v12L16 28.3 5 22V10L16 3.7Z" stroke="currentColor" stroke-width="1.6"/><path d="m10.3 16 3.6 3.7 7.8-8.2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
const DOCUMENT_ICON = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4.2 3.6h8.1l3.5 3.5v9.3H4.2V3.6Z" stroke="currentColor" stroke-width="1.35" stroke-linejoin="round"/><path d="M12.2 3.8v3.7h3.5M7 10.3h6m-6 3h6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>';

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = text;
  return node;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { ...(options.body ? { "Content-Type": "application/json" } : {}), ...(options.headers || {}) },
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || `Request failed (${response.status})`);
  return payload;
}

function showToast(message, type = "success") {
  const toast = element("div", `toast${type === "error" ? " error" : ""}`, message);
  toastRegion.append(toast);
  window.setTimeout(() => toast.remove(), 4300);
}

function scrollToLatest() {
  window.requestAnimationFrame(() => {
    conversationScroll.scrollTop = conversationScroll.scrollHeight;
  });
}

function addUserMessage(text) {
  const message = element("article", "message user-message");
  const body = element("div", "message-body", text);
  message.append(body);
  messageList.append(message);
  welcomeState.hidden = true;
  scrollToLatest();
}

function addLoadingMessage() {
  const message = element("article", "message assistant-message loading-answer");
  const avatar = element("div", "message-avatar");
  avatar.innerHTML = AGENT_ICON;
  const body = element("div", "message-body");
  body.append(element("div", "message-label", "CRAG agent"));
  const loading = element("div", "loading-message", "Checking your question");
  const dots = element("span", "thinking-dots");
  for (let i = 0; i < 3; i += 1) dots.append(element("i"));
  loading.append(dots);
  body.append(loading);
  message.append(avatar, body);
  messageList.append(message);
  scrollToLatest();
  return message;
}

function safeHttpUrl(value) {
  if (!value) return "";
  try {
    const url = new URL(value, window.location.origin);
    return ["http:", "https:"].includes(url.protocol) ? url.href : "";
  } catch {
    return "";
  }
}

function renderSources(sources) {
  if (!Array.isArray(sources) || sources.length === 0) return null;
  const list = element("div", "answer-source-list");
  sources.slice(0, 6).forEach((source) => {
    const url = source.kind === "web" ? safeHttpUrl(source.url) : "";
    const item = url ? document.createElement("a") : document.createElement("div");
    item.className = "answer-source";
    if (url) {
      item.href = url;
      item.target = "_blank";
      item.rel = "noopener noreferrer";
      item.title = source.url;
    }
    const badge = element("span", `source-badge ${source.kind === "web" ? "web" : source.kind === "tool" ? "tool" : ""}`);
    badge.textContent = source.kind === "web" ? "WEB" : source.kind === "tool" ? "TOOL" : String(source.id || "SRC").slice(0, 6);
    const meta = element("span", "source-meta");
    meta.append(element("strong", "", source.title || "Retrieved source"));
    meta.append(element("span", "", source.kind === "web" ? "WEB SEARCH RESULT" : source.kind === "tool" ? "STRUCTURED TOOL OUTPUT" : `${source.id || "SOURCE"} · ${source.source || "INDEXED"}`));
    item.append(badge, meta);
    if (url) item.append(element("span", "source-open", "↗"));
    list.append(item);
  });
  return list;
}

function renderAssistantMessage(result) {
  const message = element("article", "message assistant-message");
  const avatar = element("div", "message-avatar");
  avatar.innerHTML = AGENT_ICON;
  const body = element("div", "message-body");
  body.append(element("div", "message-label", "CRAG agent · grounded response"));
  const copy = element("div", "answer-copy");
  const answer = String(result.answer || "");
  if (answer.includes("I cannot confirm this based on the available context.")) copy.classList.add("refusal");
  answer.split(/\n\s*\n/).filter(Boolean).forEach((paragraph) => copy.append(element("p", "", paragraph.trim())));
  body.append(copy);
  const sourceList = renderSources(result.sources);
  if (sourceList) body.append(sourceList);
  if (result.answer_xml) {
    const details = element("details", "xml-details");
    const summary = element("summary", "", "View structured XML response");
    const pre = element("pre", "");
    pre.textContent = result.answer_xml;
    details.append(summary, pre);
    body.append(details);
  }
  message.append(avatar, body);
  messageList.append(message);
  scrollToLatest();
}

function renderTrace(result, running = false) {
  const steps = Array.isArray(result?.trace) ? result.trace : [];
  traceList.replaceChildren();
  traceEmpty.hidden = steps.length > 0;
  traceList.hidden = steps.length === 0;
  traceStatus.className = `trace-status ${running ? "running" : steps.length ? "done" : "idle"}`;
  traceStatus.textContent = running ? "RUNNING" : steps.length ? "COMPLETE" : "IDLE";
  if (steps.length) {
    steps.forEach((step) => {
      const status = ["warning", "unavailable", "error"].includes(step.status) ? step.status : "complete";
      const item = element("li", `trace-item ${status}`);
      const node = element("span", "trace-node");
      node.innerHTML = status === "complete"
        ? '<svg viewBox="0 0 10 10" fill="none" aria-hidden="true"><path d="m2 5 2 2 4-4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        : '<svg viewBox="0 0 10 10" fill="none" aria-hidden="true"><path d="M5 2.1v3.1m0 2.5h.01" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>';
      const copy = element("div", "trace-copy");
      const title = element("strong", "", step.stage || "Agent step");
      if (Number.isFinite(step.duration_ms)) title.append(element("span", "trace-timing", `${step.duration_ms.toFixed(step.duration_ms < 10 ? 1 : 0)} ms`));
      copy.append(title);
      if (step.detail) copy.append(element("p", "", step.detail));
      const extra = step.rewritten_query || step.query || step.result;
      if (extra) {
        const code = element("code", "", String(extra));
        const line = element("p", "");
        line.append(code);
        copy.append(line);
      }
      item.append(node, copy);
      traceList.append(item);
    });
    const duration = Number.isFinite(result.elapsed_ms) ? `${result.elapsed_ms.toFixed(result.elapsed_ms < 10 ? 1 : 0)} ms` : "Complete";
    traceFooter.replaceChildren();
    traceFooter.append(element("span", "trace-footer-dot"), element("span", "", `Finished in ${duration} · ${result.sources?.length || 0} source(s)`));
  } else if (running) {
    const item = element("li", "trace-item");
    const node = element("span", "trace-node");
    node.innerHTML = '<span class="loading-ring"></span>';
    const copy = element("div", "trace-copy");
    copy.append(element("strong", "", "Query analysis"), element("p", "", "Routing request and starting retrieval…"));
    item.append(node, copy);
    traceList.append(item);
    traceFooter.replaceChildren(element("span", "trace-footer-dot"), element("span", "", "Agent is working"));
  } else {
    traceFooter.replaceChildren(element("span", "trace-footer-dot"), element("span", "", "Each step is inspectable"));
  }
}

function renderDocuments(documents) {
  const items = Array.isArray(documents) ? documents : [];
  $("#documentCount").textContent = String(items.length);
  documentList.replaceChildren();
  if (items.length === 0) {
    documentList.append(element("div", "document-loading", "No documents indexed yet."));
    return;
  }
  items.forEach((doc) => {
    const uploaded = doc.source === "Uploaded";
    const row = element("div", `document-row${uploaded ? " uploaded" : ""}`);
    const icon = element("span", "document-symbol");
    icon.innerHTML = DOCUMENT_ICON;
    const meta = element("div", "document-meta");
    meta.append(element("strong", "", doc.title || "Untitled source"));
    meta.append(element("span", "", `${doc.id} · ${Number(doc.characters || 0).toLocaleString()} chars`));
    row.append(icon, meta);
    if (uploaded) {
      const remove = element("button", "document-remove");
      remove.type = "button";
      remove.title = `Remove ${doc.title}`;
      remove.setAttribute("aria-label", `Remove ${doc.title}`);
      remove.innerHTML = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m4 4 8 8m0-8-8 8" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>';
      remove.addEventListener("click", () => removeDocument(doc.id));
      row.append(remove);
    } else {
      row.append(element("span", "document-remove"));
    }
    documentList.append(row);
  });
}

async function loadDocuments() {
  const payload = await api("/api/documents");
  renderDocuments(payload.documents);
}

async function loadHealth() {
  try {
    latestHealth = await api("/api/health");
    $("#chunkCount").textContent = Number(latestHealth.chunks || 0).toLocaleString();
    const configured = Boolean(latestHealth.web_search_configured);
    $("#providerStatus").textContent = configured ? "Connected · Tavily" : "Not configured · local fallback only";
    $("#providerIndicator").classList.toggle("enabled", configured);
  } catch (error) {
    $("#providerStatus").textContent = "Provider status unavailable";
    showToast(error.message, "error");
  }
}

async function submitQuestion(text) {
  const query = String(text || "").trim();
  if (!query || isPending) return;
  isPending = true;
  queryInput.value = "";
  resizeTextarea();
  sendButton.disabled = true;
  addUserMessage(query);
  const loadingMessage = addLoadingMessage();
  renderTrace({ trace: [{ stage: "Query analysis", detail: "Routing request and starting retrieval…" }] }, true);
  try {
    const result = await api("/api/query", { method: "POST", body: JSON.stringify({ query }) });
    loadingMessage.remove();
    renderAssistantMessage(result);
    renderTrace(result);
  } catch (error) {
    loadingMessage.remove();
    const fallback = {
      answer: `The request could not be completed: ${error.message}`,
      sources: [],
    };
    renderAssistantMessage(fallback);
    renderTrace({ trace: [{ stage: "Request failed", detail: error.message, status: "error" }] });
  } finally {
    isPending = false;
    sendButton.disabled = false;
    queryInput.focus();
  }
}

async function removeDocument(id) {
  try {
    const payload = await api(`/api/documents/${encodeURIComponent(id)}`, { method: "DELETE" });
    renderDocuments(payload.documents);
    await loadHealth();
    showToast("Uploaded source removed from the index.");
  } catch (error) {
    showToast(error.message, "error");
  }
}

function resizeTextarea() {
  queryInput.style.height = "auto";
  queryInput.style.height = `${Math.min(queryInput.scrollHeight, 110)}px`;
}

queryForm.addEventListener("submit", (event) => {
  event.preventDefault();
  submitQuestion(queryInput.value);
});

queryInput.addEventListener("input", resizeTextarea);
queryInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    if (queryInput.value.trim()) queryForm.requestSubmit();
  }
});

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => submitQuestion(button.dataset.prompt));
});

$("#clearChatButton").addEventListener("click", () => {
  if (isPending) return;
  messageList.replaceChildren();
  welcomeState.hidden = false;
  renderTrace({ trace: [] });
  queryInput.focus();
});

$("#addDocumentButton").addEventListener("click", () => documentInput.click());
documentInput.addEventListener("change", async () => {
  const file = documentInput.files?.[0];
  documentInput.value = "";
  if (!file) return;
  if (file.size > 100_000) {
    showToast("Choose a text or Markdown file under 100 KB.", "error");
    return;
  }
  try {
    const content = await file.text();
    const title = file.name.replace(/\.(txt|md)$/i, "");
    const payload = await api("/api/documents", {
      method: "POST",
      body: JSON.stringify({ title, content }),
    });
    renderDocuments(payload.documents);
    await loadHealth();
    showToast(`“${payload.document.title}” added to the local index.`);
  } catch (error) {
    showToast(error.message, "error");
  }
});

Promise.all([loadHealth(), loadDocuments()]).catch((error) => showToast(error.message, "error"));
