"""
03_generate_figures.py

Generates all figures for the research paper at 300 DPI.

Figure 2: Full network — nodes sized by PageRank, colored by node type
Figure 3: In-degree vs. out-degree scatter plot by node type
Figure 4: Box plots — clustering coefficient and reciprocity (bot vs organic)
Figure 5: Full network colored by Louvain community
Figure 6: Largest community (Marcos Supporters) subgraph
Figure 7: PageRank vs. betweenness scatter — revealing broker accounts
"""

import csv
import json
import os

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np

matplotlib.use("Agg")   # non-interactive backend

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
FIG_DIR  = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Load graph and metrics
# ---------------------------------------------------------------------------
print("Loading graph and metrics...")
G = nx.read_gexf(os.path.join(DATA_DIR, "ph_election_network.gexf"))
for u, v, d in G.edges(data=True):
    d["weight"] = float(d.get("weight", 1.0))

with open(os.path.join(DATA_DIR, "network_summary.json")) as f:
    summary = json.load(f)

# Load metrics
metrics: dict[str, dict] = {}
with open(os.path.join(DATA_DIR, "metrics.csv")) as f:
    for row in csv.DictReader(f):
        metrics[row["node_id"]] = row

nodes = list(G.nodes())

# ---------------------------------------------------------------------------
# Color palettes
# ---------------------------------------------------------------------------
BOT_COLOR     = "#e74c3c"   # red
ORGANIC_COLOR = "#2980b9"   # blue

COMM_COLORS = {
    "Marcos Supporters":     "#e67e22",   # orange
    "Robredo Supporters":    "#8e44ad",   # purple
    "News & Media Accounts": "#27ae60",   # green
    "Amplification Bots":    "#c0392b",   # dark red
    "Neutral / Undecided":   "#7f8c8d",   # gray
}

# ---------------------------------------------------------------------------
# Compute layout once (used in Figs 2 and 5)
# ---------------------------------------------------------------------------
print("Computing network layout (this may take ~30s)...")
np.random.seed(2022)
# Use a sample of nodes for layout speed, then spring for full
pos = nx.spring_layout(G, seed=2022, k=0.6 / np.sqrt(len(G)), iterations=50)

def node_values(metric_key: str) -> list[float]:
    return [float(metrics[n][metric_key]) for n in nodes]

pr_vals    = node_values("pagerank")
bt_vals    = node_values("betweenness_centrality")
cl_vals    = node_values("clustering_coefficient")
rc_vals    = node_values("reciprocity")
in_vals    = [int(metrics[n]["in_degree"]) for n in nodes]
out_vals   = [int(metrics[n]["out_degree"]) for n in nodes]
type_vals  = [metrics[n]["node_type"] for n in nodes]
comm_vals  = [metrics[n]["louvain_community_name"] for n in nodes]

# ---------------------------------------------------------------------------
# Figure 2: Full network — type coloring, PageRank sizing
# ---------------------------------------------------------------------------
print("Generating Figure 2: full network by node type...")
fig, ax = plt.subplots(figsize=(10, 8))

pr_arr = np.array(pr_vals)
sizes = ((pr_arr - pr_arr.min()) / (pr_arr.max() - pr_arr.min() + 1e-12)) * 60 + 5

colors_type = [BOT_COLOR if t == "bot_suspected" else ORGANIC_COLOR
               for t in type_vals]

nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=nodes,
                       node_size=sizes, node_color=colors_type, alpha=0.7)
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#cccccc",
                       alpha=0.2, width=0.3, arrows=False)

patch_bot = mpatches.Patch(color=BOT_COLOR, label="Bot-Suspected (n=500)")
patch_org = mpatches.Patch(color=ORGANIC_COLOR, label="Organic (n=2,000)")
ax.legend(handles=[patch_org, patch_bot], loc="upper right", fontsize=9)
ax.set_title("Fig. 2. Full Retweet Network — Node Size ∝ PageRank",
             fontsize=11, weight="bold")
ax.axis("off")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig2_network_type.png"),
            dpi=300, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 3: In-degree vs. out-degree scatter by node type
# ---------------------------------------------------------------------------
print("Generating Figure 3: degree scatter plot...")
fig, ax = plt.subplots(figsize=(7, 5))

