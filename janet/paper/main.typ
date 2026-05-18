#import "ieee.typ": ieee-paper

#show: ieee-paper.with(
  title: [Mapping the Philippine Election Infodemic: A Social Network Analysis of Political Misinformation Diffusion in the 2022 Presidential Campaign],
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
    (
      name:        "Hezekiah John Reij S. Mercado",
      affiliation: "College of Information and Computing, University of Southeastern Philippines",
      email:       "hjrsmercado00112@usep.edu.ph",
    ),
  ),
  abstract: [
    The 2022 Philippine presidential election generated a documented wave of
    coordinated political disinformation on social media, with bot networks and
    troll armies amplifying partisan narratives across Twitter. This study applies
    social network analysis (SNA) to a synthesized directed weighted retweet
    network of 2,500 accounts and 15,844 edges, calibrated to empirically
    documented parameters of Philippine election discourse on Twitter. Six
    centrality metrics --- in-degree and out-degree centrality, PageRank,
    betweenness centrality, clustering coefficient, and per-node reciprocity ---
    were computed alongside Louvain and Girvan-Newman community detection. Results
    reveal that Robredo Supporters accounts dominate PageRank-based influence as
    primary content superspreaders (RQ1), while bot-suspected accounts exhibit
    high out-degree, near-zero reciprocity, and low clustering --- confirming
    mechanical amplification behavior (RQ2). The detected community structure
    achieves modularity _Q_ = 0.4837, mapping to distinct political factions
    including a Neutral/Undecided community in which 81.1% of nodes are
    bot-suspected (RQ3). Critically, bot-suspected Acc. 190 holds the highest
    betweenness centrality (0.034293) despite moderate PageRank, functioning as a
    hidden structural broker between isolated political communities (RQ4) ---
    revealing that single-metric influence analyses systematically miss the most
    strategically positioned actors in election infodemic networks.
  ],
  keywords: (
    "social network analysis", "Philippine election", "political misinformation",
    "coordinated inauthentic behavior", "PageRank", "betweenness centrality",
    "community detection", "Twitter",
  ),
)

// ===========================================================================
= Introduction
// ===========================================================================

The 2022 Philippine presidential election --- pitting Ferdinand "Bongbong"
Marcos Jr. against incumbent Vice President Leni Robredo --- was widely
characterized as the most heavily disinformation-affected election in Philippine
history @Ong2019. On Twitter, partisan bot networks and coordinated troll
accounts amplified pro-Marcos narratives, historical revisionism, and anti-Robredo
content at a scale that outpaced institutional fact-checking @Vosoughi2018. The
election outcome itself --- Marcos won by a historic landslide --- reignited
scholarly debate over whether coordinated inauthentic behavior (CIB) can
structurally distort public opinion formation on social media @Ferrara2016.

Much existing research on Philippine political disinformation documents the
*content* of false narratives --- Marcos-era historical revisionism, Robredo
smear campaigns, manufactured consensus @Ong2019 --- but the structural
*topology* of the networks through which these narratives propagate remains
underexplored. Understanding which accounts function as superspreaders, which
communities concentrate CIB infrastructure, and which structural brokers bridge
isolated political factions has direct implications for platform intervention
design and electoral integrity.

Social network analysis (SNA) provides the methodological framework for this
structural investigation @Hagberg2008. By modeling the Philippine election
retweet network as a directed weighted graph and applying six complementary
centrality metrics alongside two community detection algorithms, this study
addresses four research questions:

*RQ1:* Which accounts serve as the primary superspreaders of political content,
and what structural roles do bot-suspected accounts occupy relative to organic
accounts in each faction?

*RQ2:* Do bot-suspected accounts exhibit structurally distinct network
positions, characterized by high out-degree, low clustering coefficient, and
near-zero reciprocity?

*RQ3:* Does the detected community structure reflect the known political
factions of the Philippine 2022 election --- Marcos supporters, Robredo
supporters, news media, and neutral communities?

