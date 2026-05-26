LABELS = {
    "log_Teff": "log Teff",
    "log_L": "log Luminosity",
    "log_R": "log Radius",
    "star_age": "Age (yr)"
}


def set_axes(ax, xcol, ycol, xr=None, yr=None,invert_x=False,grid=True):
    ax.set_xlabel(LABELS.get(xcol, xcol))
    ax.set_ylabel(LABELS.get(ycol, ycol))
    if xr:
        ax.set_xlim(xr)

    if yr:
        ax.set_ylim(yr)

    if invert_x:
        ax.invert_xaxis()

    if grid:
        ax.grid(alpha=0.3)