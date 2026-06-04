import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #09090e;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.06) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 5rem; max-width: 1180px; }

/* ── Hero ── */
.hero {
    padding: 3.5rem 0 2rem;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 0.9rem;
    opacity: 0.85;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.6rem, 5.5vw, 4.6rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: #f0ebe0;
    margin: 0 0 0.9rem;
}
.hero h1 span { color: #ff8c32; }
.hero-sub {
    font-size: 1rem;
    font-weight: 300;
    color: #857e76;
    max-width: 500px;
    line-height: 1.7;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.25), transparent);
    margin: 2rem 0;
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,140,50,0.12);
    border-radius: 14px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.5rem;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,140,50,0.2) !important;
    border-radius: 8px !important;
    color: #f0ebe0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.97rem !important;
    padding: 0.72rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.1) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff501a 100%) !important;
    color: #09090e !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.68rem 2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 18px rgba(255,140,50,0.28) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(255,140,50,0.38) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.9rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, background 0.3s;
}
.step-card.active {
    border-color: rgba(255,140,50,0.35);
    background: rgba(255,140,50,0.035);
}
.step-card.done {
    border-color: rgba(80,200,120,0.25);
    background: rgba(80,200,120,0.025);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: rgba(255,255,255,0.04);
    transition: background 0.3s;
}
.step-card.active::before { background: #ff8c32; }
.step-card.done::before   { background: #50c878; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: #ff8c32;
    opacity: 0.65;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #e8e4dc;
}
.step-desc {
    font-size: 0.78rem;
    color: #5a5248;
    margin-top: 0.2rem;
    padding-left: calc(1.4rem + 0.75rem);
}
.step-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
}
.status-waiting { color: #3a3530; }
.status-running { color: #ff8c32; }
.status-done    { color: #50c878; }

/* ── Result panels ── */
.result-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1rem;
}
.result-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 0.9rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(255,140,50,0.12);
}
.result-content {
    font-size: 0.88rem;
    line-height: 1.8;
    color: #b0a89e;
    white-space: pre-wrap;
}

/* ── Report & feedback ── */
.report-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,140,50,0.18);
    border-radius: 14px;
    padding: 2rem 2.4rem;
    margin-top: 0.8rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(80,200,120,0.18);
    border-radius: 14px;
    padding: 2rem 2.4rem;
    margin-top: 0.8rem;
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.1rem;
    padding-bottom: 0.65rem;
}
.panel-label.orange {
    color: #ff8c32;
    border-bottom: 1px solid rgba(255,140,50,0.12);
}
.panel-label.green {
    color: #50c878;
    border-bottom: 1px solid rgba(80,200,120,0.12);
}

.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #e8e4dc;
    margin: 1.5rem 0 0.8rem;
    letter-spacing: -0.01em;
}

.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #3a3530;
    text-align: center;
    margin-top: 4rem;
    letter-spacing: 0.1em;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    color: #ff8c32 !important;
    border: 1px solid rgba(255,140,50,0.3) !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.5rem 1.4rem !important;
    transition: border-color 0.2s, background 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(255,140,50,0.08) !important;
    border-color: rgba(255,140,50,0.5) !important;
}

/* ── Expander ── */
details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #5a5248 !important;
    letter-spacing: 0.1em !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: step card ─────────────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("RUNNING", "status-running"),
        "done":    ("DONE",    "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div class='step-desc'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout ────────────────────────────────────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
    )
    run_btn = st.button("Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;align-items:center;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#3a3530;letter-spacing:0.15em;">TRY</span>
    """, unsafe_allow_html=True)
    for ex in ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]:
        st.markdown(f"""
        <span style="
            background:rgba(255,255,255,0.03);
            border:1px solid rgba(255,255,255,0.07);
            border-radius:5px;
            padding:0.22rem 0.65rem;
            font-size:0.73rem;
            color:#857e76;
            font-family:'DM Sans',sans-serif;
        ">{ex}</span>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def s(step):
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes and extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews and scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    with st.spinner("Search Agent working..."):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("Reader Agent scraping top resources..."):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("Writer drafting the report..."):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    with st.spinner("Critic reviewing the report..."):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results ───────────────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("Search Results (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Search Agent Output</div>'
                f'<div class="result-content">{r["search"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("Scraped Content (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Reader Agent Output</div>'
                f'<div class="result-content">{r["reader"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)