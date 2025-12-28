In this folder, we will build a Lego robot home base.

Model: Lego 31164 lego space robot lego set.
Dimension: 10.3 x 7.5 x 1.8 inches (26.2 x 19.1 x 4.6 cm) 

Design: 
1. Front view: Front door opens like by side ways from the right side, with a few small windows on the top
   and those windows are located on the top half part of the door. There are 3 windows on the door.
2. We will use a 3D printer. to print the parts.
3. The floor for the robot to move around. 
4. Wall and roof width is 5mm.
5. Generate a script to generate stl file and latter we will print it on
   BambuLab printer. 5.
   
## Generation
To regenerate the STL files, run:
```bash
python3 generate_garage.py
```
Ensure you have `trimesh` installed (`pip install trimesh[all]`).

To view the generated STL files, you can use any 3D model viewer that supports STL format, such as MeshLab or Blender.
The STL file that will be generated for the roop will be 'lego_robot_home_base_roof.stl'.
The STL file that will be generated for the door will be 'lego_robot_home_base_door.stl'.
The STL file that will be generated for the floor will be 'lego_robot_home_base_floor.stl'.
The STL file that will be generated for the walls will be 'lego_robot_home_base_walls.stl'.
Remember that the windows are on the door and the walls. 
## Summary
Keep in mind the following details about the Lego robot home base:
The dimensions are approximately 10.3 x 7.5 x 1.8 inches (26.2 x 19.1 x 4.6 cm).
The walls and roof are connected.
The wall and roof thickness is 5mm.
The door has 3 windows on the top half part of the door. Same for the walls. 
Remember that the door opens from the right side.
The STL files can be printed using a 3D printer such as the BambuLab printer.
Remember that the generated parts can be assembled to create the Lego robot home base.
Remember that the floor is connected to the walls.
So 'lego_robot_home_base_floor.stl' is connected to 'lego_robot_home_base_walls.stl'. so no use of those 2 STL files.
So only 3 STL files are needed to be printed. Which are these:
1. 'lego_robot_home_base_roof.stl'
2. 'lego_robot_home_base_door.stl'
3. 'lego_robot_home_base_walls_and_floor.stl'
## WAIT!! BEFORE YOU GENERATE THE STL FILES, PLEASE READ THE FOLLOWING INSTRUCTION CAREFULLY:
1. The roof and walls cannot be connected because the walls have windows on them.
2. The door cannot be connected to the walls because the door has windows on it.
3. The floor is connected to the walls. So no need to generate a separate STL file
4. So listen to avove istructions carefully before generating the STL files.
5. Make sure to generate only 4 STL files as mentioned above.
## LAST NOTES BEFORE YOU START:
1. Make sure to follow the design instructions carefully.
2. Ensure the dimensions are accurate.
3. Double-check the wall and roof thickness.
4. Verify the placement and size of the windows on the door and walls.
5. Test the door opening mechanism in the design.
6. Review the generated STL files for any errors before printing.
7. Read this README 2 times before generating the STL files.
WORK HARD TO MAKE SURE THE ROBOT HOME BASE IS PERFECT!!
## NEVERMIND THIS IS THE LAST INSTRUCTION:
DO ALL THOSE THINGS MENTIONED FROM ##LAST NOTES BEFORE YOU START:
8. MAKE THE HOUSE BIGGER THAN THE ROBOT SO IT CAN MOVE AROUND EASILY INSIDE THE HOUSE.
9. Make sure the clearance for the robot should be 2cm on each of four sides, and 4cm on
   the top.
10. Nevermind I was correct from the start. The roof and walls are connected and
    the STL file is 'lego_robot_home_base_roof_and_walls.stl'
