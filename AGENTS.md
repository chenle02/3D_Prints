# AGENTS.md - 3D Printing Projects Repository

This document provides guidelines for agentic coding agents working in this 3D printing projects repository. It covers repository structure, automation commands, coding standards, and workflows.

## Repository Overview

This is a curated collection of personal 3D printing projects, gifts, and designs. While primarily focused on 3D models (`.stl`, `.3mf`) and documentation, it includes Python automation scripts for maintenance tasks.

**Key Characteristics:**
- Non-traditional codebase: 3D modeling files + documentation + automation scripts
- Chronologically organized project folders with `YYYYMM_ProjectName` naming convention
- Python environment for automation (trimesh, etc.)
- Git hooks for automatic preview generation

## Project Structure

```
.
├── README.md, GEMINI.md, requirements.txt
├── .codex/Instructions.md
├── scripts/ (generate_stl_previews.py, install_hooks.sh)
├── .githooks/ (pre-commit hook)
├── .gitignore
└── YYYYMM_ProjectName/ (*.3mf, *.stl, *.png, README.md)
```

**Folder Naming Convention:**
  - Use `YYYYMM_ProjectName` format (e.g., `202502_Valentine_gifts`)
  - Year-month prefix indicates project creation timeline
  - Project name should be descriptive, using underscores for spaces

**File Conventions:**
  - **Source files:** Use `.3mf` for PrusaSlicer project files (preserves settings, parts, etc.)
  - **Export files:** Use `.stl` for raw geometry (printable)
  - **Previews:** `.png` images auto-generated from STL files
  - **Documentation:** Each project folder must have a `README.md`

## Build & Automation Commands

### Environment Setup
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Optional: Set up Git hooks for automatic preview generation
scripts/install_hooks.sh
```

### Preview Generation
```bash
# Generate missing PNG previews for STL files and update project READMEs
# Run from repository root - processes all project folders
python3 scripts/generate_stl_previews.py
```

### Git Hooks
- **Pre-commit hook:** Automatically runs `generate_stl_previews.py` on STL file changes
- Hook ensures PNG previews are up-to-date before commit
- Hook updates project READMEs with preview sections

### Testing Commands
*No formal testing framework is currently configured.* If tests are added:
- Run all tests: `python -m pytest tests/`
- Run a single test: `python -m pytest tests/test_preview_generation.py::test_specific_function`
- Run with coverage: `python -m pytest --cov=scripts tests/`

## Code Style Guidelines

### Python Scripts
- Follow **PEP 8** conventions (4-space indentation, 88 character line length)
- Use **double quotes** for docstrings, **single quotes** for strings
- Import order: standard library → third-party → local modules
- Use type hints where practical (Python 3.9+)
- Use `snake_case` for variables and functions, `CamelCase` for classes
- Use try-except blocks with specific exception types for error handling
- Log errors with descriptive messages; avoid silent failures

### Markdown Documentation
- Use ATX-style headers (`#`, `##`, etc.)
- Use relative links for local files
- Include alt text for images: `![Description](path/to/image.png)`
- Keep lines under 100 characters for readability
- Use bullet lists with `-` for unordered items
- Use code fences with language specification

### 3D Modeling Files
- **Naming:** Use descriptive names with underscores (e.g., `phone_stand_base.stl`)
- **Organization:** Group related parts in subdirectories within project folders
- **Versioning:** Consider adding version suffixes for iterative designs (e.g., `v2`, `final`)

## Git & Collaboration

### Commit Guidelines
- Use descriptive commit messages in imperative mood
- Scope commits to a single project or logical change
- Include references to issues or design decisions when applicable
- Follow conventional commit format (optional):
  ```
  feat: add new project 202502_Valentine_gifts
  fix: correct dimensions in truck_trailer.stl
  docs: update README with printing instructions
  ```

### Branch Strategy
- `main` branch contains stable, reviewed projects
- Feature branches for new projects or major changes: `feature/YYYYMM_ProjectName`
- Hotfix branches for urgent corrections: `hotfix/brief-description`

### Adding New Projects
1. **Create folder:** `mkdir YYYYMM_ProjectName`
2. **Add source files:** Place `.3mf` and `.stl` files in the folder
3. **Create README:** Include project description, printing instructions, and design notes
4. **Update root README:** Add project to the "Projects" section in `/README.md`
5. **Generate previews:** Run `python3 scripts/generate_stl_previews.py`
6. **Commit changes:** Stage all new files and commit with descriptive message

## Linting & Formatting

### Python
No linter configuration is currently present. If linting is needed, consider installing `black` (code formatting) and `flake8` (style checking). Type hints can be checked with `mypy`.

### Markdown
- Use consistent header hierarchy
- Check for broken links
- Keep line length under 100 characters

### Pre-commit Hooks
Consider adding automated linting via pre-commit hooks. Example configuration files can be added to the repository root.

## Agent-Specific Instructions

### Guidelines for Agents
- **Check existing patterns:** Look at similar projects for naming and structure
- **Follow chronological naming:** New projects must use `YYYYMM_` prefix  
- **Update documentation:** Both project README and root README need updates
- **Generate previews:** Ensure PNG previews exist for all STL files
- **Respect file conventions:** Use `.3mf` for source, `.stl` for exports
- **Adding new models:** Place in appropriate project folder, update README, generate preview
- **Modifying scripts:** Ensure backward compatibility, test with existing projects
- **Fixing bugs:** Verify preview generation still works after changes
- **Improving docs:** Keep README files concise but informative

### Troubleshooting
- **Preview generation fails:** Check trimesh installation, STL file integrity
- **Git hooks not running:** Verify `core.hooksPath` configuration
- **Import errors:** Ensure virtual environment is activated and dependencies installed
## References
- [.codex/Instructions.md](.codex/Instructions.md) - Detailed project addition guidelines
- [GEMINI.md](GEMINI.md) - AI agent context documentation
- [README.md](README.md) - Main repository overview
- [PrusaSlicer Documentation](https://help.prusa3d.com/article/prusaslicer-overview_2259) - For .3mf file format

---

*This document should be updated as the repository evolves. Last updated: 2025-01-30*