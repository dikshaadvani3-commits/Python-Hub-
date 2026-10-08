"""
Python Hub  |  Developer: Diksha Advani
Run:  streamlit run Python_Hub.py
Needs: Streamlit 1.30 or newer  ->  pip install --upgrade streamlit pandas numpy
Note: 'Bengaluru_House_Data_Cleaned.csv' must be in the same folder (needed for the House Price module).
Tip : keep the '.streamlit/config.toml' file next to this file so tables and inputs also use the dark theme.
"""
from datetime import datetime
from html import escape
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

DEVELOPER = "Diksha Advani"
PROJECT = "Python Hub"
DATA_FILE = Path(__file__).with_name("Bengaluru_House_Data_Cleaned.csv")

# Theme palette
GOLD, ORANGE, RED = "#F59E0B", "#FF8A00", "#EF4444"

st.set_page_config(page_title=PROJECT, page_icon="🐍", layout="wide")

# ------------------------------------------------------------------
# Version guard (clear message instead of a confusing crash)
# ------------------------------------------------------------------
try:
    _ver = tuple(int(x) for x in st.__version__.split(".")[:2])
except ValueError:
    _ver = (99, 0)
if _ver < (1, 30):
    st.error(f"Python Hub needs Streamlit 1.30 or newer (you have {st.__version__}).")
    st.code("pip install --upgrade streamlit", language="bash")
    st.stop()

rerun = getattr(st, "rerun", None) or st.experimental_rerun


def card():
    """Bordered card container."""
    return st.container(border=True)


