"""
simulation.py - Belief diffusion simulation

This module provides the Simulation class, which implements a multidimensional
belief diffusion model.
"""

# -- LICENSE HEADER ---------------------------------------------------------- #

# Copyright 2026 Merencillo, Julse M., Ga-as, James O.

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

import numpy as np
from numpy.typing import NDArray

from janet.network import NetworkConfig
from janet.strategy import Strategy
from janet.types import (
    Beliefs,
    Correlations,
    Network,
    ResponseProbability,
    SelectFn,
    SendFn,
    SendProbability,
    Stubbornness,
    UpdateFn,
)

# -- SIMULATION -------------------------------------------------------------- #


class Simulation:
    """
    Implementation of a belief diffusion model.

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

    Model Parameters
    ----------------
    network : Network
        structure of the social network. each edge weight is a vector.
        network[i,j,k] is the weight receiver i places on sender j for topic k
    strategy : Strategy
        determines the behavior of the model when selecting senders, sending
        messages, and updating beliefs
    eta : float
        belief vector learning rate
    beta : float
        correlation matrix learning rate

    Miscellaneous
    -------------
    time: int
        number of ticks the simulation has been running thus far
    seed: int
        seed value used by the random number generator
    rng : np.random.Generator
        random number generator to be used in the simulation
    """

    # -- CONSTRUCTOR --------------------------------------------------------- #

    def __init__(
        self,
        net_cfg: NetworkConfig,
        strat: Strategy | None = None,
        eta: float = 0.5,
        beta: float = 0.0,
        seed: int = 4310,
    ) -> None:
        """
        Constructs the simulation from the given network configuration, agent
        strategy, and other model parameters.
        """
        # Agent Parameters
        self.b: Beliefs = net_cfg.b.copy()
        self.c: Correlations = net_cfg.c.copy()
        self.alpha: Stubbornness = net_cfg.alpha.copy()
        self.phi: SendProbability = net_cfg.phi.copy()
        self.rho: ResponseProbability = net_cfg.rho.copy()

        # Model Parameters
        self.network: Network = net_cfg.network.copy()
        self.strategy: Strategy = strat if strat is not None else Strategy()
        self.eta: float = eta
        self.beta: float = beta

        # Miscellaneous
        self.time: int = 0
        self.seed: int = seed
        self.rng: np.random.Generator = np.random.default_rng(self.seed)

        # Internal Attributes
        self._adj_matrix: NDArray[np.bool] = np.any(self.network > 0, axis=2)
        self._one_minus_alpha: NDArray[np.float64] = (1.0 - self.alpha)[
            :, np.newaxis
        ]
        self._net_cfg: NetworkConfig = net_cfg

        # Validation
        self._validate()

    # -- DERIVED PROPERTIES -------------------------------------------------- #

    @property
    def N(self) -> int:
        return cast(int, self.b.shape[0])

    @property
    def n(self) -> int:
        return cast(int, self.b.shape[1])

    @property
    def select_fn(self) -> SelectFn:
        return self.strategy.select_fn

    @property
    def send_fn(self) -> SendFn:
        return self.strategy.send_fn

    @property
    def update_fn(self) -> UpdateFn:
        return self.strategy.update_fn

    # -- EXECUTION ----------------------------------------------------------- #

    def step(self) -> None:
        """
        Advances the simulation by one step.
        """
        self.b, self.c = self.update_fn(self)
        self.time += 1

    def run(self, steps: int, tol: float | None = None) -> None:
        """
        Runs the simulation for a given number of steps.

        If a tolerance value is given, the simulation stops whenever the mean
        absolute change in the belief vectors falls below this value.
        """
        for _ in range(steps):
            b_prev = self.b.copy() if tol is not None else None
            self.step()

            if tol is not None and b_prev is not None:
                if np.abs(self.b - b_prev).mean() < tol:
                    break

    def run_recorded(
        self, steps: int, tol: float | None = None
    ) -> dict[str, NDArray[np.float64]]:
        """
        Runs the simulation for a given number of steps, and returns a history
        of all intermediate states.

        If a tolerance value is given, the simulation stops whenever the mean
        absolute change in the belief vectors falls below this value.
        """
        b_hist: list[Beliefs] = []
        c_hist: list[Correlations] = []
        time_hist: list[int] = []

        b_hist.append(self.b.copy())
        c_hist.append(self.c.copy())
        time_hist.append(self.time)

        for _ in range(steps):
            b_prev = self.b.copy() if tol is not None else None
            self.step()

            b_hist.append(self.b.copy())
            c_hist.append(self.c.copy())
            time_hist.append(self.time)

            if tol is not None and b_prev is not None:
                if np.abs(self.b - b_prev).mean() < tol:
                    break

        return {
            "b": np.stack(b_hist),
            "c": np.stack(c_hist),
            "time": np.stack(time_hist),
        }

    def reset(self) -> None:
        """
        Resets the simulation to the initial conditions.
        """
        self.b = self._net_cfg.b.copy()
        self.c = self._net_cfg.c.copy()
        self.time = 0
        self.rng = np.random.default_rng(self.seed)

    # -- INTERNAL METHODS ---------------------------------------------------- #

    def _validate(self) -> None:
        """
        Validates the shape and ranges of all inputs.
        """
        N, n = cast(tuple[int, int], self.b.shape)

        if self.c.shape != (N, n, n):
            raise ValueError(
                f"c must have shape ({N},{n},{n}), got {self.c.shape}"
            )
        if self.alpha.shape != (N,):
            raise ValueError(
                f"alpha must have shape ({N},), got {self.alpha.shape}"
            )
        if self.phi.shape != (N,):
            raise ValueError(
                f"phi must have shape ({N},), got {self.phi.shape}"
            )
        if self.rho.shape != (N,):
            raise ValueError(
                f"rho must have shape ({N},), got {self.rho.shape}"
            )
        if self.network.shape != (N, N, n):
            net_shape = self.network.shape
            raise ValueError(
                f"network must have shape ({N},{N},{n}, got {net_shape})"
            )

        if not np.all((self.alpha >= 0.0) & (self.alpha <= 1.0)):
            raise ValueError("all alpha values must be in [0,1]")
        if not np.all((self.phi >= 0.0) & (self.phi <= 1.0)):
            raise ValueError("all phi values must be in [0,1]")
        if not np.all((self.rho >= 0.0) & (self.rho <= 1.0)):
            raise ValueError("all rho values must be in [0,1]")

        if not np.all((self.b >= -1.0) & (self.b <= 1.0)):
            raise ValueError("all b values must be in [-1,1]")
        if not np.all((self.c >= -1.0) & (self.c <= 1.0)):
            raise ValueError("all c values must be in [-1,1]")

        diag_idx = np.arange(n)
        if not np.allclose(self.c[:, diag_idx, diag_idx], 1.0):
            raise ValueError("all diagonal values of c must be 1.0")

        agent_idx = np.arange(N)
        if np.any(
            cast(NDArray[np.bool], self.network[agent_idx, agent_idx, :] != 0)
        ):
            raise ValueError(
                "agents cannot influence themselves; network[i,i,:] must be 0"
            )
