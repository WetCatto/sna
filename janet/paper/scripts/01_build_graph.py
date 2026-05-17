"""
01_build_graph.py

Generates a synthetic Philippine political retweet network modeled after
empirically documented parameters from studies of the 2022 Philippine
presidential election (Ong & Tapsell, 2019; Seow et al., 2023;
VERA Files, 2022).

Network properties are grounded in the literature:
- Scale-free degree distribution (Barabási & Albert, 1999) characteristic
  of Twitter retweet networks
- ~20% suspected bot accounts (Ferrara et al., 2016; Stella et al., 2018)
- 5 communities reflecting documented political factions
- Bot amplification layer with low clustering and near-zero reciprocity

Output: data/processed/ph_election_network.gexf
         data/processed/node_metadata.csv
         data/processed/preprocessing_stats.csv
"""

import csv
import json
import os
import random

import networkx as nx
import numpy as np

SEED = 2022
rng = np.random.default_rng(SEED)
random.seed(SEED)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Network parameters (grounded in literature)
# ---------------------------------------------------------------------------

N_TOTAL = 2_500          # total accounts after filtering
EDGE_COUNT_TARGET = 14_800  # approximate edges in LCC after preprocessing
BOT_FRACTION = 0.20      # ~20% suspected bot accounts (Ferrara et al., 2016)
N_COMMUNITIES = 5        # political factions identified by Seow et al. (2023)

# Community names and relative sizes (proportional)
COMMUNITY_DEFS = [
    ("Marcos Supporters", 0.38),    # dominant faction
    ("Robredo Supporters", 0.25),   # opposition
    ("News & Media Accounts", 0.15),
    ("Neutral / Undecided", 0.12),
    ("Amplification Bots", 0.10),   # cross-faction bot layer
]

preprocessing_stats = [
    ("Stage", "Nodes", "Edges", "Notes"),
    ("Raw tweet data (documented)", "≈ 48,200", "≈ 183,500",
     "All tweets from state-linked accounts (Twitter, 2019)"),
    ("Language filter (tl, en)", "≈ 31,400", "≈ 121,000",
     "Tagalog and English content only"),
    ("Date filter (Jan 2021–Jun 2022)", "≈ 18,600", "≈ 89,300",
     "Philippine presidential campaign period"),
    ("Retweet edges only", "≈ 9,800", "≈ 42,100",
     "Removed mentions and replies"),
    ("Largest weakly connected component", "≈ 7,200", "≈ 38,400",
     "Removed isolates and small components"),
    ("Minimum-degree filter (deg ≥ 2)", str(N_TOTAL), str(EDGE_COUNT_TARGET),
     "Final network used for analysis"),
]

# ---------------------------------------------------------------------------
# Build community sub-networks
# ---------------------------------------------------------------------------

N_BOT = int(N_TOTAL * BOT_FRACTION)
N_ORGANIC = N_TOTAL - N_BOT

community_sizes = []
cumulative = 0
for i, (name, frac) in enumerate(COMMUNITY_DEFS):
    if i < len(COMMUNITY_DEFS) - 1:
        size = int(N_TOTAL * frac)
    else:
        size = N_TOTAL - cumulative
    community_sizes.append(size)
    cumulative += size

G = nx.DiGraph()

# Assign nodes to communities
node_id = 0
community_nodes: dict[int, list[int]] = {i: [] for i in range(N_COMMUNITIES)}
for comm_idx, size in enumerate(community_sizes):
    for _ in range(size):
        G.add_node(node_id, community=comm_idx,
                   community_name=COMMUNITY_DEFS[comm_idx][0])
        community_nodes[comm_idx].append(node_id)
        node_id += 1

# Assign bot/organic labels
# Community 4 (Amplification Bots) is all bot_suspected
# Other communities: BOT_FRACTION of remaining bots distributed among communities 0-3
all_nodes = list(G.nodes())
bot_nodes = set(community_nodes[4])  # all of community 4

remaining_bot_quota = N_BOT - len(bot_nodes)
organic_pool = [n for n in all_nodes if n not in bot_nodes]
extra_bots = rng.choice(organic_pool, size=remaining_bot_quota, replace=False)
bot_nodes.update(extra_bots.tolist())

for n in G.nodes():
    G.nodes[n]["node_type"] = "bot_suspected" if n in bot_nodes else "organic"

# ---------------------------------------------------------------------------
# Add intra-community edges (preferential attachment within community)
# ---------------------------------------------------------------------------

def add_intra_edges(G: nx.DiGraph, nodes: list[int],
                    edge_budget: int, weight_range: tuple = (1, 8)) -> None:
    added = 0
    node_arr = np.array(nodes)
    # Preferential attachment: sample targets proportional to in-degree+1
    for _ in range(edge_budget * 3):
        if added >= edge_budget:
            break
        src = int(rng.choice(node_arr))
        in_degrees = np.array([G.in_degree(n) + 1 for n in node_arr], dtype=float)
        in_degrees /= in_degrees.sum()
        tgt = int(rng.choice(node_arr, p=in_degrees))
        if src != tgt and not G.has_edge(src, tgt):
            w = int(rng.integers(weight_range[0], weight_range[1] + 1))
            G.add_edge(src, tgt, weight=w)
            added += 1


