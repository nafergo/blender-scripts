import bpy

# Define task class
class Task:
    def __init__(self, name, description, priority, status, due_date, doer):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.doer = doer
    
    def delete(self):
        bpy.context.scene.bttracker_tasks.remove(self)

# Define task enum values
priority_items = [("LOW", "Low", ""), ("MEDIUM", "Medium", ""), ("HIGH", "High", "")]
status_items = [("TODO", "Todo", ""), ("DOING", "Doing", ""), ("DONE", "Done", "")]

# Define task property group
class BTTrackerTaskPropertyGroup(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Task Name", description="The name of the task")
    description: bpy.props.StringProperty(name="Task Description", description="The description of the task")
    priority: bpy.props.EnumProperty(items=priority_items, name="Priority", description="The priority of the task")
    status: bpy.props.EnumProperty(items=status_items, name="Status", description="The status of the task")
    due_date: bpy.props.StringProperty(name="Due Date", description="The due date of the task")
    doer: bpy.props.StringProperty(name="Doer", description="The person responsible for the task")

# Define task list UI element
class BTTrackerTaskListUIElement(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name)
            layout.label(text=item.due_date)

# Define task panel UI
class BTTrackerTaskPanelUI(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_bttracker_task_panel_ui"
    bl_label = "Task Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BTT Blender Tasks Tracking"
    
    def draw(self, context):
        layout = self.layout
        
        # Create task
        row = layout.row()
        row.label(text="Create Task:")
        row = layout.row()
        row.prop(context.scene.bttracker_task_props, "name")
        row = layout.row()
        row.prop(context.scene.bttracker_task_props, "description")
        row = layout.row()
        row.prop(context.scene.bttracker_task_props, "priority")
        row = layout.row()
        row.prop(context.scene.bttracker_task_props, "status")
        row = layout.row()
        row.prop(context.scene.bttracker_task_props, "due_date")
        row = layout.row()
        row.prop(context.scene.bttracker_task_props, "doer")
        row = layout.row()
        row.operator("bttracker.add_task", text="Add Task")
        
        # Delete task
        row = layout.row()
        row.label(text="Delete Task:")
        row = layout.row()
        tasks = context.scene.bttracker_tasks
        for task in tasks:
            task_row = row.row(align=True)
            task_row.label(text=task.name)
            task_row.operator("bttracker.delete_task", text="", icon='X').task_index = tasks.find(task)
        
        # Display task list
        row = layout.row()
        row.label(text="Task List:")
        row = layout.row()
        row.template_list("BTTrackerTaskListUIElement", "", context.scene, "bttracker_tasks", context.scene, "bttracker_task_index")
        task = context.scene.bt

