import streamlit as st
import matplotlib.pyplot as plt

from pathlib import Path

from mesa_star_explorer.io import load_mesa_table

from mesa_star_explorer.plotting import (
    plot_hr,
    plot_hr_age,
    plot_luminosity,
    plot_radius,
    plot_temperature,
    set_axes
)

PLOTS = {

    "HR Diagram": {
        "func": plot_hr,
        "x": "log_Teff",
        "y": "log_L",
        "invert": True
    },

    "HR Diagram Age": {
        "func": plot_hr_age,
        "x": "log_Teff",
        "y": "log_L",
        "invert": True
    },

    "Luminosity": {
        "func": plot_luminosity,
        "x": "star_age",
        "y": "log_L",
        "invert": False
    },

    "Radius": {
        "func": plot_radius,
        "x": "star_age",
        "y": "log_R",
        "invert": False
    },

    "Temperature": {
        "func": plot_temperature,
        "x": "star_age",
        "y": "log_Teff",
        "invert": False
    }
}

st.title("MESA Star Explorer")

uploaded = st.file_uploader(
    "Upload files",
    accept_multiple_files=True
)

models = {}

if uploaded:

    for i, file in enumerate(uploaded):

        name = st.text_input(
            f"Model {i+1}",
            file.name,
            key=i
        )

        path = Path(f"temp_{i}.data")

        with open(path, "wb") as f:
            f.write(file.getbuffer())

        meta, history = load_mesa_table(path)

        models[name] = {
            "meta": meta,
            "history": history
        }

    selected = st.sidebar.multiselect(
        "Models",
        list(models),
        default=list(models)[:1]
    )

    choice = st.selectbox(
        "Plot",
        list(PLOTS)
    )

    linewidth = st.sidebar.slider(
        "Line width",
        0.5,
        5.0,
        2.0
    )

    linestyle = st.sidebar.selectbox(
        "Style",
        ["-","--",":","-."]
    )

    fig, ax = plt.subplots()

    info = PLOTS[choice]

    colors = plt.cm.tab10.colors

    for i, name in enumerate(selected):

        history = models[name]["history"]

        info["func"](
            ax,
            history,
            linewidth=linewidth,
            linestyle=linestyle,
            color=colors[i]
        )

    set_axes(
        ax,
        info["x"],
        info["y"],
        invert_x=info["invert"]
    )

    ax.legend(selected)

    st.pyplot(fig)