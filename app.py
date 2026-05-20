import streamlit as st
from pathlib import Path
from mesa_star_explorer.io import load_mesa_table
from mesa_star_explorer.plotting import (plot_hr, plot_hr_age, plot_luminosity_evol,
    plot_radius_evol, plot_temperature_evol)

st.title("MESA Star Explorer")
st.write("Interactive visualisation tool for MESA stellar evolution outputs")

uploaded = st.file_uploader("Upload history.data")
if uploaded:
    save_path = (Path("temp.data"))
    with open(save_path,"wb") as f:
        f.write(uploaded.getbuffer())
    st.success("File loaded")    
    meta, history = load_mesa_table(save_path)
    #st.write(meta)
    #st.dataframe(history.head())
    choice = st.selectbox("Select plot",["HR Diagram","HR Diagram with age","Luminosity","Radius","Temperature"])
    if choice == "HR Diagram":
    	fig = plot_hr(history)
    elif choice == "HR Diagram with age":
    	fig = plot_hr_age(history)
    elif choice == "Luminosity":
    	fig = plot_luminosity_evol(history)
    elif choice == "Radius":
    	fig = plot_radius_evol(history)
    else:
    	fig = plot_temperature_evol(history)

    st.pyplot(fig)

    st.sidebar.header("Model Information")
    for key, value in meta.items():
        st.sidebar.write(f"{key}: {value}")

    fig.savefig("figure.png")
    with open("figure.png","rb") as f:
        st.download_button("Download Figure",f,"figure.png")