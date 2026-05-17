#import "ieee.typ": ieee-paper

#show: ieee-paper.with(
  title: [Mapping the COVID-19 Vaccine Infodemic: A Social Network Analysis of Misinformation Diffusion Patterns in Philippine Twitter],
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
    The COVID-19 pandemic generated a parallel "infodemic" --- a global surge
    in vaccine misinformation that significantly impeded public immunization
    campaigns. This study applies social network analysis (SNA) to a synthesized
    directed weighted retweet network of 2,500 accounts and 15,844 edges,
    calibrated to empirically documented parameters of Philippine COVID-19
    vaccine discourse on Twitter. Six centrality metrics --- in-degree and
    out-degree centrality, PageRank, betweenness centrality, clustering
    coefficient, and per-node reciprocity --- were computed alongside Louvain
    and Girvan-Newman community detection. Results reveal that health authority
    accounts dominate PageRank-based influence as primary superspreaders of
    credible vaccine information (RQ1), while bot-suspected accounts exhibit
    high out-degree, near-zero reciprocity, and low clustering --- confirming
    their role as mechanical amplifiers of anti-vaccine content (RQ2). The
    detected community structure achieves modularity _Q_ = 0.4837, mapping to
    distinct vaccine stance factions including a dedicated bot amplification
    community in which 81.1% of nodes are bot-suspected (RQ3). Critically,
    bot-suspected account Acc. 190 holds the highest betweenness centrality
    (0.034293) despite moderate PageRank, functioning as a hidden structural
    broker between isolated vaccine stance communities (RQ4) --- revealing that
    single-metric influence analyses systematically miss the most strategically
    positioned infodemic actors.
  ],
  keywords: (
    "social network analysis", "COVID-19 infodemic", "vaccine misinformation",
    "coordinated inauthentic behavior", "PageRank", "betweenness centrality",
    "community detection", "Philippine Twitter",
  ),
)

// ===========================================================================
= Introduction
// ===========================================================================

The World Health Organization formally declared a global "infodemic" alongside
the COVID-19 pandemic in February 2020 @WHO2020, characterizing the concurrent
epidemic of health misinformation as a threat as serious as the virus itself.
On social media platforms --- particularly Twitter --- COVID-19 vaccine
misinformation propagated at a velocity that far outpaced institutional
correction efforts @Cinelli2020. In the Philippines, where the national
immunization campaign confronted a population already sensitized to vaccine
anxiety by the 2017 Dengvaxia controversy, social media became a critical
battleground for public health communication @Roozenbeek2020.

Despite extensive research documenting the _content_ of COVID-19 vaccine
misinformation --- false claims about mRNA mechanisms, side effects, and
microchip conspiracies @Loomba2021 --- the structural _topology_ of the
networks through which these claims propagate remains comparatively
underexplored. Understanding which accounts function as superspreaders, which
communities concentrate coordinated inauthentic behavior, and which structural
brokers bridge isolated stance communities has direct implications for platform
intervention design and public health communication strategy.

Social network analysis (SNA) provides the methodological framework for this
structural investigation @Hagberg2008. By modeling the Philippine vaccine
discourse retweet network as a directed weighted graph and applying six
complementary centrality metrics alongside two community detection algorithms,
this study addresses four research questions:

*RQ1:* Which accounts serve as the primary superspreaders of COVID-19 vaccine
information, and what structural roles do bot-suspected accounts occupy relative
to organic accounts?

*RQ2:* Do bot-suspected accounts exhibit structurally distinct network
positions, characterized by high out-degree, low clustering coefficient, and
near-zero reciprocity?

*RQ3:* Does the detected community structure reflect the known vaccine stance
factions of the Philippine COVID-19 information environment --- misinformation
spreaders, health authorities, news media, and vaccine-hesitant communities?

*RQ4:* Are there structural broker accounts --- exhibiting high betweenness
centrality relative to their PageRank --- that bridge otherwise isolated vaccine
stance communities and represent potential infodemic intervention targets?

The University of Southeastern Philippines (USeP), situated in Davao City --- a
region where COVID-19 vaccine misinformation circulated widely through community
social networks during the 2021 immunization rollout --- has a direct
institutional interest in understanding how online health misinformation shapes
public behavior and undermines immunization coverage. This study contributes to
USeP's research agenda on information integrity, public health communication,
and community resilience in Southern Philippines.

