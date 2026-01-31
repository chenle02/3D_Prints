#!/usr/bin/env python3
"""
Advanced bullet collector design with functional latches and mounting system.
Creates a scale ammo can with swing latches, lid catches, and truck mounting points.
"""

import trimesh
import numpy as np
import os


def create_ammo_can_base(length=40.0, width=30.0, height=25.0, wall_thickness=2.0):
    """
    Create the base of the ammo can with mounting points and latch pin holes.
    """
    # Outer box
    outer = trimesh.creation.box([length, width, height])
    # Inner hollow (subtract smaller box)
    inner_length = length - 2 * wall_thickness
    inner_width = width - 2 * wall_thickness
    inner_height = height - wall_thickness  # bottom thickness
    inner = trimesh.creation.box([inner_length, inner_width, inner_height])
    inner.apply_translation([0, 0, wall_thickness])
    base = outer.difference(inner)
    return base


def create_latch_pin_hole(base, position, pin_diameter=1.5, pin_length=4.0):
    """
    Create a cylindrical hole for latch pivot pin.
    """
    # Create pin cylinder (horizontal along X axis)
    pin = trimesh.creation.cylinder(radius=pin_diameter / 2, height=pin_length)
    pin.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    pin.apply_translation(position)
    # Subtract pin from base to create hole
    base = base.difference(pin)
    return base


def create_swing_latch(
    length=12.0, width=4.0, thickness=2.0, pin_diameter=1.5, pin_length=4.0
):
    """
    Create a swing latch that rotates on a pin.
    Returns latch body and separate pin.
    """
    # Latch body (main rectangular part)
    body = trimesh.creation.box([length, width, thickness])

    # Create pin hole in latch
    pin_hole = trimesh.creation.cylinder(radius=pin_diameter / 2, height=width + 0.2)
    pin_hole.apply_transform(
        trimesh.transformations.rotation_matrix(np.pi / 2, [0, 0, 1])
    )
    pin_hole.apply_translation([-length / 2 + 2, 0, 0])
    body = body.difference(pin_hole)

    # Create catch tab at end
    catch = trimesh.creation.box([3, width, 4])
    catch.apply_translation([length / 2 - 1.5, 0, 2])
    body = body.union(catch)

    # Create separate pin
    pin = trimesh.creation.cylinder(radius=pin_diameter / 2, height=pin_length)
    pin.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 0, 1]))

    return body, pin


def create_lid_with_catches(length=40.0, width=30.0, lid_height=5.0, lip_height=3.0):
    """
    Create lid with lip and catch notches for latches.
    """
    # Main lid plate
    lid = trimesh.creation.box([length, width, lid_height])

    # Inner lip
    lip_length = length - 4.0
    lip_width = width - 4.0
    lip = trimesh.creation.box([lip_length, lip_width, lip_height])
    lip.apply_translation([0, 0, -lid_height / 2 + lip_height / 2])
    lid = lid.union(lip)

    # Create catch notches on sides for latches
    notch_depth = 2.0
    notch_height = 3.0
    notch_width = 6.0

    # Right side notch
    right_notch = trimesh.creation.box([notch_depth, notch_width, notch_height])
    right_notch.apply_translation(
        [length / 2 - notch_depth / 2, 0, lid_height / 2 - notch_height / 2]
    )
    lid = lid.difference(right_notch)

    # Left side notch
    left_notch = trimesh.creation.box([notch_depth, notch_width, notch_height])
    left_notch.apply_translation(
        [-length / 2 + notch_depth / 2, 0, lid_height / 2 - notch_height / 2]
    )
    lid = lid.difference(left_notch)

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


def add_mounting_points(base, length=40.0, width=30.0, height=25.0):
    """
    Add mounting tabs to bottom of base for truck attachment.
    """
    tab_length = 8.0
    tab_width = 6.0
    tab_height = 3.0

    # Front mounting tab
    front_tab = trimesh.creation.box([tab_length, tab_width, tab_height])
    front_tab.apply_translation(
        [0, -width / 2 + tab_width / 2, -height / 2 + tab_height / 2]
    )

    # Rear mounting tab
    rear_tab = trimesh.creation.box([tab_length, tab_width, tab_height])
    rear_tab.apply_translation(
        [0, width / 2 - tab_width / 2, -height / 2 + tab_height / 2]
    )

    # Add screw holes to tabs
    screw_hole = trimesh.creation.cylinder(radius=1.0, height=tab_height + 0.2)

    front_hole = screw_hole.copy()
    front_hole.apply_translation([0, -width / 2 + tab_width / 2, -height / 2])

    rear_hole = screw_hole.copy()
    rear_hole.apply_translation([0, width / 2 - tab_width / 2, -height / 2])

    # Create tabs with holes
    front_tab = front_tab.difference(front_hole)
    rear_tab = rear_tab.difference(rear_hole)

    # Attach tabs to base
    base = base.union(front_tab)
    base = base.union(rear_tab)

    return base


