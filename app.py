###############################################
#
# IMPORT ALL NECESSARY FUNCTIONS AND LIBRARIES
#
###############################################
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

@st.cache_data
def cached_load(file_bytes):

    path = "temp_cache.data"

    with open(path,"wb") as f:
        f.write(file_bytes)

    return load_mesa_table(path)

##################
# DARK MODE
##################
dark_mode = st.sidebar.toggle("Dark mode", False)

if dark_mode:
    st.markdown("""
    <style>

    .stApp{
        background:#0e1117;
        color:white;
    }

    .stSidebar{
        background:#161b22;
    }

    h1,h2,h3,p,label,span{
        color:white !important;
    }

    /* keep uploader untouched */

    div[data-testid="stFileUploader"]{
        background:transparent !important;
        border-color:inherit !important;
    }

    div[data-testid="stFileUploader"] *{
        color:unset !important;
        background:unset !important;
    }

    button[kind="secondary"]{
        color:unset !important;
    }

    </style>
    """, unsafe_allow_html=True)

############################
# META DATA FOR PLOTS
############################

PLOTS = {
    "HR Diagram":{
        "func":plot_hr,
        "x":"log_Teff",
        "y":"log_L",
        "invert":True
    },

    "HR Diagram Age":{
        "func":plot_hr_age,
        "x":"log_Teff",
        "y":"log_L",
        "invert":True
    },

    "Luminosity":{
        "func":plot_luminosity,
        "x":"star_age",
        "y":"log_L",
        "invert":False
    },

    "Radius":{
        "func":plot_radius,
        "x":"star_age",
        "y":"log_R",
        "invert":False
    },

    "Temperature":{
        "func":plot_temperature,
        "x":"star_age",
        "y":"log_Teff",
        "invert":False
    }
}


##################################
#
# MAIN HEADER AND UPLOADING
#
##################################

st.title("MESA Star Explorer")
st.write("Interactive visualisation tool for MESA stellar evolution outputs")

uploaded = st.file_uploader(
    "Upload MESA history.data files",
    accept_multiple_files=True
)

models = {}

if uploaded:

    for i,file in enumerate(uploaded):
        model_name = st.text_input(
            f"Model {i+1}",
            file.name.replace(".data",""),
            key=f"name_{i}"
        )
        meta,history = cached_load(file.getvalue())
        models[model_name] = {"meta":meta, "history":history}

    # SIDEBAR FEATURES
    selected = st.sidebar.multiselect("Models",list(models),default=list(models)[:1]    )

    choice = st.selectbox("Plot",list(PLOTS))
    info = PLOTS[choice]
    linewidth = st.sidebar.slider("Line width",0.5,5.0,2.0)
    linestyle = st.sidebar.selectbox("Line style",["-","--",":","-."])
    grid = st.sidebar.checkbox("Show grid",True)

    xmin = min(models[m]["history"][info["x"]].min() for m in selected)
    xmax = max(models[m]["history"][info["x"]].max() for m in selected)
    ymin = min(models[m]["history"][info["y"]].min() for m in selected)
    ymax = max(models[m]["history"][info["y"]].max() for m in selected)

    if "HR" in choice:
        xmin = float(xmin)-2
        xmax = float(xmax)+2
        ymin = float(ymin)-2
        ymax = float(ymax)+2

    elif choice == "Luminosity":
        xmin = 0.0
        ymin = float(ymin)-2
        ymax = float(ymax)+2

    elif choice == "Radius":
        xmin = 0.0
        ymin = float(ymin)-2
        ymax = float(ymax)+2

    elif choice == "Temperature":
        xmin = 0.0
        ymin = float(ymin)-2
        ymax = float(ymax)+2

    xrange = st.sidebar.slider("X range",float(xmin), float(xmax),(float(xmin),float(xmax)))
    yrange = st.sidebar.slider("Y range",float(ymin),float(ymax),(float(ymin),float(ymax)))

    with st.sidebar.expander("Model Information",True):
        colors = plt.cm.tab10.colors
        for i,name in enumerate(selected):
            meta = models[name]["meta"]
            history = models[name]["history"]
            color = colors[i]

            st.markdown(f":rainbow[{name}]")
            if "version_number" in meta:
                st.write(f"MESA: {meta['version_number']}")

            if "compiler" in meta:
                st.write(f"Compiler: {meta['compiler']}")

            if "date" in meta:
                d = str(meta["date"])
                if len(d)==8:
                    d = (f"{d[:4]}-"f"{d[4:6]}-"f"{d[6:]}")
                st.write(f"Date: {d}")

            if "star_mass" in history.columns:
                st.write(f"Mass: " f"{float(history['star_mass'].iloc[0]):.2f} M☉")

            if "log_Z" in history.columns:
                try:
                    Z = (10**float(history["log_Z"].iloc[0]))
                    st.write(f"Z: {Z:.3e}")
                except:
                    pass

            st.divider()

    # FIGURE
    fig,ax = plt.subplots()
    colors = plt.cm.tab10.colors
    for i,name in enumerate(selected):
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
        xr=xrange,
        yr=yrange,
        invert_x=info["invert"],
        grid=grid
    )

    ax.legend(selected)
    st.pyplot(fig)

    with st.sidebar.expander("Export",True):
        dpi = st.selectbox("DPI",[100,150,300,600],2)
        fmt = st.selectbox("Format",["png","pdf","svg"])
        transparent = st.checkbox("Transparent",False)
    filename = f"mesa_plot.{fmt}"
    fig.savefig(filename,dpi=dpi,transparent=transparent,bbox_inches="tight")

    with open(filename,"rb") as f:
        st.download_button("Download Figure",f,filename)