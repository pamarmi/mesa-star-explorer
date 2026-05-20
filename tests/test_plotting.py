from mesa_star_explorer.io import load_mesa_table
from mesa_star_explorer.plotting import plot_hr
from mesa_star_explorer.plotting import plot_hr_age
from mesa_star_explorer.plotting import plot_luminosity_evol
from mesa_star_explorer.plotting import plot_radius_evol
from mesa_star_explorer.plotting import plot_temperature_evol

def test_hr_plot():
    meta, history = load_mesa_table("examples/sample_LOGS/history_1M.data")
    fig = plot_hr(history)
    assert fig is not None

def test_hr_plot_age():
    meta, history = load_mesa_table("examples/sample_LOGS/history_1M.data")
    fig = plot_hr_age(history)
    assert fig is not None

def test_plot_luminosity_evol():
    meta, history = load_mesa_table("examples/sample_LOGS/history_1M.data")
    fig = plot_luminosity_evol(history)
    assert fig is not None

def test_plot_radius_evol():
    meta, history = load_mesa_table("examples/sample_LOGS/history_1M.data")
    fig = plot_radius_evol(history)
    assert fig is not None

def test_plot_temperature_evol():
    meta, history = load_mesa_table("examples/sample_LOGS/history_1M.data")
    fig = plot_temperature_evol(history)
    assert fig is not None