# ------------------------------------------------------------------
# Modules: icon, subtitle
# ------------------------------------------------------------------
MODULES = {
    "Home":                          ("🏠", "Welcome! All your student tools in one place."),
    "Student Marks":                 ("🎓", "Check your percentage, grade and scholarship eligibility."),
    "Student Performance Dashboard": ("📊", "Analyze your marks with clear, interactive charts."),
    "To-Do List":                    ("📝", "Plan your daily tasks and get them done."),
    "Calculator":                    ("🧮", "Fast and simple calculator with history."),
    "House Price Prediction":        ("🏡", "Predict house prices using real Bengaluru data."),
}

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"## 🐍 {PROJECT}")
    st.caption(f"Developer: **{DEVELOPER}**")
    st.markdown("---")
    page = st.radio(
        "Module", list(MODULES), key="nav",
        format_func=lambda n: f"{MODULES[n][0]}  {n}",
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("🚀 Final Year Project")

ICON, SUB = MODULES[page]

# ------------------------------------------------------------------
# THEME: Black + Gold + Orange + Red
#   Fonts : Poppins (headings) • Inter (body) • JetBrains Mono (numbers / calculator)
# ------------------------------------------------------------------
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&family=Poppins:wght@600;700;800&display=swap');

:root {
  --bg:#090909; --card:#171717; --side:#0D0D0D; --line:#292929;
  --gold:#F59E0B; --gold-l:#FBBF24; --orange:#FF8A00; --red:#EF4444;
  --text:#FAFAFA; --muted:#A3A3A3;
  --f-body:'Inter','Segoe UI',Arial,sans-serif;
  --f-head:'Poppins','Inter','Segoe UI',Arial,sans-serif;
  --f-mono:'JetBrains Mono','Courier New',monospace;
}

/* ---------- fonts ---------- */
html, body, .stApp, [data-testid="stMarkdownContainer"], button, input, textarea, select, label {
  font-family:var(--f-body);
}
h1, h2, h3, h4, h5, h6 { font-family:var(--f-head) !important; color:var(--text) !important; letter-spacing:.2px; }

/* ---------- background (moving glow + floating orb animation) ---------- */
.stApp { 
  background: var(--bg); 
  color: var(--text); 
}

.stApp::before {
  content: ""; 
  position: fixed; 
  inset: -50%; 
  pointer-events: none; 
  z-index: 0;
  background:
    radial-gradient(circle at 20% 20%, rgba(245,158,11,.18), transparent 40%),
    radial-gradient(circle at 80% 30%, rgba(255,138,0,.15), transparent 38%),
    radial-gradient(circle at 50% 80%, rgba(239,68,68,.15), transparent 40%);
  animation: backgroundGlow 12s ease-in-out infinite alternate;
}

.stApp::after {
  content: ""; 
  position: fixed; 
  width: 250px; 
  height: 250px; 
  right: 5%; 
  top: 15%; 
  z-index: 0; 
  pointer-events: none;
  background: radial-gradient(circle, rgba(245,158,11,.25) 0%, rgba(255,138,0,0) 70%); 
  border-radius: 50%; 
  filter: blur(40px);
  animation: floatingOrb 10s ease-in-out infinite alternate;
}

[data-testid="stSidebar"], .block-container { position:relative; z-index:1; }
.block-container { max-width:1100px; padding-top:1.6rem; }

/* ---------- keyframes ---------- */
@keyframes backgroundGlow { 
  0%   { transform: rotate(0deg) scale(1); opacity: .75; } 
  50%  { transform: rotate(180deg) scale(1.1); opacity: 1; } 
  100% { transform: rotate(360deg) scale(1); opacity: .75; } 
}

@keyframes floatingOrb { 
  0%   { transform: translate(0, 0) scale(1); } 
  50%  { transform: translate(-100px, 120px) scale(1.2); } 
  100% { transform: translate(40px, -50px) scale(0.9); } 
}

@keyframes headerGlow     { 0%{box-shadow:0 0 10px rgba(245,158,11,.08)} 50%{box-shadow:0 0 25px rgba(245,158,11,.18),0 0 45px rgba(255,138,0,.08)} 100%{box-shadow:0 0 15px rgba(239,68,68,.12)} }
@keyframes ph-line  { from{background-position:0% 0} to{background-position:300% 0} }
@keyframes ph-rise  { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
@keyframes ph-pop   { 0%{opacity:0;transform:scale(.93)} 100%{opacity:1;transform:scale(1)} }
@keyframes ph-shine { 0%{left:-60%} 60%,100%{left:130%} }
@keyframes ph-grow  { from{transform:scaleX(0)} to{transform:scaleX(1)} }
@keyframes ph-pulse { 0%,100%{box-shadow:0 0 0 0 rgba(245,158,11,.45)} 50%{box-shadow:0 0 0 8px rgba(245,158,11,0)} }
@keyframes ph-blink { 50%{opacity:0} }
@keyframes ph-tilt  { 0%,100%{transform:rotate(-6deg)} 50%{transform:rotate(6deg)} }

/* ---------- top colour line + hide default chrome ---------- */
header[data-testid="stHeader"] { background:transparent; }
header[data-testid="stHeader"]::before {
  content:""; position:absolute; top:0; left:0; right:0; height:3px;
  background:linear-gradient(90deg,#F59E0B,#FF8A00,#EF4444,#F59E0B); background-size:300% 100%;
  animation:ph-line 6s linear infinite;
}
#MainMenu, footer { visibility:hidden; }

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] { background:var(--side); border-right:1px solid var(--line); }
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color:var(--gold-l) !important; }
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label { color:var(--text); }
section[data-testid="stSidebar"] div[role="radiogroup"] { gap:8px; }
section[data-testid="stSidebar"] div[role="radiogroup"] label {
  background:var(--card); border:1px solid var(--line); border-radius:12px; padding:10px 14px; width:100%; transition:all .25s ease;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover { border-color:var(--gold); transform:translateX(5px); }
section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child { display:none; }
section[data-testid="stSidebar"] div[role="radiogroup"] label p { margin:0; font-weight:600; }
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
  background:linear-gradient(90deg,var(--gold),var(--orange)); border-color:var(--gold); animation:ph-pulse 2.4s infinite;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p { color:#090909 !important; font-weight:700; }

/* ---------- text ---------- */
p, label { color:var(--text); }
hr { border-color:var(--line); }
div[data-testid="stCaptionContainer"], .stCaption { color:var(--muted) !important; }
.muted { color:var(--muted) !important; } .primary { color:var(--gold) !important; }
.secondary { color:var(--orange) !important; } .accent { color:var(--red) !important; } .highlight { color:var(--gold-l) !important; }
.gold-glow   { color:var(--gold-l); text-shadow:0 0 10px rgba(251,191,36,.45); }
.orange-glow { color:var(--orange); text-shadow:0 0 10px rgba(255,138,0,.40); }
.red-glow    { color:var(--red);    text-shadow:0 0 10px rgba(239,68,68,.40); }

/* ---------- page header ---------- */
.dashboard-header {
  position:relative; overflow:hidden; display:flex; align-items:center; gap:20px;
  background:linear-gradient(135deg,#171717,#0D0D0D); border:1px solid var(--gold); border-radius:18px;
  padding:22px 26px; margin-bottom:18px; animation:headerGlow 4s ease-in-out infinite alternate;
}
.dashboard-header::after {
  content:""; position:absolute; top:0; left:-60%; width:40%; height:100%; transform:skewX(-20deg);
  background:linear-gradient(100deg,transparent,rgba(251,191,36,.14),transparent); animation:ph-shine 5s ease-in-out infinite;
}
.dashboard-header h1 { margin:0; padding:0; font-size:32px; font-weight:800; color:var(--gold-l) !important; }
.dashboard-header p  { margin:4px 0 0; color:var(--muted); }
.hdr-icon {
  font-size:40px; width:70px; height:70px; flex:none; display:flex; align-items:center; justify-content:center;
  background:var(--side); border:1px solid var(--gold); border-radius:18px; animation:ph-tilt 4s ease-in-out infinite;
}
.clock-bar {
  display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap; padding:9px 18px; margin-bottom:6px;
  background:var(--card); border:1px solid var(--line); border-radius:12px; font-size:13px; font-weight:600;
}
.clock-bar b { color:var(--gold-l); font-family:var(--f-mono); font-weight:700; }

.sec { font-family:var(--f-head); font-size:18px; font-weight:700; margin:26px 0 12px; display:flex; align-items:center; gap:12px; color:var(--gold-l); }
.sec::after { content:""; flex:1; height:2px; transform-origin:left; animation:ph-grow .9s ease both; background:linear-gradient(90deg,var(--gold),transparent); }

/* ---------- cards / metrics ---------- */
.custom-card, .metric-card {
  background:var(--card); border:1px solid var(--line); border-radius:16px; padding:20px; margin:10px 0; transition:all .3s ease;
}
.custom-card:hover { border-color:var(--gold); box-shadow:0 0 20px rgba(245,158,11,.12); }
.metric-card { text-align:center; margin:0; height:100%; animation:ph-pop .5s ease both; }
.metric-card:hover { border-color:var(--gold); transform:translateY(-3px); box-shadow:0 0 18px rgba(245,158,11,.15); }
.metric-title { color:var(--muted); font-size:13px; font-weight:500; margin-bottom:8px; text-transform:uppercase; letter-spacing:.8px; }
.metric-value { color:var(--gold-l); font-family:var(--f-mono); font-size:26px; font-weight:700; word-break:break-word; }
div[data-testid="stVerticalBlockBorderWrapper"] { background:var(--card); border:1px solid var(--line) !important; border-radius:16px; transition:all .3s ease; }
div[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color:var(--gold) !important; box-shadow:0 0 20px rgba(245,158,11,.10); }

.welcome-box {
  background:linear-gradient(135deg,#171717 0%,#211111 55%,#171717 100%); border:1px solid var(--gold);
  border-radius:18px; padding:25px; box-shadow:0 0 25px rgba(245,158,11,.08);
}
.welcome-box h2 { margin:0 0 6px; font-size:30px; } .welcome-box p { margin:0; color:var(--muted); font-size:15px; }

.grade-a, .grade-b, .grade-c { display:inline-block; padding:5px 14px; border-radius:20px; font-family:var(--f-head); font-weight:700; }
.grade-a { background:var(--gold);   color:#090909; }
.grade-b { background:var(--orange); color:#090909; }
.grade-c { background:var(--red);    color:#fff; }

.footer { text-align:center; color:var(--muted); padding:20px; border-top:1px solid var(--line); margin-top:30px; }
.footer span { color:var(--gold-l); font-weight:600; }

/* ---------- buttons ---------- */
.stButton > button, .stFormSubmitButton > button {
  position:relative; overflow:hidden; width:100%; background:linear-gradient(90deg,var(--gold),var(--orange)); color:#090909;
  border:none; border-radius:10px; font-weight:700; padding:10px 20px; transition:all .3s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  background:linear-gradient(90deg,var(--gold-l),var(--red)); color:#fff; transform:translateY(-2px); box-shadow:0 0 18px rgba(239,68,68,.30);
}
.stButton > button:active, .stFormSubmitButton > button:active { transform:scale(.96); }
.stButton > button::after, .stFormSubmitButton > button::after {
  content:""; position:absolute; top:0; left:-70%; width:40%; height:100%; transform:skewX(-20deg); background:rgba(255,255,255,.35);
}
.stButton > button:hover::after, .stFormSubmitButton > button:hover::after { left:130%; transition:left .6s ease; }
.stButton > button p, .stFormSubmitButton > button p { color:inherit !important; }

/* ---------- inputs & widgets fix ---------- */
div[data-baseweb="input"], 
div[data-baseweb="select"] > div, 
div[data-baseweb="base-input"] { 
  background: var(--card) !important; 
  border: 1px solid var(--line) !important; 
  border-radius: 10px !important; 
}

div[data-baseweb="input"]:focus-within, 
div[data-baseweb="select"] > div:focus-within { 
  border-color: var(--gold) !important; 
  box-shadow: 0 0 12px rgba(245,158,11,.30) !important; 
}

/* Fix text color inside input fields to prevent white background/invisible text */
div[data-baseweb="input"] input, 
div[data-baseweb="base-input"] input, 
textarea, 
select { 
  color: var(--text) !important; 
  background-color: transparent !important; 
  -webkit-text-fill-color: var(--text) !important;
}

div[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:14px; overflow:hidden; }
div[data-testid="stAlert"] { background:var(--card); border:1px solid var(--gold); border-radius:12px; color:var(--text); animation:ph-pop .4s ease both; }
div[data-testid="stProgress"] [role="progressbar"] > div, div[data-testid="stProgressBar"] > div > div {
  background:linear-gradient(90deg,var(--gold),var(--orange),var(--red)) !important;
}
.stTabs [data-baseweb="tab"] { color:var(--muted); }
.stTabs [aria-selected="true"] { color:var(--gold-l) !important; }
.stTabs [data-baseweb="tab-highlight"] { background:var(--gold); }

/* ---------- home ---------- */
.card-icon  { font-size:38px; display:inline-block; transition:transform .3s ease; }
div[data-testid="stVerticalBlockBorderWrapper"]:hover .card-icon { transform:scale(1.18) rotate(-6deg); }
.card-title { font-family:var(--f-head); font-size:17px; font-weight:700; color:var(--text); margin:8px 0 4px; }
.card-desc  { font-size:13px; color:var(--muted); margin-bottom:6px; min-height:38px; }

/* ---------- to-do ---------- */
.task-item { background:var(--card); border:1px solid var(--line); border-left:4px solid var(--gold); border-radius:12px; padding:10px 16px; font-weight:500; transition:all .25s ease; }
.task-item:hover { transform:translateX(6px); border-color:var(--gold); }
.task-item.done { border-left-color:var(--muted); color:var(--muted); text-decoration:line-through; }

/* ---------- calculator ---------- */
.calc-screen {
  display:flex; justify-content:center; align-items:center; gap:18px; padding:18px; border-radius:14px; flex-wrap:wrap;
  background:var(--bg); border:1px solid var(--gold); box-shadow:inset 0 0 22px rgba(245,158,11,.12);
  font-family:var(--f-mono); font-size:30px; font-weight:700; color:var(--gold-l);
}
.calc-screen .sym { color:var(--red); } .calc-screen .cur { animation:ph-blink 1s infinite; }
.result-box { margin-top:14px; text-align:center; animation:ph-pop .5s ease both; }
.result-box small { color:var(--muted); } .result-box h2 { margin:6px 0 0; font-size:42px; font-family:var(--f-mono) !important; }
.hist-item { background:var(--card); border:1px solid var(--line); border-left:4px solid var(--orange); border-radius:10px; padding:8px 14px; margin-bottom:6px; font-family:var(--f-mono); font-size:14px; animation:ph-rise .4s ease both; }
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def header():
    st.markdown(
        f'<div class="dashboard-header"><div class="hdr-icon">{ICON}</div>'
        f'<div><h1>{page}</h1><p>{SUB}</p></div></div>',
        unsafe_allow_html=True,
    )
    now = datetime.now()
    greet = "Good morning" if now.hour < 12 else "Good afternoon" if now.hour < 17 else "Good evening"
    st.markdown(
        f'<div class="clock-bar"><span>{greet} 👋 &nbsp;|&nbsp; {DEVELOPER}</span>'
        f'<b>{now.strftime("%a, %d %b %Y")}</b></div>',
        unsafe_allow_html=True,
    )


def section(text):
    st.markdown(f'<div class="sec">{text}</div>', unsafe_allow_html=True)


def metric(col, title, value):
    col.markdown(
        f'<div class="metric-card"><div class="metric-title">{title}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )


header()

# ==================================================================
# HOME
# ==================================================================
if page == "Home":

    def open_page(name):
        st.session_state.nav = name  # switches the sidebar radio

    st.markdown(
        f'<div class="welcome-box"><h2 class="gold-glow">Welcome to {PROJECT}</h2>'
        f'<p>Five smart tools for students — marks, performance analysis, to-dos, a calculator '
        f'and house price prediction, all in one app.</p></div>',
        unsafe_allow_html=True,
    )
    st.write("")
    h1, h2, h3 = st.columns(3)
    metric(h1, "Tools", "5")
    metric(h2, "Built With", "Python")
    metric(h3, "Developer", DEVELOPER)

    section("✨ Modules (click to open)")
    names = [n for n in MODULES if n != "Home"]
    for row in (names[:3], names[3:]):
        for col, n in zip(st.columns(3), row):
            icon, desc = MODULES[n]
            with col:
                with card():
                    st.markdown(
                        f'<div class="card-icon">{icon}</div><div class="card-title">{n}</div>'
                        f'<div class="card-desc">{desc}</div>',
                        unsafe_allow_html=True,
                    )
                    st.button("Open →", key=f"open_{n}", on_click=open_page, args=(n,))

# ==================================================================
# STUDENT MARKS
# ==================================================================
elif page == "Student Marks":
    SUBJECTS = ["Math", "English", "Hindi", "Science", "Computer"]
    with card():
        a, b = st.columns([2, 1])
        name = a.text_input("Your name")
        age = b.number_input("Age", 1, 100, 18)

        section("📚 Enter your marks (out of 100)")
        cols = st.columns(5)
        marks = [cols[i].number_input(s, 0.0, 100.0, key=f"m_{s}") for i, s in enumerate(SUBJECTS)]
        code = st.text_input("Scholarship code", placeholder="SCH100 / SCH200 / SCH300")
        go = st.button("Show Result")

    if go:
        if not name.strip():
            st.warning("Please enter your name first.")
        else:
            total = sum(marks)
            pct = total / 5
            grade = "A+" if pct >= 90 else "A" if pct >= 75 else "B" if pct >= 60 else "C" if pct >= 40 else "Fail"
            badge = "grade-a" if pct >= 75 else "grade-b" if pct >= 60 else "grade-c"

            st.success(f"Hello {name.strip()} 👋")
            section("🏅 Result")
            m1, m2, m3 = st.columns(3)
            metric(m1, "Total Marks", f"{total:g} / 500")
            metric(m2, "Percentage", f"{pct:.2f}%")
            metric(m3, "Grade", f'<span class="{badge}">{grade}</span>')
            st.write("")
            st.progress(min(pct / 100, 1.0))

            section("✅ Eligibility")
            e1, e2, e3 = st.columns(3)
            (e1.success if 18 <= age <= 25 else e1.error)("Age: Allowed" if 18 <= age <= 25 else "Age: Not Allowed")
            (e2.success if pct >= 75 else e2.error)("Percentage: Eligible" if pct >= 75 else "Percentage: Not Eligible")
            ok = code.strip().upper() in ("SCH100", "SCH200", "SCH300")
            (e3.success if ok else e3.error)("Scholarship: Eligible" if ok else "Scholarship: Not Eligible")
            if pct >= 90:
                st.balloons()

# ==================================================================
# STUDENT PERFORMANCE DASHBOARD
# ==================================================================
elif page == "Student Performance Dashboard":
    section("✏️ Edit your marks (click any cell to change it)")
    default = pd.DataFrame(
        {"Unit Test": [72, 65, 80, 70, 85], "Mid Term": [78, 70, 82, 75, 88],
         "Pre-Board": [84, 74, 85, 80, 90], "Final": [88, 79, 87, 85, 94]},
        index=["Math", "English", "Hindi", "Science", "Computer"],
    )
    df = st.data_editor(default, key="perf_table").clip(0, 100)

    subject_avg = df.mean(axis=1)
    exam_avg = df.mean(axis=0)
    growth = exam_avg.iloc[-1] - exam_avg.iloc[0]

    section("📌 Summary")
    a, b, c, d = st.columns(4)
    metric(a, "Overall Average", f"{subject_avg.mean():.1f}%")
    metric(b, "Best Subject", subject_avg.idxmax())
    metric(c, "Needs Focus", subject_avg.idxmin())
    metric(d, "Improvement", f"{growth:+.1f}%")

    g1, g2 = st.columns(2)
    with g1:
        section("📊 Subject-wise Average")
        st.bar_chart(subject_avg, color=GOLD)
    with g2:
        section("📈 Exam-wise Progress")
        st.line_chart(exam_avg, color=RED)

    weak = subject_avg.idxmin()
    st.info(f"💡 Tip: **{weak}** has the lowest average ({subject_avg.min():.1f}%). Give it some extra practice!")

# ==================================================================
# TO-DO LIST
# ==================================================================
elif page == "To-Do List":
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
        st.session_state.next_id = 1

    def toggle(task_id):
        for t in st.session_state.tasks:
            if t["id"] == task_id:
                t["done"] = st.session_state[f"chk{task_id}"]

    def delete(task_id):
        st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]

    def clear_done():
        st.session_state.tasks = [t for t in st.session_state.tasks if not t["done"]]

    section("➕ New Task")
    with st.form("add_task", clear_on_submit=True):
        title = st.text_input("Type your task and press Enter", placeholder="e.g. Finish the Maths assignment")
        if st.form_submit_button("Add Task") and title.strip():
            st.session_state.tasks.append({"id": st.session_state.next_id, "title": title.strip(), "done": False})
            st.session_state.next_id += 1
            rerun()

    tasks = st.session_state.tasks
    total = len(tasks)
    done = sum(t["done"] for t in tasks)
    section("📊 Progress")
    a, b, c = st.columns(3)
    metric(a, "Total Tasks", total)
    metric(b, "Pending", total - done)
    metric(c, "Completed", done)
    st.write("")
    st.progress(done / total if total else 0.0, text=f"{done} / {total} tasks complete")

    section("📋 Your Tasks")
    if not tasks:
        st.info("No tasks yet. Add one above 👆")
    for t in tasks:
        c1_, c2_, c3_ = st.columns([0.08, 0.77, 0.15])
        c1_.checkbox("done", value=t["done"], key=f"chk{t['id']}", on_change=toggle, args=(t["id"],), label_visibility="collapsed")
        css_cls = "task-item done" if t["done"] else "task-item"
        c2_.markdown(f'<div class="{css_cls}">{escape(t["title"])}</div>', unsafe_allow_html=True)
        c3_.button("🗑", key=f"del{t['id']}", on_click=delete, args=(t["id"],))

    if done:
        st.write("")
        st.button("🧹 Clear completed tasks", on_click=clear_done)

# ==================================================================
# CALCULATOR
# ==================================================================
elif page == "Calculator":
    OPS = {
        "➕ Addition": ("+", lambda a, b: a + b),
        "➖ Subtraction": ("−", lambda a, b: a - b),
        "✖️ Multiplication": ("×", lambda a, b: a * b),
        "➗ Division": ("÷", lambda a, b: a / b),
        "⚡ Power": ("^", lambda a, b: a ** b),
        "📐 Modulus": ("%", lambda a, b: a % b),
    }
    if "history" not in st.session_state:
        st.session_state.history = []

    left, right = st.columns([3, 2])
    with left:
        with card():
            screen = st.empty()  # live screen (filled after the inputs)
            x, y = st.columns(2)
            n1 = x.number_input("First number", value=0.0, key="n1")
            n2 = y.number_input("Second number", value=0.0, key="n2")
            op = st.selectbox("Choose operation", list(OPS))
            go = st.button("Calculate")
            symbol, fn = OPS[op]
            screen.markdown(
                f'<div class="calc-screen"><span>{n1:g}</span><span class="sym">{symbol}</span>'
                f'<span>{n2:g}</span><span>=</span><span class="cur">?</span></div>',
                unsafe_allow_html=True,
            )

        if go:
            try:
                res = fn(n1, n2)
                st.session_state.history.insert(0, f"{n1:g} {symbol} {n2:g} = {res:g}")
                st.markdown(
                    f'<div class="welcome-box result-box"><small>{op}</small><h2 class="gold-glow">{res:g}</h2></div>',
                    unsafe_allow_html=True,
                )
            except (ZeroDivisionError, OverflowError):
                st.error("This calculation is not possible (division by zero or number too large).")

    with right:
        section("🕘 History")
        if st.session_state.history:
            for h in st.session_state.history[:8]:
                st.markdown(f'<div class="hist-item">{h}</div>', unsafe_allow_html=True)
            st.button("Clear History", on_click=lambda: st.session_state.history.clear())
        else:
            st.caption("No calculations yet.")

# ==================================================================
# HOUSE PRICE PREDICTION  (Real Bengaluru dataset + Linear Regression)
# ==================================================================
elif page == "House Price Prediction":
    if not DATA_FILE.exists():
        st.error(f"Dataset file not found: `{DATA_FILE.name}` — place it in the same folder as this app file.")
        st.stop()

    @st.cache_data
    def load_data_and_model(path):
        data = pd.read_csv(path)
        top = data["location"].value_counts().head(15).index.tolist()
        locs = top + ["Other"]
        data["loc"] = data["location"].where(data["location"].isin(top), "Other")

        def features(d):
            cols = [(d["loc"] == l).astype(float) for l in locs]
            return np.column_stack(cols + [d["total_sqft"], d["bhk"], d["bath"], d["balcony"]])

        X, y = features(data), data["price"].values
        idx = np.random.default_rng(1).permutation(len(y))
        cut = int(0.8 * len(y))
        train, test = idx[:cut], idx[cut:]
        w, *_ = np.linalg.lstsq(X[train], y[train], rcond=None)
        pred = X[test] @ w
        r2 = 1 - ((y[test] - pred) ** 2).sum() / ((y[test] - y[test].mean()) ** 2).sum()
        mae = np.abs(y[test] - pred).mean()
        return data, top, locs, w, r2, mae

    data, top, locs, w, r2, mae = load_data_and_model(DATA_FILE)

    def predict(location, sqft, bhk, bath, balcony):
        loc = location if location in top else "Other"
        row = [1.0 if l == loc else 0.0 for l in locs] + [sqft, bhk, bath, balcony]
        return max(float(np.dot(w, row)), 10.0)

    def fmt(lakh):
        return f"₹ {lakh / 100:.2f} Crore" if lakh >= 100 else f"₹ {lakh:.1f} Lakh"

    section("📌 Dataset & Model")
    a, b, c, d = st.columns(4)
    metric(a, "Houses in Dataset", f"{len(data):,}")
    metric(b, "Locations", f"{int(data['location'].nunique()):,}")
    metric(c, "Model R² Score", f"{r2:.2f}")
    metric(d, "Avg Error (MAE)", f"₹{mae:.0f}L")

    section("🏡 Enter the house details")
    with card():
        l1, l2 = st.columns(2)
        location = l1.selectbox("Location", top + ["Other"], help="Top 15 areas; all other areas fall under 'Other'.")
        sqft = l2.slider("Area (sq ft)", 400, 5000, 1200, 50)
        k1, k2, k3 = st.columns(3)
        bhk = k1.selectbox("BHK", [1, 2, 3, 4, 5, 6], index=1)
        bath = k2.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1)
        balcony = k3.selectbox("Balconies", [0, 1, 2, 3], index=1)
        go = st.button("💰 Predict Price")

    if go:
        p = predict(location, sqft, bhk, bath, balcony)
        st.markdown(
            f'<div class="welcome-box result-box"><small>Estimated Price • {location}</small>'
            f'<h2 class="gold-glow">{fmt(p)}</h2>'
            f'<small>≈ ₹ {p * 100000 / sqft:,.0f} per sq ft</small></div>',
            unsafe_allow_html=True,
        )
        st.balloons()

    tab1, tab2, tab3 = st.tabs(["📈 Area vs Price", "📍 Location Prices", "🗂 Dataset"])
    with tab1:
        areas = np.arange(400, 5050, 100)
        st.line_chart(pd.DataFrame({"Price (Lakh)": [predict(location, s, bhk, bath, balcony) for s in areas]}, index=areas), color=GOLD)
        st.caption("How the price grows with area for the selected location, BHK, bathrooms and balconies.")
    with tab2:
        pps = (data["price"] * 100000 / data["total_sqft"]).groupby(data["location"]).mean()
        st.bar_chart(pps[top].sort_values(ascending=False).round(0), color=ORANGE)
        st.caption("Average price per sq ft (₹) for the top 15 locations.")
    with tab3:
        st.dataframe(data.drop(columns="loc").head(100))
        st.caption("Source: Bengaluru House Price Data (public Kaggle dataset) • prices are in ₹ Lakh.")

    st.caption("Model: Linear Regression (80% train / 20% test) • Dataset covers Bengaluru only.")

st.markdown(f'<div class="footer">Made with ❤️ by <span>{DEVELOPER}</span> • {PROJECT}</div>', unsafe_allow_html=True)