/**
 * script.js — Agentic Research Assistant
 * ========================================
 * Handles API communication and rich result rendering.
 * All JSON response fields are rendered as structured UI cards,
 * NOT as raw JSON text.
 */

// ── Config ──────────────────────────────────────────────────────────────────
const API_BASE = "http://localhost:8000";

// ── DOM refs ─────────────────────────────────────────────────────────────────
const questionInput = document.getElementById("question-input");
const submitBtn = document.getElementById("submit-btn");
const btnText = document.getElementById("btn-text");

const loadingSection = document.getElementById("loading-section");
const errorSection = document.getElementById("error-section");
const resultsSection = document.getElementById("results-section");
const errorMessage = document.getElementById("error-message");

// Pipeline step labels
const STEPS = [
    "Fetching papers",
    "Building vector DB",
    "Classifying intent",
    "Generating sub-questions",
    "Retrieval & analysis",
    "Synthesis & report",
];

// ── UI helpers ────────────────────────────────────────────────────────────────
function showOnly(...ids) {
    ["loading-section", "error-section", "results-section"].forEach(id =>
        document.getElementById(id).classList.add("hidden")
    );
    ids.forEach(id => document.getElementById(id).classList.remove("hidden"));
}

// ── Step cycle animation ──────────────────────────────────────────────────────
let stepTimer = null;
let stepIndex = 0;

function startStepCycle() {
    const steps = document.querySelectorAll(".steps .step");
    stepIndex = 0;
    updateStep(steps);
    stepTimer = setInterval(() => {
        stepIndex = (stepIndex + 1) % STEPS.length;
        updateStep(steps);
    }, 3500);
}

function updateStep(steps) {
    steps.forEach((s, i) => {
        s.classList.remove("active", "done");
        if (i < stepIndex) s.classList.add("done");
        if (i === stepIndex) s.classList.add("active");
        s.textContent = STEPS[i];
    });
}

function stopStepCycle() {
    if (stepTimer) { clearInterval(stepTimer); stepTimer = null; }
}

// ── Submit handler ────────────────────────────────────────────────────────────
async function submitResearch() {
    const question = questionInput.value.trim();
    if (!question) {
        questionInput.focus();
        questionInput.style.borderColor = "#f07175";
        setTimeout(() => { questionInput.style.borderColor = ""; }, 1800);
        return;
    }

    submitBtn.disabled = true;
    btnText.textContent = "Running…";
    showOnly("loading-section");
    startStepCycle();

    try {
        const response = await fetch(`${API_BASE}/research`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question }),
        });

        stopStepCycle();

        if (!response.ok) {
            const err = await response.json().catch(() => ({ detail: response.statusText }));
            throw new Error(err.detail || `HTTP ${response.status}`);
        }

        const data = await response.json();
        renderResults(data, question);
        showOnly("results-section");

    } catch (err) {
        stopStepCycle();
        errorMessage.textContent = err.message || "Unknown error. Is the backend running?";
        showOnly("error-section");
    } finally {
        submitBtn.disabled = false;
        btnText.textContent = "Run Research";
    }
}

// ── Result rendering ──────────────────────────────────────────────────────────
/**
 * renderResults()
 * Turns the raw JSON API response into rich structured UI.
 * Each top-level field gets its own styled card/section.
 */
function renderResults(data, question) {
    const container = document.getElementById("results-section");
    container.innerHTML = "";

    // ── Header row ──
    const header = document.createElement("div");
    header.className = "results-header";
    header.innerHTML = `
    <div>
      <h2>✅ Research Complete</h2>
      <p class="results-question">"${escHtml(question)}"</p>
    </div>
    <button class="reset-btn" onclick="resetUI()">New Search</button>
  `;
    container.appendChild(header);

    // ── 1. Intent ──
    container.appendChild(makeSection({
        icon: "🎯",
        label: "Classified Intent",
        content: renderIntent(data.intent),
        delay: 0,
    }));

    // ── 2. Sub-Questions ──
    container.appendChild(makeSection({
        icon: "🧩",
        label: "Generated Sub-Questions",
        content: renderSubQuestions(data.sub_questions || []),
        delay: 80,
    }));

    // ── 3. Synthesis ──
    container.appendChild(makeSection({
        icon: "📑",
        label: "Synthesized Findings",
        content: renderSynthesis(data.synthesis || {}),
        delay: 160,
    }));

    // ── 4. Report ──
    container.appendChild(makeSection({
        icon: "📄",
        label: "Final Research Report",
        content: renderReport(data.report || {}),
        delay: 240,
    }));
}

// ── Section factory ───────────────────────────────────────────────────────────
function makeSection({ icon, label, content, delay }) {
    const card = document.createElement("div");
    card.className = "card result-card";
    card.style.animationDelay = `${delay}ms`;

    const lbl = document.createElement("div");
    lbl.className = "card-label";
    lbl.textContent = `${icon} ${label}`;
    card.appendChild(lbl);
    card.appendChild(content);
    return card;
}

// ── Field renderers ───────────────────────────────────────────────────────────