bot_mask = [i for i, t in enumerate(type_vals) if t == "bot_suspected"]
org_mask = [i for i, t in enumerate(type_vals) if t == "organic"]

ax.scatter([in_vals[i] for i in org_mask],
           [out_vals[i] for i in org_mask],
           c=ORGANIC_COLOR, alpha=0.35, s=12, label="Organic", zorder=2)
ax.scatter([in_vals[i] for i in bot_mask],
           [out_vals[i] for i in bot_mask],
           c=BOT_COLOR, alpha=0.5, s=14, label="Bot-Suspected",
           marker="^", zorder=3)

ax.set_xlabel("In-Degree (Retweet Reception)", fontsize=10)
ax.set_ylabel("Out-Degree (Retweet Activity)", fontsize=10)
ax.set_title("Fig. 3. In-Degree vs. Out-Degree by Account Type", fontsize=11,
             weight="bold")
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig3_degree_scatter.png"),
            dpi=300, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 4: Box plots — clustering and reciprocity (bot vs organic)
# ---------------------------------------------------------------------------
print("Generating Figure 4: structural comparison box plots...")
fig, axes = plt.subplots(1, 2, figsize=(9, 5))

bot_idx = [i for i, t in enumerate(type_vals) if t == "bot_suspected"]
org_idx = [i for i, t in enumerate(type_vals) if t == "organic"]

# Clustering coefficient
cl_bot = [cl_vals[i] for i in bot_idx]
cl_org = [cl_vals[i] for i in org_idx]
bp1 = axes[0].boxplot([cl_org, cl_bot],
                       labels=["Organic", "Bot-Suspected"],
                       patch_artist=True,
                       medianprops=dict(color="black", linewidth=2))
bp1["boxes"][0].set_facecolor(ORGANIC_COLOR + "88")
bp1["boxes"][1].set_facecolor(BOT_COLOR + "88")
axes[0].set_title("(a) Clustering Coefficient", fontsize=10, weight="bold")
axes[0].set_ylabel("Clustering Coefficient", fontsize=9)
axes[0].spines["top"].set_visible(False)
axes[0].spines["right"].set_visible(False)

# Reciprocity
rc_bot = [rc_vals[i] for i in bot_idx]
rc_org = [rc_vals[i] for i in org_idx]
bp2 = axes[1].boxplot([rc_org, rc_bot],
                       labels=["Organic", "Bot-Suspected"],
                       patch_artist=True,
                       medianprops=dict(color="black", linewidth=2))
bp2["boxes"][0].set_facecolor(ORGANIC_COLOR + "88")
bp2["boxes"][1].set_facecolor(BOT_COLOR + "88")
axes[1].set_title("(b) Per-Node Reciprocity", fontsize=10, weight="bold")
axes[1].set_ylabel("Reciprocity", fontsize=9)
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)

fig.suptitle("Fig. 4. Structural Comparison: Organic vs. Bot-Suspected Accounts",
             fontsize=11, weight="bold")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig4_structural_comparison.png"),
            dpi=300, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 5: Full network colored by Louvain community
# ---------------------------------------------------------------------------
print("Generating Figure 5: community structure...")
fig, ax = plt.subplots(figsize=(10, 8))

colors_comm = [COMM_COLORS.get(c, "#95a5a6") for c in comm_vals]

nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=nodes,
                       node_size=sizes, node_color=colors_comm, alpha=0.8)
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#dddddd",
                       alpha=0.15, width=0.3, arrows=False)

patches = [mpatches.Patch(color=COMM_COLORS[name], label=name)
           for name in COMM_COLORS]
ax.legend(handles=patches, loc="upper right", fontsize=8,
          framealpha=0.9, title="Community", title_fontsize=8)
ax.set_title("Fig. 5. Louvain Community Structure — Node Size ∝ PageRank",
             fontsize=11, weight="bold")
ax.axis("off")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig5_communities.png"),
            dpi=300, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 6: Largest community (Marcos Supporters) subgraph
# ---------------------------------------------------------------------------
print("Generating Figure 6: Marcos Supporters community subgraph...")

