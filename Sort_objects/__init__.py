import bpy

bl_info = {
    "name": "Sort Objects",
    "author": "nafergo",
    "description": "Sets a simple camera rig",
    "version": (1, 0, 0),    
    "blender": (3, 4, 0),
    "location": "View3D > Sidebar > Item Tab",        
    "category": "Object",
    "doc_url": "",    
}

class SortObjectsPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_sort_objects"
    bl_label = "Sort Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(context.scene, "sort_offset", text="Offset")
        col.operator("sort.objects_y", text="Sort Y Axis")
        col.operator("sort.objects_x", text="Sort X Axis")
        col.operator("sort.objects_z", text="Sort Z Axis")

class SortObjectsYAxisOperator(bpy.types.Operator):
    bl_idname = "sort.objects_y"
    bl_label = "Sort Y Axis"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if selected_objects:
            selected_objects.sort(key=lambda obj: obj.name)
            for i, obj in enumerate(selected_objects):
                obj.location.y = i * context.scene.sort_offset
        return {'FINISHED'}

class SortObjectsXAxisOperator(bpy.types.Operator):
    bl_idname = "sort.objects_x"
    bl_label = "Sort X Axis"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if selected_objects:
            selected_objects.sort(key=lambda obj: obj.name)
            for i, obj in enumerate(selected_objects):
                obj.location.x = i * context.scene.sort_offset
        return {'FINISHED'}

class SortObjectsZAxisOperator(bpy.types.Operator):
    bl_idname = "sort.objects_z"
    bl_label = "Sort Z Axis"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if selected_objects:
            selected_objects.sort(key=lambda obj: obj.name)
            for i, obj in enumerate(selected_objects):
                obj.location.z = i * context.scene.sort_offset
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SortObjectsPanel)
    bpy.utils.register_class(SortObjectsYAxisOperator)
    bpy.utils.register_class(SortObjectsXAxisOperator)
    bpy.utils.register_class(SortObjectsZAxisOperator)
    bpy.types.Scene.sort_offset = bpy.props.FloatProperty(name="Offset", default=-0.01, min=-1.0, max=1.0)

def unregister():
    bpy.utils.unregister_class(SortObjectsPanel)
    bpy.utils.unregister_class(SortObjectsYAxisOperator)
    bpy.utils.unregister_class(SortObjectsXAxisOperator)
    bpy.utils.unregister_class(SortObjectsZAxisOperator)
    del bpy.types.Scene.sort_offset

if __name__ == "__main__":
    register() 

