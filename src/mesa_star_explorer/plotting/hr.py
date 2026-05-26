from .style import DEFAULT_STYLE

def plot_hr(ax, history, **kwargs):
    style = DEFAULT_STYLE.copy()
    style.update(kwargs)
    ax.plot(history["log_Teff"], history["log_L"], **style)


def plot_hr_age(ax, history, **kwargs):
    style = DEFAULT_STYLE.copy()
    style.update(kwargs)
    age = history["star_age"]
    line = ax.scatter(history["log_Teff"], history["log_L"],c=age,s=4)
    return line