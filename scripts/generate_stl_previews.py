#!/usr/bin/env python3
"""
Generate missing PNG previews for STL files in the repository.
"""
import os
import trimesh

def generate_previews(root_dir='.'):
    for root, _, files in os.walk(root_dir):
        for filename in files:
            if filename.lower().endswith('.stl'):
                stl_path = os.path.join(root, filename)
                png_name = os.path.splitext(filename)[0] + '.png'
                png_path = os.path.join(root, png_name)
                # Only generate if PNG is missing or outdated
                if os.path.exists(png_path):
                    try:
                        stl_mtime = os.path.getmtime(stl_path)
                        png_mtime = os.path.getmtime(png_path)
                        # skip if PNG is newer than or same as STL
                        if png_mtime >= stl_mtime:
                            continue
                    except OSError:
                        # if any issue reading mtimes, regenerate
                        pass
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

if __name__ == '__main__':
    generate_previews()