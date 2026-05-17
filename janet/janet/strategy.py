"""
strategy.py - Pluggable agent strategies

This module defines the Strategy class and the default implementations of the
three core agent behaviors: selecting senders, sending messages, and updating
beliefs.
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

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, cast

import numpy as np
from numpy.typing import NDArray

from janet.types import Beliefs, Correlations, SelectFn, SendFn, UpdateFn

if TYPE_CHECKING:
    from janet.simulation import Simulation

# -- AGENT STRATEGIES ------------------------------------------------------- #


@dataclass
class Strategy:
    """
    Defines the behavior of all agents throughout the simulation.

    Agent Behaviors
    ---------------
    select_fn : SelectFn
        determines which agents will send messages for the current tick
    send_fn : SendFn
        determines what messages are being sent by all active senders
    update_fn : UpdateFn
        determines how agents will update their beliefs and topic correlations
    """

    select_fn: SelectFn = field(default_factory=lambda: default_select_fn)
    send_fn: SendFn = field(default_factory=lambda: default_send_fn)
    update_fn: UpdateFn = field(default_factory=lambda: default_update_fn)


# -- DEFAULT BEHAVIOR ------------------------------------------------------- #


def default_select_fn(sim: "Simulation") -> NDArray[np.bool]:
    """
    Randomly select active senders for the current tick.
    """
    N = sim.N
    # Select initial senders
    initiators = sim.rng.random(N) < sim.phi
    # Select responders
    has_active_sender = cast(
        NDArray[np.bool], np.any(sim._adj_matrix & initiators, axis=1)
    )
    responders = has_active_sender & (sim.rng.random(N) < sim.rho)
    return initiators | responders


def default_send_fn(sim: "Simulation", senders: NDArray[np.bool]) -> Beliefs:
    """
    All active senders send a copy of their beliefs as their message.
    """
    messages = np.zeros_like(sim.b)
    messages[senders] = sim.b[senders]
    return messages


def default_update_fn(sim: "Simulation") -> tuple[Beliefs, Correlations]:
    """
    Computes one full tick of the simulation. Messages are aggregated via a
    weighted average.
    """
    # Determine active senders
    active = sim.select_fn(sim)
    # Collect outgoing messages
    messages = sim.send_fn(sim, active)
    # Aggregate messages (via a weighted average)
    aggregated = cast(
        NDArray[np.float64], np.einsum("ijk,jk->ik", sim.network, messages)
    )
    active_float = active.astype(np.float64)
    total_weight = cast(
        NDArray[np.float64], np.einsum("ijk,j->ik", sim.network, active_float)
    )
    has_receiver = total_weight > 0.0
    aggregated = np.where(
        has_receiver,
        aggregated / np.where(has_receiver, total_weight, 1.0),
        sim.b,
    )
    # Update beliefs
    delta_m = aggregated - sim.b
    corr_delta = np.squeeze(
        cast(NDArray[np.float64], np.matmul(sim.c, delta_m[..., np.newaxis])),
        -1,
    )
    step = sim.eta * sim._one_minus_alpha * corr_delta
    new_b = np.clip(sim.b + step, -1.0, 1.0)
    # Update correlations
    new_c = sim.c.copy()
    if sim.beta > 0.0:
        outer = cast(
            NDArray[np.float64], np.einsum("ij,ik->ijk", delta_m, delta_m)
        )
        cov = (1.0 - sim.beta) * new_c + sim.beta * outer
        any_receiver = cast(NDArray[np.bool], np.any(has_receiver, axis=1))
        var = np.diagonal(cov, axis1=1, axis2=2)
        std = np.sqrt(np.maximum(var, 0.0))
        std_matrix = cast(
            NDArray[np.float64], np.einsum("ij,ik->ijk", std, std)
        )
        safe_std = np.where(std_matrix > 0.0, std_matrix, 1.0)
        updated_c = np.clip(cov / safe_std, -1.0, 1.0)
        new_c = np.where(
            any_receiver[:, np.newaxis, np.newaxis], updated_c, new_c
        )
    # Return new beliefs and correlations
    return new_b, new_c
