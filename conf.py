import os
import pathlib
import sys

from sphinx.util.logging import getLogger

sys.path.insert(0, os.path.abspath(".") + "/_extensions")

logger = getLogger(__name__)

project = "Wildboar"
copyright = "2023, Isak Samsten"
author = "Isak Samsten"
release = "main (dev)"

extensions = [
    "sphinx.ext.intersphinx",
    "lightdarkimg",
    "myst_parser",
    "sphinx.ext.mathjax",
    "sphinx_design",
    "sphinx_inline_tabs",
    "sphinx_toggleprompt",
]
current_version = "master"
intersphinx_mapping = {
    "wildboar": (f"https://docs.wildboar.dev/{current_version}", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Markdown setting
myst_heading_anchors = 3
myst_enable_extensions = [
    "dollarmath",
    "substitution",
    "deflist",
]
myst_substitutions = {
    "doc_link": f"[text](https://docs.wildboar.dev/{current_version}/wildboar/target)",
    "dataset_link": f"[text](https://datasets.wildboar.dev/{current_version}",
}

# Setup syntax highlighting
pygments_style = "github-light-colorblind"
pygments_dark_style = "github-dark-colorblind"
syntax_highlight = "short"
add_function_parentheses = False

html_static_path = ["_static"]
html_css_files = [
    "css/pygments-override.css",
]
html_theme = "furo"
html_title = "Wildboar"


sys.path.insert(0, os.path.abspath("_gen_figures"))
import pkgutil

regenerate_plots = os.environ.get("REGENERATE_PLOTS", False)

basepath = pathlib.Path("_static", "fig")
for modinfo in pkgutil.iter_modules(["_gen_figures"]):
    if modinfo.name.startswith("gen"):
        logger.info(f"Generating figures for: '{modinfo.name}'")
        module = modinfo.module_finder.find_module(modinfo.name).load_module(
            modinfo.name
        )
        funcs = list(module.__dict__.values())
        for func in funcs:
            if callable(func) and func.__name__.startswith("gen_"):
                logger.info(f" - '{func.__name__}'")
                func(basepath, force=regenerate_plots)