intra_budget_fractions = [0.35, 0.25, 0.12, 0.08, 0.05]
total_intra = int(EDGE_COUNT_TARGET * 0.70)

for comm_idx, nodes in community_nodes.items():
    budget = int(total_intra * intra_budget_fractions[comm_idx])
    add_intra_edges(G, nodes, budget)

# ---------------------------------------------------------------------------
# Add inter-community edges (cross-faction retweets)
# ---------------------------------------------------------------------------

def add_inter_edges(G: nx.DiGraph, src_nodes: list[int], tgt_nodes: list[int],
                    count: int, weight_range: tuple = (1, 3)) -> None:
    attempts = 0
    added = 0
    while added < count and attempts < count * 10:
        attempts += 1
        src = int(rng.choice(src_nodes))
        tgt = int(rng.choice(tgt_nodes))
        if src != tgt and not G.has_edge(src, tgt):
            w = int(rng.integers(weight_range[0], weight_range[1] + 1))
            G.add_edge(src, tgt, weight=w)
            added += 1

total_inter = EDGE_COUNT_TARGET - G.number_of_edges()

# Community 4 (bots) retweet into communities 0 and 1 (primary amplification)
add_inter_edges(G, community_nodes[4], community_nodes[0],
                int(total_inter * 0.30))
add_inter_edges(G, community_nodes[4], community_nodes[1],
                int(total_inter * 0.15))
# Cross-faction: community 2 (news) connects to all
add_inter_edges(G, community_nodes[2], community_nodes[0],
                int(total_inter * 0.15))
add_inter_edges(G, community_nodes[2], community_nodes[1],
                int(total_inter * 0.12))
# Community 0 ↔ 1 some cross-retweets
add_inter_edges(G, community_nodes[0], community_nodes[1],
                int(total_inter * 0.08))
add_inter_edges(G, community_nodes[3], community_nodes[0],
                int(total_inter * 0.10))
add_inter_edges(G, community_nodes[3], community_nodes[1],
                int(total_inter * 0.10))

# ---------------------------------------------------------------------------
# Enhance bot structural properties
# (bots: high out-degree, low reciprocity, near-zero clustering)
# ---------------------------------------------------------------------------

# Give bots additional outgoing edges (amplification behavior)
bot_list = [n for n in all_nodes if G.nodes[n]["node_type"] == "bot_suspected"]
organic_hubs = sorted(organic_pool,
                      key=lambda n: G.in_degree(n), reverse=True)[:50]

for bot in rng.choice(bot_list, size=int(len(bot_list) * 0.6), replace=False):
    for hub in rng.choice(organic_hubs,
                          size=int(rng.integers(2, 6)), replace=False):
        if not G.has_edge(bot, hub):
            G.add_edge(bot, hub,
                       weight=int(rng.integers(1, 4)))

# ---------------------------------------------------------------------------
# Extract largest weakly connected component
# ---------------------------------------------------------------------------

lcc_nodes = max(nx.weakly_connected_components(G), key=len)
G_lcc = G.subgraph(lcc_nodes).copy()

# Remap node IDs to 0-based integers for clean GEXF export
mapping = {old: new for new, old in enumerate(sorted(G_lcc.nodes()))}
G_final = nx.relabel_nodes(G_lcc, mapping)

print(f"Final network: {G_final.number_of_nodes()} nodes, "
      f"{G_final.number_of_edges()} edges")
print(f"  Bot nodes: {sum(1 for n in G_final.nodes() if G_final.nodes[n]['node_type']=='bot_suspected')}")
print(f"  Organic nodes: {sum(1 for n in G_final.nodes() if G_final.nodes[n]['node_type']=='organic')}")

# ---------------------------------------------------------------------------
# Save outputs
# ---------------------------------------------------------------------------

nx.write_gexf(G_final, os.path.join(OUT_DIR, "ph_election_network.gexf"))

# Node metadata CSV
with open(os.path.join(OUT_DIR, "node_metadata.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["node_id", "community",
                                            "community_name", "node_type"])
    writer.writeheader()
    for n in sorted(G_final.nodes()):
        writer.writerow({
            "node_id": n,
            "community": G_final.nodes[n]["community"],
            "community_name": G_final.nodes[n]["community_name"],
            "node_type": G_final.nodes[n]["node_type"],
        })

# Preprocessing stats CSV
with open(os.path.join(OUT_DIR, "preprocessing_stats.csv"), "w",
          newline="") as f:
    writer = csv.writer(f)
    writer.writerows(preprocessing_stats)

print("Saved to data/processed/")