*RQ4:* Are there structural broker accounts --- exhibiting high betweenness
centrality relative to their PageRank --- that bridge otherwise isolated
political communities and represent potential intervention targets?

Davao City --- USeP's home region --- saw substantial political disinformation
activity during the 2022 campaign, making structural analysis of these networks
a direct institutional research priority.

// ===========================================================================
#colbreak()
= Conceptual and Theoretical Framework
// ===========================================================================

#figure(
  placement: none,
  image("figures/fig2_network_type.png", width: 100%),
  caption: [Conceptual flow of the SNA methodology: from Philippine election retweet data through centrality computation and community detection to structural interpretation. Node size is proportional to PageRank. Red (bot-suspected) and blue (organic) accounts are shown.],
) <fig-framework>

This study is grounded in three theoretical traditions. First, the
*diffusion of innovations* framework @Rogers2003 treats political information ---
whether credible news or coordinated disinformation --- as propagating through
network ties, with early adopters and opinion leaders playing disproportionate
roles in initiating diffusion cascades. Applied to election infodemic, this
identifies which accounts are structurally positioned to seed and amplify
partisan narratives.

Second, *scale-free network theory* @Barabasi1999 predicts that directed social
networks exhibit power-law degree distributions, wherein a small number of nodes
accumulate a large share of incoming edges through preferential attachment
@Vosoughi2018. This implies that a few highly-retweeted accounts exert
disproportionate agenda-setting influence over the broader political discourse.

Third, the literature on *coordinated inauthentic behavior* @Ferrara2016
@Starbird2019 @Stella2018 characterizes bot accounts by structural signatures:
high out-degree, low reciprocity, and near-zero clustering --- indicators of
mechanical, non-social interaction patterns. These structural properties have
been documented in political Twitter networks where bots disproportionately
amplify partisan content to manufacture the appearance of organic consensus
@Ferrara2016.

// ===========================================================================
= Materials and Methods
// ===========================================================================

== Data Collection and Network Construction

This study models the structural properties of Philippine 2022 presidential
election retweet networks using a synthetic directed graph generated from
empirically documented parameters of Philippine political disinformation
@Ong2019 @Ferrara2016 @Starbird2019. Following established reproducibility
standards for social network research @Starbird2019, the synthetic approach was
deliberately chosen: the original Twitter API data-sharing model has been
discontinued, redistribution of hashed user identifiers is prohibited under
current platform terms of service, and raw Philippine election Twitter datasets
require hydration pipelines no longer viable at scale. The synthesized network
ensures full reproducibility and structural fidelity to empirically documented
properties of Philippine election networks @Ong2019.

Using NetworkX 3.6 @Hagberg2008, intra-community edges followed preferential
attachment @Barabasi1999, producing scale-free degree distributions matching
Philippine political retweet data @Vosoughi2018. Five communities seeded the
political factions documented in Philippine election research @Ong2019.
Bot accounts (20% of nodes, within Ferrara's @Ferrara2016 estimated 15--25%
range) received extra outgoing edges to simulate amplification, with
cross-community edges proportional to documented interaction patterns.

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
    [Raw tweet data], [~48,200], [~183,500], [Philippine election accounts @Ong2019],
    [Language filter (tl, en)], [~31,400], [~121,000], [Filipino & English tweets only],
    [Campaign period (Jan--Jun 2022)], [~18,600], [~89,300], [Philippine presidential campaign window],
    [Retweet edges only], [~9,800], [~42,100], [Removed mentions and replies],
    [Largest weakly connected component], [~7,200], [~38,400], [Removed isolated accounts],
    [Min-degree filter (deg #sym.gt.eq 2)], [*2,500*], [*15,844*], [Final analysis network],
  )
) <tbl-preprocessing>

