# Gemini Context: 3D Printing Projects Repository

This document provides context for the AI agent regarding the structure, purpose, and workflows of this 3D printing project repository.

## Project Overview
This repository serves as a curated collection of personal 3D printing projects, gifts, and designs. It is a non-code project in the traditional sense, focusing on 3D models (`.stl`, `.3mf`) and documentation, but it includes Python automation for maintenance.

## Directory Structure
Projects are organized chronologically and by event/name.

*   **Root:** Contains global configuration, top-level documentation, and helper scripts.
*   **Project Folders:** Follow the naming convention `YYYYMM_ProjectName` (e.g., `202502_Valentine_gifts`).
    *   Contain source files (`.3mf`).
    *   Contain export files (`.stl`, `.zip` archives).
    *   Contain generated previews (`.png`).
    *   Contain project-specific `README.md`.

## Key Files
*   `README.md`: The main entry point, listing all projects with descriptions and paths.
*   `requirements.txt`: Python dependencies for the automation scripts (primarily `trimesh`).
*   `.codex/Instructions.md`: Detailed guidelines for adding new projects and maintaining the repository structure.
*   `scripts/generate_stl_previews.py`: A utility script that:
    1.  Generates `.png` previews for any `.stl` files that lack them or are outdated.
    2.  Automatically updates the `README.md` in each project subfolder to include a "Previews" section displaying these images.
*   `scripts/install_hooks.sh`: Script to set up git hooks (optional).

## Development & Usage

### 1. Environment Setup
The project uses Python for automation.
```bash
pip3 install -r requirements.txt
```

### 2. Automation
To generate missing previews and update project READMEs:
```bash
python3 scripts/generate_stl_previews.py
```

### 3. Adding a New Project
1.  **Create Folder:** Create a new directory named `YYYYMM_<ProjectName>`.
2.  **Add Files:** Place `.3mf` (source) and `.stl` (printable) files inside.
3.  **Documentation:** Create a `README.md` in the new folder.
4.  **Register:** Update the root `README.md` to include the new project under the "Projects" section.
5.  **Previews:** Run the preview generator script to create images and update the project's README.

## Conventions
*   **Dates:** Use `YYYYMM` prefix for folders.
*   **Files:** Prefer `.3mf` for project files (preserving settings/parts) and `.stl` for raw geometry.
*   **Docs:** Every project must have a `README.md`.
