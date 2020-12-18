import bpy
import bmesh

try:
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete(use_global=False)
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)
except:
    pass
'''
bpyscene = bpy.context.scene

# Create an empty mesh and the object.
mesh = bpy.data.meshes.new('Basic_Cube')
basic_cube = bpy.data.objects.new("Basic_Cube", mesh)

# Add the object into the scene.
bpy.data.collections[0].objects.link(basic_cube)
basic_cube.select_set(True)

# Construct the bmesh cube and assign it to the blender mesh.
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1.0)
bm.to_mesh(mesh)
bm.free()'''

bpyscene = bpy.context.scene
n=3

def create_cube_mesh(size=1.0):
    mesh = bpy.data.meshes.new('Cube')

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=size)
    bm.to_mesh(mesh)
    bm.free()

    return mesh

cube_mesh = create_cube_mesh()

'''def create_cube(mesh):
    obj = bpy.data.objects.new("Cube", mesh)
    #obj.location(x,y,z)
    # Add the object into the scene.
    bpy.data.collections[0].objects.link(obj)

    return obj
'''

def create_cube(location, scale):
    global cube_mesh
    obj = bpy.data.objects.new("Cube", cube_mesh)
    obj.location = location
    obj.scale = scale
    # Add the object into the scene.
    bpy.data.collections[0].objects.link(obj)
    return obj

#cube_mesh = create_cube_mesh()
#cube_obj_1 = create_cube(cube_mesh)

def mengerTransform(obj):
    children = []
    basicLocation = obj.location
    basicScale = obj.scale
    for i in range (-1,2): #X
        for j in range (-1,2): #Y
            for k in range (-1,2): #Z
                if((i!=0 and j!=0) or (i!=0 and k!=0) or (j!=0 and k!=0)): #assure existance de cubes vides
                    newScale = basicScale/3
                    newLocation = [0,0,0]
                    newLocation[0] = basicLocation[0] + i * newScale[0]
                    newLocation[1] = basicLocation[1] + j * newScale[1]
                    newLocation[2] = basicLocation[2] + k * newScale[2]
                    cube = create_cube(newLocation, newScale)
                    children.append(cube) #children est propre à chaque menger cube
                    
    #on va delete les cube d'avant
    bpy.data.objects.remove(obj,do_unlink = True)
    return children

def menger(objectsToTransform):
    AllChildren = []
    for obj in objectsToTransform:
        tab = mengerTransform(obj) #tab est temporaire
        for object in tab:
            AllChildren.append(object) #permet d'ajouter chaque petit cube individuellement et de les conserver TOUS
    return AllChildren

def main(n):
    locDepart = (0,0,0)
    scaleDepart = (1,1,1)
    cubeInit = create_cube(locDepart, scaleDepart)
    objectsToTransform = []
    objectsToTransform.append(cubeInit)
    for i in range (0,n):
        objectsToTransform = menger(objectsToTransform)


main(n)
#itération, position et dim de base