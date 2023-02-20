from pathlib import Path
import light_dark


def gen_interval_explain(basepath, force=False):
    path = Path(basepath, "fig", "getting-started", "interval.svg")
    if light_dark.exists(path) and not force:
        return

    from wildboar.ensemble import ShapeletForestClassifier
    from wildboar.explain import IntervalImportance
    from wildboar.datasets import load_two_lead_ecg
    import matplotlib.pyplot as plt

    plt.style
    x, y = load_two_lead_ecg()

    clf = ShapeletForestClassifier(n_jobs=-1, n_shapelets=10)
    clf.fit(x, y)

    ex = IntervalImportance(window=8)
    ex.fit(clf, x, y)

    for fig, ax in light_dark.yield_and_save_plot(path):
        _, mappable = ex.plot(x, y, ax=ax)
        fig.colorbar(mappable)


def gen_all(basepath, force=False):
    gen_interval_explain(basepath, force=force)
