"""
network.py - Network configuration and manipulation

This module provides the NetworkConfig class, which defines the initial state
of a simulation: agent beliefs, correlations, stubbornness, activation
probabilities and the network weight structure.
"""

# -- LICENSE HEADER ---------------------------------------------------------- #

# Copyright 2026 Merencillo, Julse M.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -- IMPORT LIST ------------------------------------------------------------- #

from typing import cast

import networkx as nx
import numpy as np

from janet.types import (
    Beliefs,
    Correlations,
    Network,
    NodeT,
    ResponseProbability,
    SendProbability,
    Stubbornness,
)

# -- NETWORK SETUP ---------------------------------------------------------- #


class NetworkConfig:
    """
    Stores the initial state of the simulation, including the network topology
    and the state of all the agent. Used to manipulate the starting conditions
    before the simulation begins.

    Agent Parameters
    ----------------
    b : Beliefs
        belief vectors, one for each agent
    c : Correlations
        topic correlation matrices, one for each agent. diagonals are always set
        to 1
    alpha : Stubbornness
        agent stubbornness, within [0,1]
    phi : SendProbability
        probability that each agent sends a message on a given tick,
        within [0,1]
    rho : ResponseProbability
        probability that a receiving agent replies to a sender, within [0,1]

    Network Topology
    ----------------
    network : Network
        structure of the social network. each edge weight is a vector.
        network[i,j,k] is the weight receiver i places on sender j for topic k
    """

    # -- CONSTRUCTORS ------------------------------------------------------- #

    def __init__(self, N: int, n: int) -> None:
        """
        Constructs a social network with all values set to an appropriate
        default, either a zero or identity vector/matrix.
        """
        self.b: Beliefs = np.zeros((N, n))
        self.c: Correlations = np.tile(np.eye(n), (N, 1, 1))
        self.alpha: Stubbornness = np.zeros(N)
        self.phi: SendProbability = np.zeros(N)
        self.rho: ResponseProbability = np.zeros(N)
        self.network: Network = np.zeros((N, N, n))

    @classmethod
    def from_networkx(
        cls, network: nx.DiGraph[NodeT], n: int
    ) -> tuple[NetworkConfig, dict[NodeT, int]]:
        """
        Constructs a social network based on the given NetworkX directed graph.
        All values are set to an appropriate default:

        - If two agents are connected, the weight is set to the vector filled
          with ones; otherwise, it is set to the zero vector.
        - All other parameters are set to either the zero vector or identity
          matrix.

        This also returns a mapping between the original node identifiers to
        the corresponding array indices.
        """
        nodes = list(network.nodes)
        node_index = {node: i for i, node in enumerate(nodes)}
        N = len(nodes)
        nc = cls(N, n)

        for src, dest in network.edges:
            i = node_index[src]
            j = node_index[dest]
            nc.network[j, i, :] = 1.0

        return nc, node_index

    # -- DERIVED PROPERTIES ------------------------------------------------- #

    @property
    def N(self) -> int:
        """
        Returns the number of agents in the network.
        """
        return cast(int, self.b.shape[0])

    @property
    def n(self) -> int:
        """
        Returns the number of topics under consideration.
        """
        return cast(int, self.b.shape[1])

    # -- AGENT MODIFICATION -------------------------------------------------- #

    def set_belief(self, N: int, topic: int, value: float) -> None:
        """
        Sets the belief of agent N on a given topic.
        """
        if value < -1.0 or value > 1.0:
            raise ValueError("Value must be within [-1.0, 1.0]")
        self.b[N, topic] = value

    def set_correlation(
        self, N: int, topic_1: int, topic_2: int, value: float
    ) -> None:
        """
        Sets the correlation of agent N between two topics.
        """
        if topic_1 == topic_2:
            raise ValueError("Cannot change correlation between the same topic")
        if value < -1.0 or value > 1.0:
            raise ValueError("Value must be within [-1.0, 1.0]")
        self.c[N, topic_1, topic_2] = value
        self.c[N, topic_2, topic_1] = value

    def set_stubbornness(self, N: int, value: float) -> None:
        """
        Sets the stubbornness of agent N.
        """
        if value < 0.0 or value > 1.0:
            raise ValueError("Value must be within [0.0, 1.0]")
        self.alpha[N] = value

    def set_send_probability(self, N: int, value: float) -> None:
        """
        Sets the probability of agent N to send a message.
        """
        if value < 0.0 or value > 1.0:
            raise ValueError("Value must be within [0.0, 1.0]")
        self.phi[N] = value

    def set_response_probability(self, N: int, value: float) -> None:
        """
        Sets the probability of agent N to respond to a message.
        """
        if value < 0.0 or value > 1.0:
            raise ValueError("Value must be within [0.0, 1.0]")
        self.rho[N] = value

    # -- NETWORK MODIFICATION ----------------------------------------------- #

    def set_network_weight(
        self, N_send: int, N_recv: int, topic: int, value: float
    ) -> None:
        """
        Sets the weight that N_recv places on N_send on a given topic.
        """
        if N_send == N_recv:
            raise ValueError("Agents cannot influence themselves")
        if value < -1.0 or value > 1.0:
            raise ValueError("Value must be within [-1.0, 1.0]")
        self.network[N_recv, N_send, topic] = value
