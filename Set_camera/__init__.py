import bpy

bl_info = {
    "name": "Set Camera ",
    "author": "nafergo",
    "description": "Sets a simple camera rig",
    "version": (1, 0, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Sidebar > Item Tab",    
    "category": "Camera",
    "doc_url": "",
}

class SetCameraPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_set_camera"
    bl_label = "Set Camera"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(context.scene, "camera_distance", text="Distance")
        col.operator("set.camera_operator", text="Set Camera")

class SetCameraOperator(bpy.types.Operator):
    bl_idname = "set.camera_operator"
    bl_label = "Set Camera"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        camera_distance = context.scene.camera_distance

        # Create the camera object
        camera_data = bpy.data.cameras.new(name="Camera")
        camera_object = bpy.data.objects.new(name="Camera", object_data=camera_data)
        bpy.context.scene.collection.objects.link(camera_object)

        # Set the camera position and rotation
        camera_object.location = (0, camera_distance, 1)
        camera_object.rotation_euler = (90.0 * 3.14159 / 180.0, 0, 0)

        # Create the empty object
        empty_data = bpy.data.objects.new(name="Camera Control", object_data=None)
        bpy.context.scene.collection.objects.link(empty_data)

        # Set the empty position
        empty_data.location = (0, 0, 0)

        # Parent the camera to the empty
        camera_object.parent = empty_data

        return {'FINISHED'}

def register():
    bpy.utils.register_class(SetCameraPanel)
    bpy.utils.register_class(SetCameraOperator)
    bpy.types.Scene.camera_distance = bpy.props.FloatProperty(name="Camera Distance", default=-10.0, min=-100.0, max=100.0)

def unregister():
    bpy.utils.unregister_class(SetCameraPanel)
    bpy.utils.unregister_class(SetCameraOperator)
    del bpy.types.Scene.camera_distance

if __name__ == "__main__":
    register() 