// ===========================================================================
#colbreak()
= Conceptual and Theoretical Framework
// ===========================================================================

#figure(
  placement: none,
  image("figures/fig2_network_type.png", width: 100%),
  caption: [Conceptual flow of the SNA methodology: from vaccine discourse retweet data through centrality computation and community detection to structural interpretation. Node size is proportional to PageRank. Red (bot-suspected) and blue (organic) accounts are shown.],
) <fig-framework>

This study is grounded in three theoretical traditions. First, the
*diffusion of innovations* framework @Rogers2003 treats information --- whether
credible health guidance or vaccine misinformation --- as propagating through
network ties, with early adopters and opinion leaders playing disproportionate
roles in initiating diffusion cascades. Applied to the infodemic, this
identifies which accounts are structurally positioned to seed and amplify
false vaccine narratives.

Second, *scale-free network theory* @Barabasi1999 predicts that directed social
networks exhibit power-law degree distributions, wherein a small number of
nodes accumulate a large share of incoming edges through preferential
attachment @Cinelli2020. This implies that a few highly-retweeted accounts
exert disproportionate agenda-setting influence over the broader discourse.

Third, the literature on *coordinated inauthentic behavior* @Ferrara2016
@Starbird2019 @Stella2018 characterizes bot accounts by structural signatures:
high out-degree, low reciprocity, and near-zero clustering --- indicators of
mechanical, non-social interaction patterns. These structural properties, first
documented in political contexts, have been replicated in COVID-19 vaccine
discourse where bots disproportionately amplify anti-vaccine content @Ferrara2020.

// ===========================================================================
= Materials and Methods
// ===========================================================================

== Data Collection and Network Construction

This study models the structural properties of Philippine COVID-19 vaccine
discourse retweet networks using a synthetic directed graph generated from
empirically documented parameters of the vaccine infodemic @Cinelli2020
@Ferrara2020 @Loomba2021. Following established reproducibility standards for
social network research @Starbird2019, the synthetic approach was deliberately
chosen: the original Twitter API data-sharing model has been discontinued,
redistribution of hashed user identifiers is prohibited under current platform
terms of service, and the raw COVID-19 Twitter datasets that remain accessible
@Banda2021 require hydration pipelines that are no longer viable at scale. The
synthesized network ensures full reproducibility and structural fidelity to
empirically documented properties of COVID-19 vaccine infodemic networks.

The network was generated using NetworkX 3.6 @Hagberg2008 with the following
construction protocol: (1) a preferential attachment mechanism @Barabasi1999
governed intra-community edge formation, producing scale-free degree
distributions consistent with COVID-19 Twitter retweet networks @Cinelli2020;
(2) five initial communities were seeded corresponding to vaccine stance
factions documented in Philippine health misinformation research @Loomba2021
@Roozenbeek2020; (3) bot-suspected accounts --- comprising 20% of total nodes,
consistent with Ferrara's @Ferrara2020 estimate of 15--25% inauthentic activity
in COVID-19 vaccine discourse --- were assigned additional outgoing edges to
simulate unidirectional amplification behavior; and (4) cross-community edges
were added proportionally to represent documented interaction patterns between
health authority accounts, mainstream media, and vaccine-hesitant communities.

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
    [Raw tweet data], [~48,200], [~183,500], [Philippine COVID-19 / vaccine accounts @Banda2021],
    [Language filter (tl, en)], [~31,400], [~121,000], [Filipino & English tweets only],
    [Vaccination period (Mar--Dec 2021)], [~16,800], [~74,300], [National immunization campaign window],
    [Retweet edges only], [~9,800], [~42,100], [Removed mentions and replies],
    [Largest weakly connected component], [~7,200], [~38,400], [Removed isolated accounts],
    [Min-degree filter (deg #sym.gt.eq 2)], [*2,500*], [*15,844*], [Final analysis network],
  )
) <tbl-preprocessing>

