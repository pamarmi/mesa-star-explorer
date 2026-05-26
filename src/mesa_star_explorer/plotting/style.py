DEFAULT_STYLE = {
    "linewidth": 2,
    "linestyle": "-",
    "color": "#1f77b4"
}


def apply_style(ax, grid=True):

    if grid:
        ax.grid(True, alpha=0.3)