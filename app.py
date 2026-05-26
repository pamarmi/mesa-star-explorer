import streamlit as st
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

from mesa_star_explorer.io import load_mesa_table
from mesa_star_explorer.plotting import (
    plot_hr, plot_hr_age, plot_luminosity_evol,
    plot_radius_evol, plot_temperature_evol
)

# ---------------------------
# DARK MODE
# ---------------------------
dark_mode = st.sidebar.toggle("Dark mode", value=False)

if dark_mode:
    st.markdown(
        """
        <style>
        .stApp { background-color: #0e1117; color: #ffffff; }
        p, span, label, div { color: #ffffff !important; }
        .stSidebar { background-color: #161b22; }

        div[data-testid="stFileUploader"],
        div[data-testid="stFileUploader"] * {
            background-color: initial !important;
            color: initial !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.title("MESA Star Explorer")
st.write("Interactive visualisation tool for MESA stellar evolution outputs")

# ---------------------------
# UPLOAD
# ---------------------------
uploaded_files = st.file_uploader(
    "Upload MESA history.data files",
    accept_multiple_files=True
)

models = {}

if uploaded_files:

    st.subheader("Name your models")

    for i, uploaded in enumerate(uploaded_files):

        model_name = st.text_input(
            f"Model {i+1} name",
            value=uploaded.name.replace(".data", ""),
            key=f"name_{i}"
        )

        save_path = Path(f"temp_{i}.data")
        with open(save_path, "wb") as f:
            f.write(uploaded.getbuffer())

        meta, history = load_mesa_table(save_path)

        models[model_name] = {
            "meta": meta,
            "history": history
        }

    # ---------------------------
    # SIDEBAR CONTROLS
    # ---------------------------
    st.sidebar.title("Controls")

    mode = st.sidebar.radio(
        "Analysis mode",
        ["Single model", "Overlay models"]
    )

    selected_models = st.sidebar.multiselect(
        "Select models",
        list(models.keys()),
        default=list(models.keys())[:1]
    )

    # ---------------------------
    # COLORS
    # ---------------------------
    colors = plt.cm.tab10.colors
    model_colors = {
        name: colors[i % len(colors)]
        for i, name in enumerate(selected_models)
    }

    # ---------------------------
    # PLOT DEFINITIONS
    # ---------------------------
    PLOTS = {
        "HR Diagram": ("log_Teff", "log_L"),
        "HR Diagram with age": ("log_Teff", "log_L"),
        "Luminosity": ("star_age", "log_L"),
        "Radius": ("star_age", "log_R"),
        "Temperature": ("star_age", "log_Teff")
    }

    LABELS = {
        "log_Teff": "log Teff",
        "log_L": "log L",
        "log_R": "log R",
        "star_age": "Age (yr)"
    }

    choices = st.multiselect(
        "Select plots",
        list(PLOTS.keys()),
        default=["HR Diagram"]
    )

    # ---------------------------
    # SIDEBAR MODEL INFO
    # ---------------------------
    with st.sidebar.expander("Model Comparison", expanded=True):

        for name in selected_models:
            meta = models[name]["meta"]
            history = models[name]["history"]
            color = model_colors[name]

            st.markdown(
                f"<div style='margin-top:10px; padding:6px; "
                f"border-left:6px solid rgb{color}; "
                f"background-color:rgba{(*color, 0.1)}'>"
                f"<b>{name}</b></div>",
                unsafe_allow_html=True
            )

            if "version_number" in meta:
                st.write(f"Version: {meta['version_number']}")
            if "compiler" in meta:
                st.write(f"Compiler: {meta['compiler']}")
            if "date" in meta:
                st.write(f"Date: {meta['date']}")

            for key in ["star_mass", "mass"]:
                if key in history.columns:
                    st.write(f"Mass: {history[key].iloc[0]:.2f} M☉")
                    break

            for key in ["log_Z", "Z"]:
                if key in history.columns:
                    try:
                        Z = history[key].iloc[0]
                        Z = 10**float(Z) if "log" in key else float(Z)
                        st.write(f"Metallicity: {Z:.3e}")
                    except:
                        pass

            st.markdown("---")

    # ---------------------------
    # PLOT SETTINGS (SINGLE MODE)
    # ---------------------------
    def plot_settings(name, xcol, ycol, history):
        with st.sidebar.expander(f"{name} settings", expanded=False):
            lw = st.slider(f"{name} linewidth", 0.1, 5.0, 1.5)
            ls = st.selectbox(f"{name} style", ["-", "--", ":", "-."])
            grid = st.checkbox(f"{name} grid", True)

            xmin = float(history[xcol].min())
            xmax = float(history[xcol].max())
            ymin = float(history[ycol].min())
            ymax = float(history[ycol].max())

            xr = st.slider(f"{name} x-range", xmin, xmax, (xmin, xmax))
            yr = st.slider(f"{name} y-range", ymin, ymax, (ymin, ymax))

        return lw, ls, grid, xr, yr

    # ---------------------------
    # PLOTTING
    # ---------------------------
    figures = []

    if mode == "Single model":

        model_name = selected_models[0]
        history = models[model_name]["history"]

        for choice in choices:
            xcol, ycol = PLOTS[choice]

            lw, ls, grid, xr, yr = plot_settings(choice, xcol, ycol, history)

            if choice == "HR Diagram":
                fig = plot_hr(history, lw, "#1f77b4", grid, True, ls, xr, yr)
            elif choice == "HR Diagram with age":
                fig = plot_hr_age(history, lw, "#1f77b4", grid, True, ls, xr, yr)
            elif choice == "Luminosity":
                fig = plot_luminosity_evol(history, lw, "#1f77b4", grid, ls, xr, yr)
            elif choice == "Radius":
                fig = plot_radius_evol(history, lw, "#1f77b4", grid, ls, xr, yr)
            else:
                fig = plot_temperature_evol(history, lw, "#1f77b4", grid, ls, xr, yr)

            figures.append(fig)

    # ---------------------------
    # OVERLAY MODE (WITH CONTROLS)
    # ---------------------------
    else:

        st.sidebar.subheader("Overlay settings")

        lw = st.sidebar.slider("Line width", 0.5, 5.0, 2.0)
        ls = st.sidebar.selectbox("Line style", ["-", "--", ":", "-."])
        grid = st.sidebar.checkbox("Grid", True)
        reverse_teff = st.sidebar.checkbox("Reverse Teff axis", True)
        use_global_limits = st.sidebar.checkbox("Use global axis limits", True)

        for choice in choices:

            xcol, ycol = PLOTS[choice]

            # global limits
            if use_global_limits:
                all_x = pd.concat([models[n]["history"][xcol] for n in selected_models])
                all_y = pd.concat([models[n]["history"][ycol] for n in selected_models])

                xr = (float(all_x.min()), float(all_x.max()))
                yr = (float(all_y.min()), float(all_y.max()))
            else:
                xr, yr = None, None

            fig, ax = plt.subplots()

            for name in selected_models:
                h = models[name]["history"]

                ax.plot(
                    h[xcol],
                    h[ycol],
                    label=name,
                    color=model_colors[name],
                    linewidth=lw,
                    linestyle=ls
                )

            ax.set_xlabel(LABELS.get(xcol, xcol))
            ax.set_ylabel(LABELS.get(ycol, ycol))

            ax.legend()
            ax.grid(grid)

            if xcol == "log_Teff" and reverse_teff:
                ax.invert_xaxis()

            if xr:
                ax.set_xlim(xr)
            if yr:
                ax.set_ylim(yr)

            figures.append(fig)

    # ---------------------------
    # EXPORT
    # ---------------------------
    with st.sidebar.expander("Export", expanded=True):
        dpi = st.selectbox("DPI", [100, 150, 300, 600], index=2)
        fmt = st.selectbox("Format", ["png", "pdf", "svg"])
        transparent = st.checkbox("Transparent background", False)
        tight = st.checkbox("Tight layout", True)

    for fig in figures:
        st.pyplot(fig)

    for i, fig in enumerate(figures):
        filename = f"mesa_plot_{i}.{fmt}"
        save_kwargs = {"dpi": dpi, "transparent": transparent}

        if tight:
            save_kwargs["bbox_inches"] = "tight"

        fig.savefig(filename, **save_kwargs)

        with open(filename, "rb") as f:
            st.download_button(
                f"Download Figure {i+1}",
                f,
                filename,
                mime=f"image/{fmt}"
            )