# Background on this project

There are many simulators that can mimic the path represented by G-code when it is inserted into the already developed PyCNC. These simulators are very useful for verifying the path in advance and making necessary modifications to the G-code.
However, there are not many tools available to simulate the actual machine behavior during the execution of the path, such as how inefficiencies may occur in the motion, how the behavior changes due to disturbances other than the data generated from the CNC interpolation, and how the actual machine movement is carried out.
Therefore, the goal of this project is to develop a platform that can simulate the execution of G-code not merely from the perspective of the path but as the actual movement of a CNC machine.

# Topmost structure on this project 

For this project, three main components are necessary: 1) a CNC machine, 2) a CNC controller, and 3) a user interface (UI) that demonstrates the real-time interaction between components 1 and 2.
In the case of the CNC machine, directly testing with an actual CNC machine does not align with the project's background. Therefore, a 3-axis CNC machine was simulated in the form of a CAD image using FreeCAD.
For the CNC controller, we used PyCNC, a Python-based CNC system. For more detailed information about PyCNC, please refer to the following link (https://github.com/Nikolay-Kha/PyCNC?tab=readme-ov-file).
PyCNC provides two interfaces: hal and hal_virtual. The former is used for interfacing with actual machines, while the latter displays virtual pulse outputs on the computer. Naturally, this project utilizes the latter interface.

For the UI that displays interactions, we use a professional tool called Blender. Instead of manually using Blender's editing features, we automate the simulation of these interactions through Python scripts within Blender. There are two main scenarios: 1) reading an entire G-code file, and 2) directly inputting G-code commands line by line. The system is designed to handle both cases.

![image](https://github.com/user-attachments/assets/bd4d911d-08fd-4c02-8455-ff691911becb)

# CAD file
For the CAD files, navigate to the project's UI -> CAD image directory and refer to the assembly_mod file. The other files in this directory should be understood as individual parts that make up the assembly. The final assembled result can be found in the UI -> threeaxis_CNC_obj.obj file, which was converted to an OBJ file for use in Blender instead of a STEP file.

# pyCNC modification

In the original released version of PyCNC, pulse data generated based on G-code is output to a real CNC machine or a computer through the hal/hal_virtual interface. To enable its use in Blender, a separate socket interface was added.
The modifications made compared to the original version are indicated with comments marked by the [CHG] tag. 
You can refer to the file named main_blender_interaction.py for this project. It can be viewed as an edited version of the original main.py (from PyCNC) with the added socket functionality.

# blender script 

The Blender script is designed to receive socket data transmitted from PyCNC (which includes position and time data for each axis) and remap the positions for each axis frame by frame, allowing for the generation of smooth animation data.
The Blender file can be found at UI -> threeaxis_cnc_animation.blend. After opening this file, you can check the script in the Script tab.
Absolutely, you should download the blender app in your PC. (For me, I use blender 4.2)

# How to execute 

1. Open blender file and run the script (activate server)
2. Open main_blender_interaction.py
3. If you want to run by g-code file, then write down the following command --> python .\main_blender_interaction.py .\test_gcode.txt
4. If you want to run by inputting line-by-line via console --> just run main_blender_interaction.py without any argument
5. If you start with 3., everything is performed automatically. All you need to do is just go to the animation tab in the blender and see what happen by looking at animation
6. If you start with 4., blender app. is locked until you finish your job on main_blender_interaction.py (e.g. until you enter "quit" command) After finish pycnc job, then you go to the animation tab in  the blender and see what happen by looking at animation.


If you want to see the detailed progress in blender while you are following the above step, It will be helpful to open the console ( Window > Toggle System Console) 

As an example, G-code path data has been written in the test_gcode.txt file, as shown in the image below.

![image](https://github.com/user-attachments/assets/c346cd74-5951-4cf7-a772-4b259e23692a)

The mapped animation motion can be simulated as shown in the video below.



https://github.com/user-attachments/assets/602fd915-4369-437e-88f5-aa0150cd191e

# License 

for original pyCNC : https://github.com/Karl-sim-expert/pycnc_gcode-digital-twin/blob/main/LICENSE%20for%20original%20pyCNC
for modified part : https://github.com/Karl-sim-expert/pycnc_gcode-digital-twin/blob/main/LICENSE%20for%20modified%20part
