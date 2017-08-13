import re

# 0) Read in all the verticies. 1-based index.
#    Read in all tex coords
#    Read in all normal coords
#    Read in faces
# 1) Determine if quads or trigs, 4 or 3 verts per face
#    Write num of verts
# 2) Write vertex coord function, based on faces and verts
#    Write vertex texcoord function
#    Write vertex normal function

fileIn = open("Input.obj", 'r')
line = fileIn.readline()

# Look for verticies
while line[0] != 'v':
	line = fileIn.readline()

# while line starts with 'v'...
#		store vertex, next 3 inputs are x,y,z
verticies = []
while line[:2] == "v ":
	vertex = re.findall(r'-?\d+\.\d+', line)
	verticies.append(vertex)
	line = fileIn.readline()

# while line start with 'vt'...
#		store texcoord, next 2 inputs are u, v
uvs = []
while line[:2] == "vt":
	uv = re.findall(r'-?\d+\.\d+', line)
	uvs.append(uv)
	line = fileIn.readline()

# while line starts with 'vn'
#		store texnormal, next 3 inputs are x, y, z
normals = []
while line[:2] == "vn":
	normal = re.findall(r'-?\d+\.\d+', line)
	normals.append(normal)
	line = fileIn.readline()

# Skip over junk
while line[:2] != "f ":
	line = fileIn.readline()

# while line starts with 'f'
faces = []
while line[:2] == "f ":
	face = re.findall(r'\d+\/?\d*\/?\d*', line)
	faces.append(face)
	line = fileIn.readline()

# if faces are quads, transform to trianges
# A B C D
# 
# A  D
# 
# B  C
#
#Triangles...
# A B C
# A C D
# 
#Quad to Triangles
#v1 v2 v3
#v1 v3 v4
if len(faces[0]) == 4:
	quads = faces
	faces = []
	numFaces = len(quads)
	for q in quads:
		faces.append([q[0], q[1], q[2]])
		faces.append([q[0], q[2], q[3]])

# Shadron doesn't use faces, it uses literal verticies. So, for each face we have to break
# up the v/t/n scheme into verticies, textures, and normals
faceVerticies = []
faceTextures = []
faceNormals = []
for f in faces:
	for triplet in f:
		values = re.findall(r'\d+', triplet)
		faceVerticies.append(values[0])
		if "//" in triplet:
			faceNormals.append(values[1])
		elif len(values) == 2:
			faceTextures.append(values[1])
		else:
			faceTextures.append(values[1])
			faceNormals.append(values[2])


# Ready to output!
output = open("Output.shadron", 'w')
vertCount = str(len(faceVerticies))
texCount = str(len(faceTextures))
normCount = str(len(faceNormals))

# 1) query for prefix to keep defines and function uniquely named
prefix = input('Prefix: ')

# 2) #defines
output.write("// Shadron model created using ObjToShadron by Bitzawolf\n")
output.write("// http://www.bitzawolf.com\n")
output.write("\n")
output.write("#define " + prefix + "_PRIMITIVES triangles\n")
output.write("#define " + prefix + "_VERTEX_COUNT " + vertCount + "\n")

# 3) coord function -> a giant array of ALL vertices in order
output.write("glsl vec3 " + prefix + "_Coord(int i) {\n")
output.write("    vec3[" + vertCount + "] coords = vec3[" + vertCount + "](\n")
vectors = []
for vertexIndex in faceVerticies:
	vertex = verticies[int(vertexIndex) - 1]
	vectors.append("        vec3(" + str(vertex[0]) + ", " + str(vertex[1]) + ", " + str(vertex[2]) + ")")
connector = ",\n"
vectors = connector.join(vectors)
output.write(vectors)
output.write("\n")
output.write("    );\n")
output.write("    return coords[i];\n")
output.write("}\n")
output.write("\n")

# 4) texcoord function
output.write("glsl vec2 " + prefix + "_TexCoord(int i) {\n")
output.write("    vec2[" + texCount + "] texCoords = vec2[" + texCount + "](\n")
vectors = []
for textureIndex in faceTextures:
	uv = uvs[int(textureIndex) - 1]
	vectors.append("        vec2(" + str(uv[0]) + ", " + str(uv[1]) + ")")
connector = ",\n"
vectors = connector.join(vectors)
output.write(vectors)
output.write("\n")
output.write("    );\n")
output.write("    return texCoords[i];\n")
output.write("}\n")
output.write("\n")

# 5) normal function
output.write("glsl vec3 " + prefix + "_Normal(int i) {\n")
output.write("    vec3[" + normCount + "] normals = vec3[" + normCount + "](\n")
vectors = []
for normalIndex in faceNormals:
	normal = normals[int(normalIndex) - 1]
	vectors.append("        vec3(" + str(normal[0]) + ", " + str(normal[1]) + ", " + str(normal[2]) + ")")
vectors = connector.join(vectors)
output.write(vectors)
output.write("\n")
output.write("    );\n")
output.write("    return normals[i];\n")
output.write("}\n")
output.write("\n")

# 6) vertext function -> calls coord, but returns a vec4
output.write("glsl vec4 " + prefix + "_Vertex(int i) {\n")
output.write("    return vec4(" + prefix + "_Coord(i), 1.0);\n")
output.write("}\n")
output.write("\n")