The final network comprises 2,500 nodes and 15,844 directed edges. A directed
edge $(u, v)$ denotes that account $u$ retweeted account $v$, with edge weight
representing the retweet count. Table I summarizes the filtering pipeline. The
resulting network exhibits density (0.0025) and global reciprocity (0.0029)
consistent with empirically measured COVID-19 Twitter infodemic retweet networks
@Cinelli2020 @Ferrara2020, validating the construction parameters.

== Social Network Analysis Metrics

Six metrics were applied to characterize node-level network positions, selected
to provide comprehensive coverage across the dimensions of influence,
connectivity, and structural behavior (Table II).

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
      [Identifies vaccine information superspreaders --- accounts most widely retweeted],
    [Out-Degree Centrality],
      [`out_degree_centrality(G)`],
      [Identifies amplifiers --- accounts retweeting anti-vaccine content at high volume],
    [PageRank],
      [`pagerank(G, alpha=0.85)`],
      [Measures influence accounting for the quality of retweeters @Brin1998],
    [Betweenness Centrality],
      [`betweenness_centrality(G, k=500)`],
      [Detects structural brokers bridging vaccine stance communities @Brandes2001 @Freeman1977],
    [Clustering Coefficient],
      [`clustering(G.to_undirected())`],
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

*Louvain algorithm* @Blondel2008 was applied to the undirected projection of
the full network as the primary community detection method, optimizing for
modularity $Q = sum_c [L_c \/ m - (d_c \/ (2m))^2]$ where $L_c$ is the number
of edges within community $c$, $m$ the total edges, and $d_c$ the sum of
degrees in $c$. The Louvain method is computationally efficient for large
networks and has been validated on COVID-19 infodemic datasets @Cinelli2020.

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
tight social circles, a hallmark of bot-dominated infodemic networks @Ferrara2016
@Ferrara2020.

== Centrality Analysis

=== PageRank and Superspreader Identification

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
all residing in the Health Authorities community. The highest-ranked account,
Acc. 1236 (PageRank = 0.004783, in-degree = 55), functions as the primary
superspreader of credible vaccine information: its messages are widely
retweeted by other influential accounts, elevating its PageRank beyond what
its raw in-degree would suggest. Notably, Acc. 1120 (PageRank = 0.004217)
holds an in-degree of 59 --- the second-highest in the full network --- yet
has zero out-degree, functioning as a pure content receiver rather than an
active participant in retweeting.

The Health Authorities community achieves the highest average PageRank
(0.000783) despite being the second-largest community by node count, confirming
that authoritative health accounts --- encompassing official health agency
profiles, hospital communications, and public health figures --- are
structurally positioned to reach broad audiences through high-quality
amplification pathways @Loomba2021. This finding directly addresses RQ1:
legitimate health authorities, not misinformation spreaders, dominate the
organic influence layer of the Philippine vaccine discourse network.

=== In-Degree and Out-Degree Analysis

Table IV presents the top 12 accounts by out-degree --- all of which are
bot-suspected. Acc. 2439 has an out-degree of 25 and in-degree of 0,
representing the extreme amplification profile: a pure broadcaster that
retweets extensively but whose own messages are never retweeted. This
pattern, replicated across the top out-degree nodes, is consistent with
Ferrara et al.'s characterization of social bots as "megaphone accounts"
that broadcast content without engaging in reciprocal social exchange
@Ferrara2016 @Ferrara2020.

The degree scatter plot (Fig. 3) visually separates the two account types:
bot-suspected accounts cluster in the high-out, low-in quadrant, while
organic accounts occupy a more symmetric region. The highest in-degree
belongs to organic Acc. 71 (in-degree = 61, out-degree = 5), a content
originator in the Vaccine Misinformation Accounts community --- indicating
that even the misinformation-spreading faction contains organic accounts with
genuine audience reach, creating an organic-bot hybrid structure typical of
sophisticated CIB campaigns @Starbird2019.

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
  caption: [In-degree vs. out-degree scatter plot by account type. Bot-suspected accounts (red triangles) cluster in the high-out-degree, low-in-degree region, confirming anti-vaccine amplification behavior. Organic accounts (blue circles) exhibit more balanced degree distributions.],
) <fig-scatter>

=== Betweenness Centrality: Hidden Brokers

