# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Environment

This project uses Nix flakes + direnv. Entering the directory with direnv configured activates the dev shell automatically (`use flake` in `.envrc`). Without direnv, run `nix develop` manually.

## Commands

```bash
# Lint
ruff check .

# Format
ruff format .

# Type check
mypy janet/

# Run all tests
pytest

# Run a single test file
pytest tests/test_simulation.py

# Run a single test
pytest tests/test_simulation.py::test_name

# Test with coverage
pytest --cov=janet
```

`just` is available as a command runner but the justfile currently only lists commands (`just --list`).

## Architecture

**janet** models multidimensional social diffusion: agents hold belief vectors across multiple topics and a personal topic-correlation matrix, and both evolve over time via message passing on a directed weighted network.

### Core flow

```
NetworkConfig  →  Simulation  →  .step() / .run() / .run_recorded()
                      ↑
                  Strategy (pluggable)
```

### Module responsibilities

- **`types.py`** — NumPy array type aliases. Key shapes: `Beliefs (N,n)`, `Correlations (N,n,n)`, `Network (N,N,n)`. `N` = agents, `n` = topics. `network[i,j,k]` is the weight receiver `i` places on sender `j` for topic `k`.

- **`network.py` (`NetworkConfig`)** — builds the initial simulation state. Construct directly with `NetworkConfig(N, n)` or from a NetworkX digraph via `NetworkConfig.from_networkx(G, n)`. Setter methods (`set_belief`, `set_correlation`, `set_stubbornness`, etc.) enforce valid ranges. Passed to `Simulation` as a snapshot; the simulation copies all arrays at construction.

- **`strategy.py` (`Strategy`)** — a dataclass of three pluggable callables that govern per-tick behavior:
  - `select_fn(sim)` → boolean mask of active senders (default: stochastic, driven by `phi`/`rho`)
  - `send_fn(sim, senders)` → belief messages from each active sender (default: broadcast own beliefs)
  - `update_fn(sim)` → new `(Beliefs, Correlations)` after aggregation (default: weighted average + correlation update)

- **`simulation.py` (`Simulation`)** — owns live state (`b`, `c`, `alpha`, `phi`, `rho`, `network`, `time`). Two learning rates: `eta` (beliefs) and `beta` (correlations; `0.0` disables correlation evolution). `run_recorded()` returns a dict with stacked `b`, `c`, and `time` arrays for analysis.

### Customization pattern

Override any single strategy function while keeping defaults for the rest:

```python
from janet import NetworkConfig, Simulation, Strategy

def my_send_fn(sim, senders):
    ...

sim = Simulation(net_cfg, strat=Strategy(send_fn=my_send_fn))
```

### Constraints enforced at construction

- `network[i,i,:]` must be zero (no self-influence)
- `c` diagonals must be `1.0`
- All probabilities (`alpha`, `phi`, `rho`) in `[0,1]`
- All beliefs and correlations in `[-1,1]`

## Code style

- Python 3.14, strict mypy, ruff with `E`, `F`, `I` rules, 80-char line length
- `cast()` is used instead of type: ignore for NumPy return types
- Internal attributes on `Simulation` are prefixed with `_` (`_adj_matrix`, `_one_minus_alpha`, `_net_cfg`)
