# Bullet Collector for RC M35A2 Force Truck

This project contains 3D model files for a scale bullet collector (ammo can) accessory designed for the RC M35A2 "Deuce and a Half" military truck.

## Overview

The bullet collector is a 1:16 scale ammo can style container that can be mounted on the truck bed or trailer. It features a removable lid with a handle and latch details, suitable for collecting spent cartridge casings or other small items in a military diorama.

## Design Specifications

- **Scale**: 1:16 (matches RC truck)
- **Dimensions**: 40mm (L) × 30mm (W) × 30mm (H) overall
- **Wall thickness**: 2mm
- **Material**: Designed for FDM printing with PLA or PETG

## Files

### 3D Models
- `bullet_collector_base.stl` – main container body
- `bullet_collector_lid.stl` – removable lid with handle
- `bullet_collector_combined.stl` – assembled view (for visualization only)

### Design Script
- `design_bullet_collector.py` – Python script that generates the STL files using the `trimesh` library

## Printing Instructions

1. **Material**: PLA or PETG recommended.
2. **Layer Height**: 0.2 mm for good detail.
3. **Infill**: 20‑30% for adequate strength.
4. **Supports**: Not required (all parts are self‑supporting).
5. **Orientation**: Print base and lid flat on the build plate (largest face down).
6. **Post‑processing**: Remove any minor stringing; lid may need light sanding for smooth fit.

## Assembly

1. Print one base and one lid.
2. Ensure the lid fits snugly over the base; if too tight, lightly sand the inner lip of the lid.
3. The lid handle is printed as part of the lid; no additional assembly needed.

## Mounting

The bullet collector can be attached to the truck bed using double‑sided tape, small magnets, or scale‑appropriate mounting brackets. It is designed to be a loose accessory, not a permanently fixed part.

## License

This model is licensed under the **Standard Digital File License (SDFL)**. You are free to print, modify, and share the model for personal use. Commercial use requires permission.

## Design Notes

The model was created entirely with Python code using the `trimesh` library. The script (`design_bullet_collector.py`) can be modified to adjust dimensions, wall thickness, or add additional details.

## Previews

*PNG previews could not be automatically generated in the current headless environment. Render the STL files in your preferred viewer to see the model.*

## Changelog

- **2026‑01‑30** – Initial design created.

