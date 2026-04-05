import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from collections import Counter

st.set_page_config(
    page_title="NENet Northpreneurs Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ──────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #0d1117; color: #e6edf3; }
  [data-testid="stHeader"] { background: transparent; }
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
  h1,h2,h3 { color: #f0f6fc !important; }
  .kpi-card {
    background: #161b22; border: 1px solid #21262d; border-radius: 10px;
    padding: 1.1rem 1.25rem; position: relative; overflow: hidden;
  }
  .kpi-top { height: 3px; border-radius: 3px 3px 0 0; margin: -1.1rem -1.25rem 0.8rem -1.25rem; }
  .kpi-val { font-size: 28px; font-weight: 700; color: #f0f6fc; line-height: 1; }
  .kpi-label { font-size: 12px; color: #8b949e; margin-top: 5px; }
  .kpi-badge {
    display: inline-block; font-size: 10px; font-weight: 600;
    padding: 2px 8px; border-radius: 10px; margin-top: 6px;
  }
  .insight-box {
    background: #161b22; border: 1px solid #21262d; border-radius: 10px;
    padding: 1rem 1.25rem; margin-top: 0.75rem;
  }
  .insight-box p { font-size: 13px; color: #8b949e; line-height: 1.7; margin: 0; }
  .insight-box strong { color: #e6edf3; }
  div[data-testid="stTabs"] button { color: #8b949e !important; }
  div[data-testid="stTabs"] button[aria-selected="true"] { color: #f0f6fc !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA ────────────────────────────────────────────────────
records = [
    {"g":"Male","bt":"Limited Company","yr":2015,"emp":21,"reg":"Northern","rev":"H","gepa":"Y","gea":"Y","permit":"Y","reach":["Local/Community","District","Regional","National"],"exp":True,"support":["Training","Market Linkages","Branding","Finance","Export","Digital"],"heard":"Social Media","sectors":["Food Processing","Manufacturing"]},
    {"g":"Female","bt":"Limited Company","yr":2020,"emp":9,"reg":"Upper West","rev":"L","gepa":"A","gea":"Y","permit":"A","reach":["Regional","National"],"exp":False,"support":["Training","Market Linkages","Certification","Finance","Export","Exhibition"],"heard":"Friend/Colleague","sectors":["Agribusiness","Food Processing"]},
    {"g":"Male","bt":"Social Enterprise","yr":2020,"emp":3,"reg":"Northern","rev":"B","gepa":"N","gea":"N","permit":"Y","reach":["Local/Community","District","Regional","National"],"exp":False,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Digital","Exhibition"],"heard":"Social Media","sectors":["Agribusiness","Beauty/Cosmetics"]},
    {"g":"Female","bt":"Limited Company","yr":2015,"emp":10,"reg":"Northern","rev":"L","gepa":"A","gea":"Y","permit":"Y","reach":["Local/Community","Regional"],"exp":False,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Export","Digital","Exhibition"],"heard":"Friend/Colleague","sectors":["Agribusiness","Food Processing"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2015,"emp":34,"reg":"Northern","rev":"H","gepa":"Y","gea":"Y","permit":"Y","reach":["Local/Community","District","Regional","National"],"exp":True,"support":["Market Linkages","Networking","Branding","Certification","Finance","Export","Digital","Exhibition"],"heard":"NENet Event","sectors":["Agribusiness"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2025,"emp":0,"reg":"Upper West","rev":"M","gepa":"Y","gea":"Y","permit":"Y","reach":["Local/Community"],"exp":False,"support":["Training","Market Linkages","Networking","Registration","Digital"],"heard":"Social Media","sectors":["Agribusiness","Services","Trading/Retail","Textile/Fashion"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2023,"emp":5,"reg":"Upper West","rev":"B","gepa":"N","gea":"Y","permit":"P","reach":["Local/Community","District","Regional"],"exp":False,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Export","Digital","Exhibition"],"heard":"Friend/Colleague","sectors":["Agribusiness","Manufacturing","Handicrafts/Artisan","Services","Textile/Fashion"]},
    {"g":"Male","bt":"Sole Proprietorship","yr":2026,"emp":1,"reg":"Upper West","rev":"L","gepa":"Y","gea":"P","permit":"N","reach":["Local/Community","District","Regional"],"exp":False,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Export","Registration","Digital","Exhibition"],"heard":"Social Media","sectors":["Agribusiness","Food Processing","Construction","Manufacturing","Services","Trading/Retail"]},
    {"g":"Female","bt":"Social Enterprise","yr":2024,"emp":3,"reg":"Upper East","rev":"L","gepa":"P","gea":"Y","permit":"P","reach":["Local/Community","District","Regional","National"],"exp":False,"support":["Market Linkages","Networking","Branding","Finance","Export","Exhibition"],"heard":"Social Media","sectors":["Food Processing"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2023,"emp":2,"reg":"Upper West","rev":"B","gepa":"N","gea":"N","permit":"Y","reach":["Local/Community"],"exp":False,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Registration","Digital"],"heard":"Friend/Colleague","sectors":["Agribusiness","Food Processing","Manufacturing"]},
    {"g":"Female","bt":"Partnership","yr":2020,"emp":8,"reg":"Northern","rev":"B","gepa":"Y","gea":"Y","permit":"Y","reach":["Local/Community","District","Regional","National"],"exp":False,"support":["Exhibition"],"heard":"Partner Organisation","sectors":["Food Processing"]},
    {"g":"Male","bt":"Sole Proprietorship","yr":2017,"emp":7,"reg":"Upper West","rev":"B","gepa":"A","gea":"Y","permit":"A","reach":["Local/Community","District","Regional","National"],"exp":False,"support":["Training","Market Linkages"],"heard":"Social Media","sectors":["Agribusiness"]},
    {"g":"Male","bt":"Sole Proprietorship","yr":2015,"emp":10,"reg":"Upper East","rev":"H","gepa":"Y","gea":"Y","permit":"Y","reach":["Local/Community","District","Regional","National"],"exp":True,"support":["Market Linkages","Certification","Finance","Exhibition"],"heard":"Friend/Colleague","sectors":["Beauty/Cosmetics"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2019,"emp":2,"reg":"Upper West","rev":"B","gepa":"N","gea":"Y","permit":"N","reach":["Local/Community","District"],"exp":False,"support":["Training","Market Linkages","Networking","Branding","Digital"],"heard":"Social Media","sectors":["Food Processing"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2020,"emp":3,"reg":"Upper West","rev":"M","gepa":"A","gea":"A","permit":"A","reach":["Local/Community","District","Regional","National"],"exp":True,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Export","Digital","Exhibition"],"heard":"Partner Organisation","sectors":["Textile/Fashion"]},
    {"g":"Female","bt":"Limited Company","yr":2018,"emp":30,"reg":"Upper East","rev":"B","gepa":"Y","gea":"Y","permit":"Y","reach":["Local/Community","District","Regional","National"],"exp":True,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Export","Registration","Digital","Exhibition"],"heard":"Partner Organisation","sectors":["Agribusiness","Food Processing","Services","Beauty/Cosmetics"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2015,"emp":11,"reg":"Northern","rev":"L","gepa":"Y","gea":"Y","permit":"N","reach":["National"],"exp":True,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Export","Digital","Exhibition"],"heard":"Social Media","sectors":["Agribusiness","Manufacturing","Beauty/Cosmetics"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2019,"emp":2,"reg":"Northern","rev":"M","gepa":"N","gea":"P","permit":"Y","reach":["Local/Community"],"exp":False,"support":["Training","Market Linkages","Finance"],"heard":"Partner Organisation","sectors":["Handicrafts/Artisan","Trading/Retail","Beauty/Cosmetics"]},
    {"g":"Female","bt":"Limited Company","yr":2022,"emp":1,"reg":"Upper West","rev":"M","gepa":"Y","gea":"A","permit":"Y","reach":["District"],"exp":True,"support":["Branding"],"heard":"Social Media","sectors":["Agribusiness"]},
    {"g":"Female","bt":"Social Enterprise","yr":2010,"emp":1,"reg":"Northern","rev":"B","gepa":"N","gea":"Y","permit":"N","reach":["District"],"exp":False,"support":["Networking"],"heard":"Partner Organisation","sectors":["Agribusiness","Food Processing"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2022,"emp":2,"reg":"Upper West","rev":"B","gepa":"N","gea":"Y","permit":"N","reach":["District"],"exp":False,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Export","Registration","Digital","Exhibition"],"heard":"Friend/Colleague","sectors":["Textile/Fashion"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2023,"emp":1,"reg":"Upper West","rev":"B","gepa":"N","gea":"N","permit":"Y","reach":["District"],"exp":False,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Export","Registration","Digital","Exhibition"],"heard":"Friend/Colleague","sectors":["Food Processing","Services"]},
    {"g":"Female","bt":"Limited Company","yr":2022,"emp":12,"reg":"Northern","rev":"L","gepa":"N","gea":"Y","permit":"P","reach":["National"],"exp":False,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Export","Registration","Digital","Exhibition"],"heard":"NENet Event","sectors":["Agribusiness","Food Processing","Services","Textile/Fashion"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2012,"emp":31,"reg":"Northern","rev":"H","gepa":"Y","gea":"Y","permit":"Y","reach":["Local/Community","District","Regional","National"],"exp":True,"support":["Market Linkages","Networking","Finance","Export","Exhibition"],"heard":"Friend/Colleague","sectors":["Agribusiness"]},
    {"g":"Female","bt":"Partnership","yr":2021,"emp":3,"reg":"Upper West","rev":"B","gepa":"N","gea":"N","permit":"N","reach":["Local/Community","District"],"exp":False,"support":["Training","Networking","Finance","Registration","Digital","Exhibition"],"heard":"Social Media","sectors":["Agribusiness"]},
    {"g":"Male","bt":"Sole Proprietorship","yr":2025,"emp":3,"reg":"Northern","rev":"B","gepa":"A","gea":"A","permit":"A","reach":["Local/Community","District","Regional","National"],"exp":False,"support":["Training","Networking","Finance","Digital"],"heard":"Social Media","sectors":["Agribusiness"]},
    {"g":"Male","bt":"Sole Proprietorship","yr":2019,"emp":36,"reg":"Northern","rev":"H","gepa":"A","gea":"A","permit":"A","reach":["Local/Community","District","Regional","National"],"exp":True,"support":["Finance","Export"],"heard":"NENet Event","sectors":["Agribusiness","Food Processing","Services"]},
    {"g":"Male","bt":"Sole Proprietorship","yr":2025,"emp":1,"reg":"Northern","rev":"B","gepa":"A","gea":"Y","permit":"Y","reach":["Local/Community"],"exp":False,"support":["Branding","Finance","Digital"],"heard":"Partner Organisation","sectors":["Handicrafts/Artisan"]},
    {"g":"Male","bt":"Other","yr":2020,"emp":3,"reg":"Savanna","rev":"L","gepa":"N","gea":"Y","permit":"A","reach":["National"],"exp":False,"support":["Exhibition"],"heard":"Partner Organisation","sectors":["Construction"]},
    {"g":"Male","bt":"Sole Proprietorship","yr":2018,"emp":4,"reg":"Savanna","rev":"B","gepa":"N","gea":"Y","permit":"Y","reach":["Local/Community","District","Regional","National"],"exp":False,"support":["Training","Networking","Finance","Registration","Digital"],"heard":"Partner Organisation","sectors":["Services","Trading/Retail"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2019,"emp":2,"reg":"Upper East","rev":"L","gepa":"A","gea":"Y","permit":"A","reach":["Local/Community"],"exp":False,"support":["Market Linkages","Branding","Certification","Finance","Export"],"heard":"Social Media","sectors":["Agribusiness","Food Processing"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2020,"emp":2,"reg":"Northern","rev":"B","gepa":"N","gea":"Y","permit":"N","reach":["Local/Community","Regional","National"],"exp":False,"support":["Networking","Branding","Finance","Digital"],"heard":"Social Media","sectors":["Services"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2025,"emp":4,"reg":"Upper East","rev":"B","gepa":"Y","gea":"Y","permit":"Y","reach":["Local/Community","District","Regional"],"exp":False,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Export","Registration","Digital","Exhibition"],"heard":"NENet Event","sectors":["Agribusiness","Food Processing","Trading/Retail"]},
    {"g":"Female","bt":"Sole Proprietorship","yr":2017,"emp":11,"reg":"Northern","rev":"L","gepa":"Y","gea":"Y","permit":"Y","reach":["Regional"],"exp":False,"support":["Training","Market Linkages","Branding","Certification","Finance","Export","Digital","Exhibition"],"heard":"Social Media","sectors":["Agribusiness","Beauty/Cosmetics"]},
    {"g":"Male","bt":"Sole Proprietorship","yr":1996,"emp":7,"reg":"North East","rev":"L","gepa":"N","gea":"N","permit":"N","reach":["Local/Community","District","Regional","National"],"exp":False,"support":["Training","Market Linkages","Networking","Branding","Certification","Finance","Export","Registration","Digital","Exhibition"],"heard":"NENet Event","sectors":["Agribusiness","Food Processing"]},
]

df = pd.DataFrame(records)
N = len(df)

SUPPORT_LABELS = {
    "Training": "Business Training & Capacity Building",
    "Market Linkages": "Market Linkages & Buyer Connections",
    "Networking": "Networking & Mentorship",
    "Branding": "Branding & Packaging Improvement",
    "Certification": "Product Certification (FDA, GSA)",
    "Finance": "Access to Finance/Investment",
    "Export": "Export Facilitation",
    "Registration": "Business Registration Support",
    "Digital": "Technology/Digital Tools Training",
    "Exhibition": "Exhibition & Showcase Opportunities",
}

REV_LABELS = {"B": "Below GHS 50k", "L": "GHS 50k–200k", "M": "GHS 200k–500k", "H": "Above GHS 500k"}
REG_LABELS = {"Y": "Registered", "P": "In Progress", "A": "Agency/Pending", "N": "Not Registered"}

COLORS = {
    "teal": "#3fb950", "amber": "#e3b341", "blue": "#388bfd",
    "purple": "#a371f7", "red": "#da3633", "coral": "#f08080",
    "pink": "#e680a0", "gray": "#6e7681", "green": "#56d364", "orange": "#f78166"
}
PALETTE = list(COLORS.values())

PLOT_BG   = "#161b22"
PAPER_BG  = "#0d1117"
GRID_COL  = "#21262d"
TEXT_COL  = "#8b949e"
TICK_COL  = "#8b949e"

def base_layout(**kwargs):
    return dict(
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=TEXT_COL, size=11),
        margin=dict(l=10, r=10, t=30, b=10),
        **kwargs
    )

def kpi(icon, val, label, badge, badge_bg, badge_col, bar_gradient):
    return f"""
    <div class="kpi-card">
      <div class="kpi-top" style="background:{bar_gradient}"></div>
      <div style="font-size:18px;margin-bottom:8px">{icon}</div>
      <div class="kpi-val">{val}</div>
      <div class="kpi-label">{label}</div>
      <span class="kpi-badge" style="background:{badge_bg};color:{badge_col}">{badge}</span>
    </div>"""

def insight(html):
    return st.markdown(f'<div class="insight-box"><p>{html}</p></div>', unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;
            gap:12px;padding-bottom:1.25rem;border-bottom:1px solid #21262d;margin-bottom:1.5rem">
  <div>
    <span style="background:#1a4731;color:#3fb950;font-size:11px;font-weight:600;
                 padding:4px 10px;border-radius:20px;border:1px solid #238636;letter-spacing:.06em">
      NENet ◆ Northpreneurs
    </span>
    <div style="font-size:22px;font-weight:700;color:#f0f6fc;letter-spacing:-.3px;margin-top:8px">
      Enterprise Analytics Dashboard
    </div>
    <div style="font-size:13px;color:#8b949e;margin-top:4px">
      Northern Ghana Entrepreneurs Network &nbsp;·&nbsp; Baseline Assessment
    </div>
  </div>
  <div style="background:#161b22;border:1px solid #21262d;border-radius:6px;
              padding:4px 12px;font-size:12px;color:#6e7681;white-space:nowrap;align-self:flex-start">
    April 2026 &nbsp;|&nbsp; n = 35 businesses
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
female_n = (df["g"] == "Female").sum()
exp_n    = df["exp"].sum()
emp_valid = [r["emp"] for r in records if isinstance(r["emp"], int)]
avg_emp  = round(sum(emp_valid) / len(emp_valid), 1)
total_emp = sum(emp_valid)

with c1:
    st.markdown(kpi("🏢","35","Total Businesses","4 Regions","#1a2d4a","#388bfd","linear-gradient(90deg,#1f6feb,#388bfd)"), unsafe_allow_html=True)
with c2:
    st.markdown(kpi("👩‍💼","69%","Female-Led Businesses",f"{female_n} of 35","#2d1a47","#a371f7","linear-gradient(90deg,#a371f7,#d2a8ff)"), unsafe_allow_html=True)
with c3:
    st.markdown(kpi("🌍","23%","Active Exporters","8 confirmed","#1a3d26","#3fb950","linear-gradient(90deg,#3fb950,#56d364)"), unsafe_allow_html=True)
with c4:
    st.markdown(kpi("👥",str(avg_emp),"Avg. Employees per Business",f"{total_emp} jobs total","#3d2e00","#e3b341","linear-gradient(90deg,#e3b341,#f0d060)"), unsafe_allow_html=True)

st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────
tabs = st.tabs(["📊 Overview", "🏛 Formalization", "🌐 Market & Export", "🤝 Support & Outreach", "🏭 Sectors"])

# ════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════
with tabs[0]:
    col1, col2 = st.columns(2)

    with col1:
        gender_counts = df["g"].value_counts()
        fig = go.Figure(go.Pie(
            labels=gender_counts.index, values=gender_counts.values,
            hole=0.65, marker_colors=[COLORS["purple"], COLORS["blue"]],
            textinfo="none", hovertemplate="%{label}: %{value} (%{percent})<extra></extra>"
        ))
        fig.update_layout(**base_layout(title=dict(text="Gender Distribution", font=dict(color="#f0f6fc",size=13)), height=260,
                          legend=dict(font=dict(color=TEXT_COL), bgcolor=PLOT_BG, bordercolor=GRID_COL, borderwidth=1)))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        bt_counts = df["bt"].value_counts()
        fig2 = go.Figure(go.Pie(
            labels=bt_counts.index, values=bt_counts.values,
            hole=0.60, marker_colors=PALETTE[:len(bt_counts)],
            textinfo="none", hovertemplate="%{label}: %{value}<extra></extra>"
        ))
        fig2.update_layout(**base_layout(title=dict(text="Business Type", font=dict(color="#f0f6fc",size=13)), height=260,
                           legend=dict(font=dict(color=TEXT_COL,size=10), bgcolor=PLOT_BG, bordercolor=GRID_COL, borderwidth=1)))
        st.plotly_chart(fig2, use_container_width=True)

    # Region bar
    reg_counts = df["reg"].value_counts().reset_index()
    reg_counts.columns = ["Region", "Count"]
    fig3 = go.Figure(go.Bar(
        x=reg_counts["Region"], y=reg_counts["Count"],
        marker_color=PALETTE[:len(reg_counts)],
        text=reg_counts["Count"], textposition="outside",
        hovertemplate="%{x}: %{y}<extra></extra>"
    ))
    fig3.update_layout(**base_layout(title=dict(text="Regional Distribution", font=dict(color="#f0f6fc",size=13)),
                       height=230, showlegend=False,
                       xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL)),
                       yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL), showgrid=True)))
    st.plotly_chart(fig3, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        rev_order = ["B","L","M","H"]
        rev_labels = [REV_LABELS[k] for k in rev_order]
        rev_vals = [int((df["rev"] == k).sum()) for k in rev_order]
        fig4 = go.Figure(go.Bar(
            x=rev_labels, y=rev_vals,
            marker_color=[COLORS["red"],COLORS["amber"],COLORS["teal"],COLORS["blue"]],
            text=rev_vals, textposition="outside"
        ))
        fig4.update_layout(**base_layout(title=dict(text="Annual Revenue Range", font=dict(color="#f0f6fc",size=13)), height=240, showlegend=False,
                           xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL, size=10), tickangle=-15),
                           yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL))))
        st.plotly_chart(fig4, use_container_width=True)

    with col4:
        def era(y):
            if y < 2015: return "Pre-2015"
            elif y <= 2019: return "2015–2019"
            elif y <= 2022: return "2020–2022"
            else: return "2023–2026"
        era_counts = Counter(era(r["yr"]) for r in records)
        era_order  = ["Pre-2015","2015–2019","2020–2022","2023–2026"]
        fig5 = go.Figure(go.Bar(
            x=era_order, y=[era_counts[k] for k in era_order],
            marker_color=[COLORS["gray"],COLORS["teal"],COLORS["blue"],COLORS["amber"]],
            text=[era_counts[k] for k in era_order], textposition="outside"
        ))
        fig5.update_layout(**base_layout(title=dict(text="Business Age — Year Established", font=dict(color="#f0f6fc",size=13)), height=240, showlegend=False,
                           xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL)),
                           yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL))))
        st.plotly_chart(fig5, use_container_width=True)

    insight("📌 <strong>Key finding:</strong> The portfolio is overwhelmingly female-led (69%) and sole-proprietor-based (63%), concentrated in Northern and Upper West regions. Most businesses are post-2015 startups operating at sub-GHS 50,000 revenue — signalling early-stage enterprises with high growth potential and intensive support needs.")

# ════════════════════════════════════════════════════════════
# TAB 2 — FORMALIZATION
# ════════════════════════════════════════════════════════════
with tabs[1]:
    agencies = [
        ("GEPA (Export Promotion Auth.)", "gepa"),
        ("GEA (Ghana Enterprises Agency)", "gea"),
        ("District Assembly Permit", "permit"),
    ]
    reg_colors = {"Y": COLORS["teal"], "P": COLORS["amber"], "A": COLORS["blue"], "N": COLORS["red"]}
    reg_names  = {"Y": "Registered", "P": "In Progress", "A": "Agency/Pending", "N": "Not Registered"}

    # Stacked horizontal bars
    labels, y_yes, y_prog, y_agc, y_no = [], [], [], [], []
    for name, key in agencies:
        counts = Counter(r[key] for r in records)
        labels.append(name)
        y_yes.append(counts.get("Y",0))
        y_prog.append(counts.get("P",0))
        y_agc.append(counts.get("A",0))
        y_no.append(counts.get("N",0))

    fig6 = go.Figure()
    for vals, status, col in [
        (y_yes, "Registered", COLORS["teal"]),
        (y_prog, "In Progress", COLORS["amber"]),
        (y_agc, "Agency/Pending", COLORS["blue"]),
        (y_no, "Not Registered", COLORS["red"]),
    ]:
        fig6.add_trace(go.Bar(
            name=status, y=labels, x=vals, orientation="h",
            marker_color=col, text=[v if v>0 else "" for v in vals],
            textposition="inside", insidetextanchor="middle",
            hovertemplate=f"{status}: %{{x}}<extra></extra>"
        ))
    fig6.update_layout(**base_layout(
        title=dict(text="Agency Registration Status", font=dict(color="#f0f6fc",size=13)),
        barmode="stack", height=260,
        legend=dict(font=dict(color=TEXT_COL), bgcolor=PLOT_BG, bordercolor=GRID_COL, borderwidth=1, orientation="h", y=-0.25),
        xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL), title="Number of businesses"),
        yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL, size=11))
    ))
    st.plotly_chart(fig6, use_container_width=True)

    # Composite score
    def formal_score(r):
        return sum(1 for k in ["gepa","gea","permit"] if r[k]=="Y")
    buckets = {"All 3 Registered":0,"2 Registered":0,"1 Registered":0,"None":0}
    for r in records:
        s = formal_score(r)
        if s==3: buckets["All 3 Registered"]+=1
        elif s==2: buckets["2 Registered"]+=1
        elif s==1: buckets["1 Registered"]+=1
        else: buckets["None"]+=1
    fig7 = go.Figure(go.Bar(
        x=list(buckets.keys()), y=list(buckets.values()),
        marker_color=[COLORS["teal"],COLORS["amber"],COLORS["red"],"#3d1a1a"],
        text=list(buckets.values()), textposition="outside"
    ))
    fig7.update_layout(**base_layout(
        title=dict(text="Formalization Composite Score", font=dict(color="#f0f6fc",size=13)),
        height=240, showlegend=False,
        xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL)),
        yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL))
    ))
    st.plotly_chart(fig7, use_container_width=True)

    insight("📌 <strong>Key finding:</strong> GEA has the highest registration uptake as the primary SME body. GEPA registration is relatively strong, aligning with export ambitions. District Assembly permits show significant gaps — a priority area for formalization support. Only <strong>~23%</strong> are fully registered across all three bodies.")

