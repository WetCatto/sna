"""
app.py — Dark minimal narrative dashboard for:
"Structural Architecture of Political Misinformation Diffusion:
 A Social Network Analysis of Coordinated Inauthentic Behavior
 in the 2022 Philippine Presidential Election"

Run: streamlit run app.py
"""

from __future__ import annotations

import io
import os
import sys

import networkx as nx
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, os.path.dirname(__file__))
from core import (
    COMM_COLORS,
    COMMUNITY_DEFS,
    BOT_COLOR,
    ORGANIC_COLOR,
    build_graph,
    compute_metrics,
)

# ---------------------------------------------------------------------------
# Page config — must be first Streamlit call
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="PH Political Disinformation — SNA",
    page_icon="🕸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Global CSS
# ---------------------------------------------------------------------------

st.markdown("""
<style>
/* Page resets */
section[data-testid="stMain"] > div { padding-top: 0.5rem; }
.block-container { padding: 1rem 2.5rem 4rem 2.5rem; max-width: 1400px; }
html, body { overflow-x: hidden; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* Section labels — replace all st.subheader() */
.section-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #4f8ef7;
    margin: 2.5rem 0 0.75rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1e2130;
}

/* Section divider */
.section-divider {
    border: none;
    border-top: 1px solid #1e2130;
    margin: 2.5rem 0;
}

/* Metric cards */
.metric-card {
    background: #1e2130;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    border: 1px solid rgba(79,142,247,0.12);
    position: relative;
    overflow: hidden;
    height: 100%;
}
.metric-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #4f8ef7 0%, transparent 100%);
    opacity: 0.6;
}
.metric-card.bot-card::before {
    background: linear-gradient(90deg, #e05c5c 0%, transparent 100%);
}
.metric-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8890a4;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #e8eaf0;
    line-height: 1;
    margin-bottom: 0.25rem;
    letter-spacing: -0.02em;
}
.metric-card.bot-card .metric-value { color: #e05c5c; }
.metric-sub {
    font-size: 0.7rem;
    color: #8890a4;
    margin-top: 0.3rem;
    line-height: 1.3;
}

/* Finding callout cards */
.finding-card {
    background: rgba(79,142,247,0.06);
    border-left: 3px solid #4f8ef7;
    border-radius: 0 8px 8px 0;
    padding: 1.1rem 1.4rem;
    height: 100%;
}
.finding-card.rq4-card {
    background: rgba(224,92,92,0.06);
    border-left-color: #e05c5c;
}
.finding-rq {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #4f8ef7;
    margin-bottom: 0.4rem;
}
.finding-card.rq4-card .finding-rq { color: #e05c5c; }
.finding-body {
    font-size: 0.88rem;
    color: #e8eaf0;
    line-height: 1.55;
}
.finding-body strong { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Caching
# ---------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def run_simulation(n_total: int, bot_fraction: float, seed: int = 2022) -> tuple[bytes, dict]:
    G = build_graph(n_total=n_total, bot_fraction=bot_fraction, seed=seed)
    results = compute_metrics(G)
    buf = io.BytesIO()
    nx.write_gexf(G, buf)
    return buf.getvalue(), results


def load_graph(gexf_bytes: bytes) -> nx.DiGraph:
    G = nx.read_gexf(io.BytesIO(gexf_bytes))
    # GEXF round-trip converts integer node IDs to strings; convert back
    return nx.relabel_nodes(G, {n: int(n) for n in G.nodes()})


def metric_card(label: str, value: str, sub: str = "", bot: bool = False) -> str:
    cls = "metric-card bot-card" if bot else "metric-card"
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ""
    return (
        f'<div class="{cls}">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'{sub_html}</div>'
    )


CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(30,33,48,0.5)",
    font=dict(color="#e8eaf0", size=11),
    title_font=dict(size=12, color="#8890a4"),
    legend=dict(
        bgcolor="rgba(30,33,48,0.8)",
        bordercolor="rgba(79,142,247,0.15)",
        borderwidth=1,
        font=dict(size=10),
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(size=9, color="#8890a4"),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(size=9, color="#8890a4"),
    ),
    margin=dict(l=40, r=20, t=40, b=40),
)


def apply_chart_style(fig, title: str = "") -> None:
    fig.update_layout(**CHART_LAYOUT)
    if title:
        fig.update_layout(title=dict(text=title, x=0, xanchor="left",
                                     font=dict(size=12, color="#8890a4")))


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown('<p class="section-label">Simulation Parameters</p>',
                unsafe_allow_html=True)
    n_total = st.slider("Total Accounts (N)", 500, 5000, 2500, step=100)
    bot_pct = st.slider("Bot Fraction", 5, 40, 20, step=1,
                        format="%d%%")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Community Breakdown</p>',
                unsafe_allow_html=True)
    for name, frac in COMMUNITY_DEFS:
        count = int(n_total * frac)
        st.caption(f"{name} — ~{count} ({int(frac*100)}%)")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    regenerate = st.button("Regenerate", use_container_width=True, type="primary")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Dataset</p>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:0.72rem;color:#8890a4;line-height:1.6;">'
        'Twitter Information Operations<br>'
        'Philippines Release — August 2019<br><br>'
        '<span style="font-size:0.65rem;color:#555c70;">'
        'Original source (transparency.x.com)<br>is no longer publicly accessible.</span>'
        '</p>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Computation
# ---------------------------------------------------------------------------

if regenerate:
    with st.spinner("Rebuilding network…"):
        gexf_bytes, results = run_simulation(n_total, bot_pct / 100.0, 2022)
else:
    with st.spinner("Loading simulation with paper parameters…"):
        gexf_bytes, results = run_simulation(2500, 0.20, 2022)

df = pd.DataFrame(results["rows"])
summary = results["summary"]

comm_stats = df.groupby(["louvain_community", "louvain_community_name"]).agg(
    N=("node_id", "count"),
    Bots=("node_type", lambda x: (x == "bot_suspected").sum()),
    Avg_PageRank=("pagerank", "mean"),
    Avg_Betweenness=("betweenness_centrality", "mean"),
    Avg_Clustering=("clustering_coefficient", "mean"),
    Avg_Reciprocity=("reciprocity", "mean"),
).reset_index()
comm_stats["Bot %"] = (comm_stats["Bots"] / comm_stats["N"] * 100).round(1)
comm_stats = comm_stats.sort_values("N", ascending=False).reset_index(drop=True)

# Dynamic findings derivation
top12 = df.nlargest(12, "pagerank")
all_organic = (top12["node_type"] == "organic").all()
top_comm = top12["louvain_community_name"].mode()[0]
rq1_text = (
    f'Top <strong>12</strong> content hubs are exclusively organic — concentrated in '
    f'<strong>{top_comm}</strong>'
    if all_organic else
    f'Top <strong>12</strong> content hubs include bot-suspected accounts — '
    f'concentrated in <strong>{top_comm}</strong>'
)

top_bt = df.nlargest(1, "betweenness_centrality").iloc[0]
broker_id = int(top_bt["node_id"])
broker_is_bot = top_bt["node_type"] == "bot_suspected"
broker_comm = top_bt["louvain_community_name"]
broker_bt = top_bt["betweenness_centrality"]
rq2_qualifier = "bot-suspected" if broker_is_bot else "organic"
rq2_text = (
    f'<strong>Acc. {broker_id}</strong> ({rq2_qualifier}) holds highest betweenness '
    f'({broker_bt:.4f}) — primary structural bridge across community boundaries'
)

worst = comm_stats.loc[comm_stats["Bot %"].idxmax()]
rq4_text = (
    f'<strong>{worst["louvain_community_name"]}</strong> has '
    f'<strong>{worst["Bot %"]:.0f}%</strong> bot concentration '
    f'({int(worst["N"])} nodes) — pure amplification layer'
)

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------

st.markdown("""
<div style="padding: 2rem 0 1.25rem 0; border-bottom: 1px solid #1e2130; margin-bottom: 0.5rem;">
    <h1 style="font-size:1.7rem; font-weight:800; color:#e8eaf0;
               letter-spacing:-0.03em; margin:0 0 0.4rem 0; line-height:1.2;">
        Structural Architecture of Political Misinformation Diffusion
    </h1>
    <p style="font-size:0.85rem; color:#8890a4; margin:0; line-height:1.5;">
        A Social Network Analysis of Coordinated Inauthentic Behavior in the 2022 Philippine Presidential Election
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SECTION 1 — Network Overview
# ---------------------------------------------------------------------------

st.markdown('<p class="section-label">Network Overview</p>', unsafe_allow_html=True)

cols1 = st.columns(4)
cards_row1 = [
    ("Nodes (N)", f"{summary['nodes']:,}", "Total simulated accounts"),
    ("Edges (E)", f"{summary['edges']:,}", "Directed retweet relationships"),
    ("Density", f"{summary['density']:.4f}", "Typical for large social networks"),
    ("Global Reciprocity", f"{summary['global_reciprocity']:.4f}", "Near-zero = unidirectional amplification"),
]
for col, (label, value, sub) in zip(cols1, cards_row1):
    col.markdown(metric_card(label, value, sub), unsafe_allow_html=True)

st.markdown("<div style='margin-top:0.75rem'></div>", unsafe_allow_html=True)

cols2 = st.columns(4)
cards_row2 = [
    ("Avg Clustering", f"{summary['avg_clustering']:.4f}", "Low = hub-and-spoke, not social"),
    ("Communities", str(summary["louvain_communities"]), "Louvain partitions detected"),
    ("Modularity (Q)", f"{summary['louvain_modularity']:.4f}", "Q > 0.3 = meaningful structure"),
    ("Bot-Suspected", f"{summary['bot_count']:,}",
     f"{summary['bot_count']/summary['nodes']*100:.1f}% of all accounts"),
]
for col, (label, value, sub) in zip(cols2, cards_row2):
    is_bot = label == "Bot-Suspected"
    col.markdown(metric_card(label, value, sub, bot=is_bot), unsafe_allow_html=True)

st.markdown('<p class="section-label">Community Breakdown</p>', unsafe_allow_html=True)

display_comm = comm_stats[[
    "louvain_community_name", "N", "Bots", "Bot %",
    "Avg_PageRank", "Avg_Reciprocity",
]].rename(columns={
    "louvain_community_name": "Community",
    "Avg_PageRank": "Avg PageRank",
    "Avg_Reciprocity": "Avg Reciprocity",
})

st.dataframe(
    display_comm.style
    .format({"Avg PageRank": "{:.5f}", "Avg Reciprocity": "{:.4f}", "Bot %": "{:.1f}%"})
    .background_gradient(subset=["Bot %"], cmap="Reds"),
    use_container_width=True,
    hide_index=True,
)

# ---------------------------------------------------------------------------
# SECTION 2 — Key Findings
# ---------------------------------------------------------------------------

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Key Findings</p>', unsafe_allow_html=True)

fc1, fc2, fc3 = st.columns(3)

with fc1:
    st.markdown(f"""
    <div class="finding-card">
        <div class="finding-rq">RQ1 — Content Hubs</div>
        <div class="finding-body">{rq1_text}</div>
    </div>""", unsafe_allow_html=True)

with fc2:
    st.markdown(f"""
    <div class="finding-card">
        <div class="finding-rq">RQ2 — Structural Broker</div>
        <div class="finding-body">{rq2_text}</div>
    </div>""", unsafe_allow_html=True)

with fc3:
    st.markdown(f"""
    <div class="finding-card rq4-card">
        <div class="finding-rq">RQ4 — Bot Community</div>
        <div class="finding-body">{rq4_text}</div>
    </div>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SECTION 3 — Centrality Analysis
# ---------------------------------------------------------------------------

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Centrality Analysis</p>', unsafe_allow_html=True)

ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 1])
with ctrl1:
    metric_col = st.selectbox(
        "Sort by metric",
        ["pagerank", "in_degree", "out_degree",
         "betweenness_centrality", "clustering_coefficient", "reciprocity"],
        format_func=lambda x: {
            "pagerank": "PageRank",
            "in_degree": "In-Degree",
            "out_degree": "Out-Degree",
            "betweenness_centrality": "Betweenness Centrality",
            "clustering_coefficient": "Clustering Coefficient",
            "reciprocity": "Reciprocity",
        }[x],
    )
with ctrl2:
    type_filter = st.selectbox(
        "Account type",
        ["All", "Organic only", "Bot-suspected only"],
    )
with ctrl3:
    top_n = st.slider("Top N", 5, 50, 12)

filtered = df.copy()
if type_filter == "Organic only":
    filtered = filtered[filtered["node_type"] == "organic"]
elif type_filter == "Bot-suspected only":
    filtered = filtered[filtered["node_type"] == "bot_suspected"]

top_df = filtered.nlargest(top_n, metric_col)[[
    "node_id", "node_type", "louvain_community_name",
    "pagerank", "in_degree", "out_degree",
    "betweenness_centrality", "clustering_coefficient", "reciprocity",
]].rename(columns={
    "node_id": "Account", "node_type": "Type",
    "louvain_community_name": "Community",
    "pagerank": "PageRank", "in_degree": "In-Deg",
    "out_degree": "Out-Deg",
    "betweenness_centrality": "Betweenness",
    "clustering_coefficient": "Clustering",
})
top_df["Account"] = top_df["Account"].apply(lambda x: f"Acc. {x}")

def highlight_bots(row: pd.Series) -> list[str]:
    if row["Type"] == "bot_suspected":
        return ["background-color: rgba(224,92,92,0.12)"] * len(row)
    return [""] * len(row)

st.dataframe(
    top_df.style.apply(highlight_bots, axis=1),
    use_container_width=True,
    hide_index=True,
)

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

col_sc, col_empty = st.columns(2)
with col_sc:
    sample = df.sample(min(1000, len(df)), random_state=42)
    fig_scatter = px.scatter(
        sample, x="in_degree", y="out_degree",
        color="node_type",
        color_discrete_map={"bot_suspected": BOT_COLOR, "organic": ORGANIC_COLOR},
        labels={"in_degree": "In-Degree", "out_degree": "Out-Degree",
                "node_type": "Account Type"},
        opacity=0.5,
    )
    fig_scatter.update_traces(marker=dict(size=4))
    apply_chart_style(fig_scatter, "In-Degree vs Out-Degree")
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_empty:
    st.markdown("""
    <div style="padding:1.5rem; color:#8890a4; font-size:0.8rem; line-height:1.7;
                border:1px solid #1e2130; border-radius:10px; margin-top:0.5rem;">
        <strong style="color:#e8eaf0; font-size:0.85rem;">Reading the scatter</strong><br><br>
        Bot-suspected accounts cluster in the <em>high out-degree, low in-degree</em> quadrant —
        many retweets sent, few received. This asymmetry is the primary structural signature
        of automated amplification behavior documented by Ferrara et al. (2016).<br><br>
        Organic accounts occupy a more symmetric region, reflecting genuine bidirectional
        social exchange.
    </div>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SECTION 4 — Bot Detection Patterns
# ---------------------------------------------------------------------------

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Bot Detection Patterns</p>', unsafe_allow_html=True)

sample2 = df.sample(min(1000, len(df)), random_state=42)
fig_pr_bt = px.scatter(
    sample2, x="pagerank", y="betweenness_centrality",
    color="node_type",
    color_discrete_map={"bot_suspected": BOT_COLOR, "organic": ORGANIC_COLOR},
    labels={"pagerank": "PageRank",
            "betweenness_centrality": "Betweenness Centrality",
            "node_type": "Account Type"},
    opacity=0.5,
)
fig_pr_bt.update_traces(marker=dict(size=4))

pr_90 = df["pagerank"].quantile(0.9)
bt_90 = df["betweenness_centrality"].quantile(0.9)
fig_pr_bt.add_vline(
    x=pr_90, line_dash="dot",
    line_color="rgba(255,255,255,0.2)",
    annotation_text="90th pct PageRank",
    annotation_font=dict(size=8, color="#8890a4"),
    annotation_position="top right",
)
fig_pr_bt.add_hline(
    y=bt_90, line_dash="dot",
    line_color="rgba(255,255,255,0.2)",
    annotation_text="90th pct Betweenness",
    annotation_font=dict(size=8, color="#8890a4"),
    annotation_position="top right",
)
apply_chart_style(fig_pr_bt, "PageRank vs Betweenness — Structural Broker Detection")
st.plotly_chart(fig_pr_bt, use_container_width=True)

col_cl, col_rc = st.columns(2)
with col_cl:
    fig_clust = px.box(
        df, x="node_type", y="clustering_coefficient",
        color="node_type",
        color_discrete_map={"bot_suspected": BOT_COLOR, "organic": ORGANIC_COLOR},
        labels={"node_type": "Account Type",
                "clustering_coefficient": "Clustering Coefficient"},
        points=False,
    )
    fig_clust.update_layout(showlegend=False)
    apply_chart_style(fig_clust, "Clustering Coefficient by Account Type")
    st.plotly_chart(fig_clust, use_container_width=True)

with col_rc:
    fig_recip = px.box(
        df, x="node_type", y="reciprocity",
        color="node_type",
        color_discrete_map={"bot_suspected": BOT_COLOR, "organic": ORGANIC_COLOR},
        labels={"node_type": "Account Type", "reciprocity": "Per-node Reciprocity"},
        points=False,
    )
    fig_recip.update_layout(showlegend=False)
    apply_chart_style(fig_recip, "Reciprocity by Account Type")
    st.plotly_chart(fig_recip, use_container_width=True)

# ---------------------------------------------------------------------------
# SECTION 5 — Community Structure
# ---------------------------------------------------------------------------

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Community Structure</p>', unsafe_allow_html=True)

col_bar, col_pie = st.columns(2)
with col_bar:
    fig_bot_pct = px.bar(
        comm_stats, x="louvain_community_name", y="Bot %",
        color="louvain_community_name",
        color_discrete_sequence=COMM_COLORS,
        text_auto=True,
    )
    fig_bot_pct.update_traces(opacity=0.85, textfont_size=9, textposition="outside")
    fig_bot_pct.update_layout(showlegend=False, xaxis_tickangle=-25)
    apply_chart_style(fig_bot_pct, "Bot Percentage by Community")
    st.plotly_chart(fig_bot_pct, use_container_width=True)

with col_pie:
    fig_pie = px.pie(
        comm_stats, values="N", names="louvain_community_name",
        color_discrete_sequence=COMM_COLORS,
        hole=0.4,
    )
    fig_pie.update_traces(textinfo="label+percent", textfont_size=10)
    apply_chart_style(fig_pie, "Community Size Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------------------------------------------------------
# SECTION 6 — Interactive Network
# ---------------------------------------------------------------------------

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Interactive Network</p>', unsafe_allow_html=True)
st.caption(
    "Top 200 nodes by PageRank. Node size proportional to PageRank. Hover for full metrics."
)

color_by = st.radio(
    "Color nodes by", ["Community", "Account Type"], horizontal=True
)

try:
    from pyvis.network import Network as PyvisNetwork

    top_node_ids = df.nlargest(200, "pagerank")["node_id"].tolist()
    G_full = load_graph(gexf_bytes)
    G_sub = G_full.subgraph(top_node_ids)
    df_sub = df[df["node_id"].isin(top_node_ids)].set_index("node_id")

    net = PyvisNetwork(height="600px", width="100%", directed=True,
                       bgcolor="#0f1117", font_color="#e8eaf0",
                       cdn_resources="in_line")
    net.set_options("""{
      "physics": {
        "barnesHut": {"gravitationalConstant": -8000, "springLength": 120},
        "stabilization": {"iterations": 100}
      },
      "nodes": {"borderWidth": 1, "borderWidthSelected": 2},
      "edges": {
        "arrows": {"to": {"enabled": true, "scaleFactor": 0.35}},
        "color": {"opacity": 0.25},
        "smooth": {"type": "continuous"}
      }
    }""")

    pr_vals = df_sub["pagerank"]
    pr_min, pr_max = pr_vals.min(), pr_vals.max()
    pr_range = max(pr_max - pr_min, 1e-9)

    for nd in G_sub.nodes():
        row = df_sub.loc[nd]
        size = 5 + 35 * (row["pagerank"] - pr_min) / pr_range

        if color_by == "Community":
            lc = int(row["louvain_community"])
            color = COMM_COLORS[lc % len(COMM_COLORS)]
        else:
            color = BOT_COLOR if row["node_type"] == "bot_suspected" else ORGANIC_COLOR

        type_label = "Bot-Suspected" if row["node_type"] == "bot_suspected" else "Organic"
        title = "\n".join([
            f"Account  {nd}",
            "─" * 22,
            f"Type        {type_label}",
            f"Community   {row['louvain_community_name']}",
            "",
            f"PageRank    {row['pagerank']:.4f}",
            f"In-Degree   {row['in_degree']}",
            f"Out-Degree  {row['out_degree']}",
            f"Betweenness {row['betweenness_centrality']:.4f}",
            f"Clustering  {row['clustering_coefficient']:.4f}",
            f"Reciprocity {row['reciprocity']:.4f}",
        ])
        net.add_node(nd, label=f"Acc.{nd}", title=title,
                     size=float(size), color=color)

    for u, v, d in G_sub.edges(data=True):
        net.add_edge(u, v, value=d.get("weight", 1))

    _html = net.generate_html()
    _tooltip_css = """
<style>
div.vis-tooltip {
  background: #1e2130 !important;
  border: 1px solid rgba(79,142,247,0.22) !important;
  border-radius: 8px !important;
  color: #e8eaf0 !important;
  font-family: 'Inter','Segoe UI',system-ui,monospace !important;
  font-size: 11.5px !important;
  line-height: 1.7 !important;
  padding: 10px 16px !important;
  box-shadow: 0 8px 28px rgba(0,0,0,0.6) !important;
  white-space: pre !important;
  max-width: none !important;
  pointer-events: none !important;
}
</style>
"""
    _html = _html.replace("</head>", _tooltip_css + "</head>")
    components.html(_html, height=620, scrolling=False)

except ImportError:
    st.warning("pyvis is not installed. Run `pip install pyvis` to enable the network view.")

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
st.download_button(
    "Download GEXF",
    data=gexf_bytes,
    file_name="ph_election_network.gexf",
    mime="application/gexf+xml",
)