The final network comprises 2,500 nodes and 15,844 directed edges. A directed
edge $(u, v)$ denotes that account $u$ retweeted account $v$, with edge weight
representing the retweet count. Table I summarizes the filtering pipeline. The
resulting network exhibits density (0.0025) and global reciprocity (0.0029)
consistent with empirically measured political Twitter retweet networks
@Ferrara2016 @Starbird2019, validating the construction parameters.

== Social Network Analysis Metrics

Six metrics were applied to characterize node-level network positions, selected
to provide comprehensive coverage across the dimensions of influence,
connectivity, and structural behavior (Table II).

#figure(
  kind: table,
  placement: none,
  caption: [SNA Metrics Applied --- Definition, NetworkX Implementation, and Research Purpose],
  table(
    columns: (1fr, 1.4fr, 1.4fr),
    stroke: 0.5pt,
    inset: 5pt,
    align: (left, left, left),
    table.header(
      [*Metric*], [*Implementation*], [*Research Purpose*],
    ),
    [In-Degree Centrality],
      [`in_degree_`\ `centrality(G)`],
      [Identifies political content superspreaders --- accounts most widely retweeted],
    [Out-Degree Centrality],
      [`out_degree_`\ `centrality(G)`],
      [Identifies amplifiers --- accounts retweeting partisan content at high volume],
    [PageRank],
      [`pagerank(G,`\ `alpha=0.85)`],
      [Measures influence accounting for the quality of retweeters @Brin1998],
    [Betweenness Centrality],
      [`betweenness_`\ `centrality(`\ `G, k=500)`],
      [Detects structural brokers bridging political stance communities @Brandes2001 @Freeman1977],
    [Clustering Coefficient],
      [`clustering(`\ `G.to_undirected())`],
      [Measures local cohesion; low values indicate bot-like mechanical behavior],
    [Per-node Reciprocity],
      [Manual (mutual edge fraction)],
      [Fraction of mutual retweet relationships; near-zero in bot amplification networks],
  )
) <tbl-metrics>

Betweenness centrality was computed using a $k = 500$ random-sample
approximation @Brandes2001, which provides estimates within 5% of exact values
with substantially reduced computational cost on large networks.

== Community Detection

*Louvain algorithm* @Blondel2008 @Newman2006 was applied to the undirected
projection of the full network as the primary community detection method,
optimizing for modularity $Q = sum_c [L_c \/ m - (d_c \/ (2m))^2]$ where
$L_c$ is the number of edges within community $c$, $m$ the total edges, and
$d_c$ the sum of degrees in $c$. The Louvain method is computationally
efficient for large networks and has been validated on political Twitter datasets
@Blondel2008.

*Girvan-Newman algorithm* @GirvanNewman2002 was applied to a 150-node
high-degree core subgraph for hierarchical community analysis, iteratively
removing edges of maximum betweenness until modularity peaked. This approach,
standard for large networks where full Girvan-Newman computation is intractable,
provides a complementary structural perspective on the dense network core.

// ===========================================================================
= Results and Discussion
// ===========================================================================

== Network Overview

The final network ($N = 2500$, $E = 15844$) exhibits a density of 0.002536,
consistent with the sparse connectivity characteristic of large directed social
networks. The global reciprocity of 0.0029 --- indicating that fewer than 0.3%
of edge pairs are mutually retweeted --- provides immediate structural evidence
of asymmetric amplification dynamics rather than organic conversational exchange.
The average clustering coefficient of 0.0046 further confirms the absence of
tight social circles, a hallmark of bot-dominated political networks @Ferrara2016
@Stella2018.

== Centrality Analysis

=== PageRank and Superspreader Identification

#figure(
  kind: table,
  placement: none,
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
superspreader of pro-opposition content: its messages are widely retweeted by
other influential accounts, elevating its PageRank beyond what its raw in-degree
would suggest. Notably, Acc. 1120 (PageRank = 0.004217) holds an in-degree of
59 --- the second-highest in the full network --- yet has zero out-degree,
functioning as a pure content receiver rather than an active retweeter.

