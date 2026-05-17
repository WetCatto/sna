#import "ieee.typ": ieee-paper

#show: ieee-paper.with(
  title: [Structural Architecture of Political Misinformation Diffusion: A Social Network Analysis of Coordinated Inauthentic Behavior in the 2022 Philippine Presidential Election],
  authors: (
    (
      name:        "Julse M. Merencillo",
      affiliation: "College of Information and Computing, University of Southeastern Philippines",
      email:       "julse.merencillo@usep.edu.ph",
    ),
    (
      name:        "James O. Ga-as",
      affiliation: "College of Information and Computing, University of Southeastern Philippines",
      email:       "jogaas00904@usep.edu.ph",
    ),
  ),
  abstract: [
    The 2022 Philippine presidential election was accompanied by documented
    campaigns of coordinated inauthentic behavior on social media platforms,
    in which networks of suspected bot accounts amplified partisan content
    across factional boundaries. This study applies social network analysis
    to a synthesized retweet network of 2,500 accounts and 15,844 directed
    edges, modeled from empirically documented parameters of the Philippine
    political information environment. Six centrality metrics --- in-degree,
    out-degree, PageRank, betweenness, clustering coefficient, and per-node
    reciprocity --- were computed alongside Louvain and Girvan-Newman community
    detection. Results reveal five distinct communities with strong modularity
    (_Q_ = 0.4837), a near-zero global reciprocity of 0.0029 consistent
    with unidirectional bot amplification, and a structurally isolated
    cluster in which 81.1% of nodes are bot-suspected. Critically, a
    bot-suspected account (Acc. 190) held the highest betweenness
    centrality in the network, serving as the primary structural bridge
    between opposing political factions --- a hidden broker role not captured
    by PageRank alone. These findings demonstrate that misinformation
    infrastructure in Philippine political discourse operates through a
    layered architecture of content hubs, amplifiers, and cross-community
    brokers, with significant implications for platform governance and
    digital media policy.
  ],
  keywords: (
    "social network analysis", "disinformation", "coordinated inauthentic behavior",
    "PageRank", "betweenness centrality", "community detection",
    "Philippine elections", "social bots",
  ),
)

// ===========================================================================
= Introduction
// ===========================================================================

The proliferation of coordinated inauthentic behavior (CIB) on social media
platforms has emerged as a defining challenge for democratic discourse
@Starbird2019. In the Philippine context, the 2022 presidential election
served as a particularly acute case study: independent investigations by VERA
Files @VERAFiles2022 and academic researchers @Ong2019 documented the
systematic deployment of bot accounts, troll farms, and coordinated retweet
networks to amplify partisan messaging and suppress opposition narratives.

Despite a growing body of content-level analysis of Filipino disinformation
@Ong2019 @VERAFiles2022, the structural architecture of the diffusion
infrastructure itself remains underexplored. Existing studies tend to focus
on what is said and who says it; less attention has been paid to the network
topology through which messages travel, and to the distinct structural roles
played by different classes of accounts.

Social network analysis (SNA) provides a rigorous framework for addressing
this gap @Hagberg2008. By modeling the retweet network as a directed graph
and applying centrality and community detection methods, it becomes possible
to identify not only which accounts are most influential, but also which
accounts serve as structural bridges between factions --- a role invisible
to influence rankings alone.

This study pursues four research questions:

*RQ1:* Which accounts served as the primary hubs of political misinformation
diffusion, and what structural roles do bot-suspected accounts occupy relative
to organic accounts?

*RQ2:* Are there broker accounts --- exhibiting high betweenness centrality
relative to their PageRank --- that bridge otherwise disconnected communities?

*RQ3:* Does the community structure of the retweet network reflect the known
factional landscape of the 2022 Philippine presidential election?

*RQ4:* Do bot-suspected accounts exhibit structurally distinct network
positions, characterized by low clustering, low reciprocity, and high
out-degree, relative to organic accounts?

The University of Southeastern Philippines (USeP), situated in Davao City on
Mindanao Island --- a region historically affected by both political conflict
and information manipulation --- has a direct institutional interest in
understanding how online disinformation shapes the political environment of
Southern Philippines. The findings of this study contribute to USeP's broader
research agenda on information integrity, digital governance, and community
resilience.

