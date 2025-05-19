#!/usr/bin/env python3
"""
Generate missing PNG previews for STL files in the repository.
"""
import os
import trimesh

def generate_previews(root_dir='.'):
    """
    Generate PNG previews for STL files, then update README.md in each folder containing PNGs.
    """
    # First, generate or update PNG previews
    for root, _, files in os.walk(root_dir):
        for filename in files:
            if not filename.lower().endswith('.stl'):
                continue
            stl_path = os.path.join(root, filename)
            png_name = os.path.splitext(filename)[0] + '.png'
            png_path = os.path.join(root, png_name)
            # Determine if regeneration is needed
            regenerate = True
            if os.path.exists(png_path):
                try:
                    stl_mtime = os.path.getmtime(stl_path)
                    png_mtime = os.path.getmtime(png_path)
                    if png_mtime >= stl_mtime:
                        regenerate = False
                except OSError:
                    regenerate = True
            if not regenerate:
                continue
            try:
                mesh = trimesh.load(stl_path)
                from trimesh import Scene
                if isinstance(mesh, Scene):
                    scene = mesh
                elif hasattr(mesh, 'scene'):
                    scene = mesh.scene()
                else:
                    scene = Scene(mesh)
                png = scene.save_image(resolution=[800, 600])
                if png:
                    with open(png_path, 'wb') as f:
                        f.write(png)
                    print(f"Generated preview: {png_path}")
                else:
                    print(f"Warning: could not render preview for {stl_path}")
            except Exception as e:
                print(f"Error generating preview for {stl_path}: {e}")

    # Then, update README.md in any subdirectory containing PNGs
    base_dir = os.path.abspath(root_dir)
    def update_readme(dirpath, png_files):
        readme_path = os.path.join(dirpath, 'README.md')
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                lines = f.read().splitlines()
        else:
            # start new README with title
            title = os.path.basename(dirpath)
            lines = [f"# {title}", ""]
        # remove existing Previews section
        new_lines = []
        in_previews = False
        for line in lines:
            if line.strip().startswith('## Previews'):
                in_previews = True
                continue
            if in_previews:
                if line.startswith('## '):
                    in_previews = False
                    new_lines.append(line)
                # else skip preview lines
                continue
            new_lines.append(line)
        # ensure blank line before new section
        if new_lines and new_lines[-1].strip() != '':
            new_lines.append('')
        # append previews
        new_lines.append('## Previews')
        new_lines.append('')
        for png in png_files:
            new_lines.append(f"![{png}]({png})")
        new_lines.append('')
        # write back
        with open(readme_path, 'w') as f:
            f.write("\n".join(new_lines))

    for root, _, files in os.walk(root_dir):
        # skip top-level folder
        if os.path.abspath(root) == base_dir:
            continue
        pngs = [f for f in files if f.lower().endswith('.png')]
        if pngs:
            update_readme(root, sorted(pngs))

if __name__ == '__main__':
    generate_previews()