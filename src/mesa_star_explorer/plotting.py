import matplotlib.pyplot as plt


def plot_hr(history, linewidth=2, linecolor="black", grid=False,reverse_x=True,linestyle="solid",xrange =None,yrange=None):
    """
    Hertzsprung-Russell diagram.

    Parameters
    ----------
    history : pandas.DataFrame

    Returns
    -------
    matplotlib figure
    """

    fig, ax = plt.subplots(figsize=(7,5))
    ax.plot(history["log_Teff"], history["log_L"], linewidth=linewidth, color = linecolor,ls=linestyle)
    ax.set_xlim(3,6)
    ax.set_ylim(-4,12)
    if xrange:
         ax.set_xlim(xrange)
    if yrange:
        ax.set_ylim(yrange)
    if reverse_x:
        ax.invert_xaxis()
    if grid:
        ax.grid()
    ax.set_xlabel(r"$\log T_{\rm eff}$[K]")
    ax.set_ylabel(r"$\log L/L_\odot$")
    ax.set_title("HR Diagram")
    return fig

def plot_hr_age(history, linewidth=0.5, linecolor="black", grid=False,reverse_x=True,linestyle="solid",xrange =None,yrange=None):
    """
    Hertzsprung-Russell diagram.

    Parameters
    ----------
    history : pandas.DataFrame

    Returns
    -------
    matplotlib figure
    """

    fig, ax = plt.subplots(figsize=(7,5))
    ax.plot(history["log_Teff"], history["log_L"], linewidth=linewidth, color = linecolor,ls=linestyle)
    scatter = ax.scatter(history["log_Teff"],history["log_L"],c=history["star_age"],s=3)
    fig.colorbar(scatter, label="Age (yr)")
    ax.set_xlim(3,6)
    ax.set_ylim(-4,12)
    if xrange:
         ax.set_xlim(xrange)
    if yrange:
        ax.set_ylim(yrange)
    if reverse_x:
        ax.invert_xaxis()
    if grid:
        ax.grid()
    ax.set_xlabel(r"$\log T_{\rm eff}$[K]")
    ax.set_ylabel(r"$\log L/L_\odot$")
    ax.set_title("HR Diagram")
    return fig

def plot_luminosity_evol(history, linewidth=0.5, linecolor="black", grid=False,linestyle="solid",xrange =None,yrange=None):
    fig, ax = plt.subplots()
    ax.plot(history["star_age"], history["log_L"], linewidth=linewidth, color = linecolor,ls=linestyle)
    if xrange:
         ax.set_xlim(xrange)
    if yrange:
        ax.set_ylim(yrange)
    if grid:
        ax.grid()
    ax.set_xlabel("Age [yr]")
    ax.set_ylabel(r"$\log L/L_\odot$")
    return fig

def plot_radius_evol(history, linewidth=0.5, linecolor="black", grid=False,linestyle="solid",xrange =None,yrange=None):
    fig, ax = plt.subplots()
    ax.plot(history["star_age"],history["log_R"],linewidth=linewidth, color = linecolor,ls=linestyle)
    if xrange:
         ax.set_xlim(xrange)
    if yrange:
        ax.set_ylim(yrange)
    if grid:
        ax.grid()
    ax.set_xlabel("Age [yr]")
    ax.set_ylabel(r"$\log R/R_\odot$")
    return fig

def plot_temperature_evol(history, linewidth=0.5, linecolor="black", grid=False,linestyle="solid",xrange =None,yrange=None):
    fig, ax = plt.subplots()
    ax.plot(history["star_age"], history["log_Teff"],linewidth=linewidth, color = linecolor,ls=linestyle)
    if xrange:
         ax.set_xlim(xrange)
    if yrange:
        ax.set_ylim(yrange)
    if grid:
        ax.grid()
    ax.set_xlabel("Age [yr]")
    ax.set_ylabel(r"$\log T_{\rm eff}$ [K]")
    return fig