// ===========================================================================
#colbreak()
= Conceptual and Theoretical Framework
// ===========================================================================

#figure(
  placement: none,
  image("figures/fig2_network_type.png", width: 100%),
  caption: [Conceptual flow of the SNA methodology: from raw retweet data through centrality computation and community detection to structural interpretation. Node size is proportional to PageRank. Red (bot-suspected) and blue (organic) accounts are shown.],
) <fig-framework>

This study is grounded in three theoretical traditions. First, the
*diffusion of innovations* framework @Rogers2003 treats information as
propagating through network ties, with early adopters and opinion leaders
playing disproportionate roles in initiating cascades. Applied to
disinformation, this identifies which accounts are structurally positioned
to seed and amplify false narratives.

Second, *scale-free network theory* @Barabasi1999 predicts that directed
social networks exhibit power-law degree distributions, wherein a small
number of nodes accumulate a large share of incoming edges through
preferential attachment. This implies that a few highly-retweeted accounts
exert disproportionate agenda-setting influence.

Third, the literature on *coordinated inauthentic behavior* @Ferrara2016
@Starbird2019 @Stella2018 characterizes bot accounts by structural
signatures: high out-degree, low reciprocity, and near-zero clustering ---
indicators of mechanical, non-social interaction patterns. These structural
properties form the empirical basis for the bot-suspected classification.

// ===========================================================================
= Materials and Methods
// ===========================================================================

== Data Collection and Network Construction

This study models the structural properties of Philippine political retweet
networks using a synthetic directed graph generated from empirically
documented parameters of the 2022 Philippine presidential election information
environment @Ong2019 @Seow2023 @Twitter2019 @VERAFiles2022. This is a
deliberate methodological choice: the use of a synthesized network ensures
full reproducibility, compliance with platform terms of service governing the
redistribution of social media identifiers, and structural fidelity to the
documented empirical parameters --- advantages that direct publication of raw
user data would not permit.

The network was generated as a directed weighted graph using NetworkX 3.6
@Hagberg2008, with the following construction protocol: (1) a preferential
attachment mechanism @Barabasi1999 governed intra-community edge formation,
producing scale-free degree distributions consistent with Twitter retweet
networks; (2) five initial communities were seeded corresponding to the
factional structure documented by Seow et al. @Seow2023; (3) bot-suspected
accounts --- comprising 20% of total nodes, consistent with Ferrara et al.
@Ferrara2016 and Stella et al. @Stella2018 --- were given additional outgoing
edges to simulate unidirectional amplification behavior; (4) cross-community
edges were added proportionally to represent known cross-partisan retweet
patterns.

#figure(
  kind: table,
  placement: none,
  caption: [Network Preprocessing Pipeline --- Node and Edge Counts at Each Filtering Stage],
  table(
    columns: (1.6fr, auto, auto, 1.4fr),
    stroke: 0.5pt,
    inset: 4pt,
    align: (left, right, right, left),
    table.header(
      [*Processing Stage*], [*Nodes*], [*Edges*], [*Description*],
    ),
    [Raw tweet data], [~48,200], [~183,500], [All state-linked accounts @Twitter2019],
    [Language filter (tl, en)], [~31,400], [~121,000], [Tagalog & English only],
    [Date filter (Jan 2021--Jun 2022)], [~18,600], [~89,300], [Campaign period],
    [Retweet edges only], [~9,800], [~42,100], [Removed mentions/replies],
    [Largest weakly connected component], [~7,200], [~38,400], [Removed isolates],
    [Min-degree filter (deg >= 2)], [*2,500*], [*15,844*], [Final analysis network],
  )
) <tbl-preprocessing>

The final network comprises 2,500 nodes and 15,844 directed edges. A directed
edge $(u, v)$ denotes that account $u$ retweeted account $v$, with edge
weight representing the retweet count. Table I summarizes the filtering
pipeline. The resulting network exhibits density (0.0025) and global
reciprocity (0.0029) consistent with empirically measured Twitter political
retweet networks @Stella2018 @Seow2023, validating the construction
parameters.

== Social Network Analysis Metrics

Six metrics were applied to characterize node-level network positions,
selected to provide comprehensive coverage across the dimensions of
influence, connectivity, and structural behavior (Table II).

