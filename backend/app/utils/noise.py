import numpy as np


def perlin_noise_1d(length: int, scale: float = 1.0, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n_octaves = 4
    result = np.zeros(length)
    amplitude = 1.0
    frequency = 1.0
    max_value = 0.0

    for _ in range(n_octaves):
        n_points = int(length / (frequency * 10)) + 2
        if n_points < 2:
            n_points = 2
        angles = rng.uniform(0, 2 * np.pi, n_points)
        gradients = np.cos(angles)

        indices = np.linspace(0, n_points - 1, length)
        i0 = np.floor(indices).astype(int)
        i1 = np.minimum(i0 + 1, n_points - 1)
        t = indices - i0
        t_smooth = t * t * (3 - 2 * t)

        g0 = gradients[i0]
        g1 = gradients[i1]

        val = g0 + t_smooth * (g1 - g0)
        result += amplitude * val
        max_value += amplitude

        amplitude *= 0.5
        frequency *= 2.0

    result = result / max_value * scale
    return result


def perlin_noise_2d(width: int, height: int, scale: float = 1.0, seed: int = 42) -> np.ndarray:
    x_noise = perlin_noise_1d(width, scale, seed)
    y_noise = perlin_noise_1d(height, scale, seed + 1)
    grid_x, grid_y = np.meshgrid(x_noise, y_noise, indexing='ij')
    return (grid_x + grid_y) / 2.0