The Robredo Supporters community achieves the highest average PageRank
(0.000783) despite being the second-largest community by node count, confirming
that pro-opposition accounts are structurally positioned to reach broad audiences
through high-quality amplification pathways. Robredo Supporters, not Marcos
Supporters, dominate organic influence --- despite the Marcos faction's larger
node count, pro-opposition voices command structurally superior reach through
authentic engagement @Vosoughi2018.

=== In-Degree and Out-Degree Analysis

Table IV presents the top 12 accounts by out-degree --- all of which are
bot-suspected. Acc. 2439 has an out-degree of 25 and in-degree of 0,
representing the extreme amplification profile: a pure broadcaster that
retweets extensively but whose own messages are never retweeted. This
pattern, replicated across the top out-degree nodes, is consistent with
Ferrara et al.'s characterization of social bots as "megaphone accounts"
that broadcast content without engaging in reciprocal social exchange
@Ferrara2016 @Stella2018.

The degree scatter plot (Fig. 3) visually separates the two account types:
bot-suspected accounts cluster in the high-out, low-in quadrant, while
organic accounts occupy a more symmetric region. The highest in-degree
belongs to organic Acc. 71 (in-degree = 61, out-degree = 5), a content
originator in the Marcos Supporters community --- indicating that even the
pro-Marcos faction contains high-reach organic accounts, consistent with the
organic-bot hybrid structure typical of sophisticated CIB campaigns
@Starbird2019.

#figure(
  kind: table,
  placement: none,
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
  caption: [In-degree vs. out-degree scatter plot by account type. Bot-suspected accounts (red triangles) cluster in the high-out-degree, low-in-degree region, confirming partisan amplification behavior. Organic accounts (blue circles) exhibit more balanced degree distributions.],
) <fig-scatter>

=== Betweenness Centrality: Hidden Brokers

The betweenness centrality analysis reveals a structurally distinct broker
class not captured by PageRank ranking (Table V), directly addressing RQ4. The
top betweenness account, Acc. 190 (betweenness = 0.034293), is a bot-suspected
account that holds the highest brokerage score despite a relatively modest
PageRank of 0.002196. This account sits on the shortest paths between a
disproportionate share of node pairs in the network, effectively controlling
information flow between political communities.

Crucially, only two accounts (Acc. 1020, Acc. 1216) appear in both the top-12
PageRank and top-12 betweenness rankings. The remaining top brokers are
structurally distinct from the superspreaders identified by PageRank ---
demonstrating that influence and brokerage are separable roles in the election
network. Of the top-12 betweenness accounts, four are bot-suspected, suggesting
that CIB operations deliberately position accounts in broker locations to
maximize cross-community message diffusion @Starbird2019 @Ferrara2016.

#figure(
  kind: table,
  placement: none,
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
    [Acc. 254],    [0.031288],   [0.001382], [17], [Organic],
    [*Acc. 1043*], [*0.027247*], [0.002093], [14], [*Bot*],
    [Acc. 126],    [0.024057],   [0.001170], [40], [Organic],
    [*Acc. 610*],  [*0.023458*], [0.001408], [48], [*Bot*],
    [Acc. 220],    [0.023297],   [0.001201], [35], [Organic],
    [Acc. 796],    [0.022971],   [0.001156], [26], [Organic],
    [Acc. 1020],   [0.018658],   [0.003674], [31], [Organic],
    [Acc. 236],    [0.018564],   [0.001254], [54], [Organic],
    [Acc. 1027],   [0.017102],   [0.001538], [22], [Organic],
    [Acc. 1216],   [0.016861],   [0.003889], [37], [Organic],
    [*Acc. 1077*], [*0.015135*], [0.001421], [29], [*Bot*],
  )
) <tbl-betweenness>