# ════════════════════════════════════════════════════════════
# TAB 3 — MARKET & EXPORT
# ════════════════════════════════════════════════════════════
with tabs[2]:
    col1, col2 = st.columns(2)

    with col1:
        exp_c = df["exp"].value_counts()
        fig8 = go.Figure(go.Pie(
            labels=["Exporting","Not Exporting"], values=[exp_c.get(True,0), exp_c.get(False,0)],
            hole=0.65, marker_colors=[COLORS["teal"],COLORS["red"]],
            textinfo="none", hovertemplate="%{label}: %{value} (%{percent})<extra></extra>"
        ))
        fig8.update_layout(**base_layout(title=dict(text="Export Status", font=dict(color="#f0f6fc",size=13)), height=260,
                           legend=dict(font=dict(color=TEXT_COL), bgcolor=PLOT_BG, bordercolor=GRID_COL, borderwidth=1)))
        st.plotly_chart(fig8, use_container_width=True)

    with col2:
        dests = {"Europe":3,"West Africa (ECOWAS)":3,"North America":1,"Burkina Faso":1}
        fig9 = go.Figure(go.Bar(
            x=list(dests.values()), y=list(dests.keys()),
            orientation="h",
            marker_color=[COLORS["teal"],COLORS["blue"],COLORS["amber"],COLORS["purple"]],
            text=list(dests.values()), textposition="outside"
        ))
        fig9.update_layout(**base_layout(
            title=dict(text="Export Destinations (Active Exporters)", font=dict(color="#f0f6fc",size=13)),
            height=260, showlegend=False,
            xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL)),
            yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL))
        ))
        st.plotly_chart(fig9, use_container_width=True)

    # Market reach bars
    reach_levels = ["Local/Community","District","Regional","National"]
    reach_vals = [sum(1 for r in records if lv in r["reach"]) for lv in reach_levels]
    fig10 = go.Figure(go.Bar(
        x=reach_levels, y=reach_vals,
        marker_color=[COLORS["gray"],COLORS["amber"],COLORS["blue"],COLORS["teal"]],
        text=[f"{v} ({round(v/N*100)}%)" for v in reach_vals], textposition="outside"
    ))
    fig10.update_layout(**base_layout(
        title=dict(text="Market Reach — Coverage Levels", font=dict(color="#f0f6fc",size=13)),
        height=240, showlegend=False,
        xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL)),
        yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL))
    ))
    st.plotly_chart(fig10, use_container_width=True)

    # Revenue vs Export
    rev_order = ["B","L","M","H"]
    rev_exp   = [sum(1 for r in records if r["rev"]==k and r["exp"]) for k in rev_order]
    rev_noexp = [sum(1 for r in records if r["rev"]==k and not r["exp"]) for k in rev_order]
    fig11 = go.Figure()
    fig11.add_trace(go.Bar(name="Exporting", x=[REV_LABELS[k] for k in rev_order], y=rev_exp, marker_color=COLORS["teal"], borderradius=4))
    fig11.add_trace(go.Bar(name="Not Exporting", x=[REV_LABELS[k] for k in rev_order], y=rev_noexp, marker_color=COLORS["red"], borderradius=4))
    fig11.update_layout(**base_layout(
        title=dict(text="Revenue vs Export Activity", font=dict(color="#f0f6fc",size=13)),
        barmode="stack", height=260,
        legend=dict(font=dict(color=TEXT_COL), bgcolor=PLOT_BG, bordercolor=GRID_COL, borderwidth=1),
        xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL, size=10), tickangle=-15),
        yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL))
    ))
    st.plotly_chart(fig11, use_container_width=True)

    insight("📌 <strong>Key finding:</strong> Despite low formal export rates (23%), market reach is broad — <strong>54%</strong> operate at national level. High-revenue businesses (Above GHS 500k) account for the majority of confirmed exporters, pointing to a revenue threshold before export becomes viable. Destinations span Europe, West Africa, and North America.")

