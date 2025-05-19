 # Codex CLI Instructions

 This repository stores 3D modeling projects. Each project is organized in its own subfolder containing model files and documentation.

 ## Repository Structure

- `202505_Tool_Organizer/`: First project—goody bag (tool organizer) for Kailai's birthday.
- `202502_Valentine_gifts/`: Second project—personalized phone stands as Valentine’s gifts.
- `202502_Zhihe_Gift/`: Third project—custom gift box for Zhihe Wu’s 6th birthday.

 ## Guidelines

 - When adding a new 3D modeling project:
   - Create a new subfolder named with the pattern `YYYYMM_<ProjectName>`, where `YYYYMM` is the year and month prefix (e.g., `202505_Tool_Organizer`).
   - Place source files (.3mf) and export files (.stl, archives) inside.
   - Add a `README.md` in the project folder describing the design, listing files, and providing printing instructions.
   - Update the top-level `README.md` to include the new project.

 ## Workflow

 1. Commit model files and documentation.
 2. Use Git LFS for large binary files if necessary.
 3. Tag releases for distribution.