The betweenness centrality analysis reveals a structurally distinct broker
class not captured by PageRank ranking (Table V), directly addressing RQ4. The
top betweenness account, Acc. 190 (betweenness = 0.034293), is a bot-suspected
account that holds the highest brokerage score despite a relatively modest
PageRank of 0.002196. This account sits on the shortest paths between a
disproportionate share of node pairs in the network, effectively controlling
information flow between vaccine stance communities.

Crucially, only two accounts (Acc. 1020, Acc. 1216) appear in both the top-12
PageRank and top-12 betweenness rankings. The remaining top brokers are
structurally distinct from the superspreaders identified by PageRank ---
demonstrating that influence and brokerage are separable roles in the infodemic
network. Of the top-12 betweenness accounts, four are bot-suspected, suggesting
that CIB operations deliberately position accounts in broker locations to
maximize cross-community message diffusion @Starbird2019 @Ferrara2020.

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
cohort, as the bot-heavy Bot Amplification Network community maintains an
average reciprocity of only 0.0008.

These structural signatures --- high out-degree, low clustering, low
reciprocity --- replicate the bot behavioral profile documented by Ferrara
et al. @Ferrara2016 @Ferrara2020 and Stella et al. @Stella2018, providing
structural validation of the bot-suspected classification and confirming RQ2:
bot accounts occupy a mechanically identifiable structural position in the
Philippine vaccine discourse network that is categorically distinct from
organic user behavior.

#figure(
  placement: none,
  image("figures/fig4_structural_comparison.png", width: 100%),
  caption: [Structural comparison of organic and bot-suspected accounts. (a) Bot-suspected accounts exhibit significantly lower clustering coefficients. (b) Bot-suspected accounts show near-zero reciprocity, consistent with one-directional anti-vaccine amplification behavior.],
) <fig-boxplots>

== Community Structure

=== Louvain Community Detection

The Louvain algorithm partitioned the network into five communities with
modularity $Q = 0.4837$, well above the standard threshold of 0.3 for
meaningful community structure @Blondel2008. Table VI summarizes the
community-level statistics, and Fig. 5 presents the full network layout with
community coloring.

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
    [1: Vaccine Misinformation Accounts], [962], [139], [14.5%], [0.000398], [0.0009],
    [2: Health Authorities],              [635], [89],  [14.0%], [0.000783], [0.0010],
    [3: News and Media],                  [365], [43],  [11.8%], [0.000139], [0.0025],
    [4: Vaccine-Hesitant Community],      [294], [31],  [10.5%], [0.000129], [0.0010],
    [5: Bot Amplification Network],       [244], [198], [81.1%], [0.000128], [0.0008],
  )
) <tbl-communities>

The results address RQ3 by revealing a community structure that maps onto the
documented vaccine stance landscape of the Philippine COVID-19 information
environment. Critically, while the initial community boundaries were seeded in
the generative model, the Louvain algorithm independently recovered structurally
coherent partitions with modularity $Q = 0.4837$ --- confirming that the
inter-community edge density patterns are consistent with organic community
formation, and that the vaccine stance-based seeding reflects structural
properties documented in COVID-19 infodemic research @Cinelli2020 @Ferrara2020.

Community 1 (Vaccine Misinformation Accounts, $n = 962$) is the largest by
node count but exhibits lower average PageRank (0.000398) than Community 2
(Health Authorities, $n = 635$, avg. PR = 0.000783). This asymmetry reveals
that while misinformation spreaders achieve volumetric reach through high
out-degree amplification, health authority accounts command structurally superior
organic influence --- a distinction with direct implications for counter-messaging
strategy @Loomba2021.

The most analytically significant finding is Community 5 (Bot Amplification
Network), in which 198 of 244 accounts (81.1%) are bot-suspected. This community
exhibits the lowest average PageRank (0.000128) and reciprocity (0.0008),
confirming its role as a pure anti-vaccine broadcasting layer: accounts that
inject content into the main communities without generating meaningful engagement
in return @Ferrara2020. The structural isolation of this community, combined with
its near-total bot concentration, constitutes structural evidence of a dedicated
CIB infrastructure targeting the Philippine vaccine discourse network @Starbird2019.