/** Intent — large badge pill */
function renderIntent(intent) {
    const wrap = document.createElement("div");
    if (!intent) { wrap.textContent = "—"; return wrap; }
    // intent may be a string or array
    const values = Array.isArray(intent) ? intent : [intent];
    values.forEach(v => {
        const badge = document.createElement("span");
        badge.className = `intent-badge intent-${String(v).toLowerCase()}`;
        badge.textContent = v;
        wrap.appendChild(badge);
    });
    return wrap;
}

/** Sub-questions — numbered list with icons */
function renderSubQuestions(list) {
    if (!list.length) {
        return makeEmpty("No sub-questions generated.");
    }
    const ol = document.createElement("ol");
    ol.className = "subq-list";
    list.forEach((sq, i) => {
        const li = document.createElement("li");
        li.innerHTML = `<span class="subq-num">${i + 1}</span><span class="subq-text">${escHtml(sq)}</span>`;
        ol.appendChild(li);
    });
    return ol;
}

/** Synthesis — accordion cards, one per sub-question */
function renderSynthesis(synthesis) {
    const entries = Object.entries(synthesis);
    if (!entries.length) return makeEmpty("No synthesis data.");

    const wrap = document.createElement("div");
    wrap.className = "synthesis-list";

    entries.forEach(([subq, text], i) => {
        const details = document.createElement("details");
        details.className = "synth-item";
        if (i === 0) details.open = true; // open first by default

        const summary = document.createElement("summary");
        summary.innerHTML = `<span class="synth-q">${escHtml(subq)}</span>`;
        details.appendChild(summary);

        const body = document.createElement("div");
        body.className = "synth-body";
        // Split on newlines for readable paragraphs
        const paragraphs = String(text || "").split(/\n+/).filter(Boolean);
        paragraphs.forEach(p => {
            const para = document.createElement("p");
            para.textContent = p;
            body.appendChild(para);
        });
        details.appendChild(body);
        wrap.appendChild(details);
    });
    return wrap;
}

/**
 * Report — structured field-by-field display.
 * Renders: research_question, overview, detailed_findings, limitations, conclusion
 * as distinct labelled sections — NO raw JSON.
 */
function renderReport(report) {
    const wrap = document.createElement("div");
    wrap.className = "report-wrap";

    if (!Object.keys(report).length) {
        wrap.appendChild(makeEmpty("No report data."));
        return wrap;
    }

    // research_question
    if (report.research_question) {
        wrap.appendChild(reportField("Research Question", report.research_question, "rq"));
    }

    // overview
    if (report.overview) {
        wrap.appendChild(reportField("Overview", report.overview, "overview"));
    }

    // detailed_findings — dict of subq → text
    if (report.detailed_findings && Object.keys(report.detailed_findings).length) {
        const section = document.createElement("div");
        section.className = "report-field";
        const heading = document.createElement("div");
        heading.className = "report-field-label";
        heading.textContent = "Detailed Findings";
        section.appendChild(heading);

        const findingsWrap = document.createElement("div");
        findingsWrap.className = "findings-list";

        Object.entries(report.detailed_findings).forEach(([subq, finding], i) => {
            const item = document.createElement("details");
            item.className = "finding-item";
            if (i === 0) item.open = true;

            const summary = document.createElement("summary");
            summary.innerHTML = `<span>${escHtml(subq)}</span>`;
            item.appendChild(summary);

            const body = document.createElement("div");
            body.className = "finding-body";
            String(finding || "").split(/\n+/).filter(Boolean).forEach(p => {
                const para = document.createElement("p");
                para.textContent = p;
                body.appendChild(para);
            });
            item.appendChild(body);
            findingsWrap.appendChild(item);
        });

        section.appendChild(findingsWrap);
        wrap.appendChild(section);
    }

    // limitations
    if (report.limitations) {
        wrap.appendChild(reportField("Limitations", report.limitations, "limits"));
    }

    // conclusion
    if (report.conclusion) {
        wrap.appendChild(reportField("Conclusion", report.conclusion, "conclusion"));
    }

    return wrap;
}

/** Single text field in the report */
function reportField(label, text, cssKey) {
    const div = document.createElement("div");
    div.className = `report-field report-field--${cssKey}`;

    const lbl = document.createElement("div");
    lbl.className = "report-field-label";
    lbl.textContent = label;
    div.appendChild(lbl);

    const p = document.createElement("p");
    p.className = "report-field-text";
    p.textContent = text;
    div.appendChild(p);

    return div;
}

// ── Utilities ─────────────────────────────────────────────────────────────────
function makeEmpty(msg) {
    const p = document.createElement("p");
    p.className = "empty-msg";
    p.textContent = msg;
    return p;
}

function escHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}

// ── Reset ─────────────────────────────────────────────────────────────────────
function resetUI() {
    questionInput.value = "";
    showOnly();
    questionInput.focus();
}

// ── Enter key ─────────────────────────────────────────────────────────────────
questionInput.addEventListener("keydown", e => {
    if (e.key === "Enter") submitResearch();
});
