"""
types.py - Type aliases for the belief diffusion model

This module defines type aliases for the network and agent arrays used
throughout the library.
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

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Hashable, TypeVar

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from janet.simulation import Simulation

# -- TYPE ALIASES ------------------------------------------------------------ #

# Legend:
# - N: number of agents/entities
# - n: number of topics under consideration

BeliefVector = NDArray[np.float64]  # shape (n,)
CorrelationMatrix = NDArray[np.float64]  # shape (n,n)

Beliefs = NDArray[np.float64]  # shape (N,n)
Correlations = NDArray[np.float64]  # shape (N,n,n)
Stubbornness = NDArray[np.float64]  # shape (N,)
SendProbability = NDArray[np.float64]  # shape (N,)
ResponseProbability = NDArray[np.float64]  # shape (N,)
Network = NDArray[np.float64]  # shape (N,N,n)

SelectFn = Callable[["Simulation"], NDArray[np.bool]]
SendFn = Callable[["Simulation", NDArray[np.bool]], Beliefs]
UpdateFn = Callable[["Simulation"], tuple[Beliefs, Correlations]]

NodeT = TypeVar("NodeT", bound=Hashable)
