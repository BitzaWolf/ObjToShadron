# OBJ to Shadron
This python script converts a Wavefront OBJ file into a Shadron-friendly format.

It simply reads an object file, computes the important information, and writes
out a Shadron file. The file is ready for use as an #include inside another
shadron script. Simply use it like you would with the default library's Cube or
Sphere models.

# Example
![Example Image](https://github.com/BitzaWolf/ObjToShadron/blob/master/Example.PNG)

# How to use
Make sure you have python installed. If you have a recent version of blender,
you'll have the python executable too.

1. Download the ObjToShadron.py file
2. Open a terminal to that directory
3. Place your .obj file in the directory
4. Name the .obj file "Input.obj"
5. Run `python ObjToShadron`
6. It will prompt you for a prefix. The prefix will be prepended to every function and variable generated. The prefix ensures the functions and variables have a unique name and will not conflict with other Shadron variables or functions.
7. Your Shadron file will pop out in the same directory, called "Output.shadron"
8. Copy the "Output.shadron" file in the same directory as your main shadron file
9. Add the code `#include "Output.shadron"` to the top of the file

**Shadron will take a few minutes to compile the large glsl function. I don't think this is avoidable right now, just give it ample time.**

# Shadron?
Shadron is a software tool that makes it easy to write and play with GLSL shaders.

Unfortunately it can't import object files (or any custom models at all), and its
syntax for drawing models is uncomfortable for doing by hand.

Check out [Shadron's Site](https://www.arteryengine.com/shadron/)
