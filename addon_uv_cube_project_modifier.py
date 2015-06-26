bl_info = {
    "name": "UV Cube Project Modifier",
    "author": "Judd Cohen",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "category": "Add Mesh",
    "description": "Adds a modifier to a mesh that does automagic uv cube projection",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
}

import math
import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector



def deg2rad(angle):
    return math.pi * angle / 180.0



def create_camera(name, euler):
    cam = bpy.data.cameras.new(name)
    cam_obj = bpy.data.objects.new(name, cam)
    bpy.context.scene.objects.link(cam_obj)
    cam_obj.data.type = 'ORTHO'
    cam_obj.data.ortho_scale = 1.0
    cam_obj.location = (0.0, 0.0, 0.0)
    cam_obj.rotation_euler = [ deg2rad(euler[0]), deg2rad(euler[1]), deg2rad(euler[2]) ]
    return cam_obj



class UVCubeProjectModifier(bpy.types.Operator):
    """ Sets up a UV Cube Projection modifier """
    bl_idname = "uvcubeproject.modifier"
    bl_label = "Add UV Cube Projection Modifier"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def get_or_create_camera(self, context, name, rot):
        """ Retrieves the requested camera, creating it if needed """
        foundCamera = None
        
        for key,val in context.scene.objects.items():
            if key.startswith(name):
                foundCamera = key
                break

        if foundCamera is not None:
            return context.scene.objects[foundCamera]
        else:
            return create_camera(name, rot)
    
    
    def get_cameras(self, context):
        """ Returns a list of 6 cameras, each pointing in a different direction """
        cameras = []
        
        cameras.append(self.get_or_create_camera(context, "Camera_X+", (90.0, 0.0, 270.0)))
        cameras.append(self.get_or_create_camera(context, "Camera_X-", (90.0, 0.0, 90.0)))
        
        cameras.append(self.get_or_create_camera(context, "Camera_Y+", (90.0, 0.0, 0.0)))
        cameras.append(self.get_or_create_camera(context, "Camera_Y-", (90.0, 0.0, 180.0)))
        
        cameras.append(self.get_or_create_camera(context, "Camera_Z+", (180.0, 0.0, 0.0)))
        cameras.append(self.get_or_create_camera(context, "Camera_Z-", (0.0, 0.0, 0.0)))
        
        return cameras
    
    
    # called when running operator
    def execute(self, context):
        for ob in context.selected_objects:
            ob.modifiers.new(type="UV_PROJECT", name="UVCubeProjection")
            mod = ob.modifiers["UVCubeProjection"]
            cameras = self.get_cameras(context)
            mod.projector_count = len(cameras)
            for i in range(len(cameras)):
                mod.projectors[i].object = cameras[i]
            mod.scale_x = 100.0
            mod.scale_y = 100.0
        
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(UVCubeProjectModifier)


def unregister():
    bpy.utils.unregister_class(UVCubeProjectModifier)


if __name__ == "__main__":
    register()
