"""
02_compute_metrics.py

Computes all six SNA metrics and performs community detection on the
Philippine political retweet network.

Metrics:
  1. In-Degree Centrality
  2. Out-Degree Centrality
  3. PageRank (alpha=0.85, weighted)
  4. Betweenness Centrality (weighted, normalized)
  5. Clustering Coefficient (undirected projection, weighted)
  6. Per-node Reciprocity

Community Detection:
  - Louvain (primary — full network; Blondel et al., 2008)
  - Girvan-Newman (applied to 150-node core subgraph for hierarchical analysis;
    standard practice for large networks — Girvan & Newman, 2002)
"""

import csv
import json
import os

import networkx as nx
import networkx.algorithms.community as nx_comm
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
GEXF_PATH = os.path.join(DATA_DIR, "ph_election_network.gexf")

print("Loading graph...")
G = nx.read_gexf(GEXF_PATH)
for u, v, d in G.edges(data=True):
    d["weight"] = float(d.get("weight", 1.0))

N = G.number_of_nodes()
E = G.number_of_edges()
print(f"  {N} nodes, {E} edges")

G_und = G.to_undirected()
G_und_simple = nx.Graph(G_und)
G_und_simple.remove_edges_from(nx.selfloop_edges(G_und_simple))

# ---------------------------------------------------------------------------
# 1. In-Degree Centrality
# ---------------------------------------------------------------------------
print("Computing in-degree centrality...")
in_deg = dict(G.in_degree())
in_deg_cent = nx.in_degree_centrality(G)

# ---------------------------------------------------------------------------
# 2. Out-Degree Centrality
# ---------------------------------------------------------------------------
print("Computing out-degree centrality...")
out_deg = dict(G.out_degree())
out_deg_cent = nx.out_degree_centrality(G)

# ---------------------------------------------------------------------------
# 3. PageRank
# ---------------------------------------------------------------------------
print("Computing PageRank...")
pagerank = nx.pagerank(G, alpha=0.85, weight="weight")

# ---------------------------------------------------------------------------
# 4. Betweenness Centrality (approximation on full graph)
# ---------------------------------------------------------------------------
print("Computing betweenness centrality...")
# Use k-sample approximation (k=500) for tractability on large networks
betweenness = nx.betweenness_centrality(
    G, k=500, weight="weight", normalized=True, seed=2022
)

# ---------------------------------------------------------------------------
# 5. Clustering Coefficient
# ---------------------------------------------------------------------------
print("Computing clustering coefficient...")
clustering = nx.clustering(G_und_simple, weight="weight")

# ---------------------------------------------------------------------------
# 6. Per-node Reciprocity
# ---------------------------------------------------------------------------
print("Computing per-node reciprocity...")
reciprocity: dict[str, float] = {}
for node in G.nodes():
    out_neighbors = set(G.successors(node))
    in_neighbors = set(G.predecessors(node))
    mutual = len(out_neighbors & in_neighbors)
    total = len(out_neighbors | in_neighbors)
    reciprocity[node] = mutual / total if total > 0 else 0.0

# ---------------------------------------------------------------------------
# Louvain community detection (primary — full network)
# ---------------------------------------------------------------------------
print("Running Louvain community detection (full network)...")
louvain_partition = nx_comm.louvain_communities(G_und_simple, seed=2022)
louvain_mod = nx_comm.modularity(G_und_simple, louvain_partition)
n_louvain = len(louvain_partition)
print(f"  Louvain: {n_louvain} communities, modularity={louvain_mod:.4f}")

louvain_community: dict[str, int] = {}
for comm_idx, members in enumerate(louvain_partition):
    for node in members:
        louvain_community[node] = comm_idx

# Sort Louvain communities by size (largest first) for stable labeling
sorted_louvain = sorted(louvain_partition, key=len, reverse=True)
louvain_community_sorted: dict[str, int] = {}
for comm_idx, members in enumerate(sorted_louvain):
    for node in members:
        louvain_community_sorted[node] = comm_idx

# ---------------------------------------------------------------------------
# Girvan-Newman on 150-node core subgraph
# ---------------------------------------------------------------------------
print("Running Girvan-Newman on 150-node high-degree subgraph...")

# Extract top-150 nodes by degree for hierarchical community analysis
top_nodes = sorted(G_und_simple.nodes(),
                   key=lambda n: G_und_simple.degree(n), reverse=True)[:150]
G_core = G_und_simple.subgraph(top_nodes).copy()

gn_comp = nx_comm.girvan_newman(G_core)
best_gn: list[frozenset] = []
best_gn_mod = -1.0
for i, partition in enumerate(gn_comp):
    mod = nx_comm.modularity(G_core, partition)
    if mod > best_gn_mod:
        best_gn_mod = mod
        best_gn = list(partition)
    if i >= 12:
        break

print(f"  Girvan-Newman (core): {len(best_gn)} communities, "
      f"modularity={best_gn_mod:.4f}")

gn_community_core: dict[str, int] = {}
for comm_idx, members in enumerate(best_gn):
    for node in members:
        gn_community_core[node] = comm_idx

# ---------------------------------------------------------------------------
# Named community labels for Louvain communities (by size order)
# ---------------------------------------------------------------------------
comm_label_map = {
    0: "Marcos Supporters",
    1: "Robredo Supporters",
    2: "News & Media Accounts",
    3: "Amplification Bots",
    4: "Neutral / Undecided",
}

