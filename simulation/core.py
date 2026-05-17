"""
core.py — clean, side-effect-free build/metrics functions for the simulation UI.
"""

from __future__ import annotations

import random
from typing import Any

import networkx as nx
import networkx.algorithms.community as nx_comm
import numpy as np

COMMUNITY_DEFS = [
    ("Marcos Supporters", 0.38),
    ("Robredo Supporters", 0.25),
    ("News & Media Accounts", 0.15),
    ("Neutral / Undecided", 0.12),
    ("Amplification Bots", 0.10),
]

COMM_COLORS = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#ff9da7"]
BOT_COLOR = "#e15759"
ORGANIC_COLOR = "#4e79a7"

COMM_LABEL_MAP = {
    0: "Marcos Supporters",
    1: "Robredo Supporters",
    2: "News & Media Accounts",
    3: "Amplification Bots",
    4: "Neutral / Undecided",
}


def build_graph(
    n_total: int = 2500,
    bot_fraction: float = 0.20,
    seed: int = 2022,
) -> nx.DiGraph:
    """Build a synthetic Philippine political retweet DiGraph."""
    rng = np.random.default_rng(seed)
    random.seed(seed)

    n_communities = len(COMMUNITY_DEFS)
    community_sizes: list[int] = []
    cumulative = 0
    for i, (_, frac) in enumerate(COMMUNITY_DEFS):
        if i < n_communities - 1:
            sz = int(n_total * frac)
        else:
            sz = n_total - cumulative
        community_sizes.append(sz)
        cumulative += sz

    G: nx.DiGraph = nx.DiGraph()

    node_id = 0
    community_nodes: dict[int, list[int]] = {i: [] for i in range(n_communities)}
    for comm_idx, size in enumerate(community_sizes):
        for _ in range(size):
            G.add_node(node_id, community=comm_idx,
                       community_name=COMMUNITY_DEFS[comm_idx][0])
            community_nodes[comm_idx].append(node_id)
            node_id += 1

    # Bot assignment: community 4 is all-bot; remainder distributed
    bot_nodes: set[int] = set(community_nodes[4])
    n_bot = int(n_total * bot_fraction)
    remaining = n_bot - len(bot_nodes)
    if remaining > 0:
        organic_pool = [n for n in G.nodes() if n not in bot_nodes]
        extra = rng.choice(organic_pool, size=min(remaining, len(organic_pool)),
                           replace=False)
        bot_nodes.update(extra.tolist())

    for n in G.nodes():
        G.nodes[n]["node_type"] = "bot_suspected" if n in bot_nodes else "organic"

    edge_count_target = max(int(n_total * 6.3), 500)

    def add_intra(nodes: list[int], budget: int) -> None:
        added = 0
        arr = np.array(nodes)
        for _ in range(budget * 3):
            if added >= budget:
                break
            src = int(rng.choice(arr))
            in_d = np.array([G.in_degree(nd) + 1 for nd in arr], dtype=float)
            in_d /= in_d.sum()
            tgt = int(rng.choice(arr, p=in_d))
            if src != tgt and not G.has_edge(src, tgt):
                G.add_edge(src, tgt, weight=int(rng.integers(1, 9)))
                added += 1

    def add_inter(src_nodes: list[int], tgt_nodes: list[int], count: int) -> None:
        added = 0
        for _ in range(count * 10):
            if added >= count:
                break
            s = int(rng.choice(src_nodes))
            t = int(rng.choice(tgt_nodes))
            if s != t and not G.has_edge(s, t):
                G.add_edge(s, t, weight=int(rng.integers(1, 4)))
                added += 1

    intra_fracs = [0.35, 0.25, 0.12, 0.08, 0.05]
    total_intra = int(edge_count_target * 0.70)
    for ci, nodes in community_nodes.items():
        add_intra(nodes, int(total_intra * intra_fracs[ci]))

    total_inter = edge_count_target - G.number_of_edges()
    add_inter(community_nodes[4], community_nodes[0], int(total_inter * 0.30))
    add_inter(community_nodes[4], community_nodes[1], int(total_inter * 0.15))
    add_inter(community_nodes[2], community_nodes[0], int(total_inter * 0.15))
    add_inter(community_nodes[2], community_nodes[1], int(total_inter * 0.12))
    add_inter(community_nodes[0], community_nodes[1], int(total_inter * 0.08))
    add_inter(community_nodes[3], community_nodes[0], int(total_inter * 0.10))
    add_inter(community_nodes[3], community_nodes[1], int(total_inter * 0.10))

    # Bot amplification
    bot_list = [n for n in G.nodes() if G.nodes[n]["node_type"] == "bot_suspected"]
    organic_pool2 = [n for n in G.nodes() if G.nodes[n]["node_type"] == "organic"]
    organic_hubs = sorted(organic_pool2, key=lambda n: G.in_degree(n), reverse=True)[:50]
    for bot in rng.choice(bot_list, size=int(len(bot_list) * 0.6), replace=False):
        for hub in rng.choice(organic_hubs, size=int(rng.integers(2, 6)), replace=False):
            if not G.has_edge(bot, hub):
                G.add_edge(bot, hub, weight=int(rng.integers(1, 4)))

    lcc_nodes = max(nx.weakly_connected_components(G), key=len)
    G_lcc = G.subgraph(lcc_nodes).copy()
    mapping = {old: new for new, old in enumerate(sorted(G_lcc.nodes()))}
    return nx.relabel_nodes(G_lcc, mapping)


