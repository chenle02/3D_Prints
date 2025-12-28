import trimesh
import numpy as np
import os

def create_garage():
    # --- Dimensions (mm) ---
    # Car dimensions (approx 20cm x 8cm x 4cm)
    car_l = 200
    car_w = 80
    car_h = 40

    # Design parameters
    wall_th = 5.0
    clearance = 20.0  # Total internal clearance (width/length)
    height_clearance = 40.0 # Extra height for hand access/door mechanism

    # Internal dimensions
    int_w = car_w + clearance
    int_h = car_h + height_clearance
    int_l = car_l + clearance

    # External dimensions
    ext_w = int_w + 2 * wall_th
    ext_h = int_h + wall_th # Roof only, no floor
    ext_l = int_l + wall_th # Back wall only, front open

    print(f"Generating Garage with External Dimensions: {ext_w}x{ext_l}x{ext_h} mm")

    # --- 1. Garage Body ---
    
    # Create outer solid block
    # Center at origin initially
    outer_box = trimesh.creation.box([ext_w, ext_l, ext_h])
    
    # Position outer box so Z=0 is the bottom (ground)
    # and Back wall is at +Y
    # Y range: [-(ext_l - wall_th/2), wall_th/2] ? No, let's keep it simple.
    # Let's align Back Wall Outer Face to Y = ext_l
    # Front Opening Face to Y = 0
    
    # Re-centering strategy:
    # Outer Box Size: W, L, H
    # We want bounds:
    # X: [-ext_w/2, ext_w/2]
    # Y: [0, ext_l]
    # Z: [0, ext_h]
    outer_box.apply_translation([0, ext_l/2, ext_h/2])

    # Create inner subtraction block (Air)
    # We want to remove material in:
    # X: [-int_w/2, int_w/2]
    # Y: [-infinity, ext_l - wall_th] (Front open, Back closed)
    # Z: [-infinity, int_h] (Bottom open, Top closed)
    
    buffer = 5.0
    
    # Cut dimensions
    cut_w = int_w
    cut_l = (ext_l - wall_th) + buffer # Length from -buffer to (ext_l - wall_th)
    cut_h = int_h + buffer # Height from -buffer to int_h
    
    inner_box = trimesh.creation.box([cut_w, cut_l, cut_h])
    
    # Position inner box
    # X: 0 (Centered)
    # Y: Center of range [-buffer, ext_l - wall_th]
    cut_y_center = (ext_l - wall_th - buffer) / 2
    # Z: Center of range [-buffer, int_h]
    cut_z_center = (int_h - buffer) / 2
    
    inner_box.apply_translation([0, cut_y_center, cut_z_center])

    # Create Door Grooves (Vertical Slots)
    # We want the door to slide down from the top? Or just sit there?
    # "Garage door opens upwards".
    # Simplest meaningful printable mechanism: Vertical slots in the side walls at the front opening.
    # Slot size: 
    door_th = 4.0
    slot_depth = 2.5 # Into the wall
    slot_width = door_th + 1.0 # Tolerance
    
    # Slot location: Just inside the front opening (Y approx 5mm from front?)
    slot_y_pos = 5.0 
    
    left_slot = trimesh.creation.box([slot_depth*2, slot_width, int_h * 2]) # Tall enough to cut through
    # Position Left Slot:
    # X: -int_w/2 - slot_depth/2 + epsilon?
    # We want to cut into the wall at X = -int_w/2.
    # So slot center X = -int_w/2
    left_slot.apply_translation([-int_w/2, slot_y_pos, int_h/2])
    
    right_slot = trimesh.creation.box([slot_depth*2, slot_width, int_h * 2])
    # Position Right Slot: X = int_w/2
    right_slot.apply_translation([int_w/2, slot_y_pos, int_h/2])

    # Top Slot (Cut through the roof to allow door insertion)
    top_slot = trimesh.creation.box([int_w, slot_width, wall_th * 2])
    top_slot.apply_translation([0, slot_y_pos, ext_h])

    # Combine subtractions
    # Garage = Outer - Inner - Slots
    garage = trimesh.boolean.difference([outer_box, inner_box, left_slot, right_slot, top_slot])

    # --- 2. Garage Door ---
    
    # Door dimensions
    # Width: int_w + 2*slot_depth_engagement - tolerance
    # Let's say it engages 2mm into each slot (which is 2.5mm deep).
    # Width = int_w + 4mm - 1mm(tolerance)
    door_print_w = int_w + 3.0
    door_print_h = ext_h + 5.0 # Taller than roof to grab from top
    
    door_panel = trimesh.creation.box([door_print_w, door_th, door_print_h])
    door_panel.apply_translation([0, 0, door_print_h/2])
    
    # Windows
    # "Top half part of the door"
    # Create 3 small windows
    win_w = 12.0
    win_h = 10.0
    win_th = door_th + 10.0
    
    windows = []
    # Z position: Top half. say 75% height
    win_z = door_print_h * 0.75
    
    for x_off in [-door_print_w/4, 0, door_print_w/4]:
        w = trimesh.creation.box([win_w, win_th, win_h])
        w.apply_translation([x_off, 0, win_z])
        windows.append(w)
        
    door_final = trimesh.boolean.difference([door_panel] + windows)

    # --- 3. Garage Base ---
    base_h = 6.0
    groove_depth = 4.0
    tol = 0.2  # Tolerance for fit
    
    # Base Plate
    base_plate = trimesh.creation.box([ext_w, ext_l, base_h])
    base_plate.apply_translation([0, ext_l/2, base_h/2])
    
    # Ramp
    ramp_l = 15.0
    ramp_w = int_w
    ramp_start_h = 1.0
    ramp_end_h = base_h
    
    # Ramp is a convex hull of 8 points
    ramp_pts = np.array([
        [-ramp_w/2, -ramp_l, 0], [ramp_w/2, -ramp_l, 0],
        [ramp_w/2, 0, 0], [-ramp_w/2, 0, 0],
        [-ramp_w/2, -ramp_l, ramp_start_h], [ramp_w/2, -ramp_l, ramp_start_h],
        [ramp_w/2, 0, ramp_end_h], [-ramp_w/2, 0, ramp_end_h]
    ])
    ramp = trimesh.convex.convex_hull(ramp_pts)
    
    # Grooves
    # Cutters need to be taller than groove_depth to ensure clean cut from top
    cut_h_tool = groove_depth * 2 
    cut_z = base_h  # Centered at top surface roughly? No, box center needs to be positioned.
    # If box is centered at Z_c, it spans [Z_c - h/2, Z_c + h/2]
    # We want it to go down to Z = base_h - groove_depth = 2.0
    # Top at Z = 2 + cut_h_tool = 2 + 8 = 10.
    # Center Z = 6.0 (base_h) works if cut_h_tool is large enough?
    # Center at base_h: spans [6-4, 6+4] = [2, 10]. Perfect. Bottom is at 2.0.
    
    # Left Groove
    # Wall center X was -int_w/2 - wall_th/2
    left_groove = trimesh.creation.box([wall_th + tol, ext_l, cut_h_tool])
    left_groove.apply_translation([-int_w/2 - wall_th/2, ext_l/2, base_h])
    
    # Right Groove
    right_groove = trimesh.creation.box([wall_th + tol, ext_l, cut_h_tool])
    right_groove.apply_translation([int_w/2 + wall_th/2, ext_l/2, base_h])
    
    # Back Groove
    # Wall center Y was ext_l - wall_th/2
    # Width should cover the whole back
    back_groove = trimesh.creation.box([ext_w, wall_th + tol, cut_h_tool])
    back_groove.apply_translation([0, ext_l - wall_th/2, base_h])
    
    # Door Groove
    # At slot_y_pos
    door_groove = trimesh.creation.box([door_print_w + tol, door_th + tol, cut_h_tool])
    door_groove.apply_translation([0, slot_y_pos, base_h])
    
    # Friction Nubs (Small bumps inside the groove to click)
    # 4 small spheres protruding into the groove from the inner wall
    nubs = []
    nub_r = 0.6
    # Y positions for nubs
    nub_ys = [ext_l * 0.3, ext_l * 0.7]
    # Height: Middle of the groove (Z=4.0)
    nub_z = base_h - groove_depth/2 
    
    for y in nub_ys:
        # Left side nubs (on inner wall X = -int_w/2, pushing Left)
        # Actually, let's put them on the outer wall pushing In? 
        # Or inner wall pushing Out?
        # Let's put them on the Inner Wall of the groove (X = -int_w/2)
        # Center them slightly inside the groove so they protrude
        # Groove is from X = -int_w/2 - wall_th to -int_w/2
        # Nub at -int_w/2. Radius 0.6. Protrudes 0.6 into groove? That's a lot.
        # Let's center at -int_w/2 + 0.3? No, -int_w/2 is the edge.
        # -int_w/2 is the Right edge of the Left Wall.
        # So we want nub at -int_w/2. It sticks 0.6 into the garage (bad) and 0.6 into the wall (good).
        # Wait, the wall is SOLID. The groove is AIR.
        # The base has material at X > -int_w/2 (Floor).
        # So if we put a sphere at X = -int_w/2, half is in the floor, half is in the groove.
        # Result: A bump sticking into the groove. Perfect.
        
        # Left Nubs
        n1 = trimesh.creation.icosphere(radius=nub_r)
        n1.apply_translation([-int_w/2, y, nub_z])
        nubs.append(n1)
        
        # Right Nubs (Mirror)
        n2 = trimesh.creation.icosphere(radius=nub_r)
        n2.apply_translation([int_w/2, y, nub_z])
        nubs.append(n2)
        
    # Combine
    # Base = (Plate + Ramp) - Grooves + Nubs
    # Note: Union Nubs with Plate first, then Subtract Grooves?
    # No, Nubs must protrude INTO the Groove.
    # If we Subtract Groove from Plate, we get a hole.
    # Then we Union Nubs. The Nubs will fill part of that hole.
    # Correct.
    
    base_solid = trimesh.boolean.union([base_plate, ramp] + nubs)
    base_final = trimesh.boolean.difference([base_solid, left_groove, right_groove, back_groove, door_groove])

    # --- 4. Export ---
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    garage_path = os.path.join(output_dir, 'garage_structure.stl')
    door_path = os.path.join(output_dir, 'garage_door.stl')
    base_path = os.path.join(output_dir, 'garage_base.stl')
    
    print(f"Exporting to {garage_path}...")
    garage.export(garage_path)
    
    print(f"Exporting to {door_path}...")
    door_final.export(door_path)
    
    print(f"Exporting to {base_path}...")
    base_final.export(base_path)
    print("Done.")

if __name__ == "__main__":
    create_garage()
