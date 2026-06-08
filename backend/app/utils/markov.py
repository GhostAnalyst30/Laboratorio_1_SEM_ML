import numpy as np


class MarkovChain:
    def __init__(self, transition_matrix: np.ndarray, states: list[str],
                 initial_state: int = 0, seed: int = 42):
        self.transition_matrix = np.array(transition_matrix)
        self.states = states
        self.current_state = initial_state
        self.n_states = len(states)
        self.rng = np.random.default_rng(seed)

    def step(self) -> int:
        probs = self.transition_matrix[self.current_state]
        self.current_state = self.rng.choice(self.n_states, p=probs)
        return self.current_state

    @property
    def current_state_name(self) -> str:
        return self.states[self.current_state]

    def reset(self, state: int = 0):
        self.current_state = state