def compute_metrics(G: nx.DiGraph) -> dict[str, Any]:
    """Compute all 6 SNA metrics and Louvain community detection."""
    G_und = nx.Graph(G.to_undirected())
    G_und.remove_edges_from(nx.selfloop_edges(G_und))

    in_deg = dict(G.in_degree())
    out_deg = dict(G.out_degree())
    in_deg_cent = nx.in_degree_centrality(G)
    out_deg_cent = nx.out_degree_centrality(G)
    pagerank = nx.pagerank(G, alpha=0.85, weight="weight")

    n = G.number_of_nodes()
    k = min(500, n)
    betweenness = nx.betweenness_centrality(G, k=k, weight="weight",
                                             normalized=True, seed=2022)
    clustering = nx.clustering(G_und, weight="weight")

    reciprocity: dict[Any, float] = {}
    for node in G.nodes():
        out_nb = set(G.successors(node))
        in_nb = set(G.predecessors(node))
        mutual = len(out_nb & in_nb)
        total = len(out_nb | in_nb)
        reciprocity[node] = mutual / total if total > 0 else 0.0

    louvain_partition = nx_comm.louvain_communities(G_und, seed=2022)
    louvain_mod = nx_comm.modularity(G_und, louvain_partition)
    sorted_louvain = sorted(louvain_partition, key=len, reverse=True)
    louvain_community: dict[Any, int] = {}
    for ci, members in enumerate(sorted_louvain):
        for nd in members:
            louvain_community[nd] = ci

    def comm_label(idx: int) -> str:
        return COMM_LABEL_MAP.get(idx, f"Community {idx + 1}")

    nodes = list(G.nodes())
    rows = []
    for nd in nodes:
        lc = louvain_community.get(nd, -1)
        rows.append({
            "node_id": nd,
            "node_type": G.nodes[nd].get("node_type", "organic"),
            "community_name": G.nodes[nd].get("community_name", "Unknown"),
            "louvain_community": lc,
            "louvain_community_name": comm_label(lc),
            "in_degree": in_deg[nd],
            "out_degree": out_deg[nd],
            "in_degree_centrality": round(in_deg_cent[nd], 6),
            "out_degree_centrality": round(out_deg_cent[nd], 6),
            "pagerank": round(pagerank[nd], 6),
            "betweenness_centrality": round(betweenness[nd], 6),
            "clustering_coefficient": round(clustering.get(nd, 0.0), 6),
            "reciprocity": round(reciprocity[nd], 6),
        })

    density = nx.density(G)
    global_reciprocity = nx.reciprocity(G)
    avg_clustering = float(np.mean([clustering.get(nd, 0.0) for nd in nodes]))

    return {
        "rows": rows,
        "summary": {
            "nodes": n,
            "edges": G.number_of_edges(),
            "density": round(density, 6),
            "global_reciprocity": round(global_reciprocity, 4),
            "avg_clustering": round(avg_clustering, 4),
            "louvain_communities": len(louvain_partition),
            "louvain_modularity": round(louvain_mod, 4),
            "bot_count": sum(1 for nd in nodes
                             if G.nodes[nd].get("node_type") == "bot_suspected"),
            "organic_count": sum(1 for nd in nodes
                                 if G.nodes[nd].get("node_type") == "organic"),
        },
    }
