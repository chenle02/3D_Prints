# Gemini Context: Lego Robot Home Base Project

This document provides context for the AI agent regarding the `Boda_lego_robot_home_base` project, which is part of a larger 3D printing repository.

## Project Overview
This project is a Python-based procedural generator for a 3D printable "Home Base" (Garage) designed for a Lego robot (specifically Lego set 31164). The project uses the `trimesh` library to programmatically create STL files for the garage structure, base, and door based on defined dimensions and clearances.

## Directory Structure
*   `generate_garage.py`: The core Python script that defines the geometry using CSG (Constructive Solid Geometry) and exports the STL files.
*   `README.md`: Contains design specifications, dimensions, and iterative notes on the design requirements.

## Key Files & Logic

### `generate_garage.py`
This script generates three distinct parts:
1.  **Garage Structure (`garage_structure.stl`)**: The main body comprising the walls and roof. It features vertical slots for the door and is designed to sit on the base.
2.  **Garage Base (`garage_base.stl`)**: The floor of the garage, featuring a ramp and grooves with friction nubs to hold the walls securely.
3.  **Garage Door (`garage_door.stl`)**: A sliding door with windows, designed to fit into the structure's slots.

**Key Parameters (in script):**
*   **Car Dimensions:** 200mm x 80mm x 40mm
*   **Wall Thickness:** 5.0mm
*   **Clearance:** 20.0mm (total internal width/length buffer)
*   **Height Clearance:** 40.0mm

### `README.md`
The README reflects an iterative design process with evolving requirements.
*   **Target Dimensions:** ~10.3 x 7.5 x 1.8 inches.
*   **Design Intent:** A garage with a sliding door, windows, and a connected floor/wall structure (though the script currently separates the base).
*   **Note:** There is a naming discrepancy between the README (e.g., `lego_robot_home_base_roof.stl`) and the actual script output (`garage_structure.stl`). The script's output names are authoritative.

## Usage

### 1. Prerequisites
Ensure Python 3 and `trimesh` are installed:
```bash
pip install trimesh[all] numpy
```

### 2. Generation
To generate the STL files, run the script:
```bash
python3 generate_garage.py
```
This will create `garage_structure.stl`, `garage_base.stl`, and `garage_door.stl` in the current directory.

## Development Conventions
*   **Procedural Design:** Modifications to the model should be made by adjusting parameters or logic in `generate_garage.py`, not by editing the STL files directly.
*   **Units:** All dimensions in the Python script are in **millimeters**.
*   **Orientation:** The script attempts to orient parts for printing (e.g., base flat on Z=0), though slicer auto-orientation is recommended.
