#!/usr/bin/env python3
"""
Design script for bullet collector accessory for RC M35A2 truck.
Creates a scale ammo can style bullet collector with separate lid.
"""

import trimesh
import numpy as np
import os


def create_ammo_can_base(length=40.0, width=30.0, height=25.0, wall_thickness=2.0):
    """
    Create the base of the ammo can (container).
    Returns a trimesh.Trimesh object.
    """
    outer = trimesh.creation.box([length, width, height])
    inner_length = length - 2 * wall_thickness
    inner_width = width - 2 * wall_thickness
    inner_height = height - wall_thickness  # bottom thickness
    inner = trimesh.creation.box([inner_length, inner_width, inner_height])
    inner.apply_translation([0, 0, wall_thickness])
    base = outer.difference(inner)
    return base


def create_ammo_can_lid(length=40.0, width=30.0, lid_height=5.0, lip_height=3.0):
    """
    Create lid that fits over the base.
    """
    lid = trimesh.creation.box([length, width, lid_height])
    lip_length = length - 4.0  # small gap
    lip_width = width - 4.0
    lip = trimesh.creation.box([lip_length, lip_width, lip_height])
    lip.apply_translation([0, 0, -lid_height / 2 + lip_height / 2])
    lid = lid.union(lip)
    return lid


def create_handle(length=30.0, diameter=3.0):
    """
    Create a handle for the lid.
    """
    post_height = 10.0
    post = trimesh.creation.cylinder(radius=diameter / 2, height=post_height)
    post1 = post.copy()
    post2 = post.copy()
    post1.apply_translation([-length / 2, 0, 0])
    post2.apply_translation([length / 2, 0, 0])
    bar = trimesh.creation.cylinder(radius=diameter / 2, height=length)
    bar.apply_translation([0, 0, post_height / 2])
    bar.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    handle = trimesh.util.concatenate([post1, post2, bar])
    return handle


def add_latch(base, position):
    """Add a simple latch detail."""
    latch = trimesh.creation.box([8, 4, 2])
    latch.apply_translation(position)
    return base.union(latch)


def main():
    print("Designing bullet collector (ammo can) at 1:16 scale")

    base_length = 40.0
    base_width = 30.0
    base_height = 25.0
    wall_thickness = 2.0

    print("Creating base...")
    base = create_ammo_can_base(base_length, base_width, base_height, wall_thickness)

    print("Creating lid...")
    lid = create_ammo_can_lid(base_length, base_width, lid_height=5.0)

    print("Creating handle...")
    handle = create_handle(length=base_length - 10)
    handle.apply_translation([0, 0, 5.0])

    lid_with_handle = lid.union(handle)

    print("Adding latches...")
    latch_pos1 = [base_length / 2 - 5, base_width / 2, base_height - 2]
    latch_pos2 = [-base_length / 2 + 5, base_width / 2, base_height - 2]
    base = add_latch(base, latch_pos1)
    base = add_latch(base, latch_pos2)

    output_dir = os.path.dirname(os.path.abspath(__file__))
    base_stl = os.path.join(output_dir, "bullet_collector_base.stl")
    lid_stl = os.path.join(output_dir, "bullet_collector_lid.stl")

    print(f"Exporting base to {base_stl}")
    base.export(base_stl)
    print(f"Exporting lid to {lid_stl}")
    lid_with_handle.export(lid_stl)

    combined = trimesh.util.concatenate([base, lid_with_handle])
    combined_stl = os.path.join(output_dir, "bullet_collector_combined.stl")
    combined.export(combined_stl)
    print(f"Exported combined model to {combined_stl}")

    print("Design complete.")


if __name__ == "__main__":
    main()
