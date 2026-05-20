import matplotlib.pyplot as plt


def plot_hr(history):
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
    ax.plot(history["log_Teff"], history["log_L"], linewidth=2)
    ax.invert_xaxis()
    ax.set_xlabel(r"$\log T_{\rm eff}$[K]")
    ax.set_ylabel(r"$\log L/L_\odot$")
    ax.set_title("HR Diagram")
    return fig

def plot_hr_age(history):
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
    ax.plot(history["log_Teff"], history["log_L"], color = "black", linewidth=0.5)
    scatter = ax.scatter(history["log_Teff"],history["log_L"],c=history["star_age"],s=3)
    fig.colorbar(scatter, label="Age (yr)")
    ax.invert_xaxis()
    ax.set_xlabel(r"$\log T_{\rm eff}$[K]")
    ax.set_ylabel(r"$\log L/L_\odot$")
    ax.set_title("HR Diagram")
    return fig

def plot_luminosity_evol(history):
    fig, ax = plt.subplots()
    ax.plot(history["star_age"], history["log_L"])
    ax.set_xlabel("Age [yr]")
    ax.set_ylabel(r"$\log L/L_\odot$")
    return fig

def plot_radius_evol(history):
    fig, ax = plt.subplots()
    ax.plot(history["star_age"],history["log_R"])
    ax.set_xlabel("Age [yr]")
    ax.set_ylabel(r"$\log R/R_\odot$")
    return fig

def plot_temperature_evol(history):
    fig, ax = plt.subplots()
    ax.plot(history["star_age"], history["log_Teff"])
    ax.set_xlabel("Age [yr]")
    ax.set_ylabel(r"$\log T_{\rm eff}$ [K]")
    return fig