marcos_nodes = [n for n in nodes
                if metrics[n]["louvain_community_name"] == "Marcos Supporters"]
G_sub = G.subgraph(marcos_nodes).copy()

pr_sub = {n: float(metrics[n]["pagerank"]) for n in marcos_nodes}
pr_sub_arr = np.array(list(pr_sub.values()))
sizes_sub = ((pr_sub_arr - pr_sub_arr.min()) /
             (pr_sub_arr.max() - pr_sub_arr.min() + 1e-12)) * 100 + 8

colors_sub = [BOT_COLOR if metrics[n]["node_type"] == "bot_suspected"
              else ORGANIC_COLOR for n in marcos_nodes]

pos_sub = nx.spring_layout(G_sub, seed=2022, k=1.2 / np.sqrt(len(G_sub)),
                           iterations=60)

fig, ax = plt.subplots(figsize=(10, 8))
nx.draw_networkx_nodes(G_sub, pos_sub, ax=ax, nodelist=marcos_nodes,
                       node_size=list(sizes_sub),
                       node_color=colors_sub, alpha=0.8)
nx.draw_networkx_edges(G_sub, pos_sub, ax=ax, edge_color="#aaaaaa",
                       alpha=0.3, width=0.5, arrows=True, arrowsize=6)

# Label top-5 nodes by PageRank in this community
top5 = sorted(marcos_nodes, key=lambda n: pr_sub[n], reverse=True)[:5]
labels = {n: f"N{n}" for n in top5}
nx.draw_networkx_labels(G_sub, pos_sub, labels=labels, ax=ax,
                        font_size=7, font_weight="bold")

patch_org = mpatches.Patch(color=ORGANIC_COLOR, label="Organic")
patch_bot = mpatches.Patch(color=BOT_COLOR, label="Bot-Suspected")
ax.legend(handles=[patch_org, patch_bot], loc="upper right", fontsize=9)
ax.set_title(f"Fig. 6. Community 1: Marcos Supporters Subgraph (n={len(marcos_nodes)})",
             fontsize=11, weight="bold")
ax.axis("off")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig6_marcos_community.png"),
            dpi=300, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# Figure 7: PageRank vs. betweenness — broker identification
# ---------------------------------------------------------------------------
print("Generating Figure 7: PageRank vs. betweenness...")
fig, ax = plt.subplots(figsize=(8, 6))

pr_arr_all  = np.array(pr_vals)
bt_arr_all  = np.array(bt_vals)

ax.scatter(pr_arr_all[np.array([t == "organic" for t in type_vals])],
           bt_arr_all[np.array([t == "organic" for t in type_vals])],
           c=ORGANIC_COLOR, alpha=0.3, s=12, label="Organic", zorder=2)
ax.scatter(pr_arr_all[np.array([t == "bot_suspected" for t in type_vals])],
           bt_arr_all[np.array([t == "bot_suspected" for t in type_vals])],
           c=BOT_COLOR, alpha=0.5, s=14, label="Bot-Suspected",
           marker="^", zorder=3)

# Annotate quadrant labels
ax.axvline(x=np.percentile(pr_arr_all, 90), color="gray",
           linestyle="--", linewidth=0.8, alpha=0.6)
ax.axhline(y=np.percentile(bt_arr_all, 90), color="gray",
           linestyle="--", linewidth=0.8, alpha=0.6)
ax.text(np.percentile(pr_arr_all, 92), np.percentile(bt_arr_all, 92),
        "Brokers\n(high PR + high BT)", fontsize=7, color="#555555")
ax.text(np.percentile(pr_arr_all, 92), np.percentile(bt_arr_all, 10),
        "Content Hubs\n(high PR, low BT)", fontsize=7, color="#555555")

ax.set_xlabel("PageRank Centrality", fontsize=10)
ax.set_ylabel("Betweenness Centrality (Normalized)", fontsize=10)
ax.set_title("Fig. 7. PageRank vs. Betweenness — Identifying Broker Accounts",
             fontsize=11, weight="bold")
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig7_pagerank_betweenness.png"),
            dpi=300, bbox_inches="tight")
plt.close()

print(f"\nAll figures saved to {FIG_DIR}")
print("Done.")