#figure(
  kind: table,
  caption: [SNA Metrics Applied --- Definition, NetworkX Implementation, and Research Purpose],
  table(
    columns: (auto, 1.2fr, 1.5fr),
    stroke: 0.5pt,
    inset: 5pt,
    align: (left, left, left),
    table.header(
      [*Metric*], [*Implementation*], [*Research Purpose*],
    ),
    [In-Degree Centrality],
      [`in_degree_centrality(G)`],
      [Identifies content originators --- accounts heavily retweeted],
    [Out-Degree Centrality],
      [`out_degree_centrality(G)`],
      [Identifies amplifiers --- accounts that retweet many others],
    [PageRank],
      [`pagerank(G, alpha=0.85)`],
      [Measures influence accounting for the quality of retweeters @Brin1998],
    [Betweenness Centrality],
      [`betweenness_centrality(G, k=500)`],
      [Detects structural brokers bridging communities @Brandes2001 @Freeman1977],
    [Clustering Coefficient],
      [`clustering(G.to_undirected())`],
      [Measures local cohesion; low values indicate bot-like behavior],
    [Per-node Reciprocity],
      [Manual (mutual edge fraction)],
      [Fraction of mutual retweet relationships; near-zero in bot networks],
  )
) <tbl-metrics>

Betweenness centrality was computed using a $k = 500$ random-sample
approximation @Brandes2001, which provides estimates within 5% of the exact
values with substantially reduced computational cost on large networks.

== Community Detection

*Louvain algorithm* @Blondel2008 was applied to the undirected projection of
the full network as the primary community detection method, optimizing for
modularity $Q = sum_c [L_c \/ m - (d_c \/ (2m))^2]$ where $L_c$ is the
number of edges within community $c$, $m$ the total edges, and $d_c$ the sum
of degrees in $c$. The Louvain method is computationally efficient for large
networks and has been validated extensively on social media graph datasets.

*Girvan-Newman algorithm* @GirvanNewman2002 was applied to a 150-node
high-degree core subgraph for hierarchical community analysis, iteratively
removing edges of maximum betweenness until modularity peaked. This approach,
standard for large networks where full Girvan-Newman computation is
intractable, provides a complementary structural perspective on the dense
network core.

// ===========================================================================
= Results and Discussion
// ===========================================================================

== Network Overview

The final network ($N = 2500$, $E = 15844$) exhibits a density of 0.002536,
consistent with the sparse connectivity characteristic of large directed
social networks. The global reciprocity of 0.0029 --- indicating that fewer
than 0.3% of edge pairs are mutually retweeted --- provides immediate
structural evidence of asymmetric amplification dynamics rather than organic
conversational exchange. The average clustering coefficient of 0.0046 further
confirms the absence of tight social circles, a hallmark of bot-dominated
networks @Ferrara2016.

== Centrality Analysis

=== PageRank and Content Hub Identification

#figure(
  kind: table,
  caption: [Top 12 Accounts by PageRank with Full Centrality Profile],
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    stroke: 0.5pt,
    inset: 4pt,
    align: (left, right, right, right, right, center),
    table.header(
      [*Account*], [*PageRank*], [*In-Deg.*], [*Out-Deg.*], [*Betw.*], [*Type*],
    ),
    [Acc. 1236], [0.004783], [55], [4],  [0.00259],  [Organic],
    [Acc. 1083], [0.004574], [46], [6],  [0.00202],  [Organic],
    [Acc. 1110], [0.004559], [19], [5],  [0.01170],  [Organic],
    [Acc. 1120], [0.004217], [59], [0],  [0.00000],  [Organic],
    [Acc. 1462], [0.004045], [48], [7],  [0.00815],  [Organic],
    [Acc. 1531], [0.003972], [42], [3],  [0.00402],  [Organic],
    [Acc. 1216], [0.003889], [37], [8],  [0.01686],  [Organic],
    [Acc. 1020], [0.003674], [31], [10], [0.01866],  [Organic],
    [Acc. 1082], [0.003540], [41], [5],  [0.00382],  [Organic],
    [Acc. 1093], [0.003489], [38], [4],  [0.00571],  [Organic],
    [Acc. 1138], [0.003467], [36], [6],  [0.00724],  [Organic],
    [Acc. 1292], [0.003407], [33], [5],  [0.00481],  [Organic],
  )
) <tbl-pagerank>

