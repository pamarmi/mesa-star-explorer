from .style import DEFAULT_STYLE


def _plot(ax, history, x, y, **kwargs):
    style = DEFAULT_STYLE.copy()
    style.update(kwargs)
    ax.plot(history[x],history[y],**style)


def plot_luminosity(ax,history,**kwargs):
    _plot(ax,history,"star_age","log_L",**kwargs)


def plot_radius(ax,history,**kwargs):
    _plot(ax, history,"star_age", "log_R",**kwargs)


def plot_temperature(ax,history, **kwargs):
    _plot(ax, history,"star_age","log_Teff",**kwargs)