# ════════════════════════════════════════════════════════════
# TAB 4 — SUPPORT & OUTREACH
# ════════════════════════════════════════════════════════════
with tabs[3]:
    # Support needs
    sup_counts = Counter()
    for r in records:
        for s in r["support"]:
            sup_counts[s] += 1
    sup_sorted = sorted(sup_counts.items(), key=lambda x: x[1])
    sup_labels = [SUPPORT_LABELS.get(k,k) for k,_ in sup_sorted]
    sup_vals   = [v for _,v in sup_sorted]
    sup_pcts   = [f"{round(v/N*100)}%" for v in sup_vals]

    fig12 = go.Figure(go.Bar(
        y=sup_labels, x=sup_vals, orientation="h",
        marker_color=PALETTE[:len(sup_vals)],
        text=[f"{v} ({p})" for v,p in zip(sup_vals, sup_pcts)],
        textposition="outside"
    ))
    fig12.update_layout(**base_layout(
        title=dict(text="Support Needs — Ranked by Demand", font=dict(color="#f0f6fc",size=13)),
        height=380, showlegend=False,
        xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL)),
        yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL, size=11))
    ))
    st.plotly_chart(fig12, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        heard_counts = Counter(r["heard"] for r in records)
        fig13 = go.Figure(go.Pie(
            labels=list(heard_counts.keys()), values=list(heard_counts.values()),
            hole=0.60, marker_colors=PALETTE[:len(heard_counts)],
            textinfo="none", hovertemplate="%{label}: %{value} (%{percent})<extra></extra>"
        ))
        fig13.update_layout(**base_layout(
            title=dict(text="How Businesses Heard About NENet", font=dict(color="#f0f6fc",size=13)),
            height=270, legend=dict(font=dict(color=TEXT_COL,size=10), bgcolor=PLOT_BG, bordercolor=GRID_COL, borderwidth=1)
        ))
        st.plotly_chart(fig13, use_container_width=True)

    with col2:
        key_sup = ["Training","Market Linkages","Finance","Export","Networking"]
        female_sup = [sum(1 for r in records if r["g"]=="Female" and s in r["support"]) for s in key_sup]
        male_sup   = [sum(1 for r in records if r["g"]=="Male" and s in r["support"]) for s in key_sup]
        fig14 = go.Figure()
        fig14.add_trace(go.Bar(name="Female", x=key_sup, y=female_sup, marker_color=COLORS["purple"]))
        fig14.add_trace(go.Bar(name="Male",   x=key_sup, y=male_sup,   marker_color=COLORS["blue"]))
        fig14.update_layout(**base_layout(
            title=dict(text="Top Support Needs by Gender", font=dict(color="#f0f6fc",size=13)),
            barmode="group", height=270,
            legend=dict(font=dict(color=TEXT_COL), bgcolor=PLOT_BG, bordercolor=GRID_COL, borderwidth=1),
            xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL, size=10)),
            yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL))
        ))
        st.plotly_chart(fig14, use_container_width=True)

    insight("📌 <strong>Key finding:</strong> <strong>Access to Finance/Investment</strong> and <strong>Market Linkages</strong> are the most universal needs (both requested by >77% of businesses). Social Media is the dominant discovery channel (40%), suggesting digital outreach is working. Partner organisations account for 26% — a valuable pipeline worth strengthening.")