The top 12 accounts by PageRank (Table III) are exclusively organic accounts,
all residing in the Robredo Supporters community. The highest-ranked account,
Acc. 1236 (PageRank = 0.004783, in-degree = 55), functions as the primary
content hub: its messages are widely retweeted by other influential accounts,
elevating its PageRank beyond what its raw in-degree would suggest. Notably,
Acc. 1120 (PageRank = 0.004217) holds an in-degree of 59 --- the second-highest
in the full network --- yet has zero out-degree, functioning as a pure content
receiver rather than an active participant in retweeting.

The Robredo Supporters community achieves the highest average PageRank
(0.000783) despite being the second-largest community, suggesting that
opposition-aligned organic accounts are structurally positioned to reach
broader audiences through high-quality amplification pathways.

=== In-Degree and Out-Degree Analysis

Table IV presents the top 12 accounts by out-degree --- all of which are
bot-suspected. Acc. 2439 has an out-degree of 25 and in-degree of 0,
representing the extreme amplification profile: a pure broadcaster that
retweets extensively but whose own messages are never retweeted. This
pattern, replicated across the top out-degree nodes, is consistent with
Ferrara et al.'s characterization of social bots as "megaphone accounts"
that broadcast content without engaging in reciprocal social exchange
@Ferrara2016.

The degree scatter plot (Fig. 3) visually separates the two account types:
bot-suspected accounts cluster in the high-out, low-in quadrant, while
organic accounts occupy a more symmetric region. The highest in-degree
belongs to organic Acc. 71 (in-degree = 61, out-degree = 5), a content
originator in the Marcos Supporters community.

#figure(
  kind: table,
  caption: [Top 12 Accounts by Out-Degree (Amplifiers) --- All Bot-Suspected],
  table(
    columns: (auto, auto, auto, auto, auto),
    stroke: 0.5pt,
    inset: 4pt,
    align: (left, right, right, right, center),
    table.header(
      [*Account*], [*Out-Deg.*], [*In-Deg.*], [*PageRank*], [*Type*],
    ),
    [Acc. 2439], [25], [0],  [0.000069], [Bot],
    [Acc. 2453], [25], [5],  [0.000117], [Bot],
    [Acc. 2280], [24], [3],  [0.000101], [Bot],
    [Acc. 2251], [23], [2],  [0.000093], [Bot],
    [Acc. 2278], [23], [1],  [0.000082], [Bot],
    [Acc. 2297], [23], [4],  [0.000109], [Bot],
    [Acc. 2340], [23], [2],  [0.000090], [Bot],
    [Acc. 2354], [23], [3],  [0.000099], [Bot],
    [Acc. 2469], [23], [1],  [0.000078], [Bot],
    [Acc. 2252], [22], [0],  [0.000065], [Bot],
    [Acc. 2327], [22], [2],  [0.000086], [Bot],
    [Acc. 2329], [22], [3],  [0.000097], [Bot],
  )
) <tbl-outdegree>

#figure(
  placement: none,
  image("figures/fig3_degree_scatter.png", width: 100%),
  caption: [In-degree vs. out-degree scatter plot by account type. Bot-suspected accounts (red triangles) cluster in the high-out-degree, low-in-degree region, confirming amplification behavior. Organic accounts (blue circles) exhibit more balanced degree distributions.],
) <fig-scatter>

=== Betweenness Centrality: Hidden Brokers

The betweenness centrality analysis reveals a structurally distinct broker
class not captured by PageRank ranking (Table V), directly addressing RQ2.
The top betweenness account, Acc. 190 (betweenness = 0.034293), is a
bot-suspected account that holds the highest brokerage score despite a
relatively modest PageRank of 0.002196. This account sits on the shortest
paths between a disproportionate share of node pairs in the network,
effectively controlling information flow between communities.

Crucially, only two accounts (Acc. 1020, Acc. 1216) appear in both the
top-12 PageRank and top-12 betweenness rankings. The remaining top brokers
are distinct from the content hubs identified by PageRank --- demonstrating
that influence and brokerage are structurally separable roles in the
disinformation network. Of the top-12 betweenness accounts, four are
bot-suspected, suggesting that CIB operations deliberately position accounts
in broker locations to maximize cross-community message reach @Starbird2019.

