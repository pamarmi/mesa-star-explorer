# MESA Star Explorer

Interactive visualisation and analysis tool for MESA stellar evolution outputs.

MESA Star Explorer provides a lightweight GUI to inspect and visualise stellar evolution calculations from MESA (Modules for Experiments in Stellar Astrophysics), avoiding custom plotting scripts for common exploratory tasks.

## Features

- Parse MESA `history.data` files without external MESA-specific readers
- Streamlit graphical interface
- Hertzsprung–Russell diagrams
- HR diagrams coloured by stellar age
- Evolution plots:
  - Luminosity
  - Radius
  - Effective temperature
- Interactive controls:
  - Line colour
  - Line width
  - Axis ranges
  - Grid display
  - Temperature-axis inversion
- Figure export:
  - PNG / PDF / SVG
  - DPI selection
  - Transparent background
  - Tight layout
- Automatic model metadata extraction

## Motivation

MESA outputs often require custom scripts for exploratory visualisation. This project aims to provide a lightweight, extensible interface for rapid stellar evolution inspection while following scientific software development practices.

## Installation

Clone repository:

```bash
git clone https://github.com/YOUR_USERNAME/MESA_star_explorer.git
cd MESA_star_explorer
```

Create environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install:

```bash
pip install -e .
pip install streamlit
```

## Usage

Launch:

```bash
streamlit run app.py
```

Upload a MESA `history.data` file through the GUI.

## Structure

```
MESA_star_explorer/
├── src/mesa_star_explorer/
│   ├── io.py
│   └── plotting.py
├── tests/
├── examples/
├── app.py
├── pyproject.toml
└── README.md
```

## Planned features

- Multiple-track comparison
- `profile*.data` support
- Evolutionary phase highlighting
- Additional stellar diagnostics
- Plot presets for publication figures

## Author

Pablo Martínez-Miravé  
Postdoctoral Fellow, Niels Bohr Institute, University of Copenhagen

Particle astrophysics • Neutrino astrophysics • Scientific computing