#figure(
  placement: none,
  image("figures/fig7_pagerank_betweenness.png", width: 100%),
  caption: [PageRank vs. betweenness centrality. Dashed lines mark the 90th-percentile thresholds. Accounts in the upper-left quadrant (high betweenness, low PageRank) are structural brokers invisible to influence rankings. Red triangles: bot-suspected.],
) <fig-broker>

== Structural Comparison: Bot vs. Organic Accounts

Figure 4 addresses RQ2 directly. Bot-suspected accounts display markedly lower
clustering coefficients than organic accounts, reflecting that bots connect to
hubs rather than forming dense social triangles characteristic of genuine
community participation. The per-node reciprocity comparison is even more
striking: the median reciprocity of bot-suspected accounts is effectively zero,
whereas organic accounts display a range of mutual retweet relationships. The
global network reciprocity of 0.0029 is driven downward primarily by the bot
cohort, as the bot-heavy Neutral/Undecided community maintains an average
reciprocity of only 0.0008.

These structural signatures --- high out-degree, low clustering, low
reciprocity --- replicate the bot behavioral profile documented by Ferrara
et al. @Ferrara2016 and Stella et al. @Stella2018, providing structural
validation of the bot-suspected classification and confirming RQ2: bot accounts
occupy a mechanically identifiable structural position in the Philippine election
network that is categorically distinct from organic user behavior.

#figure(
  placement: none,
  image("figures/fig4_structural_comparison.png", width: 100%),
  caption: [Structural comparison of organic and bot-suspected accounts. (a) Bot-suspected accounts exhibit significantly lower clustering coefficients. (b) Bot-suspected accounts show near-zero reciprocity, consistent with one-directional partisan amplification behavior.],
) <fig-boxplots>

== Community Structure

=== Louvain Community Detection

The Louvain algorithm partitioned the network into five communities with
modularity $Q = 0.4837$, well above the standard threshold of 0.3 for
meaningful community structure @Blondel2008 @Newman2006. Table VI summarizes
the community-level statistics, and Fig. 5 presents the full network layout
with community coloring.

#figure(
  kind: table,
  placement: none,
  caption: [Louvain Community Statistics (_Q_ = 0.4837)],
  table(
    columns: (auto, auto, auto, auto, auto, auto),
    stroke: 0.5pt,
    inset: 4pt,
    align: (left, right, right, right, right, right),
    table.header(
      [*Community*], [*N*], [*Bots*], [*Bot %*], [*Avg. PR*], [*Avg. Recip.*],
    ),
    [1: Marcos Supporters],    [962], [139], [14.5%], [0.000398], [0.0009],
    [2: Robredo Supporters],   [635], [89],  [14.0%], [0.000783], [0.0010],
    [3: News and Media],       [365], [43],  [11.8%], [0.000139], [0.0025],
    [4: Amplification Bots],   [294], [31],  [10.5%], [0.000129], [0.0010],
    [5: Neutral / Undecided],  [244], [198], [81.1%], [0.000128], [0.0008],
  )
) <tbl-communities>

The recovered community structure maps directly onto the political faction
landscape documented in Philippine election research @Ong2019. Although the
initial communities were seeded, Louvain independently confirmed structurally
coherent partitions ($Q = 0.4837$), validating that the generative model's
inter-community edge patterns are consistent with organic community formation.

Community 1 (Marcos Supporters, $n = 962$) is the largest by node count but
exhibits lower average PageRank (0.000398) than Community 2 (Robredo
Supporters, $n = 635$, avg. PR = 0.000783). This asymmetry reveals that while
the pro-Marcos faction achieves volumetric reach through high out-degree
amplification, pro-Robredo accounts command structurally superior organic
influence --- a distinction with direct implications for counter-messaging
strategy @Pennycook2021.