def main():
    print("Designing ADVANCED bullet collector with functional mechanisms")

    # Dimensions (mm) - same as original for compatibility
    base_length = 40.0
    base_width = 30.0
    base_height = 25.0
    wall_thickness = 2.0

    print("Creating base with mounting points...")
    base = create_ammo_can_base(base_length, base_width, base_height, wall_thickness)

    print("Adding latch pin holes...")
    # Pin positions on side walls near top
    right_pin_pos = [base_length / 2 - 4, base_width / 2, base_height / 2 - 2]
    left_pin_pos = [-base_length / 2 + 4, base_width / 2, base_height / 2 - 2]

    base = create_latch_pin_hole(base, right_pin_pos)
    base = create_latch_pin_hole(base, left_pin_pos)

    print("Adding mounting points for truck...")
    base = add_mounting_points(base, base_length, base_width, base_height)

    print("Creating swing latches...")
    right_latch, right_pin = create_swing_latch()
    left_latch, left_pin = create_swing_latch()

    # Position latches
    right_latch.apply_translation(
        [base_length / 2 - 4, base_width / 2 - 2, base_height / 2 - 2]
    )
    left_latch.apply_translation(
        [-base_length / 2 + 4, base_width / 2 - 2, base_height / 2 - 2]
    )

    # Position pins
    right_pin.apply_translation(
        [base_length / 2 - 4, base_width / 2, base_height / 2 - 2]
    )
    left_pin.apply_translation(
        [-base_length / 2 + 4, base_width / 2, base_height / 2 - 2]
    )

    print("Creating lid with catch notches...")
    lid = create_lid_with_catches(base_length, base_width, lid_height=5.0)

    print("Creating handle...")
    handle = create_handle(length=base_length - 10)
    handle.apply_translation([0, 0, 5.0])
    lid_with_handle = lid.union(handle)

    # Export all parts
    output_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"\nExporting parts to {output_dir}:")

    # Base assembly (base alone)
    base_stl = os.path.join(output_dir, "advanced_base.stl")
    base.export(base_stl)
    print(f"  Base: {base_stl}")

    # Lid assembly
    lid_stl = os.path.join(output_dir, "advanced_lid.stl")
    lid_with_handle.export(lid_stl)
    print(f"  Lid: {lid_stl}")

    # Latches (right and left)
    right_latch_stl = os.path.join(output_dir, "advanced_latch_right.stl")
    right_latch.export(right_latch_stl)
    print(f"  Right latch: {right_latch_stl}")

    left_latch_stl = os.path.join(output_dir, "advanced_latch_left.stl")
    left_latch.export(left_latch_stl)
    print(f"  Left latch: {left_latch_stl}")

    # Pins
    right_pin_stl = os.path.join(output_dir, "advanced_pin_right.stl")
    right_pin.export(right_pin_stl)
    print(f"  Right pin: {right_pin_stl}")

    left_pin_stl = os.path.join(output_dir, "advanced_pin_left.stl")
    left_pin.export(left_pin_stl)
    print(f"  Left pin: {left_pin_stl}")

    # Combined assembly for visualization
    combined = trimesh.util.concatenate(
        [base, lid_with_handle, right_latch, left_latch, right_pin, left_pin]
    )
    combined_stl = os.path.join(output_dir, "advanced_combined.stl")
    combined.export(combined_stl)
    print(f"  Combined assembly: {combined_stl}")

    print("\nDesign complete!")
    print("\nAssembly instructions:")
    print("1. Print all parts")
    print("2. Insert pins through base holes and latch holes")
    print("3. Latches swing to secure lid catch notches")
    print("4. Use screws through mounting tabs to attach to truck")


if __name__ == "__main__":
    main()
