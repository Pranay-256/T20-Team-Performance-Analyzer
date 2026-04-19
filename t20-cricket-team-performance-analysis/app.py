import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
if "df2" not in st.session_state:
    st.session_state.df2 = None

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="T20 Cricket Team Performance Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap" rel="stylesheet">

<style>

/* ── Root tokens ─────────────────────────────────────────── */
:root {
    --bg-base:      #0d1117;
    --bg-card:      #161b22;
    --bg-card2:     #1c2330;
    --border:       #2a3444;
    --gold:         #c9a84c;
    --gold-light:   #e0c070;
    --teal:         #2dd4bf;
    --teal-dim:     #1a9e8f;
    --text-primary: #e6edf3;
    --text-muted:   #8b949e;
    --text-accent:  #c9a84c;
    --danger:       #e05252;
    --success:      #3fb950;
    --tab-active:   #c9a84c;
}

/* ── Base ────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

/* ── Streamlit chrome overrides ──────────────────────────── */
.stApp { background-color: var(--bg-base) !important; }
header[data-testid="stHeader"] { background: var(--bg-base) !important; border-bottom: 1px solid var(--border); }

/* ── FIX #6: Shift content up — reduce top padding ──────── */
.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}

/* ── FIX #1: Dataframe visibility fix ───────────────────── */
/* ── SAFE DATAFRAME STYLING (STREAMLIT-COMPATIBLE) ── */

/* Outer container */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--bg-card) !important;
    padding: 4px;
}

/* Inner wrapper */
div[data-testid="stDataFrame"] > div {
    background: var(--bg-card) !important;
}

/* Text color (safe override) */
div[data-testid="stDataFrame"] * {
    color: var(--text-primary) !important;
}

/* Header styling (optional premium touch) */
div[data-testid="stDataFrame"] thead {
    background: rgba(201,168,76,0.08) !important;
}

/* Scrollbar inside dataframe */
div[data-testid="stDataFrame"] ::-webkit-scrollbar {
    height: 6px;
    width: 6px;
}

div[data-testid="stDataFrame"] ::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 4px;
}

div[data-testid="stDataFrame"] ::-webkit-scrollbar-thumb:hover {
    background: var(--gold);
}

/* ── FIX #2: Tab buttons look like real buttons ──────────── */
/* ── PREMIUM BUTTON-LIKE TABS ─────────────────────────── */

/* ── MINIMAL PREMIUM TABS (LIKE STREAMLIT DEFAULT) ───────── */

div[data-baseweb="tab-list"] {
    border-bottom: 1px solid var(--border) !important;
    gap: 18px;
}

/* Individual tabs */
div[data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600;
    font-size: 16px !important;

    color: var(--text-muted) !important;

    padding: 10px 6px !important;
    background: transparent !important;
    border: none !important;

    transition: all 0.2s ease;
}

/* Hover effect (subtle, not button-like) */
div[data-baseweb="tab"]:hover {
    color: var(--gold-light) !important;
}

/* ACTIVE TAB */
div[data-baseweb="tab"][aria-selected="true"] {
    color: var(--gold) !important;
    font-weight: 700 !important;
}

/* 🔥 GOLD UNDERLINE (THIS IS THE KEY PART) */
div[data-baseweb="tab-highlight"] {
    background: linear-gradient(90deg, #c9a84c, #e0c070) !important;
    height: 3px !important;
    border-radius: 2px;
}

/* remove default border line artifacts */
div[data-baseweb="tab-border"] {
    background: transparent !important;
}

/* ── Sidebar ─────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Radio buttons ───────────────────────────────────────── */
div[role="radiogroup"] label {
    font-family: 'Rajdhani', sans-serif !important;
    color: var(--text-primary) !important;
    font-size: 14px;
}

/* ── Buttons ─────────────────────────────────────────────── */
div.stButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700;
    font-size: 15px;
    letter-spacing: 0.5px;
    background: linear-gradient(135deg, #b8922e 0%, #e0c070 100%) !important;
    color: #0d1117 !important;
    border: none !important;
    border-radius: 8px !important;
    height: 46px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 2px 12px rgba(201,168,76,0.15) !important;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #e0c070 0%, #c9a84c 100%) !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.30) !important;
    transform: translateY(-1px) !important;
}

/* ── Download buttons ────────────────────────────────────── */
div.stDownloadButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 500;
    font-size: 14px;
    background: transparent !important;
    color: var(--teal) !important;
    border: 1px solid var(--teal-dim) !important;
    border-radius: 7px !important;
    height: 40px !important;
    transition: all 0.2s ease !important;
}
div.stDownloadButton > button:hover {
    background: rgba(45,212,191,0.08) !important;
    border-color: var(--teal) !important;
    box-shadow: 0 0 10px rgba(45,212,191,0.15) !important;
}

/* ── Selectbox ───────────────────────────────────────────── */
div[data-baseweb="select"] > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
div[data-baseweb="select"] span { color: var(--text-primary) !important; }

/* ── Expanders ───────────────────────────────────────────── */
div[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin-bottom: 10px;
}
div[data-testid="stExpander"] summary {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    color: var(--gold-light) !important;
    padding: 12px 16px !important;
}
div[data-testid="stExpander"] summary:hover {
    background: rgba(201,168,76,0.06) !important;
}
div[data-testid="stExpander"] > div > div {
    padding: 4px 20px 16px 20px !important;
    color: var(--text-primary) !important;
}

/* ── Alerts / messages ───────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
}

/* ── Dividers ────────────────────────────────────────────── */
hr { border-color: var(--border) !important; }

/* ── Pyplot figures background ───────────────────────────── */
div[data-testid="stImage"] img { border-radius: 8px; }

/* ── File uploader ───────────────────────────────────────── */
div[data-testid="stFileUploader"] {
    background: var(--bg-card2) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 10px !important;
    padding: 8px;
}
div[data-testid="stFileUploader"] * { color: var(--text-primary) !important; }

/* ── FIX #5: Markdown / body text font → Rajdhani ────────── */
p, li {
    color: var(--text-primary) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px;
    line-height: 1.7;
}
strong { color: var(--text-primary) !important; font-family: 'Rajdhani', sans-serif !important; }
a { color: var(--teal) !important; text-decoration: none; }
a:hover { text-decoration: underline; color: var(--gold-light) !important; }

