import bpy
import bmesh


bpyscene = bpy.context.scene
n=3

def create_pyramide_mesh(size=1.0):
    mesh = bpy.data.meshes.new('Pyramide')
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=True, segments=4, diameter1=size/1.4, diameter2=0, depth=size)
    bm.to_mesh(mesh)
    bm.free()
    return mesh

pyramide_mesh = create_pyramide_mesh()

def create_pyramide(location, scale):
    global pyramide_mesh
    obj = bpy.data.objects.new("Pyramide", pyramide_mesh)
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
    basicDiameter1 = obj.scale
    basicDepth = obj.scale
    newDiameter1 = basicDiameter1/2
    newDepth = basicDepth/2
    '''for i in range (0,4):
        for j in range (0,2):
            newLocation = [0,0,0]
            if (i % 2) == 0:
                newLocation[0] = basicLocation[0] - newDepth[0]/2*1.4
            else:
                newLocation[0] = basicLocation[0] + newDepth[0]/2*1.4
            if (j % 2) == 0:
                newLocation[1] = basicLocation[1] - newDepth[0]/2*1.4
            else:
                newLocation[1] = basicLocation[1] + newDepth[0]/2*1.4
            newLocation[2] = basicLocation[2] - newDepth[0]
            pyramide = create_pyramide(newLocation, newDiameter1)
            children.append(pyramide) #children est propre à chaque menger cube'''
    #crée la pyramide du dessus
    newLocation = [0,0,0]
    newLocation[2] = basicLocation[2] + newDiameter1[0]/2
    pyramide = create_pyramide(newLocation, newDiameter1)
    children.append(pyramide)
    
    newLocation = [0,0,0]
    #on se place au niveau du socle
    newLocation[2] = basicLocation[2] - newDiameter1[0]/2
    #on place les pyramides du socle une à une
    newLocation[0] = basicLocation[0] + newDiameter1[0]/1.4
    pyramide = create_pyramide(newLocation, newDiameter1)
    children.append(pyramide)
    
    newLocation[0] = basicLocation[0] - newDiameter1[0]/1.4
    pyramide = create_pyramide(newLocation, newDiameter1)
    children.append(pyramide)
    
    newLocation[0] = 0 #on reset le paramètre
    newLocation[1] = basicLocation[1] + newDiameter1[0]/1.4
    pyramide = create_pyramide(newLocation, newDiameter1)
    children.append(pyramide)
    
    newLocation[1] = basicLocation[1] - newDiameter1[0]/1.4
    pyramide = create_pyramide(newLocation, newDiameter1)
    children.append(pyramide)
    #on va delete les cubes d'avant
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
    pyramideInit = create_pyramide(locDepart, scaleDepart)
    objectsToTransform = []
    objectsToTransform.append(pyramideInit)
    for i in range (0,n):
        objectsToTransform = menger(objectsToTransform)


main(n)
#itération, position et dim de base