import streamlit as st
from pathlib import Path
from mesa_star_explorer.io import load_mesa_table
from mesa_star_explorer.plotting import (
    plot_hr, plot_hr_age, plot_luminosity_evol,
    plot_radius_evol, plot_temperature_evol
)

dark_mode = st.sidebar.toggle("Dark mode", value=False)

if dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }

        p, span, label, div {
            color: #ffffff !important;
        }

        .stSidebar {
            background-color: #161b22;
        }

        .stSelectbox label,
        .stSlider label,
        .stCheckbox label {
            color: #ffffff !important;
        }

        /* keep file uploader unchanged */
        div[data-testid="stFileUploader"] {
            background-color: initial !important;
            color: initial !important;
        }

        div[data-testid="stFileUploader"] * {
            color: initial !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.title("MESA Star Explorer")
st.write("Interactive visualisation tool for MESA stellar evolution outputs")

uploaded = st.file_uploader("Upload history.data")

if uploaded:
    save_path = Path("temp.data")
    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())

    st.success("File loaded")
    meta, history = load_mesa_table(save_path)


    ########################################
    #SIDE BAR
    ########################################
    st.sidebar.title("Controls")
    st.sidebar.divider()
    with st.sidebar.expander("Model Information", expanded=True):
        meta_map = {"version_number": "MESA Version","compiler": "Compiler","date": "Build Date"}
        for key, label in meta_map.items():
            if key in meta:
                value = meta[key]
                if key == "date":
                    value = str(value)
                    if len(value) == 8:
                        value = value[:4] + "-" + value[4:6] + "-" + value[6:]
                st.write(f"{label}: {value}")

    with st.sidebar.expander("Stellar Properties", expanded=True):
        for key in ["star_mass", "mass"]:
            if key in history.columns:
                st.write(f"Initial Mass: {history[key].iloc[0]:.2f} M☉")
                break
        for key in ["log_Z", "Z"]:
            if key in history.columns:
                Z = history[key].iloc[0]
                try:
                    Z = 10**float(Z) if "log" in key else float(Z)
                    st.write(f"Metallicity: {Z:.3e}")
                except:
                    pass


    #######################################
    # PLOT
    #######################################
    choice = st.selectbox(
        "Select plot",
        ["HR Diagram", "HR Diagram with age", "Luminosity", "Radius", "Temperature"]
    )

    if choice == "HR Diagram":
        with st.sidebar.expander("Plot Settings", expanded=True):

            linewidth = st.slider("Line width", 1, 5, 2)
            linecolor = st.color_picker("Line color", "#1f77b4")
            linestyle = st.selectbox("Line style", ["-", "--", ":", "-."])
            grid = st.checkbox("Grid", value=True)
            reverse_x = st.checkbox("Reverse Teff axis", value=True)

            xmin_data = round(float(history["log_Teff"].min())-2)
            xmax_data = round(float(history["log_Teff"].max())+2)
            ymin_data = round(float(history["log_L"].min())-2)
            ymax_data = round(float(history["log_L"].max())+2)
            xrange = st.slider("logT range",xmin_data,xmax_data,(xmin_data, xmax_data))
            yrange = st.slider("logL range",ymin_data,ymax_data,(ymin_data, ymax_data))
        fig = plot_hr(history, linewidth, linecolor, grid,reverse_x,linestyle,xrange, yrange)

    elif choice == "HR Diagram with age":
        with st.sidebar.expander("Plot Settings", expanded=True):
            linewidth = st.slider("Line width", 0.1, 2.0, 0.5, 0.1)
            linecolor = st.color_picker("Line color", "#00ffaa")
            linestyle = st.selectbox("Line style", ["-", "--", ":", "-."])
            grid = st.checkbox("Grid", value=True)
            reverse_x = st.checkbox("Reverse Teff axis", value=True)

            xmin_data = round(float(history["log_Teff"].min())-2)
            xmax_data = round(float(history["log_Teff"].max())+2)
            ymin_data = round(float(history["log_L"].min())-2)
            ymax_data = round(float(history["log_L"].max())+2)
            xrange = st.slider("logT range",xmin_data,xmax_data,(xmin_data, xmax_data))
            yrange = st.slider("logL range",ymin_data,ymax_data,(ymin_data, ymax_data))
        fig = plot_hr_age(history, linewidth, linecolor, grid,reverse_x,linestyle,xrange, yrange)
    elif choice == "Luminosity":
        with st.sidebar.expander("Plot Settings", expanded=True):
            linewidth = st.slider("Line width", 0.1, 2.0, 0.5, 0.1)
            linecolor = st.color_picker("Line color", "#00ffaa")
            linestyle = st.selectbox("Line style", ["-", "--", ":", "-."])
            grid = st.checkbox("Grid", value=True)

            ymin_data = round(float(history["log_L"].min())-2)
            ymax_data = round(float(history["log_L"].max())+2)
            xmin_data = float(history["star_age"].min())
            xmax_data = float(history["star_age"].max())
            xrange = st.slider("logL range",xmin_data,xmax_data,(xmin_data, xmax_data))
            yrange = st.slider("Age range",ymin_data,ymax_data,(ymin_data, ymax_data))
        fig = plot_luminosity_evol(history, linewidth, linecolor, grid,linestyle,xrange, yrange)
    elif choice == "Radius":
        with st.sidebar.expander("Plot Settings", expanded=True):
            linewidth = st.slider("Line width", 0.1, 2.0, 0.5, 0.1)
            linecolor = st.color_picker("Line color", "#00ffaa")
            linestyle = st.selectbox("Line style", ["-", "--", ":", "-."])
            grid = st.checkbox("Grid", value=True)

            ymin_data = round(float(history["log_R"].min())-0.5)
            ymax_data = round(float(history["log_R"].max())+0.5)
            xmin_data = float(history["star_age"].min())
            xmax_data = float(history["star_age"].max())
            xrange = st.slider("logR range",xmin_data,xmax_data,(xmin_data, xmax_data))
            yrange = st.slider("Age range",ymin_data,ymax_data,(ymin_data, ymax_data))
        fig = plot_radius_evol(history,linewidth, linecolor, grid,linestyle,xrange, yrange)
    else:
        with st.sidebar.expander("Plot Settings", expanded=True):
            linewidth = st.slider("Line width", 0.1, 2.0, 0.5, 0.1)
            linecolor = st.color_picker("Line color", "#00ffaa")
            linestyle = st.selectbox("Line style", ["-", "--", ":", "-."])
            grid = st.checkbox("Grid", value=True)

            ymin_data = round(float(history["log_Teff"].min())-2)
            ymax_data = round(float(history["log_Teff"].max())+2)
            xmin_data = float(history["star_age"].min())
            xmax_data = float(history["star_age"].max())
            xrange = st.slider("logT range",xmin_data,xmax_data,(xmin_data, xmax_data))
            yrange = st.slider("Age range",ymin_data,ymax_data,(ymin_data, ymax_data))
        fig = plot_temperature_evol(history,linewidth, linecolor, grid,linestyle)

    with st.sidebar.expander("Export", expanded=True):
        dpi = st.selectbox("Resolution (DPI)", [100,150,300,600], index=2)
        fmt = st.selectbox("Format", ["png","pdf","svg"])
        transparent = st.checkbox("Transparent background", False)
        tight = st.checkbox("Tight layout", True)

    st.pyplot(fig)
    filename = f"mesa_plot.{fmt}"
    save_kwargs = {"dpi": dpi,"transparent": transparent}
    if tight:
        save_kwargs["bbox_inches"] = "tight"
    fig.savefig(filename, **save_kwargs)
    with open(filename,"rb") as f:
        st.download_button("Download Figure", f,filename,mime=f"image/{fmt}")