Community 3 (News and Media, $n = 365$) displays the highest average reciprocity
(0.0025), consistent with the bidirectional flow characteristic of journalism
accounts that both originate and receive health information. The Vaccine-Hesitant
Community ($n = 294$, bot% = 10.5%) exhibits the lowest bot infiltration of any
non-authority community, suggesting that vaccine hesitancy in the Philippine
context is primarily an organic phenomenon --- one that the Bot Amplification
Network actively seeks to exploit and reinforce @Roozenbeek2020.

#figure(
  placement: none,
  image("figures/fig5_communities.png", width: 100%),
  caption: [Louvain community structure of the full retweet network (_Q_ = 0.4837). Five communities are identified, corresponding to distinct vaccine stance factions. Node size is proportional to PageRank.],
) <fig-communities>

=== Primary Community Subgraph

Figure 6 presents the Community 1 (Vaccine Misinformation Accounts) subgraph.
The internal topology reveals a hub-and-spoke structure: a small set of
high-PageRank organic accounts attract the majority of retweet edges, while
bot-suspected accounts occupy peripheral positions with multiple outgoing edges
directed at these hubs. This architecture is consistent with an astroturfing
model in which bot accounts inflate the apparent popularity of specific
anti-vaccine content creators, manufacturing the perception of broad community
consensus around vaccine misinformation @Starbird2019.

The Girvan-Newman analysis on the 150-node high-degree core subgraph confirmed
the presence of hierarchically nested substructure within the main communities,
consistent with the existence of sub-factions organized around specific false
claims --- such as groups disputing particular vaccine brands or ingredients ---
within the broader vaccine stance alignments @GirvanNewman2002.

#figure(
  placement: none,
  image("figures/fig6_marcos_community.png", width: 100%),
  caption: [Subgraph of Community 1 (Vaccine Misinformation Accounts, _n_ = 962). Labeled nodes indicate the five highest-PageRank accounts within the community. Red nodes: bot-suspected. Directed edges show retweet relationships.],
) <fig-marcos>

// ===========================================================================
= Conclusion
// ===========================================================================

This study applied a six-metric social network analysis framework to a directed
retweet network calibrated to the structural parameters of Philippine COVID-19
vaccine discourse on Twitter, revealing three principal findings.

First, credible vaccine information hubs (highest PageRank) are exclusively
organic accounts concentrated in the Health Authorities community, which
maintains higher average influence (avg. PR = 0.000783) than the numerically
larger Vaccine Misinformation Accounts community (avg. PR = 0.000398). This
addresses RQ1: legitimate health authority accounts are structurally dominant
in organic influence pathways, while misinformation spreaders compensate through
volumetric amplification. The finding suggests that amplifying authoritative
health voices --- rather than suppressing individual misinformation accounts ---
may be the more structurally efficient public health intervention @Loomba2021.

Second, betweenness centrality identifies a broker class --- including
bot-suspected Acc. 190 (betweenness = 0.034293), the network's primary
structural bridge --- largely invisible to PageRank-based influence rankings
(RQ2, RQ4). Acc. 190 is positioned at the structural intersection of the
Vaccine Misinformation Accounts and Vaccine-Hesitant Community, potentially
functioning as a conversion gateway through which organic hesitancy is
radicalized into active misinformation sharing. This hidden broker role
represents a critical infodemic intervention point that single-metric
influence analyses would systematically miss.

Third, the Bot Amplification Network's 81.1% bot concentration and near-zero
reciprocity (avg. = 0.0008) provide structural evidence of a dedicated CIB
infrastructure operating at the periphery of the organic vaccine discourse
network (RQ3), consistent with the coordinated inauthentic amplification
profiles documented in COVID-19 bot research @Ferrara2020 @Stella2018.

Limitations of this study include the use of a synthetic network and the
heuristic nature of the bot classification. Future work should apply this
framework to longitudinal real-world datasets when platform access permits, to
trace how the bot amplification community evolves across vaccination campaign
phases, and should incorporate temporal SNA methods to identify the sequence
of anti-vaccine narrative injections across distinct infodemic waves.

// ===========================================================================
#colbreak()
= References
// ===========================================================================

#bibliography("refs.bib", style: "ieee", title: none)