/* ── Scrollbar ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CHART THEME
# ─────────────────────────────────────────────────────────────
mpl.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.titlesize":    14,
    "axes.titleweight":  "bold",
    "axes.labelsize":    11,
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "legend.fontsize":   9,
    "legend.framealpha": 1.0,
    "legend.edgecolor":  "#000000",
    "legend.facecolor":  "#ffffff",
    "legend.labelcolor": "#000000",
    "legend.title_fontsize": 9,
})

# ─────────────────────────────────────────────────────────────
# COLOUR PALETTES — thematically matched per chart
# ─────────────────────────────────────────────────────────────
# Batting: warm gold→amber tones (runs = fire)
BATTING_CMAP   = "YlOrRd"
# Bowling: cool blue→teal tones (precision = cool)
BOWLING_CMAP   = "YlGnBu"
# Phase pie: distinct qualitative
PHASE_COLORS   = ["#e05252", "#e0c070", "#3fb950"]
# Role pie (batting): warm earthy
ROLE_BAT_COLORS = ["#c9a84c", "#dd8452", "#4c9be8"]
# Role pie (bowling): cool blues
ROLE_BOWL_COLORS = ["#2dd4bf", "#4c72b0", "#c9a84c"]
# Batting order: viridis stays
ORDER_PAL      = "viridis"
# Runs per match / wickets per match: gold line already set
# Strike rate — role split colours (kept readable)
SR_ROLE_COLORS = {"batsman": "#c9a84c", "all-rounder": "#2dd4bf"}
ECO_ROLE_COLORS = {"bowler": "#4c72b0", "all-rounder": "#2dd4bf"}

# ─────────────────────────────────────────────────────────────
# CHART FIGURE WIDTH  — matches dataframe width in pixels
# The dataframe uses use_container_width=True so we set figsize
# to fill the same space. DPI=120 keeps it sharp.
# ─────────────────────────────────────────────────────────────
BAR_W, BAR_H   = 10, 5      # horizontal bar charts
LINE_W, LINE_H = 8,  5      # line charts
PIE_W,  PIE_H  = 8,  6      # pie charts
SIDE_W, SIDE_H = 10, 4      # side-by-side (summary)

# ─────────────────────────────────────────────────────────────
# HELPER: section heading banner
# ─────────────────────────────────────────────────────────────
def section_heading(icon, title):
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, rgba(201,168,76,0.12) 0%, transparent 100%);
        border-left: 3px solid #c9a84c;
        border-radius: 0 8px 8px 0;
        padding: 10px 18px;
        margin: 18px 0 10px 0;
    ">
        <span style="font-family:'Rajdhani',sans-serif; font-weight:700;
                     font-size:20px; color:#e0c070; letter-spacing:0.4px;">
            {icon}&nbsp; {title}
        </span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HELPER: column info card
# ─────────────────────────────────────────────────────────────
def column_info(title, text):
    st.markdown(f"""
    <div style="
        background: #1c2330;
        border: 1px solid #2a3444;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 8px;
    ">
        <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                  font-size:15px; color:#c9a84c; margin:0 0 4px 0;">{title}</p>
        <p style="font-family:'Rajdhani',sans-serif; font-size:13px;
                  color:#8b949e; margin:0; line-height:1.55;">{text}</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HELPER: KPI card
# ─────────────────────────────────────────────────────────────
def kpi_card(icon, label, value, sub=""):
    sub_html = f"<p style='font-size:12px; color:#8b949e; margin:2px 0 0 0; font-family:Rajdhani,sans-serif;'>{sub}</p>" if sub else ""
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #1c2330, #161b22);
        border: 1px solid #2a3444;
        border-top: 2px solid #c9a84c;
        border-radius: 10px;
        padding: 16px 18px;
        text-align: center;
        height: 100%;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    ">
        <div style="font-size:26px; margin-bottom:6px;">{icon}</div>
        <p style="font-family:'Rajdhani',sans-serif; font-size:12px;
                  color:#8b949e; margin:0 0 4px 0; text-transform:uppercase;
                  letter-spacing:0.8px;">{label}</p>
        <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                  font-size:22px; color:#e0c070; margin:0; line-height:1.1;">{value}</p>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HELPER: insight line
# ─────────────────────────────────────────────────────────────
def insight_line(number, text):
    st.markdown(f"""
    <div style="
        background: #161b22;
        border: 1px solid #2a3444;
        border-left: 3px solid #2dd4bf;
        border-radius: 0 8px 8px 0;
        padding: 10px 16px;
        margin-bottom: 8px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    ">
        <span style="font-family:'Rajdhani',sans-serif; font-weight:700;
                     font-size:16px; color:#2dd4bf; min-width:24px;">{number}.</span>
        <span style="font-family:'Rajdhani',sans-serif; font-size:14px;
                     color:#e6edf3; line-height:1.6;">{text}</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATA VALIDATION
# ─────────────────────────────────────────────────────────────
def data_validation(df):        
    out_over_numeric = pd.to_numeric(df["Out_Over"], errors="coerce")

    invalid_over = out_over_numeric > 20

    match_player_counts = df.groupby("Match_No")["Player_Name"].nunique()

    bat_stats = (df["Batting_Start_Over"].isnull() &
                (df["Out_Over"].notnull() |
                 df["Balls_Played"].notnull() |
                 df["Runs_Scored"].notnull()))

    bat_stats2 = (df["Batting_Start_Over"].notnull() &
                  (df["Out_Over"].isnull() | df["Balls_Played"].isnull() | df["Runs_Scored"].isnull()))

    bat_stats3 = (
        (df["Batting_Start_Over"].notnull()) &
        (out_over_numeric.notnull()) &
        (df["Batting_Start_Over"] > out_over_numeric)
    )

    bowl_stats = ((df["Overs_Bowled"].isnull() | df["Overs_Bowled"] == 0) &
                  (df["Runs_Given"].notnull() | df["Wickets_Taken"].notnull()))
    
    bowl_stats2 = ((df["Overs_Bowled"].notnull()) &
                  (df["Overs_Bowled"] > 0) & 
                  (df["Runs_Given"].isnull() | df["Wickets_Taken"].isnull()))

    invalid_player = ((df["Player_Name"].isnull()) &
                     (df["Role"].notnull() |
                      df["Batting_Position"].notnull() |
                      df["Batting_Start_Over"].notnull() |
                      df["Out_Over"].notnull() |
                      df["Balls_Played"].notnull() |
                      df["Runs_Scored"].notnull() |
                      df["Overs_Bowled"].notnull() |
                      df["Runs_Given"].notnull() |
                      df["Wickets_Taken"].notnull()))

    no_match    = df["Match_No"].isnull()
    no_position = df["Batting_Position"].isnull()

    if invalid_over.any():
        raise ValueError("Current Version only supports T20 data (Out_Over cannot exceed 20)")
    if (match_player_counts > 11).any():
        raise ValueError("A single match cannot have more than 11 players")
    if df["Player_Name"].nunique() > 22:
        raise ValueError("Dataset contains too many unique players. Please limit uploads to 2 matches at a time.")
    if no_match.any():
        raise ValueError("Some players don't have Match Number information")
    elif no_position.any():
        raise ValueError("Some players don't have Batting Position information")
    elif invalid_player.any():
        raise ValueError("Some players don't have their name")
    elif (bat_stats.any()) or (bat_stats2.any()) or (bat_stats3.any()):
        raise ValueError("Invalid data found in batting columns")
    elif (bowl_stats.any()) or (bowl_stats2.any()):
        raise ValueError("Invalid data found in bowling columns")

    return True

# ─────────────────────────────────────────────────────────────
# DATA PROCESSING (CACHED)
# ─────────────────────────────────────────────────────────────
@st.cache_data
def process_data(df):

    df2 = df.copy()

    df2["Role"] = df2["Role"].str.strip().str.lower()
    df2["Role"] = df2["Role"].fillna(df2["Role"].mode()[0])
    df2["Role"] = df2["Role"].replace("wicketkeeper", "batsman")

    df2["Batting_Start_Over"] = df2["Batting_Start_Over"].fillna(0)

    df2["Out_Over"] = pd.to_numeric(df2["Out_Over"], errors="coerce")
    df2["Out_Over"] = df2["Out_Over"].fillna(0)

    df2["Balls_Played"] = df2["Balls_Played"].fillna(0)
    df2["Runs_Scored"]  = df2["Runs_Scored"].fillna(0)
    df2["Overs_Bowled"] = df2["Overs_Bowled"].fillna(0)

    df2.loc[(df2["Overs_Bowled"] > 0) & (df2["Runs_Given"].isnull()), "Runs_Given"] = 0
    df2.loc[(df2["Overs_Bowled"] > 0) & (df2["Wickets_Taken"].isnull()), "Wickets_Taken"] = 0

    df2["Runs_Given"]    = df2["Runs_Given"].fillna(0)
    df2["Wickets_Taken"] = df2["Wickets_Taken"].fillna(0)

    df2["Batted"]  = df2["Batting_Start_Over"] > 0
    df2["Was_Out"] = df2["Out_Over"] > 0

    # Strike Rate
    df2["Strike_Rate"] = 0.0
    df2.loc[df2["Balls_Played"] > 0, "Strike_Rate"] = (
        (df2["Runs_Scored"] / df2["Balls_Played"]) * 100
    )
    df2["Strike_Rate"] = df2["Strike_Rate"].round(2)

    # Economy Rate (FIXED)
    over  = df2["Overs_Bowled"].astype(int)
    balls = ((df2["Overs_Bowled"] - over) * 10).round().astype(int)

    df2["real_over"] = over + (balls / 6)

    df2["Economy_Rate"] = 0.0
    df2.loc[df2["real_over"] > 0, "Economy_Rate"] = (
        df2["Runs_Given"] / df2["real_over"]
    )

    df2.drop(columns=["real_over"], inplace=True)
    df2["Economy_Rate"] = df2["Economy_Rate"].round(2)

    return df2

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
def render_footer():
    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body { margin:0; padding:0; background:transparent; }

        .footer-wrapper {
            display: flex;
            justify-content: space-around;
            text-align: center;
            padding: 28px 0 8px 0;
            border-top: 1px solid #2a3444;
        }

        .footer-item { flex: 1; }

        .footer-item .title {
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            font-size: 16px;
            color: #c9a84c;
            margin-bottom: 4px;
        }

        .footer-item .subtitle {
            font-family: 'Rajdhani', sans-serif;
            color: #8b949e;
            font-size: 13px;
            margin-top: 0;
        }

        .footer-credit {
            text-align: center;
            font-family: 'Rajdhani', sans-serif;
            color: #8b949e;
            font-size: 13px;
            padding: 12px 0 4px 0;
        }
    </style>

    <div class="footer-wrapper">
        <div class="footer-item">
            <p class="title">&#128274; Secure &amp; Reliable</p>
            <p class="subtitle">Your data is processed securely</p>
        </div>
        <div class="footer-item">
            <p class="title">&#9889; Real Time Results</p>
            <p class="subtitle">Instant results in seconds</p>
        </div>
        <div class="footer-item">
            <p class="title">&#128200; 100% Accuracy</p>
            <p class="subtitle">Get 100% accurate Insights</p>
        </div>
    </div>

    <p class="footer-credit">Developed by Pranay Jha &nbsp;|&nbsp; Powered by Python and Streamlit</p>
    """, height=240)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:12px 0 8px 0;'>
        <span style="font-family:'Rajdhani',sans-serif; font-size:28px;
                     font-weight:700; color:#c9a84c; letter-spacing:1px;">
            🏏 Tool Menu
        </span>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("", ["Analyze your Dataset", "About"])

    st.markdown("<hr style='border-color:#2a3444; margin:12px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'Rajdhani',sans-serif; font-size:13px;
                color:#8b949e; line-height:1.9; padding:4px 0;">
        <strong style="color:#c9a84c;">Current Version:</strong> 2.01<br>
        <strong style="color:#c9a84c;">Last Updated:</strong> 18th April 2026<br>
        <strong style="color:#c9a84c;">Initial Release:</strong> 27th February 2026
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────────────────────────
left, center, right = st.columns([1, 3, 1])

with center:

    # ══════════════════════════════════════════════════════
    # ANALYZE PAGE
    # ══════════════════════════════════════════════════════
    if page == "Analyze your Dataset":

        st.markdown("""
        <div style="text-align:center; padding:24px 0 6px 0;">
            <h1 style="font-family:'Rajdhani',sans-serif; font-weight:700;
                       font-size:38px; color:#e0c070; margin:0; letter-spacing:1px;">
                🏏 T20 Team Performance Analyzer
            </h1>
            <p style="font-family:'Rajdhani',sans-serif; font-size:16px;
                      color:#8b949e; margin:6px 0 0 0;">
                Data-Driven Analysis of Your T20 Team Performance
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        tab1, tab2, tab3, tab4 = st.tabs(
            ["📊 Dataset", "🏏 Batting Analytics", "⚾ Bowling Analytics", "📋 Summary"]
        )

        # ══════════════════════════════════════════════════
        # TAB 1 — DATASET
        # ══════════════════════════════════════════════════
        with tab1:

            st.markdown("""
            <p style="color:#8b949e; font-size:13px; margin:6px 0 4px 0;">
                Supports <code style="color:#2dd4bf;">.csv</code> and
                <code style="color:#2dd4bf;">.xlsx</code> file formats
            </p>
            """, unsafe_allow_html=True)

            with open("template.csv", "rb") as f:
                st.download_button("⬇ Download Template Dataset", f, "template.csv")

            st.markdown("""
            <p style="color:#8b949e; font-size:13px;">
                Download the template dataset, fill in your match data, and upload it here.
            </p>
            """, unsafe_allow_html=True)

            st.divider()

            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                      font-size:20px; color:#e0c070; margin:4px 0 8px 0;">
                Upload Your Files
            </p>
            <p style="color:#8b949e; font-size:13px; margin-bottom:10px;">
                For testing refer to the example datasets attached below.
            </p>
            """, unsafe_allow_html=True)

            upload_type    = st.radio("", ["Upload Single Dataset", "Upload Multiple Datasets"])
            uploaded_files = None

            if upload_type == "Upload Single Dataset":
                uploaded_files = st.file_uploader("Upload Single Dataset",  type=["csv","xlsx"], accept_multiple_files=False)
            else:
                uploaded_files = st.file_uploader("Upload Multiple Datasets", type=["csv","xlsx"], accept_multiple_files=True)

            if uploaded_files is None or uploaded_files == []:
                if st.session_state.df2 is not None:
                    st.session_state.df2 = None
                    st.rerun()    

            st.markdown("""
            <p style="color:#8b949e; font-size:13px; margin-top:6px;">
                A single dataset may contain data from one match or multiple matches combined.
            </p>
            """, unsafe_allow_html=True)

            confirm = st.button("Confirm Upload", use_container_width=True)

            if confirm:
                st.session_state.df2 = None

                if uploaded_files is None:
                    st.error("Please upload a dataset first.")
                else:
                    all_datasets = []

                    if not isinstance(uploaded_files, list):
                        file = uploaded_files
                        df_temp = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
                        all_datasets.append(df_temp)
                    else:
                        for file in uploaded_files:
                            df_temp = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
                            all_datasets.append(df_temp)

                    if len(all_datasets) == 0:
                        st.error("No dataset loaded.")
                    else:
                        df = pd.concat(all_datasets, ignore_index=True)

                        try:
                            data_validation(df)
                            st.success(f"Dataset passed data validation | {df.shape[0]} rows loaded")
                           
                            df2 = process_data(df)
                           
                            st.success("Data cleaning and feature engineering completed.")
                            st.session_state.df2 = df2
                        except Exception as err:      
                            st.error(f"Dataset is invalid: {err}")

            st.divider()

            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                      font-size:20px; color:#e0c070; margin:4px 0 10px 0;">
                Dataset Columns Overview
            </p>
            """, unsafe_allow_html=True)

            with st.expander("🙎 Match & Player Info", expanded=False):
                column_info("Match_No",
                    "The match number this player's performance belongs to. "
                    "Use 1 for your first match, 2 for your second, and so on. "
                    "Every row must have a match number — blank values are NOT allowed. "
                    "Preferred datatype: Integer (whole number, e.g. 1, 2, 3).")
            
                column_info("Player_Name",
                    "The full name or short name of the player. Every row must have a name — "
                    "blank values are NOT allowed. Use the same spelling consistently across all matches; "
                    "for example do not write 'Virat Kohli' in one match and 'V Kohli' in another, "
                    "as the tool will treat them as two different players. "
                    "Preferred datatype: Text (e.g. Rohit Sharma).")
            
                column_info("Role",
                    "The player's role in the team. Accepted values are: batsman, bowler, all-rounder, wicketkeeper. "
                    "Capitalisation do not matter — 'Batsman', 'BATSMAN', and 'batsman' are all accepted. However, spelling must be consistent same as the accepted values. "
                    "Blank values are allowed and will be auto-filled with the most common role in the dataset. "
                    "Important: A wicketkeeper who also bats can be entered as wicketkeeper or batsman. If entered wicketkeeper, they will be treated as a batsman for batting stats. "
                    "Preferred datatype: Text.")

            with st.expander("🏏 Batting Info", expanded=False):
                column_info("Batting_Position",
                    "The position at which this player came in to bat, from 1 (opener) to 11 (last). "
                    "Every row must have a batting position — blank values are NOT allowed. "
                    "If two players opened the batting, one gets position 1 and the other gets position 2. "
                    "Do not repeat the same position number for two players in the same match. "
                    "Preferred datatype: Integer (whole number from 1 to 11).")
            
                column_info("Batting_Start_Over",
                    "The over number when this player walked in to bat. "
                    "For example, if a player came in during over 4, enter 4. "
                    "If they came in mid-over (e.g. during the 3rd ball of over 6), you can enter 6.3. "
                    "Leave this blank ONLY if the player did not bat at all in that match. "
                    "This value must always be less than or equal to Out_Over. "
                    "Preferred datatype: Numeric (e.g. 1, 4, 6.3).")
            
                column_info("Out_Over",
                    "The over number when this player got out. "
                    "For example, if a player was dismissed in over 14, enter 14. "
                    "If the player was NOT OUT (finished the innings without getting dismissed), "
                    "leave this blank or write 'not-out' — both are accepted. "
                    "This value must always be greater than or equal to Batting_Start_Over. "
                    "Cannot exceed 20 (this tool only supports T20 matches). "
                    "Preferred datatype: Numeric or leave blank / write not-out for not-out players.")
            
                column_info("Balls_Played",
                    "The total number of balls this player faced during their innings. "
                    "For example, if a player faced 34 balls, enter 34. "
                    "Leave blank ONLY if the player did not bat. "
                    "If a player batted but faced 0 balls (extremely rare), enter 0. "
                    "Must be filled if Batting_Start_Over is filled. "
                    "Preferred datatype: Integer (whole number).")
            
                column_info("Runs_Scored",
                    "The total runs scored by this player in their innings, including extras attributed to them. "
                    "If a player got out for a duck (0 runs), enter 0 — do not leave blank. "
                    "Leave blank ONLY if the player did not bat at all. "
                    "Must be filled if Batting_Start_Over is filled. "
                    "Preferred datatype: Integer (whole number, e.g. 0, 45, 102).")

            with st.expander("⚾ Bowling Info", expanded=False):
                column_info("Overs_Bowled",
                    "The total overs bowled by this player in the match. "
                    "For complete overs, enter a whole number (e.g. 4). "
                    "For partial overs, use one decimal place where the digit after the decimal is the number of balls bowled — "
                    "for example, 3.4 means 3 complete overs and 4 balls (NOT 3.4 overs mathematically). "
                    "Valid ball values after the decimal are 1 through 5 only — "
                    "for example 2.6 is invalid because an over only has 6 balls and .6 would mean a complete over. "
                    "Leave blank or enter 0 if the player did not bowl. "
                    "Preferred datatype: Numeric (e.g. 2, 3.4, 4.0).")
            
                column_info("Runs_Given",
                    "The total runs conceded by this player while bowling (excluding extras not attributed to the bowler). "
                    "If the player bowled but gave 0 runs, enter 0. "
                    "Leave blank ONLY if the player did not bowl — blank values are auto-filled to 0 during cleaning "
                    "for players who have Overs_Bowled filled. "
                    "Must be filled if Overs_Bowled is filled. "
                    "Preferred datatype: Integer (whole number, e.g. 0, 24, 56).")
            
                column_info("Wickets_Taken",
                    "The number of wickets taken by this player while bowling. "
                    "If the player bowled but took no wickets, enter 0 — do not leave blank. "
                    "Leave blank ONLY if the player did not bowl — blank values are auto-filled to 0 during cleaning "
                    "for players who have Overs_Bowled filled. "
                    "Must be filled if Overs_Bowled is filled. "
                    "Runouts are generally not credited to a bowler and should not be counted here. "
                    "Preferred datatype: Integer (whole number, e.g. 0, 1, 2, 3).")

            st.divider()

            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                      font-size:20px; color:#e0c070; margin:4px 0 10px 0;">
                Example Datasets
            </p>
            """, unsafe_allow_html=True)

            with open("RCB_IPL2024_FirstMatch.csv","rb") as f:
                st.download_button("⬇ Download Example Dataset 1", f, "RCB_IPL2024_FirstMatch.csv")
            with open("RCB_IPL2024_Match2_vs_PBKS.csv","rb") as f:
                st.download_button("⬇ Download Example Dataset 2", f, "RCB_IPL2024_Match2_vs_PBKS.csv")
            with open("RCB_IPL2024_Match3_vs_GT.csv","rb") as f:
                st.download_button("⬇ Download Example Dataset 3", f, "RCB_IPL2024_Match3_vs_GT.csv")

            #st.divider()
            st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════
        # TAB 2 — BATTING ANALYTICS
        # ══════════════════════════════════════════════════
        with tab2:

            if st.session_state.df2 is None:
                st.warning("Please upload and confirm your dataset in the Dataset tab first.")
            else:
                df2 = st.session_state.df2

                # ── Individual runs ──
                section_heading("🏏", "Individual Runs Scored by Players")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Total runs scored based on balls faced by each player across all matches,
                    sorted from highest to lowest scorer.
                </p>
                """, unsafe_allow_html=True)

                done_batting = df2[df2["Balls_Played"] > 0]

                runs_difference = (
                    done_batting.groupby("Player_Name")
                    .agg({"Runs_Scored": "sum", "Balls_Played": "sum"})
                    .sort_values(by="Runs_Scored", ascending=False).astype(int).reset_index()
                )
                runs_difference.index = runs_difference.index + 1

                # FIX #1: dataframe above chart, use_container_width fills full width
                st.dataframe(runs_difference[["Player_Name","Runs_Scored","Balls_Played"]], use_container_width=True)

                n = len(runs_difference)
                colors = sns.color_palette(BATTING_CMAP, n)
                fig, ax = plt.subplots(figsize=(BAR_W, BAR_H), dpi=120)
                sns.barplot(y=runs_difference["Player_Name"], x=runs_difference["Runs_Scored"], palette=colors, ax=ax)
                ax.set_title("Individual Runs Scored by Players", fontsize=14, fontweight="bold")
                ax.set_xlabel("Runs Scored", fontsize=11)
                ax.set_ylabel("Players", fontsize=11)
                ax.grid(axis='x', linestyle='--', alpha=0.4)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                st.divider()

                # ── Runs contribution pie ──
                section_heading("📊", "Total Runs Contribution")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Contribution of runs scored by each player to the team's total runs across all matches.
                </p>
                """, unsafe_allow_html=True)                

                top_batters  = runs_difference[["Player_Name","Runs_Scored"]].head(5).reset_index(drop=True)
                other_runs   = runs_difference["Runs_Scored"].sum().astype(int) - top_batters["Runs_Scored"].sum().astype(int)
                batting_data = top_batters.copy()
                batting_data.loc[len(batting_data)] = ["Others", int(other_runs)]
                batting_data = batting_data[batting_data["Runs_Scored"] > 0]

                st.dataframe(batting_data, use_container_width=True)

                pie_colors = sns.color_palette("YlOrRd", len(batting_data))
                fig, ax = plt.subplots(figsize=(PIE_W, PIE_H), dpi=120)
                wedges, texts, autotexts = ax.pie(
                    batting_data["Runs_Scored"], labels=None, autopct="%1.1f%%",
                    startangle=90, wedgeprops={"edgecolor": "black"},
                    colors=pie_colors
                )
                for at in autotexts:
                    at.set_fontsize(9)
                    at.set_fontweight("bold")
                    at.set_color("black")
                legend_labels = [f"{p}  —  {r}" for p, r in zip(batting_data["Player_Name"], batting_data["Runs_Scored"])]
                ax.legend(wedges, legend_labels, title="Players", title_fontsize=9,
                          loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9,
                          framealpha=1.0, edgecolor="#000000", facecolor="#ffffff",
                          labelcolor="#000000")
                ax.set_title("Total Runs Contribution", fontsize=14, fontweight="bold")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                st.divider()

                # ── Runs per match ──
                section_heading("📈", "Player's Total Runs in Each Match")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Total runs scored by each player in each match, allows tracking of performance trends across matches by selecting the player.
                </p>
                """, unsafe_allow_html=True)                

                if done_batting["Match_No"].nunique() > 1:
                    players_list    = sorted(done_batting["Player_Name"].unique())
                    selected_player = st.selectbox("Select Player", players_list)
                    selected_player_df = done_batting[done_batting["Player_Name"] == selected_player]

                    player_runs = (
                        selected_player_df.groupby("Match_No")["Runs_Scored"]
                        .sum().reset_index().sort_values("Match_No")
                    )
                    player_runs["Runs_Scored"] = player_runs["Runs_Scored"].astype(int)
                    player_runs.index += 1

                    st.dataframe(player_runs, use_container_width=True)

                    x_vals = player_runs["Match_No"].astype(int)
                    y_vals = player_runs["Runs_Scored"]

                    fig, ax = plt.subplots(figsize=(LINE_W, LINE_H), dpi=120)
                    sns.lineplot(x=x_vals, y=y_vals, marker="o", color="#c9a84c", ax=ax)
                    ax.set_xticks(x_vals.tolist())
                    ax.set_yticks(y_vals.tolist())
                    ax.set_title(f"{selected_player}'s Total Runs in Each Match", fontsize=14, fontweight="bold")
                    ax.set_xlabel("Match No", fontsize=11)
                    ax.set_ylabel("Runs Scored", fontsize=11)
                    ax.grid(linestyle='--', alpha=0.4)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.warning("Player's Total Runs in Each Match is not applicable for a single-match dataset.")

                st.divider()

                # ── Runs by role ──
                section_heading("🎭", "Runs Scored Contribution Based on Roles")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Total runs scored by players based on their roles (batsman, bowler, all-rounder) across all matches.
                </p>
                """, unsafe_allow_html=True)                

                runs_contribution_by_role = done_batting[done_batting["Runs_Scored"] > 0]
                runs_contribution_by_role = (
                    runs_contribution_by_role.groupby("Role", as_index=False)["Runs_Scored"]
                    .sum().sort_values(by="Runs_Scored", ascending=False).reset_index(drop=True)
                )
                runs_contribution_by_role["Runs_Scored"] = runs_contribution_by_role["Runs_Scored"].astype(int)
                runs_contribution_by_role.index = runs_contribution_by_role.index + 1

                st.dataframe(runs_contribution_by_role, use_container_width=True)

                role_pie_colors = ROLE_BAT_COLORS[:len(runs_contribution_by_role)]
                fig, ax = plt.subplots(figsize=(PIE_W, PIE_H), dpi=120)
                wedges, texts, autotexts = ax.pie(
                    runs_contribution_by_role["Runs_Scored"], labels=None, autopct="%1.1f%%",
                    startangle=90, wedgeprops={"edgecolor": "black"},
                    colors=role_pie_colors
                )
                for at in autotexts:
                    at.set_fontsize(9)
                    at.set_fontweight("bold")
                    at.set_color("black")
                legend_labels = [f"{r}  —  {s}" for r, s in zip(runs_contribution_by_role["Role"], runs_contribution_by_role["Runs_Scored"])]
                ax.legend(wedges, legend_labels, title="Roles", title_fontsize=9,
                          loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9,
                          framealpha=1.0, edgecolor="#000000", facecolor="#ffffff",
                          labelcolor="#000000")
                ax.set_title("Runs Scored Contribution Based on Roles", fontsize=14, fontweight="bold")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                st.divider()

                # ── Strike rate comparison ──
                section_heading("⚡", "Strike-Rate Comparison — Batsmen vs All-Rounders")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Comparison of strike rates between batsmen and all-rounders for players who have played 10 or more balls, to identify who is scoring faster.
                </p>
                """, unsafe_allow_html=True) 

                batters_allrounders = done_batting[
                    (done_batting["Role"] == "batsman") | (done_batting["Role"] == "all-rounder")
                ]

                if batters_allrounders.empty:
                    st.warning("No batsmen or all-rounders found in the dataset.")
                else:
                    strike_rate_diff = (
                        batters_allrounders.groupby("Player_Name")
                        .agg({"Role": "first", "Strike_Rate": "mean", "Runs_Scored": "sum", "Balls_Played": "sum"})
                        .sort_values(by="Strike_Rate", ascending=False)
                    ).round(2).reset_index()
                    strike_rate_diff = strike_rate_diff[strike_rate_diff["Balls_Played"] >= 10]
                    strike_rate_diff["Runs_Scored"]  = strike_rate_diff["Runs_Scored"].astype(int)
                    strike_rate_diff["Balls_Played"] = strike_rate_diff["Balls_Played"].astype(int)
                    strike_rate_diff.index = strike_rate_diff.index + 1

                    st.dataframe(strike_rate_diff[["Player_Name","Role","Strike_Rate"]], use_container_width=True)

                    fig, ax = plt.subplots(figsize=(BAR_W, BAR_H), dpi=120)
                    sns.barplot(x=strike_rate_diff["Strike_Rate"], y=strike_rate_diff["Player_Name"],
                                hue=strike_rate_diff["Role"], palette=SR_ROLE_COLORS, ax=ax)
                    legend = ax.get_legend()
                    if legend:
                        legend.set_title("Role")
                        legend.get_frame().set_facecolor("#ffffff")
                        legend.get_frame().set_edgecolor("#000000")
                        legend.get_frame().set_alpha(1.0)
                        for t in legend.get_texts():
                            t.set_fontsize(9)
                            t.set_fontweight("bold")
                            t.set_color("#000000")
                        legend.get_title().set_color("#000000")
                    ax.set_title("Strike-Rate Comparison — Batsmen vs All-Rounders", fontsize=14, fontweight="bold")
                    ax.set_xlabel("Strike Rate", fontsize=11)
                    ax.set_ylabel("Players", fontsize=11)
                    ax.grid(axis='x', linestyle='--', alpha=0.4)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)

                st.divider()

                # ── Batting consistency ──
                section_heading("📉", "Players Consistency in Batting")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    A consistency score for each player based on their average runs scored and variability across matches.
                </p>
                """, unsafe_allow_html=True)                 

                match_balls_played = df2[df2["Balls_Played"] > 0]
                match_runs = match_balls_played.groupby(["Match_No","Player_Name"])["Runs_Scored"].sum().reset_index()
                players_per_match = match_balls_played.groupby("Player_Name")["Match_No"].nunique()
                all_players_unique = (players_per_match == 1).all()

                if match_balls_played["Match_No"].nunique() == 1:
                    st.warning("Players Consistency in Batting is not applicable for a single-match dataset.")

                elif all_players_unique: 
                    st.warning("The dataset only consists unique players in each match, Players consistency cannot be calculated without same player appearing in multiple matches.")                    

                else:
                    batting_consistency = (
                        match_runs.groupby("Player_Name")["Runs_Scored"]
                        .agg(["mean","std","count"]).round(2).reset_index()
                    )
                    batting_consistency = batting_consistency[batting_consistency["count"] > 1]
                    batting_consistency["Consistency_Score"] = (
                        batting_consistency["mean"] / (batting_consistency["std"] + 1)
                    ).round(2)
                    batting_consistency = batting_consistency.sort_values(
                        by="Consistency_Score", ascending=False).reset_index(drop=True)
                    batting_consistency.index += 1

                    st.dataframe(batting_consistency[["Player_Name","Consistency_Score"]], use_container_width=True)

                    n = len(batting_consistency)
                    colors = sns.color_palette(BATTING_CMAP, n)
                    fig, ax = plt.subplots(figsize=(BAR_W, BAR_H), dpi=120)
                    sns.barplot(y=batting_consistency["Player_Name"], x=batting_consistency["Consistency_Score"],
                                palette=colors, ax=ax)
                    ax.set_title("Players Consistency in Batting", fontsize=14, fontweight="bold")
                    ax.set_ylabel("Players", fontsize=11)
                    ax.set_xlabel("Consistency Score", fontsize=11)
                    ax.grid(axis='x', linestyle='--', alpha=0.4)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)

                st.divider()

                # ── Runs by batting order ──
                section_heading("🔢", "Average Runs by Batting Order")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Average runs scored by players based on the batting order (top, middle, lower) across all matches.
                </p>
                """, unsafe_allow_html=True)                 

                df2["Batting_Order"] = pd.cut(
                    df2["Batting_Position"], bins=[0,3,7,11], labels=["top","middle","lower"]
                ).astype(str)
                order_runs = (
                    df2.groupby("Batting_Order", as_index=False)["Runs_Scored"]
                    .sum().sort_values(by="Runs_Scored", ascending=False).reset_index(drop=True)
                )
                order_runs["Average_Runs_Scored"] = order_runs["Runs_Scored"]
                order_runs = order_runs.drop("Runs_Scored", axis=1)
                order_runs.index += 1

                st.dataframe(order_runs, use_container_width=True)

                fig, ax = plt.subplots(figsize=(LINE_W, BAR_H), dpi=120)
                sns.barplot(x=order_runs["Batting_Order"], y=order_runs["Average_Runs_Scored"],
                            palette=ORDER_PAL, ax=ax)
                ax.set_title("Average Runs by Batting Order", fontsize=14, fontweight="bold")
                ax.set_xlabel("Batting Order", fontsize=11)
                ax.set_ylabel("Average Runs Scored", fontsize=11)
                ax.grid(axis='y', linestyle='--', alpha=0.4)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                st.divider()

                # ── Phase-wise wickets lost ──
                section_heading("🔻", "Phase-wise Wickets Lost Breakdown")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Total wickets lost by the team in each match phase (powerplay, middle overs, death overs).
                </p>
                """, unsafe_allow_html=True)                 

                wickets_df = df2[(df2["Was_Out"] == True) & (df2["Out_Over"] > 0)].copy()
                wickets_df["Out_Over"] = pd.to_numeric(wickets_df["Out_Over"], errors="coerce")

                def assign_phase(over):
                    if (over > 0) & (over <= 6):    return "Powerplay"
                    elif (over > 6) & (over <= 15): return "Middle Overs"
                    else:            return "Death Overs"

                wickets_df["Wicket_Phase"] = wickets_df["Out_Over"].apply(assign_phase)
                phase_wickets = (
                    wickets_df.groupby("Wicket_Phase")["Player_Name"]
                    .size().reindex(["Powerplay","Middle Overs","Death Overs"])
                    .reset_index(name="Wickets_Lost").sort_values(by="Wickets_Lost", ascending=False)
                )
                phase_wickets.index += 1

                st.dataframe(phase_wickets, use_container_width=True)

                fig, ax = plt.subplots(figsize=(LINE_W, BAR_H), dpi=120)
                # Phase-specific colors: red=danger(powerplay), amber=mid, green=death
                phase_order = phase_wickets["Wicket_Phase"].tolist()
                phase_color_map = {"Powerplay": "#e05252", "Middle Overs": "#e0c070", "Death Overs": "#3fb950"}
                phase_pal = [phase_color_map.get(p, "#8b949e") for p in phase_order]
                sns.barplot(x=phase_wickets["Wicket_Phase"], y=phase_wickets["Wickets_Lost"],
                            palette=phase_pal, ax=ax)
                ax.set_title("Phase-wise Wickets Lost", fontsize=14, fontweight="bold")
                ax.set_xlabel("Match Phases", fontsize=11)
                ax.set_ylabel("Wickets Lost", fontsize=11)
                ax.grid(axis='y', linestyle='--', alpha=0.4)
                # Add a simple legend
                patches = [mpatches.Patch(color=v, label=k) for k, v in phase_color_map.items()]
                ax.legend(handles=patches, title="Phase", fontsize=9,
                          framealpha=1.0, edgecolor="#000000", facecolor="#ffffff",
                          labelcolor="#000000")
                ax.get_legend().get_title().set_color("#000000")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                #st.divider()
                st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════
        # TAB 3 — BOWLING ANALYTICS
        # ══════════════════════════════════════════════════
        with tab3:

            if st.session_state.get("df2") is None:
                st.warning("Please upload and confirm your dataset in the Dataset tab first.")
            else:
                df2 = st.session_state.df2

                # ── Individual wickets ──
                section_heading("⚾", "Individual Wickets Taken by Players")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Total wickets taken based on overs bowled by each player across all matches, sorted from highest to lowest wicket-taker.
                </p>
                """, unsafe_allow_html=True)                 

                done_bowling = df2[df2["Overs_Bowled"] > 0]

                bowling_diff = (
                    done_bowling.groupby("Player_Name", as_index=False)
                    .agg({"Wickets_Taken": "sum", "Overs_Bowled": "sum"})
                    .sort_values(by="Wickets_Taken", ascending=False).reset_index(drop=True)
                )
                bowling_diff["Wickets_Taken"] = bowling_diff["Wickets_Taken"].astype(int)
                bowling_diff.index = bowling_diff.index + 1

                st.dataframe(bowling_diff, use_container_width=True)

                n = len(bowling_diff)
                colors = sns.color_palette(BOWLING_CMAP, n)
                fig, ax = plt.subplots(figsize=(BAR_W, BAR_H), dpi=120)
                sns.barplot(x=bowling_diff["Wickets_Taken"], y=bowling_diff["Player_Name"],
                            palette=colors, ax=ax)
                ax.set_title("Individual Wickets Taken by Players", fontsize=14, fontweight="bold")
                ax.set_ylabel("Players", fontsize=11)
                ax.set_xlabel("Wickets Taken", fontsize=11)
                ax.grid(axis='x', linestyle='--', alpha=0.4)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                st.divider()

                # ── Wickets contribution pie ──
                section_heading("📊", "Total Wickets Contribution")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Contribution of total wickets taken by each player to the team's total wickets across all matches.
                </p>
                """, unsafe_allow_html=True)                     

                top_bowling   = bowling_diff[["Player_Name","Wickets_Taken"]].head()
                other_bowlers = (
                    bowling_diff["Wickets_Taken"].sum().astype(int) - top_bowling["Wickets_Taken"].sum().astype(int)
                )
                bowling_data = top_bowling.copy().reset_index(drop=True)
                bowling_data.loc[len(bowling_data)] = ["Others", int(other_bowlers)]
                bowling_data.index += 1
                bowling_data = bowling_data[bowling_data["Wickets_Taken"] > 0]

                st.dataframe(bowling_data, use_container_width=True)

                bowl_pie_colors = sns.color_palette("YlGnBu", len(bowling_data))
                fig, ax = plt.subplots(figsize=(PIE_W, PIE_H), dpi=120)
                wedges, texts, autotexts = ax.pie(
                    bowling_data["Wickets_Taken"], labels=None, autopct="%1.1f%%",
                    startangle=90, wedgeprops={"edgecolor": "black"},
                    colors=bowl_pie_colors
                )
                for at in autotexts:
                    at.set_fontsize(9)
                    at.set_fontweight("bold")
                    at.set_color("black")
                legend_labels = [f"{p}  —  {w}" for p, w in zip(bowling_data["Player_Name"], bowling_data["Wickets_Taken"])]
                ax.legend(wedges, legend_labels, title="Players", title_fontsize=9,
                          loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9,
                          framealpha=1.0, edgecolor="#000000", facecolor="#ffffff",
                          labelcolor="#000000")
                ax.get_legend().get_title().set_color("#000000")
                ax.set_title("Total Wickets Contribution", fontsize=14, fontweight="bold")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                st.divider()

                # ── Wickets per match ──
                section_heading("📈", "Player's Total Wickets in Each Match")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Total wickets taken by each player in each match, allows tracking of performance trends across matches by selecting the player.
                </p>
                """, unsafe_allow_html=True)                           

                if done_bowling["Match_No"].nunique() > 1:
                    players_list_bowl       = sorted(done_bowling["Player_Name"].unique())
                    selected_player_bowl    = st.selectbox("Select Player", players_list_bowl)
                    selected_player_bowl_df = done_bowling[done_bowling["Player_Name"] == selected_player_bowl]

                    player_wickets = (
                        selected_player_bowl_df.groupby("Match_No")["Wickets_Taken"]
                        .sum().reset_index().sort_values("Match_No")
                    )
                    player_wickets["Wickets_Taken"] = player_wickets["Wickets_Taken"].astype(int)
                    player_wickets.index += 1

                    st.dataframe(player_wickets, use_container_width=True)

                    x_vals = player_wickets["Match_No"].astype(int)
                    y_vals = player_wickets["Wickets_Taken"].astype(int)

                    fig, ax = plt.subplots(figsize=(LINE_W, LINE_H), dpi=120)
                    sns.lineplot(x=x_vals, y=y_vals, marker="o", color="#2dd4bf", ax=ax)
                    ax.set_xticks(x_vals.tolist())
                    ax.set_yticks(y_vals.tolist())
                    ax.set_title(f"{selected_player_bowl}'s Total Wickets in Each Match", fontsize=14, fontweight="bold")
                    ax.set_xlabel("Match No", fontsize=11)
                    ax.set_ylabel("Wickets Taken", fontsize=11)
                    ax.grid(linestyle='--', alpha=0.4)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.warning("Player's Total Wickets in Each Match is not applicable for a single-match dataset.")

                st.divider()

                # ── Wickets by role ──
                section_heading("🎭", "Wickets Taken Contribution Based on Roles")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Total wickets taken by players based on their roles (batsman, bowler, all-rounder) across all matches.
                </p>
                """, unsafe_allow_html=True)                           

                wickets_contribution_by_role = done_bowling[done_bowling["Wickets_Taken"] > 0]
                wickets_contribution_by_role = (
                    wickets_contribution_by_role.groupby("Role", as_index=False)["Wickets_Taken"]
                    .sum().sort_values(by="Wickets_Taken", ascending=False)
                )
                wickets_contribution_by_role["Wickets_Taken"] = wickets_contribution_by_role["Wickets_Taken"].astype(int)
                wickets_contribution_by_role.index += 1

                st.dataframe(wickets_contribution_by_role, use_container_width=True)

                role_bowl_colors = ROLE_BOWL_COLORS[:len(wickets_contribution_by_role)]
                fig, ax = plt.subplots(figsize=(PIE_W, PIE_H), dpi=120)
                wedges, texts, autotexts = ax.pie(
                    wickets_contribution_by_role["Wickets_Taken"], labels=None, autopct="%1.1f%%",
                    startangle=90, wedgeprops={"edgecolor": "black"},
                    colors=role_bowl_colors
                )
                for at in autotexts:
                    at.set_fontsize(9)
                    at.set_fontweight("bold")
                    at.set_color("black")
                legend_labels = [f"{r}  —  {w}" for r, w in zip(wickets_contribution_by_role["Role"], wickets_contribution_by_role["Wickets_Taken"])]
                ax.legend(wedges, legend_labels, title="Roles", title_fontsize=9,
                          loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9,
                          framealpha=1.0, edgecolor="#000000", facecolor="#ffffff",
                          labelcolor="#000000")
                ax.get_legend().get_title().set_color("#000000")
                ax.set_title("Wickets Taken Contribution Based on Roles", fontsize=14, fontweight="bold")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                st.divider()

                # ── Economy rate comparison ──
                section_heading("💰", "Economy-Rate Comparison — Bowlers vs All-Rounders")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Comparison of economy rates between bowlers and all-rounders for players who have bowled 2 or more overs, to identify who is conceding runs at a lower rate.
                </p>
                """, unsafe_allow_html=True)                           

                bowlers_allrounders = done_bowling[
                    (done_bowling["Role"] == "bowler") | (done_bowling["Role"] == "all-rounder")
                ]

                if bowlers_allrounders.empty:
                    st.warning("No bowlers or all-rounders found in the dataset.")
                else:
                    economy_diff = (
                        bowlers_allrounders.groupby("Player_Name", as_index=False)
                        .agg({"Role": "first", "Economy_Rate": "mean", "Overs_Bowled": "sum", "Runs_Given": "sum"})
                        .sort_values(by="Economy_Rate")
                    ).round(2).reset_index(drop=True)
                    economy_diff = economy_diff[economy_diff["Overs_Bowled"] >= 2]
                    economy_diff.index += 1

                    st.dataframe(economy_diff[["Player_Name","Role","Economy_Rate"]], use_container_width=True)

                    fig, ax = plt.subplots(figsize=(BAR_W, BAR_H), dpi=120)
                    sns.barplot(x=economy_diff["Economy_Rate"], y=economy_diff["Player_Name"],
                                hue=economy_diff["Role"], palette=ECO_ROLE_COLORS, ax=ax)
                    legend = ax.get_legend()
                    if legend:
                        legend.set_title("Role")
                        legend.get_frame().set_facecolor("#ffffff")
                        legend.get_frame().set_edgecolor("#000000")
                        legend.get_frame().set_alpha(1.0)
                        for t in legend.get_texts():
                            t.set_fontsize(9)
                            t.set_fontweight("bold")
                            t.set_color("#000000")
                        legend.get_title().set_color("#000000")
                    ax.set_title("Economy-Rate Comparison — Bowlers vs All-Rounders", fontsize=14, fontweight="bold")
                    ax.set_xlabel("Economy Rate", fontsize=11)
                    ax.set_ylabel("Players", fontsize=11)
                    ax.grid(axis='x', linestyle='--', alpha=0.4)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)

                st.divider()

                # ── Bowling consistency ──
                section_heading("📉", "Players Consistency in Bowling")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    A consistency score for each player based on their average wickets taken and variability across matches.
                </p>
                """, unsafe_allow_html=True)                           

                match_overs   = df2[df2["Overs_Bowled"] > 0]
                match_wickets = match_overs.groupby(["Match_No","Player_Name"])["Wickets_Taken"].sum().reset_index()
                players_per_match = match_balls_played.groupby("Player_Name")["Match_No"].nunique()
                all_players_unique = (players_per_match == 1).all()

                if match_balls_played["Match_No"].nunique() == 1:
                    st.warning("Players Consistency in Bowling is not applicable for a single-match dataset.")   

                elif all_players_unique: 
                    st.warning("The dataset only consists unique players in each match, Players consistency cannot be calculated without same player appearing in multiple matches.")                                 

                else:
                    bowling_consistency = (
                        match_wickets.groupby("Player_Name")["Wickets_Taken"]
                        .agg(["mean","std","count"]).round(2).reset_index()
                    )
                    bowling_consistency = bowling_consistency[bowling_consistency["count"] > 1]
                    bowling_consistency["Consistency_Score"] = (
                        bowling_consistency["mean"] / (bowling_consistency["std"] + 1)
                    ).round(2)
                    bowling_consistency = bowling_consistency.sort_values(
                        by="Consistency_Score", ascending=False).reset_index(drop=True)
                    bowling_consistency.index += 1

                    st.dataframe(bowling_consistency[["Player_Name","Consistency_Score"]], use_container_width=True)

                    n = len(bowling_consistency)
                    colors = sns.color_palette(BOWLING_CMAP, n)
                    fig, ax = plt.subplots(figsize=(BAR_W, BAR_H), dpi=120)
                    sns.barplot(y=bowling_consistency["Player_Name"], x=bowling_consistency["Consistency_Score"],
                                palette=colors, ax=ax)
                    ax.set_title("Players Consistency in Bowling", fontsize=14, fontweight="bold")
                    ax.set_xlabel("Consistency Score", fontsize=11)
                    ax.set_ylabel("Players", fontsize=11)
                    ax.grid(axis='x', linestyle='--', alpha=0.4)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)

                #st.divider()
                st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════
        # TAB 4 — SUMMARY
        # ══════════════════════════════════════════════════
        with tab4:

            if st.session_state.get("df2") is None:
                st.warning("Please upload and confirm your dataset in the Dataset tab first.")
            else:
                df2 = st.session_state.df2

                done_batting_s  = df2[df2["Balls_Played"] > 0]
                done_bowling_s  = df2[df2["Overs_Bowled"] > 0]

                runs_difference_s = (
                    done_batting_s.groupby("Player_Name")
                    .agg({"Runs_Scored": "sum", "Balls_Played": "sum"})
                    .sort_values(by="Runs_Scored", ascending=False).astype(int).reset_index()
                )

                bowling_diff_s = (
                    done_bowling_s.groupby("Player_Name", as_index=False)
                    .agg({"Wickets_Taken": "sum", "Overs_Bowled": "sum"})
                    .sort_values(by="Wickets_Taken", ascending=False).reset_index(drop=True)
                )
                bowling_diff_s["Wickets_Taken"] = bowling_diff_s["Wickets_Taken"].astype(int)

                batters_allrounders_s = done_batting_s[
                    (done_batting_s["Role"] == "batsman") | (done_batting_s["Role"] == "all-rounder")
                ]
                strike_rate_diff_s = (
                    batters_allrounders_s.groupby("Player_Name")
                    .agg({"Role": "first", "Strike_Rate": "mean"})
                    .sort_values(by="Strike_Rate", ascending=False)
                ).round(2).reset_index()

                bowlers_allrounders_s = done_bowling_s[
                    (done_bowling_s["Role"] == "bowler") | (done_bowling_s["Role"] == "all-rounder")
                ]
                economy_diff_s = (
                    bowlers_allrounders_s.groupby("Player_Name", as_index=False)
                    .agg({"Role": "first", "Economy_Rate": "mean"})
                    .sort_values(by="Economy_Rate")
                ).round(2).reset_index(drop=True)

                runs_contribution_by_role_s = done_batting_s[done_batting_s["Runs_Scored"] > 0]
                runs_contribution_by_role_s = (
                    runs_contribution_by_role_s.groupby("Role", as_index=False)["Runs_Scored"]
                    .sum().sort_values(by="Runs_Scored", ascending=False).reset_index(drop=True)
                )
                runs_contribution_by_role_s["Runs_Scored"] = runs_contribution_by_role_s["Runs_Scored"].astype(int)

                wickets_df_s = df2[df2["Was_Out"] == True].copy()
                wickets_df_s["Out_Over"] = pd.to_numeric(wickets_df_s["Out_Over"], errors="coerce")

                def assign_phase_s(over):
                    if over <= 6:    return "Powerplay"
                    elif over <= 15: return "Middle Overs"
                    else:            return "Death Overs"

                wickets_df_s["Wicket_Phase"] = wickets_df_s["Out_Over"].apply(assign_phase_s)
                phase_wickets_s = (
                    wickets_df_s.groupby("Wicket_Phase")["Player_Name"]
                    .size().reindex(["Powerplay","Middle Overs","Death Overs"])
                    .reset_index(name="Wickets_Lost").sort_values(by="Wickets_Lost", ascending=False)
                )

                wickets_contribution_by_role_s = done_bowling_s[done_bowling_s["Wickets_Taken"] > 0]
                wickets_contribution_by_role_s = (
                    wickets_contribution_by_role_s.groupby("Role", as_index=False)["Wickets_Taken"]
                    .sum().sort_values(by="Wickets_Taken", ascending=False)
                )
                wickets_contribution_by_role_s["Wickets_Taken"] = wickets_contribution_by_role_s["Wickets_Taken"].astype(int)

                df2["Batting_Order"] = pd.cut(
                    df2["Batting_Position"], bins=[0,3,7,11], labels=["top","middle","lower"]
                ).astype(str)
                order_runs_s = (
                    df2.groupby("Batting_Order", as_index=False)["Runs_Scored"]
                    .sum().sort_values(by="Runs_Scored", ascending=False).reset_index(drop=True)
                )

                top_scorer      = runs_difference_s.iloc[0]["Player_Name"]  if not runs_difference_s.empty  else "N/A"
                top_scorer_runs = runs_difference_s.iloc[0]["Runs_Scored"]  if not runs_difference_s.empty  else 0
                top_scorer_balls= runs_difference_s.iloc[0]["Balls_Played"] if not runs_difference_s.empty  else 0

                top_wicket_taker  = bowling_diff_s.iloc[0]["Player_Name"]    if not bowling_diff_s.empty    else "N/A"
                top_wicket_taker_w= bowling_diff_s.iloc[0]["Wickets_Taken"]  if not bowling_diff_s.empty    else 0

                top_sr_player = strike_rate_diff_s.iloc[0]["Player_Name"]  if not strike_rate_diff_s.empty else "N/A"
                top_sr_value  = strike_rate_diff_s.iloc[0]["Strike_Rate"]  if not strike_rate_diff_s.empty else 0

                top_eco_player = economy_diff_s.iloc[0]["Player_Name"]    if not economy_diff_s.empty    else "N/A"
                top_eco_value  = economy_diff_s.iloc[0]["Economy_Rate"]   if not economy_diff_s.empty    else 0

                runs_role_1     = runs_contribution_by_role_s.iloc[0]["Role"]        if len(runs_contribution_by_role_s) > 0 else "N/A"
                runs_role_1_val = runs_contribution_by_role_s.iloc[0]["Runs_Scored"] if len(runs_contribution_by_role_s) > 0 else 0
                runs_role_2     = runs_contribution_by_role_s.iloc[1]["Role"]        if len(runs_contribution_by_role_s) > 1 else "N/A"
                runs_role_2_val = runs_contribution_by_role_s.iloc[1]["Runs_Scored"] if len(runs_contribution_by_role_s) > 1 else 0

                wkt_role_1     = wickets_contribution_by_role_s.iloc[0]["Role"]          if len(wickets_contribution_by_role_s) > 0 else "N/A"
                wkt_role_1_val = wickets_contribution_by_role_s.iloc[0]["Wickets_Taken"] if len(wickets_contribution_by_role_s) > 0 else 0
                wkt_role_2     = wickets_contribution_by_role_s.iloc[1]["Role"]          if len(wickets_contribution_by_role_s) > 1 else "N/A"
                wkt_role_2_val = wickets_contribution_by_role_s.iloc[1]["Wickets_Taken"] if len(wickets_contribution_by_role_s) > 1 else 0

                top_order    = order_runs_s.iloc[0]["Batting_Order"] if len(order_runs_s) > 0 else "N/A"
                second_order = order_runs_s.iloc[1]["Batting_Order"] if len(order_runs_s) > 1 else "N/A"

                top_phase      = phase_wickets_s.iloc[0]["Wicket_Phase"]  if not phase_wickets_s.empty else "N/A"
                top_phase_wkts = phase_wickets_s.iloc[0]["Wickets_Lost"]  if not phase_wickets_s.empty else 0

                # ── Runs & Wickets per match chart ──
                section_heading("📊", "Total Runs Scored and Wickets Taken in Each Match")
                st.markdown("""
                <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                          margin: -6px 0 10px 0; line-height:1.6;">
                    Total runs scored and wickets taken by the team in each match.
                </p>
                """, unsafe_allow_html=True)                           

                runs_wickets = (
                    df2.groupby("Match_No", as_index=False)
                    .agg({"Runs_Scored": "sum", "Wickets_Taken": "sum"}).astype(int)
                )
                runs_wickets.index += 1

                st.dataframe(runs_wickets[["Match_No","Runs_Scored","Wickets_Taken"]], use_container_width=True)

                fig, ax = plt.subplots(1, 2, figsize=(SIDE_W, SIDE_H), dpi=120)
                n_matches = len(runs_wickets)
                run_colors  = sns.color_palette(BATTING_CMAP, n_matches)
                bowl_colors = sns.color_palette(BOWLING_CMAP, n_matches)

                sns.barplot(x=runs_wickets["Match_No"], y=runs_wickets["Runs_Scored"],   palette=run_colors,  ax=ax[0])
                ax[0].set_xlabel("Match Number", fontsize=11)
                ax[0].set_ylabel("Runs Scored", fontsize=11)
                ax[0].set_title("Runs Scored in Each Match", fontsize=12, fontweight="bold")
                ax[0].grid(axis='y', linestyle='--', alpha=0.4)

                sns.barplot(x=runs_wickets["Match_No"], y=runs_wickets["Wickets_Taken"], palette=bowl_colors, ax=ax[1])
                ax[1].set_xlabel("Match Number", fontsize=11)
                ax[1].set_ylabel("Wickets Taken", fontsize=11)
                ax[1].set_title("Wickets Taken in Each Match", fontsize=12, fontweight="bold")
                ax[1].grid(axis='y', linestyle='--', alpha=0.4)

                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

                st.divider()

                # ── KPI cards row ──
                st.markdown("""
                <div style="font-family:'Rajdhani',sans-serif; font-weight:700;
                            font-size:24px; color:#e0c070; margin:6px 0 14px 0;
                            letter-spacing:0.4px;">
                    🏆 Top Performers
                </div>
                """, unsafe_allow_html=True)

                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    kpi_card("🏏", "Top Run Scorer",    f"{top_scorer}",    f"{top_scorer_runs} runs off {top_scorer_balls} balls")
                with c2:
                    kpi_card("⚾", "Top Wicket Taker",  f"{top_wicket_taker}",  f"{top_wicket_taker_w} wickets")
                with c3:
                    kpi_card("⚡", "Best Strike Rate",  f"{top_sr_player}",  f"SR: {top_sr_value}")
                with c4:
                    kpi_card("💰", "Best Econ. Rate", f"{top_eco_player}", f"ER: {top_eco_value}")

                st.markdown("<br>", unsafe_allow_html=True)
                st.divider()

                # ── Narrative insight lines ──
                st.markdown("""
                <div style="font-family:'Rajdhani',sans-serif; font-weight:700;
                            font-size:22px; color:#e0c070; margin:10px 0 12px 0;">
                    📋 Team Performance Summary
                </div>
                """, unsafe_allow_html=True)

                insight_line(1, f"<strong>{top_scorer}</strong> is the highest run scorer with <strong>{top_scorer_runs} runs</strong>.")
                insight_line(2, f"<strong>{top_wicket_taker}</strong> is the highest wicket taker with <strong>{top_wicket_taker_w} wickets</strong>.")
                insight_line(3, f"<strong>{top_sr_player}</strong> has the highest strike rate of <strong>{top_sr_value}</strong>.")
                insight_line(4, f"<strong>{top_eco_player}</strong> has the best bowling economy rate of <strong>{top_eco_value}</strong>.")
                insight_line(5, f"<strong>{runs_role_1}s</strong> are the highest contributors in scoring runs with <strong>{runs_role_1_val} runs</strong>, followed by <strong>{runs_role_2}s</strong> with <strong>{runs_role_2_val} runs</strong>.")
                insight_line(6, f"<strong>{wkt_role_1}s</strong> are the highest contributors in taking wickets with <strong>{wkt_role_1_val} wickets</strong>, followed by <strong>{wkt_role_2}s</strong> with <strong>{wkt_role_2_val} wickets</strong>.")
                insight_line(7, f"The <strong>{top_order} order</strong> is the strongest batting unit, followed by the <strong>{second_order} order</strong>.")
                insight_line(8, f"The team has lost the most wickets in the <strong>{top_phase}</strong>, losing <strong>{top_phase_wkts.astype(int)} wickets</strong>.")

                #st.divider()
                st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # ABOUT PAGE
    # ══════════════════════════════════════════════════════
    elif page == "About":

        st.markdown("""
        <div style="text-align:center; padding:24px 0 6px 0;">
            <h1 style="font-family:'Rajdhani',sans-serif; font-weight:700;
                       font-size:38px; color:#e0c070; margin:0; letter-spacing:1px;">
                🏏 T20 Team Performance Analyzer
            </h1>
            <p style="font-family:'Rajdhani',sans-serif; font-size:16px;
                      color:#8b949e; margin:6px 0 0 0;">
                Data-Driven Analysis of Your T20 Team Performance
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        with st.expander("👨‍💻 About the Developer — Pranay Jha", expanded=False):
            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:14px;
                        color:#e6edf3; line-height:1.8;">
                Hello! My name is <strong style="color:#e0c070;">Pranay Jha</strong>, and I am currently pursuing a
                <strong style="color:#e0c070;">Bachelor of Technology (B.Tech) in Computer Science and Engineering</strong>.<br><br>
                I am actively learning and exploring the fields of <strong style="color:#e0c070;">Data Science, Data Analytics,
                and Data Visualization</strong>.<br><br>
                This project — <strong style="color:#c9a84c;">T20 Cricket Team Performance Analyzer</strong> — has been developed
                as part of my learning journey in data analytics. The main goal is to demonstrate how structured data analysis
                and interactive dashboards can evaluate sports performance effectively.<br><br>
                The tool uses Python libraries including <strong style="color:#2dd4bf;">NumPy, Pandas, Matplotlib, Seaborn,
                and Streamlit</strong>.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                       font-size:17px; color:#c9a84c; margin-bottom:8px;">
                🚀 Key Highlights
            </p>
            """, unsafe_allow_html=True)

            for item in [
                "Work with <strong>real-world structured datasets</strong>",
                "Perform <strong>data cleaning and feature engineering</strong>",
                "Build <strong>interactive analytical dashboards</strong>",
                "Communicate insights through <strong>data visualization</strong>",
                "Design <strong>user-friendly analytical tools</strong>",
            ]:
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-radius:6px;
                            padding:8px 14px; margin-bottom:6px; font-family:'Rajdhani',sans-serif;
                            font-size:14px; color:#e6edf3;">
                    ▸ &nbsp;{item}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                       font-size:17px; color:#c9a84c; margin-bottom:8px;">
                🔗 Connect With Me
            </p>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="display:flex; gap:14px; flex-wrap:wrap;">
                <a href="https://github.com/Pranay-256" target="_blank"
                   style="display:inline-flex; align-items:center; gap:8px;
                          background:#1c2330; border:1px solid #2a3444;
                          border-radius:8px; padding:10px 18px;
                          font-family:'Rajdhani',sans-serif; font-size:14px;
                          color:#e6edf3; text-decoration:none;
                          transition:border-color 0.2s;">
                    <span style="font-size:18px;">🐙</span>
                    <strong>GitHub</strong> — Pranay-256
                </a>
                <a href="https://www.linkedin.com/in/pranay-jha-6582a937b/" target="_blank"
                   style="display:inline-flex; align-items:center; gap:8px;
                          background:#1c2330; border:1px solid #2a3444;
                          border-radius:8px; padding:10px 18px;
                          font-family:'Rajdhani',sans-serif; font-size:14px;
                          color:#e6edf3; text-decoration:none;">
                    <span style="font-size:18px;">💼</span>
                    <strong>LinkedIn</strong> — Pranay Jha
                </a>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("❗ Problem Statement", expanded=False):
            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:14px;
                        color:#e6edf3; line-height:1.8; margin-bottom:10px;">
                In many <strong style="color:#e0c070;">local cricket matches, school tournaments, inter-college
                competitions, and community leagues</strong>, player performance is usually evaluated
                <strong>manually or based on personal observation</strong>. This creates several limitations.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                       font-size:17px; color:#c9a84c; margin:8px 0;">⚠️ Key Challenges</p>
            """, unsafe_allow_html=True)

            for item in [
                "Player contributions are often judged <strong>subjectively</strong>",
                "Awards like <strong>Best Batsman / Bowler</strong> may not always be fairly decided",
                "Bowling performance is usually evaluated <strong>only by wickets</strong>, ignoring economy rate",
                "<strong>Match-to-match comparison</strong> is difficult without proper records",
                "Lack of a <strong>structured data system</strong> for multi-match analysis",
            ]:
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-left:3px solid #e05252;
                            border-radius:0 6px 6px 0; padding:8px 14px; margin-bottom:6px;
                            font-family:'Rajdhani',sans-serif; font-size:14px; color:#e6edf3;">
                    {item}
                </div>
                """, unsafe_allow_html=True)
                

        with st.expander("🎯 Objective", expanded=False):
            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:14px;
                        color:#e6edf3; line-height:1.8; margin-bottom:10px;">
                The main objective is to build a <strong style="color:#e0c070;">clear, structured, and unbiased
                cricket performance analysis system</strong> using match-level data — replacing manual judgements
                with <strong>data-driven insights</strong>.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                       font-size:17px; color:#c9a84c; margin:8px 0;">📊 Core Focus Areas</p>
            """, unsafe_allow_html=True)

            for item in [
                "Measuring <strong>individual batting contribution</strong>",
                "Evaluating <strong>bowling impact</strong> using wickets and economy rate",
                "Measuring <strong>player consistency</strong> across multiple matches",
                "Comparing performances between <strong>batsmen, bowlers, and all-rounders</strong>",
                "Providing <strong>fair statistical summaries</strong> for team evaluation",
            ]:
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-left:3px solid #3fb950;
                            border-radius:0 6px 6px 0; padding:8px 14px; margin-bottom:6px;
                            font-family:'Rajdhani',sans-serif; font-size:14px; color:#e6edf3;">
                    ✓ &nbsp;{item}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                       font-size:17px; color:#c9a84c; margin:8px 0;">🏏 Target Users</p>
            """, unsafe_allow_html=True)

            targets = ["Local cricket teams", "Gully cricket players", "School & college tournaments",
                       "Small-scale cricket competitions", "Teams seeking simple data-based evaluation"]
            cols = st.columns(3)
            for i, t in enumerate(targets):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style="background:#1c2330; border:1px solid #2a3444; border-radius:8px;
                                padding:8px 12px; margin-bottom:8px; text-align:center;
                                font-family:'Rajdhani',sans-serif; font-size:13px; color:#e6edf3;">
                        {t}
                    </div>
                    """, unsafe_allow_html=True)

        with st.expander("🛠️ Tech Stack", expanded=False):
            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#e6edf3;
                      line-height:1.8; margin-bottom:10px;">
                Built using the <strong style="color:#e0c070;">Python data analytics ecosystem</strong>
                combined with an interactive dashboard framework.
            </p>
            """, unsafe_allow_html=True)

            tools = [
                ("🐍 Python",      "Core language for data processing and analytics"),
                ("🔢 NumPy",       "Numerical operations and structured numeric data"),
                ("🐼 Pandas",      "Data cleaning, manipulation, and aggregation"),
                ("📉 Matplotlib",  "Charts and plots for visualizing statistics"),
                ("🎨 Seaborn",     "Enhanced statistical and aesthetic visualizations"),
                ("🚀 Streamlit",   "Interactive dashboard for dynamic data exploration"),
            ]
            for name, desc in tools:
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-radius:8px;
                            padding:10px 16px; margin-bottom:7px; display:flex;
                            font-family:'Rajdhani',sans-serif; font-size:14px; color:#e6edf3;
                            gap:10px; align-items:flex-start;">
                    <strong style="color:#c9a84c; min-width:110px;">{name}</strong>
                    <span style="color:#8b949e;">{desc}</span>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("📊 Analytical Approach & Visualizations", expanded=False):

            def analysis_block(emoji, title, items):
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-radius:8px;
                            padding:12px 16px; margin-bottom:10px;">
                    <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                              font-size:17px; color:#c9a84c; margin:0 0 6px 0;">
                        {emoji} {title}
                    </p>
                    {''.join(f"<p style='font-family:Rajdhani,sans-serif; font-size:14px; color:#e6edf3; margin:3px 0;'>▸ &nbsp;{item}</p>" for item in items)}
                </div>
                """, unsafe_allow_html=True)
        
            analysis_block("🏏", "Batting Analysis", [
                "Individual runs scored",
                "Total runs contribution",
                "Runs per match per player",
                "Strike rate comparison",
                "Role-wise contribution",
                "Batting consistency",
                "Batting order strength",
            ])
        
            analysis_block("🎯", "Bowling Analysis", [
                "Individual wickets taken",
                "Total wickets contribution",
                "Wickets per match per player",
                "Role-wise wicket contribution",
                "Economy rate comparison",
                "Bowling consistency",
            ])

        with st.expander("🔄 Recent Updates", expanded=False):

            def version_block(version, date, items):
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-radius:8px;
                            padding:12px 16px; margin-bottom:10px;">
                    <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                              font-size:16px; color:#c9a84c; margin:0 0 4px 0;">
                        Version {version} &nbsp;·&nbsp;
                        <span style="color:#8b949e; font-size:14px; font-weight:500;">{date}</span>
                    </p>
                    {''.join(f"<p style='font-family:Rajdhani,sans-serif; font-size:13px; color:#e6edf3; margin:3px 0;'>— {i}</p>" for i in items)}
                </div>
                """, unsafe_allow_html=True)

            version_block("2.01", "18th April 2026", [
                "Improved overall tool user interface",
                "Improved data validation and cleaning",
                "Added drop-down expanders for Dataset Columns Overview and About Section",
                "Improved visualization clarity and chart styling",
                "Added KPI cards for key performance indicators in the Summary tab",
                "Improved logic for line charts and Runs/Wickets Contributions",
                "Organized insights into clear analytical sections",
                "Fixed Bugs and issues"
            ])
            version_block("2.0", "16th March 2026", [
                "Improved overall tool user interface",
                "Added support for .xlsx dataset uploads",
                "Enhanced data validation and cleaning",
                "Added more detailed batting and bowling analytics",
                "Improved visualization clarity",
                "Added interactive player performance analysis",
            ])
            version_block("1.0", "27th February 2026", ["Initial release"])

        #st.divider()
        st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
render_footer()
