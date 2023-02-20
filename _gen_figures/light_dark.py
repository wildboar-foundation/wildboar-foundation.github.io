import matplotlib.pyplot as plt
from pathlib import Path


def light_dark_paths(path: Path):
    file = Path(path.parts[-1])
    path = Path(*path.parts[:-1])
    ext = file.suffix
    name = file.stem

    return path.joinpath(f"{name}-light{ext}"), path.joinpath(f"{name}-dark{ext}")


def exists(path):
    light, dark = light_dark_paths(path)
    return light.exists() and dark.exists()


def yield_and_save_plot(path, transparent=True, figsize=(5.0, 3.1), **kwargs):
    light, dark = light_dark_paths(path)
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=figsize, **kwargs)
    yield fig, ax
    fig.savefig(light, transparent=transparent)

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=figsize, **kwargs)
    yield fig, ax
    fig.savefig(dark, transparent=transparent)

    plt.style.use("default")