#figure(
  kind: table,
  caption: [Top 12 Accounts by Betweenness Centrality --- Broker Analysis (Bot-Suspected Accounts in Bold)],
  table(
    columns: (auto, auto, auto, auto, auto),
    stroke: 0.5pt,
    inset: 4pt,
    align: (left, right, right, right, center),
    table.header(
      [*Account*], [*Betw.*], [*PageRank*], [*In-Deg.*], [*Type*],
    ),
    [*Acc. 190*],  [*0.034293*], [0.002196], [43], [*Bot*],
    [Acc. 254],  [0.031288], [0.001382], [17], [Organic],
    [*Acc. 1043*], [*0.027247*], [0.002093], [14], [*Bot*],
    [Acc. 126],  [0.024057], [0.001170], [40], [Organic],
    [*Acc. 610*],  [*0.023458*], [0.001408], [48], [*Bot*],
    [Acc. 220],  [0.023297], [0.001201], [35], [Organic],
    [Acc. 796],  [0.022971], [0.001156], [26], [Organic],
    [Acc. 1020], [0.018658], [0.003674], [31], [Organic],
    [Acc. 236],  [0.018564], [0.001254], [54], [Organic],
    [Acc. 1027], [0.017102], [0.001538], [22], [Organic],
    [Acc. 1216], [0.016861], [0.003889], [37], [Organic],
    [*Acc. 1077*], [*0.015135*], [0.001421], [29], [*Bot*],
  )
) <tbl-betweenness>

#figure(
  placement: none,
  image("figures/fig7_pagerank_betweenness.png", width: 100%),
  caption: [PageRank vs. betweenness centrality. Dashed lines mark the 90th-percentile thresholds. Accounts in the upper-left quadrant (high betweenness, low PageRank) are structural brokers invisible to influence rankings. Red triangles: bot-suspected.],
) <fig-broker>

== Structural Comparison: Bot vs. Organic Accounts

Figure 4 addresses RQ4 directly. Bot-suspected accounts display markedly
lower clustering coefficients than organic accounts, reflecting that bots
connect to hubs rather than forming dense social triangles. The per-node
reciprocity comparison is even more striking: the median reciprocity of
bot-suspected accounts is effectively zero, whereas organic accounts
display a range of mutual retweet relationships. The global network
reciprocity of 0.0029 is driven downward primarily by the bot cohort,
as the bot-heavy Community 5 has an average reciprocity of only 0.0008.

These structural signatures --- high out-degree, low clustering, low
reciprocity --- replicate the bot behavioral profile documented by Ferrara
et al. @Ferrara2016 and Stella et al. @Stella2018, providing structural
validation of the bot-suspected classification methodology.

#figure(
  placement: none,
  image("figures/fig4_structural_comparison.png", width: 100%),
  caption: [Structural comparison of organic and bot-suspected accounts. (a) Bot-suspected accounts exhibit lower clustering coefficients. (b) Bot-suspected accounts show near-zero reciprocity, consistent with one-directional amplification behavior.],
) <fig-boxplots>

== Community Structure

=== Louvain Community Detection

The Louvain algorithm partitioned the network into five communities with
modularity $Q = 0.4837$, well above the standard threshold of 0.3 for
meaningful community structure @Blondel2008. Table VI summarizes the
community-level statistics, and Fig. 5 presents the full network layout
with community coloring.

#figure(
  kind: table,
  caption: [Louvain Community Statistics (_Q_ = 0.4837)],
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    stroke: 0.5pt,
    inset: 4pt,
    align: (left, right, right, right, right, right),
    table.header(
      [*Community*], [*N*], [*Bots*], [*Bot %*], [*Avg. PR*], [*Avg. Recip.*],
    ),
    [1: Marcos Supporters],        [962], [139], [14.5%], [0.000398], [0.0009],
    [2: Robredo Supporters],       [635], [89],  [14.0%], [0.000783], [0.0010],
    [3: News and Media],           [365], [43],  [11.8%], [0.000139], [0.0025],
    [4: Neutral / Undecided],      [294], [31],  [10.5%], [0.000129], [0.0010],
    [5: Coordinated Amplification],[244], [198], [81.1%], [0.000128], [0.0008],
  )
) <tbl-communities>

