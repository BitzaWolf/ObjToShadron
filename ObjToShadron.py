# 0) Read in all the verticies. 1-based index.
#    Read in all tex coords
#    Read in all normal coords
#    Read in faces
# 1) Determine if quads or trigs, 4 or 3 verts per face
#    Write num of verts
# 2) Write vertex coord function, based on faces and verts
#    Write vertex texcoord function
#    Write vertex normal function

input = open("Input.obj", 'r')

line = input.readline();
# if line starts with 'v'
# while line starts with 'v'...
#		store vertex, next 3 inputs are x,y,z
# while line start with 'vt'...
#		store texcoord, next 2 inputs are u, v
# while line starts with 'vn'
#		store texnormal, next 3 inputs are x, y, z
# ... junk
# if 'f' has 3 verts -> Triangles, if 4 -> Quads
# while line starts with 'f'
#
#A  B
#
#C  D
#
#A C D B
#
#Triangles...
#A C D
#A D B
#
#Quad to Triangles
#v1 v2 v3
#v1 v3 v4
# 
# End data for 1 object.




# Ready to output!
# 1) query for prefix to keep defines and function uniquely named
# 2) #defines
# 3) coord function -> a giant array of ALL vertices in order
# 4) texcoord function
# 5) normal function
# 6) vertext function -> calls coord, but returns a vec4