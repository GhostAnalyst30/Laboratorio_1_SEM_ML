import numpy as np


def sample_family_size(rng: np.random.Generator) -> int:
    probs = [0.10, 0.25, 0.35, 0.20, 0.10]
    return int(rng.choice([1, 2, 3, 4, 5], p=probs))


def sample_income_level(rng: np.random.Generator) -> str:
    probs = [0.20, 0.40, 0.30, 0.10]
    return str(rng.choice(["low", "medium", "high", "premium"], p=probs))


def sample_ages(rng: np.random.Generator, family_size: int) -> list[int]:
    ages = []
    for _ in range(family_size):
        age_probs = [0.15, 0.20, 0.30, 0.25, 0.10]
        age_group = rng.choice([5, 15, 30, 45, 65], p=age_probs)
        noise = int(rng.normal(0, 3))
        ages.append(max(1, min(90, age_group + noise)))
    return sorted(ages)


def sample_sustainability_awareness(rng: np.random.Generator, income_level: str) -> float:
    base = {"low": 0.3, "medium": 0.5, "high": 0.6, "premium": 0.7}
    return float(np.clip(base.get(income_level, 0.5) + rng.normal(0, 0.1), 0.1, 0.95))


def sample_work_from_home(rng: np.random.Generator, income_level: str) -> bool:
    probs = {"low": 0.1, "medium": 0.2, "high": 0.4, "premium": 0.5}
    return rng.random() < probs.get(income_level, 0.2)


def truncated_normal(mean: float, std: float, low: float, high: float,
                     size: int = 1, rng: np.random.Generator = None) -> np.ndarray:
    if rng is None:
        rng = np.random.default_rng()
    samples = rng.normal(mean, std, size)
    return np.clip(samples, low, high)