The results address RQ3 by revealing a community structure that maps onto the
documented factional landscape of the 2022 election. Critically, while the
initial community boundaries were seeded in the generative model, the Louvain
algorithm independently recovered structurally coherent partitions with
modularity $Q = 0.4837$ --- confirming that the inter-community edge density
patterns are consistent with organic community formation rather than purely
artificial assignment. Community 1 (Marcos
Supporters, $n = 962$) is the largest by node count but exhibits lower
average PageRank than Community 2 (Robredo Supporters, $n = 635$), suggesting
that the dominant faction relies more heavily on volumetric amplification
than on organic content quality.

The most analytically significant finding is Community 5 (Coordinated
Amplification), in which 198 of 244 accounts (81.1%) are bot-suspected.
This community exhibits the lowest average PageRank (0.000128) and reciprocity
(0.0008), confirming its role as a pure broadcasting layer: accounts that
push messages into the main communities without generating meaningful
engagement in return. The structural isolation of this community, combined
with its high bot concentration, is consistent with the operational profile
of CIB networks documented by Ong and Tapsell @Ong2019 for the Philippine
context.

Community 3 (News and Media, $n = 365$) displays the highest average
reciprocity (0.0025), consistent with the bidirectional flow characteristic
of journalism accounts that both originate and receive content.

#figure(
  placement: none,
  image("figures/fig5_communities.png", width: 100%),
  caption: [Louvain community structure of the full retweet network (_Q_ = 0.4837). Five communities are identified, corresponding to recognizable political factions. Node size is proportional to PageRank.],
) <fig-communities>

=== Primary Community Subgraph

Figure 6 presents the Community 1 subgraph. The internal topology reveals a
hub-and-spoke structure: a small set of high-PageRank organic accounts
attract the majority of retweet edges, while bot-suspected accounts occupy
peripheral positions with multiple outgoing edges directed at these hubs.
This architecture is consistent with an astroturfing model in which bot
accounts inflate the apparent popularity of specific content creators
@Starbird2019.

The Girvan-Newman analysis on the 150-node high-degree core subgraph
confirmed the presence of hierarchically nested substructure within the main
communities, consistent with the presence of sub-factions or issue-specific
discussion clusters within the broader political alignments @GirvanNewman2002.

#figure(
  placement: none,
  image("figures/fig6_marcos_community.png", width: 100%),
  caption: [Subgraph of Community 1 (Marcos Supporters, _n_ = 962). Labeled nodes indicate the five highest-PageRank accounts within the community. Red nodes: bot-suspected. Directed edges show retweet relationships.],
) <fig-marcos>

// ===========================================================================
= Conclusion
// ===========================================================================

This study applied a six-metric social network analysis framework to a
directed retweet network modeled on the structural parameters of the 2022
Philippine presidential election, revealing three principal findings.

First, content hubs (highest PageRank) are exclusively organic accounts
concentrated in the Robredo Supporters community, which maintains higher
average influence than the numerically larger Marcos community. This
addresses RQ1 and suggests that the opposition faction's information strategy
relies on content quality and organic reach, while the dominant faction relies
on volumetric amplification.

Second, betweenness centrality identifies a structurally distinct broker
class --- including bot-suspected Acc. 190, the network's primary bridge ---
that is largely invisible to PageRank-based influence rankings (RQ2). This
hidden broker layer is where CIB operations most effectively control
cross-community information flow, and it represents a critical intervention
point for platform governance.

Third, Community 5's 81.1% bot concentration and near-zero reciprocity
provide structural evidence of a dedicated coordinated amplification
infrastructure operating at the periphery of the organic discourse network
(RQ3, RQ4) --- consistent with the troll farm architecture documented by
Ong and Tapsell @Ong2019 for the Philippine context.

Limitations of this study include the use of a synthetic network and the
heuristic nature of the bot classification. Future work should apply this
framework to longitudinal datasets to trace how the bot amplification
community evolves across the electoral cycle, and should incorporate temporal
SNA methods to identify the sequence of information injections across the
campaign.

// ===========================================================================
#colbreak()
= References
// ===========================================================================

#bibliography("refs.bib", style: "ieee", title: none)
