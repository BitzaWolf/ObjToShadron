import re
import sys

print("**********************************\n")
print("* Welcome to Object-to-Shadron!  *\n")
print("**********************************\n\n")

# 1) Read in all the verticies. 1-based index.
#    Read in all tex coords
#    Read in all normal coords
#    Read in faces
# 2) Write Vertex Data and VertexList

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

# If faces don't have 3 verts, quit now.
if len(faces[0]) != 3:
	print("Faces are not made from triangles.\n")
	print("Please re-export .obj file model with just triangles.")
	sys.exit()

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
vertCount = len(faceVerticies)
texCount = len(faceTextures)
normCount = len(faceNormals)
hasTex = texCount != 0
hasNorm = normCount != 0

# 1) query for prefix to keep defines and function uniquely named
prefix = input('Prefix: ')

# 2) Shameless plug
output.write("// Shadron model created using ObjToShadron by Bitzawolf\n")
output.write("// https://github.com/BitzaWolf/ObjToShadron\n")
output.write("// http://www.bitzawolf.com\n")
output.write("\n")

# 3) Write Vertex Struct
output.write("glsl struct " + prefix + "_VertexData {\n")
output.write("    vec3 coord;\n")
if hasTex:
	output.write("    vec2 texCoord;\n")
if hasNorm:
	output.write("    vec3 normal;\n")
output.write("};\n\n")
output.write("vertex_list " + prefix + "_VertexData " + prefix + "_VertList = {\n")

# 4) Gather array of verticies based on faces
vectorsVerticies = []
for vertexIndex in faceVerticies:
	vertex = verticies[int(vertexIndex) - 1]
	vectorsVerticies.append(str(vertex[0]) + ", " + str(vertex[1]) + ", " + str(vertex[2]))

# 5) Gather array of texture coords
vectorsTextures = []
for textureIndex in faceTextures:
	uv = uvs[int(textureIndex) - 1]
	vectorsTextures.append(str(uv[0]) + ", " + str(uv[1]))

# 6) Gather array of normal coords
vectorsNormals = []
for normalIndex in faceNormals:
	normal = normals[int(normalIndex) - 1]
	vectorsNormals.append(str(normal[0]) + ", " + str(normal[1]) + ", " + str(normal[2]))

# 7) Append 'em all and stuff it into the list!
vectors = []
for index in range(0, vertCount):
    string = "    " + vectorsVerticies[index]
    if hasTex:
	    string = string + ", " + vectorsTextures[index]
    if hasNorm:
        string = string + ", " + vectorsNormals[index]
    vectors.append(string)

connector = ",\n"
vectors = connector.join(vectors)
output.write(vectors)

# 8) Cleanup
output.write("\n")
output.write("};")