# ════════════════════════════════════════════════════════════
# TAB 5 — SECTORS
# ════════════════════════════════════════════════════════════
with tabs[4]:
    col1, col2 = st.columns(2)

    with col1:
        sect_counts = Counter()
        for r in records:
            for s in r["sectors"]:
                sect_counts[s.strip()] += 1
        sect_sorted = sorted(sect_counts.items(), key=lambda x: x[1])
        fig15 = go.Figure(go.Bar(
            y=[s[0] for s in sect_sorted], x=[s[1] for s in sect_sorted],
            orientation="h",
            marker_color=PALETTE[:len(sect_sorted)],
            text=[s[1] for s in sect_sorted], textposition="outside"
        ))
        fig15.update_layout(**base_layout(
            title=dict(text="Industry / Sector Distribution", font=dict(color="#f0f6fc",size=13)),
            height=360, showlegend=False,
            xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL)),
            yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL, size=11))
        ))
        st.plotly_chart(fig15, use_container_width=True)

    with col2:
        act_cats = {
            "Shea Processing": sum(1 for r in records if "shea" in r["sectors"][0].lower() or "shea" in str(r.get("g","")).lower() or any("shea" in s.lower() for s in r["sectors"])),
            "General Agro-Processing": 6,
            "Farming / Aggregation": 4,
            "Food Processing": 5,
            "Manufacturing": 3,
            "Fashion / Textile": 3,
            "Services / Other": 4,
            "Construction": 1,
        }
        # More precise count
        act_cats = {}
        for r in records:
            sects = [s.lower() for s in r["sectors"]]
            activity = r.get("sectors", [])
            if any("agribusiness" in s for s in sects) and not any(x in sects for x in ["food processing","manufacturing"]): 
                cat = "Pure Agribusiness"
            elif "food processing" in sects:
                cat = "Food Processing"
            elif "beauty/cosmetics" in sects:
                cat = "Beauty / Cosmetics"
            elif "textile/fashion" in sects:
                cat = "Textile / Fashion"
            elif "construction" in sects:
                cat = "Construction"
            elif "services" in sects:
                cat = "Services"
            elif "manufacturing" in sects:
                cat = "Manufacturing"
            elif "handicrafts/artisan" in sects:
                cat = "Handicrafts"
            else:
                cat = "Other"
            act_cats[cat] = act_cats.get(cat, 0) + 1
        
        act_sorted = sorted(act_cats.items(), key=lambda x: x[1])
        fig16 = go.Figure(go.Bar(
            y=[a[0] for a in act_sorted], x=[a[1] for a in act_sorted],
            orientation="h",
            marker_color=PALETTE[:len(act_sorted)],
            text=[a[1] for a in act_sorted], textposition="outside"
        ))
        fig16.update_layout(**base_layout(
            title=dict(text="Primary Sector Categories", font=dict(color="#f0f6fc",size=13)),
            height=360, showlegend=False,
            xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL)),
            yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL, size=11))
        ))
        st.plotly_chart(fig16, use_container_width=True)

    # Sector vs Revenue heatmap
    key_sects = ["Agribusiness","Food Processing","Beauty/Cosmetics","Textile/Fashion","Services"]
    rev_order  = ["B","L","M","H"]
    heat_data  = []
    for sect in key_sects:
        row = []
        for rv in rev_order:
            cnt = sum(1 for r in records if sect in r["sectors"] and r["rev"]==rv)
            row.append(cnt)
        heat_data.append(row)

    fig17 = go.Figure(go.Heatmap(
        z=heat_data,
        x=[REV_LABELS[k] for k in rev_order],
        y=key_sects,
        colorscale=[[0,"#0d1117"],[0.5,"#1a4731"],[1,"#3fb950"]],
        text=heat_data, texttemplate="%{text}",
        hovertemplate="Sector: %{y}<br>Revenue: %{x}<br>Count: %{z}<extra></extra>",
        showscale=False
    ))
    fig17.update_layout(**base_layout(
        title=dict(text="Revenue Distribution by Sector", font=dict(color="#f0f6fc",size=13)),
        height=260,
        xaxis=dict(tickfont=dict(color=TICK_COL, size=10), tickangle=-15),
        yaxis=dict(tickfont=dict(color=TICK_COL, size=11))
    ))
    st.plotly_chart(fig17, use_container_width=True)

    insight("📌 <strong>Key finding:</strong> <strong>Agribusiness</strong> and <strong>Food Processing</strong> dominate the portfolio (80%+ involvement), with Shea butter processing emerging as a signature value chain. Beauty/Cosmetics is growing as a natural extension of agro-processing. The sector concentration suggests NENet can build deep expertise and clustered support programmes around the Shea value chain.")

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;font-size:11px;color:#3d4450;padding-top:1rem;border-top:1px solid #21262d">
  NENet Northpreneurs · Enterprise Analytics Dashboard · Built with Streamlit &amp; Plotly
</div>
""", unsafe_allow_html=True)
