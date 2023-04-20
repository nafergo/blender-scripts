bl_info = {
    "name": "BTT Blender Tasks Tracking",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
from bpy.types import Panel, Operator
from bpy.props import StringProperty, EnumProperty

# Define task properties
class Task:
    def __init__(self, name, description, priority, status, due_date, doer):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.doer = doer

# Define task list
tasks = []

# Define task creation operator
class BTT_CreateTaskOperator(Operator):
    bl_idname = "btt.create_task_operator"
    bl_label = "Create Task"

    # Task properties inputs
    name: StringProperty(name="Task Name")
    description: StringProperty(name="Task Description")
    priority: EnumProperty(
        name="Priority",
        items=[
            ("LOW", "Low", "Low priority task"),
            ("MEDIUM", "Medium", "Medium priority task"),
            ("HIGH", "High", "High priority task"),
        ]
    )
    status: EnumProperty(
        name="Status",
        items=[
            ("TODO", "Todo", "Task not started"),
            ("DOING", "Doing", "Task in progress"),
            ("DONE", "Done", "Task completed"),
        ]
    )
    due_date: StringProperty(name="Due Date")
    doer: StringProperty(name="Doer")

    def execute(self, context):
        # Create task and add to task list
        task = Task(self.name, self.description, self.priority, self.status, self.due_date, self.doer)
        tasks.append(task)

        return {'FINISHED'}

# Define task deletion operator
class BTT_DeleteTaskOperator(Operator):
    bl_idname = "btt.delete_task_operator"
    bl_label = "Delete Task"

    index: bpy.props.IntProperty()

    def execute(self, context):
        # Remove task from task list
        del tasks[self.index]

        return {'FINISHED'}

# Define task display panel
class BTT_TaskDisplayPanel(Panel):
    bl_idname = "BTT_TaskDisplayPanel"
    bl_label = "Tasks"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BTT Tasks Tracking"

    def draw(self, context):
        layout = self.layout

        # Display task list
        for i, task in enumerate(tasks):
            row = layout.row()
            row.operator("btt.delete_task_operator", text="", icon="X").index = i
            row.label(text=task.name)
            row.label(text=task.due_date)

        # Add task creation panel
        box = layout.box()
        box.label(text="Create New Task")
        box.prop(self, "name")
        box.prop(self, "description")
        box.prop(self, "priority")
        box.prop(self, "status")
        box.prop(self, "due_date")
        box.prop(self, "doer")
        box.operator("btt.create_task_operator")

# Register addon
def register():
    bpy.utils.register_class(BTT_CreateTaskOperator)
    bpy.utils.register_class(BTT_DeleteTaskOperator)
    bpy.utils.register_class(BTT_TaskDisplayPanel)

def unregister():
    bpy.utils.unregister_class(BTT_CreateTaskOperator)
    bpy.utils.unregister_class(BTT_DeleteTaskOperator)
    bpy.utils.unregister_class(BTT_TaskDisplayPanel)

if __name__ == "__main__":
    register()