def community_label(idx: int) -> str:
    return comm_label_map.get(idx, f"Community {idx + 1}")

# ---------------------------------------------------------------------------
# Save metrics.csv
# ---------------------------------------------------------------------------
print("Saving metrics.csv...")
nodes = list(G.nodes())
fieldnames = [
    "node_id", "node_type", "community_name",
    "in_degree", "out_degree",
    "in_degree_centrality", "out_degree_centrality",
    "pagerank", "betweenness_centrality",
    "clustering_coefficient", "reciprocity",
    "louvain_community", "louvain_community_name",
]

with open(os.path.join(DATA_DIR, "metrics.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for node in nodes:
        lc = louvain_community_sorted.get(node, -1)
        writer.writerow({
            "node_id": node,
            "node_type": G.nodes[node].get("node_type", "organic"),
            "community_name": G.nodes[node].get("community_name", "Unknown"),
            "in_degree": in_deg[node],
            "out_degree": out_deg[node],
            "in_degree_centrality": round(in_deg_cent[node], 6),
            "out_degree_centrality": round(out_deg_cent[node], 6),
            "pagerank": round(pagerank[node], 6),
            "betweenness_centrality": round(betweenness[node], 6),
            "clustering_coefficient": round(clustering.get(node, 0.0), 6),
            "reciprocity": round(reciprocity[node], 6),
            "louvain_community": lc,
            "louvain_community_name": community_label(lc),
        })

# ---------------------------------------------------------------------------
# Community-level statistics
# ---------------------------------------------------------------------------
comm_groups: dict[int, list] = {}
for node in nodes:
    c = louvain_community_sorted.get(node, -1)
    comm_groups.setdefault(c, []).append(node)

with open(os.path.join(DATA_DIR, "community_stats.csv"), "w",
          newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "community_id", "community_name", "node_count",
        "bot_count", "organic_count",
        "avg_pagerank", "avg_betweenness",
        "avg_clustering", "avg_reciprocity",
        "top_node_by_pagerank",
    ])
    writer.writeheader()
    for comm_id in sorted(comm_groups.keys()):
        members = comm_groups[comm_id]
        bot_c = sum(1 for n in members
                    if G.nodes[n].get("node_type") == "bot_suspected")
        avg_pr = float(np.mean([pagerank[n] for n in members]))
        avg_bt = float(np.mean([betweenness[n] for n in members]))
        avg_cl = float(np.mean([clustering.get(n, 0.0) for n in members]))
        avg_rc = float(np.mean([reciprocity[n] for n in members]))
        top_node = max(members, key=lambda n: pagerank[n])
        writer.writerow({
            "community_id": comm_id,
            "community_name": community_label(comm_id),
            "node_count": len(members),
            "bot_count": bot_c,
            "organic_count": len(members) - bot_c,
            "avg_pagerank": round(avg_pr, 6),
            "avg_betweenness": round(avg_bt, 6),
            "avg_clustering": round(avg_cl, 4),
            "avg_reciprocity": round(avg_rc, 4),
            "top_node_by_pagerank": top_node,
        })

# ---------------------------------------------------------------------------
# Network summary JSON
# ---------------------------------------------------------------------------
density = nx.density(G)
global_reciprocity = nx.reciprocity(G)
avg_clustering_val = float(np.mean(list(clustering.values())))

summary = {
    "nodes": N,
    "edges": E,
    "density": round(density, 6),
    "global_reciprocity": round(global_reciprocity, 4),
    "avg_clustering_coefficient": round(avg_clustering_val, 4),
    "louvain_communities": n_louvain,
    "louvain_modularity": round(louvain_mod, 4),
    "gn_core_communities": len(best_gn),
    "gn_core_modularity": round(best_gn_mod, 4),
    "bot_node_count": sum(1 for n in G.nodes()
                          if G.nodes[n].get("node_type") == "bot_suspected"),
    "organic_node_count": sum(1 for n in G.nodes()
                               if G.nodes[n].get("node_type") == "organic"),
    "top12_pagerank": sorted(
        [(n, round(v, 6)) for n, v in pagerank.items()],
        key=lambda x: -x[1]
    )[:12],
    "top12_betweenness": sorted(
        [(n, round(v, 6)) for n, v in betweenness.items()],
        key=lambda x: -x[1]
    )[:12],
    "top12_in_degree": sorted(
        [(n, v) for n, v in in_deg.items()],
        key=lambda x: -x[1]
    )[:12],
    "top12_out_degree": sorted(
        [(n, v) for n, v in out_deg.items()],
        key=lambda x: -x[1]
    )[:12],
}

with open(os.path.join(DATA_DIR, "network_summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== Network Summary ===")
print(f"  Nodes: {N}, Edges: {E}")
print(f"  Density: {density:.6f}")
print(f"  Global reciprocity: {global_reciprocity:.4f}")
print(f"  Avg clustering: {avg_clustering_val:.4f}")
print(f"  Louvain communities: {n_louvain}, modularity={louvain_mod:.4f}")
print(f"  GN core communities: {len(best_gn)}, modularity={best_gn_mod:.4f}")
print("\nTop 5 by PageRank:")
for n, v in summary["top12_pagerank"][:5]:
    nt = G.nodes[n].get("node_type", "?")
    print(f"  Node {n}: {v:.6f} ({nt})")
print("\nDone.")
