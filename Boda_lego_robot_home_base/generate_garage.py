import trimesh
import numpy as np
import os

def create_garage():
    # --- Dimensions (mm) ---
    # Robot Dimensions from README: 10.3 x 7.5 x 1.8 inches -> 262 x 191 x 46 mm
    robot_l = 262.0
    robot_w = 191.0
    robot_h = 46.0

    # Clearances (mm)
    # "2cm on each of four sides, and 4cm on the top" -> REDUCED SIDE CLEARANCE to 10mm (User request: too wide)
    clearance_side = 10.0
    clearance_top = 40.0
    
    wall_th = 5.0

    # Internal Dimensions
    # Length: Robot L + Front Clearance + Back Clearance
    int_l = robot_l + clearance_side + clearance_side
    # Width: Robot W + Left Clearance + Right Clearance
    int_w = robot_w + clearance_side + clearance_side
    # Height: Robot H + Top Clearance
    int_h = robot_h + clearance_top

    # External Dimensions
    # Width: Int W + 2 walls
    ext_w = int_w + 2 * wall_th
    # Length: Int L + Back wall (Front is open/door)
    # Wait, if we want a floor, we need the floor to cover the whole length.
    # If the door is at the front, the external length includes the back wall thickness.
    ext_l = int_l + wall_th 
    # Height: Int H + Roof + Floor
    ext_h = int_h + wall_th + wall_th # Roof (5mm) + Floor (5mm)

    print(f"Robot Dimensions: {robot_l}x{robot_w}x{robot_h} mm")
    print(f"Internal Dimensions: {int_w}x{int_l}x{int_h} mm")
    print(f"External Dimensions: {ext_w}x{ext_l}x{ext_h} mm")

    # --- 1. Main Body (Roof + Walls + Floor) ---
    
    # Create the solid block
    main_box = trimesh.creation.box([ext_w, ext_l, ext_h])
    
    # Alignments
    # We want the floor bottom at Z=0.
    # We want the Front Face at Y=0.
    # We want the Back Wall at Y=ext_l.
    # Center X at 0.
    
    # Currently centered at 0,0,0.
    # Shift Z up by ext_h/2
    # Shift Y... Box Y length is ext_l.
    # To have front at Y=0, we need center at Y=ext_l/2.
    main_box.apply_translation([0, ext_l/2, ext_h/2])

    # Create the internal cutout (The Room)
    # Dimensions: int_w, int_l, int_h
    # Position:
    # X: 0
    # Y: Starts at 0 (Front), ends at int_l. 
    #    The Back Wall is at Y > int_l.
    #    Back wall thickness starts at int_l.
    #    So cutout Y range: [0, int_l].
    #    Center Y = int_l / 2.
    # Z: Starts above floor (wall_th).
    #    Z range: [wall_th, wall_th + int_h].
    #    Center Z = wall_th + int_h / 2.
    
    # To ensure clean cuts at the front face, we add a buffer to the front Y.
    buffer = 10.0
    
    cutout_w = int_w
    cutout_l = int_l + buffer
    cutout_h = int_h
    
    room_cutout = trimesh.creation.box([cutout_w, cutout_l, cutout_h])
    
    # Position Cutout
    # Y Center: We want it to span [-buffer, int_l].
    # Center = (-buffer + int_l) / 2
    room_y_center = (int_l - buffer) / 2
    # Z Center
    room_z_center = wall_th + int_h / 2
    
    room_cutout.apply_translation([0, room_y_center, room_z_center])

    # --- Door Mechanism (Sliding Sideways) ---
    # "Front door opens like by side ways from the right side"
    # We'll create a slot in the RIGHT wall (X > 0) for the door to slide through.
    # And grooves in the Floor and Roof near the front.
    
    door_th = 4.0
    door_groove_depth = 2.5 # How deep into floor/roof
    door_pos_y = 10.0 # Distance from front face
    
    # Door Slot in Right Wall
    # Needs to be slightly wider than door thickness and tall enough.
    # Slot Height: int_h (full height of opening)
    # Slot Width: door_th + tolerance
    slot_tol = 1.0
    wall_slot_w = door_th + slot_tol
    wall_slot_h = int_h # Cut through the wall fully in Z? No, keep structural integrity if possible?
    # If we cut fully, the front pillar of the right wall separates.
    # Usually better to make a "tunnel" through the wall.
    # But for printing, a full cut is often cleaner if supported.
    # Let's make a tunnel (leaving a bridge at top and bottom? No, floor/roof handles that).
    
    # Slot Cutout Object
    # Long enough to go through the wall (wall_th).
    # Width (Y axis in this context? No, slot is along X axis? No, slot allows X movement).
    # The slot is a hole in the Y-Z plane of the wall?
    # No, the Right Wall is in the Y-Z plane.
    # We want a hole through it.
    # Dimensions: 
    # X: wall_th + buffer (to cut through)
    # Y: wall_slot_w (Thickness of door)
    # Z: wall_slot_h (Height of door passage)
    
    # Wait, the door is a panel in the X-Z plane (when closed).
    # It slides along X.
    # So it needs to pass through the Right Wall.
    # Right Wall is at X = int_w/2 to ext_w/2.
    # We need a cut there.
    # Cut Size:
    # X: wall_th * 2 (big enough)
    # Y: wall_slot_w
    # Z: wall_slot_h + 2*clearance?
    # Actually, the door needs to slide in grooves.
    # Grooves are in Floor and Roof.
    # The Slot in the Wall connects these grooves.
    
    # 1. Floor/Roof Grooves (spanning full width to allow sliding)
    # We need the groove to go from Left Wall (stopper) through Right Wall (exit).
    # Groove Length (X): From -int_w/2 to +ext_w/2 + extra (for door to stick out?)
    # Let's just cut through the Right Wall entirely.
    groove_len = ext_w # Full width
    groove_w = door_th + slot_tol
    groove_d = door_groove_depth
    
    # Floor Groove
    floor_groove = trimesh.creation.box([groove_len, groove_w, groove_d * 2]) # *2 for clean cut
    # Position:
    # X: 0 (Center)
    # Y: door_pos_y
    # Z: wall_th (Floor surface) - groove_d/2? No, we want to cut DOWN from wall_th.
    # Center at Z = wall_th.
    floor_groove.apply_translation([0, door_pos_y, wall_th])

    # Roof Groove
    roof_groove = trimesh.creation.box([groove_len, groove_w, groove_d * 2])
    # Position:
    # X: 0
    # Y: door_pos_y
    # Z: wall_th + int_h (Ceiling surface). We want to cut UP into roof.
    # Center at Z = wall_th + int_h.
    roof_groove.apply_translation([0, door_pos_y, wall_th + int_h])

    # Wall Pass-through Slot (Right Wall)
    # This clears the material between floor and roof in the right wall.
    # X Position: Right Wall Center = int_w/2 + wall_th/2
    # Y Position: door_pos_y
    # Z Position: Center of room height
    wall_pass = trimesh.creation.box([wall_th * 2, groove_w, int_h])
    wall_pass.apply_translation([int_w/2 + wall_th/2, door_pos_y, wall_th + int_h/2])

    # --- Windows ---
    # "3 windows on the door. Same for the walls."
    # We'll put 3 windows on the Left Wall and 3 on the Right Wall.
    # (The Right Wall has the door slot, but there is plenty of length behind it).
    
    win_w = 30.0
    win_h = 20.0
    win_depth = wall_th * 3 # To cut through
    
    # Window Spacing
    # Wall Length = ext_l. Room Length = int_l.
    # Distribute 3 windows along Y axis in the room area.
    # Range: Y=[0, int_l]
    # Positions: 25%, 50%, 75%
    win_y_positions = [int_l * 0.25, int_l * 0.50, int_l * 0.75]
    # Height: "Top half part".
    win_z_pos = wall_th + int_h * 0.75
    
    wall_windows = []
    
    for y in win_y_positions:
        # Left Wall Window
        # X: -ext_w/2
        wl = trimesh.creation.box([win_depth, win_w, win_h]) # Note: win_w is length along Y here
        wl.apply_translation([-ext_w/2, y, win_z_pos])
        wall_windows.append(wl)
        
        # Right Wall Window
        # X: ext_w/2
        wr = trimesh.creation.box([win_depth, win_w, win_h])
        wr.apply_translation([ext_w/2, y, win_z_pos])
        wall_windows.append(wr)

    # --- Boolean Operations for Body ---
    cutters = [room_cutout, floor_groove, roof_groove, wall_pass] + wall_windows
    main_body = trimesh.boolean.difference([main_box] + cutters)

    # --- SPLIT FOR PRINTER (256mm limit) ---
    # The total length (ext_l) is ~307mm, which exceeds 256mm.
    # We must split the body into Front and Back parts.
    print(f"Total Length {ext_l:.1f}mm > 256mm. Splitting model into Front and Back parts.")
    
    split_y = ext_l / 2
    
    # Create cutting masks
    # Front Mask: Covers Y from -inf to split_y
    # Back Mask: Covers Y from split_y to +inf
    # Size needs to be large enough to cover the whole object
    mask_size = 1000.0
    
    # Front Part: Intersect with a box from Y = -500 to split_y
    # Center Y of this box: split_y - mask_size/2
    front_mask = trimesh.creation.box([mask_size, mask_size, mask_size])
    front_mask.apply_translation([0, split_y - mask_size/2, 0])
    
    # Back Part: Intersect with a box from Y = split_y to +500
    # Center Y of this box: split_y + mask_size/2
    back_mask = trimesh.creation.box([mask_size, mask_size, mask_size])
    back_mask.apply_translation([0, split_y + mask_size/2, 0])
    
    # Perform Split
    # Using intersection is cleaner than difference for splitting usually
    garage_front = trimesh.boolean.intersection([main_body, front_mask])
    garage_back = trimesh.boolean.intersection([main_body, back_mask])

    # --- 2. Garage Door ---
    # Dimensions:
    # Width: Must cover the opening (int_w) + some overlap?
    # Actually, it slides. It needs to be wider than the opening to not fall out?
    # Let's make it int_w + 10mm overlap on left (stopper side).
    # And tall enough to ride in grooves.
    # Height: int_h + 2*groove_depth - tolerance
    door_h_total = int_h + 2 * door_groove_depth - 1.0 # 1mm vertical play
    door_w_total = int_w + 10.0 
    
    door_panel = trimesh.creation.box([door_w_total, door_th, door_h_total])
    # Center at origin for export
    
    # Windows on Door
    # 3 Windows. "Top half".
    # Distributed along X.
    door_win_y_size = 10.0 # Height of window
    door_win_x_size = 30.0 # Width of window
    door_win_depth = door_th * 2
    
    door_windows = []
    win_x_positions = [-door_w_total*0.3, 0, door_w_total*0.3]
    # Z pos relative to door center. Door height is door_h_total.
    # Top half center -> Z = door_h_total/4 (since 0 is center)
    door_win_z = door_h_total * 0.25 
    
    for x in win_x_positions:
        dw = trimesh.creation.box([door_win_x_size, door_win_depth, door_win_y_size])
        dw.apply_translation([x, 0, door_win_z])
        door_windows.append(dw)
        
    door_final = trimesh.boolean.difference([door_panel] + door_windows)

    # --- Export ---
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Split Filenames
    front_path = os.path.join(output_dir, 'lego_robot_home_base_part1_front.stl')
    back_path = os.path.join(output_dir, 'lego_robot_home_base_part2_back.stl')
    door_path = os.path.join(output_dir, 'lego_robot_home_base_door.stl')
    
    print(f"Exporting Front Part to {front_path}...")
    garage_front.export(front_path)
    
    print(f"Exporting Back Part to {back_path}...")
    garage_back.export(back_path)
    
    print(f"Exporting Door to {door_path}...")
    door_final.export(door_path)
    
    print("Generation Complete.")

if __name__ == "__main__":
    create_garage()