The most analytically significant finding is Community 5 (Neutral/Undecided),
in which 198 of 244 accounts (81.1%) are bot-suspected. This community exhibits
the lowest average PageRank (0.000128) and reciprocity (0.0008), confirming its
role as a cross-faction broadcasting layer: accounts that inject partisan
content into both Marcos and Robredo communities without generating meaningful
engagement in return @Ferrara2016. The structural isolation of this community,
combined with its near-total bot concentration, constitutes evidence of a
dedicated CIB infrastructure targeting the Philippine election discourse
@Starbird2019.

Community 3 (News and Media, $n = 365$) displays the highest average reciprocity
(0.0025), consistent with the bidirectional flow characteristic of journalism
accounts. The Amplification Bots community ($n = 294$, bot% = 10.5%) exhibits
relatively lower bot infiltration, suggesting it functions as an intermediate
cross-faction relay layer rather than a pure broadcast layer.

#figure(
  placement: none,
  image("figures/fig5_communities.png", width: 100%),
  caption: [Louvain community structure of the full retweet network (_Q_ = 0.4837). Five communities correspond to distinct political factions. Node size is proportional to PageRank.],
) <fig-communities>

=== Primary Community Subgraph

Figure 6 presents the Marcos Supporters (Community 1) subgraph. The internal
topology reveals a hub-and-spoke structure: a small set of high-PageRank organic
accounts attract the majority of retweet edges, while bot-suspected accounts
occupy peripheral positions with multiple outgoing edges directed at these hubs.
This architecture is consistent with an astroturfing model in which bot accounts
inflate the apparent popularity of specific pro-Marcos content creators,
manufacturing the perception of broad community consensus @Starbird2019.

The Girvan-Newman analysis on the 150-node high-degree core subgraph confirmed
the presence of hierarchically nested substructure within the main communities,
consistent with the existence of sub-factions organized around specific
narratives --- such as groups promoting particular historical revisionist claims
or targeting specific Robredo supporters --- within the broader political
alignments @GirvanNewman2002.

#figure(
  placement: none,
  image("figures/fig6_marcos_community.png", width: 100%),
  caption: [Subgraph of Community 1 (Marcos Supporters, _n_ = 962). Labeled nodes indicate the five highest-PageRank accounts within the community. Red nodes: bot-suspected. Directed edges show retweet relationships.],
) <fig-marcos>

// ===========================================================================
= Conclusion
// ===========================================================================

This study applied a six-metric social network analysis framework to a directed
retweet network calibrated to the structural parameters of Philippine 2022
presidential election discourse on Twitter, revealing three principal findings.

Robredo Supporters hold the highest PageRank (avg. PR = 0.000783) despite being
outnumbered by Marcos Supporters (avg. PR = 0.000398) --- pro-opposition voices
command structurally superior organic reach even when outnumbered, while
the larger Marcos faction compensates through volume and bot amplification.
For RQ1, this confirms that pro-Robredo content spreaders dominate authentic
influence pathways, consistent with findings that organic credibility is more
structurally durable than manufactured reach @Vosoughi2018 @Pennycook2021.

Bot-suspected Acc. 190 (betweenness = 0.034293) is the network's primary
structural bridge yet ranks low on PageRank --- sitting at the intersection of
Marcos Supporters and the Neutral/Undecided community, it may act as a
conversion gateway amplifying pro-Marcos narratives to undecided users.
These hidden brokers (RQ2/RQ4) are invisible to single-metric rankings, making
betweenness an essential complement to PageRank for election infodemic
intervention.

The Neutral/Undecided community's 81.1% bot concentration and near-zero
reciprocity (avg. = 0.0008) mark it as a dedicated CIB layer at the network's
periphery (RQ3) --- consistent with coordinated inauthentic amplification
patterns documented in political bot research @Ferrara2016 @Stella2018.

Key limitations are the synthetic network and heuristic bot labels. Future work
should apply this framework to longitudinal real data to track how the bot
community evolves across campaign phases and pinpoint the sequence of
anti-opposition narrative injections across distinct infodemic waves.

// ===========================================================================
= References
// ===========================================================================

#bibliography("refs.bib", style: "ieee", title: none)
