# OBJ to Shadron
This python script converts a Wavefront OBJ file into a Shadron-friendly format.

It simply reads an object file, computes the important information, and writes
out a Shadron file. The file is ready for use as an #include inside another
shadron script. Simply use it like you would with the default library's Cube or
Sphere models.

# Shadron?
Shadron is a software tool that makes it easy to write and play with GLSL shaders.

Unfortunately it can't import object files (or any custom models at all), and its
syntax for drawing models is uncomfortable for doing by hand.

Check out [Shadron's Site](https://www.arteryengine.com/shadron/)