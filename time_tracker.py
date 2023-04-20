import bpy
import time

bl_info = {
    "name": "TimeTracker",
    "description": "Track the amount of time the current file has been open in Blender",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Render Properties",
    "category": "System"
}

class TimeTrackerProperties(bpy.types.PropertyGroup):
    start_time: bpy.props.FloatProperty()
    total_time: bpy.props.FloatProperty()

def update_time(scene):
    if scene.my_addon_time_tracker_data.is_tracking:
        scene.my_addon_time_tracker_data.total_time += time.time() - scene.my_addon_time_tracker_data.start_time
        scene.my_addon_time_tracker_data.start_time = time.time()

class TimeTrackerPanel(bpy.types.Panel):
    bl_label = "Time Tracker"
    bl_idname = "RENDER_PT_time_tracker_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if "my_addon_time_tracker_data" not in bpy.types.Scene.__annotations__:
            bpy.types.Scene.my_addon_time_tracker_data = bpy.props.PointerProperty(type=TimeTrackerProperties)
            bpy.types.Scene.my_addon_time_tracker_data.is_tracking = False
            bpy.types.Scene.my_addon_time_tracker_data.total_time = 0.0

        time_tracker_data = scene.my_addon_time_tracker_data

        row = layout.row(align=True)
        if time_tracker_data.is_tracking:
            row.operator("my_addon.stop_timer", text="Stop Timer", icon="PAUSE")
        else:
            row.operator("my_addon.start_timer", text="Start Timer", icon="PLAY")

        layout.label(text=f"Total Time: {time_tracker_data.total_time:.2f}s")

class StartTimerOperator(bpy.types.Operator):
    bl_idname = "my_addon.start_timer"
    bl_label = "Start Timer"

    def execute(self, context):
        scene = context.scene
        scene.my_addon_time_tracker_data.is_tracking = True
        scene.my_addon_time_tracker_data.start_time = time.time()
        bpy.app.handlers.scene_update_post.append(update_time)
        return {'FINISHED'}

class StopTimerOperator(bpy.types.Operator):
    bl_idname = "my_addon.stop_timer"
    bl_label = "Stop Timer"

    def execute(self, context):
        scene = context.scene
        scene.my_addon_time_tracker_data.is_tracking = False
        scene.my_addon_time_tracker_data.total_time += time.time() - scene.my_addon_time_tracker_data.start_time
        bpy.app.handlers.scene_update_post.remove(update_time)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(TimeTrackerProperties)
    bpy.utils.register_class(TimeTrackerPanel)
    bpy.utils.register_class(StartTimerOperator)
    bpy.utils.register_class(StopTimerOperator)

def unregister():
    bpy.utils.unregister_class(TimeTrackerProperties)
    bpy.utils.unregister_class(TimeTrackerPanel)
    bpy.utils.unregister_class(StartTimerOperator)
    bpy.utils.unregister_class(StopTimerOperator)

if __name__ == "__main__":
    register()

