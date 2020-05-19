# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under The MIT License:
# see LICENSE for the full license text
#
# ##### END LICENSE BLOCK #####

bl_info = {
    "name": "BeamNG forest item (*.forest4.json)",
    "author": "BeamNG / dmn",
    "version": (0, 1, 1),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import-Export forest files",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.7/Py/"
                "Scripts/Import-Export/forest",
    "support": 'COMMUNITY',
    "category": "Import-Export"}

import bpy
from bpy.props import (
        BoolProperty,
        EnumProperty,
        FloatProperty,
        StringProperty,
        CollectionProperty,
        )
from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        )

#this is needed to force refresh of changed file
if "bpy" in locals() and "import_forest" in locals():
    import importlib
    importlib.reload(import_forest)
    importlib.reload(export_forest)
else:
    from . import import_forest
    from . import export_forest


class ExportForest(bpy.types.Operator, ExportHelper):
    """Export to FOREST file format (.FOREST4.JSON)"""
    bl_idname = "export_scene.forest"
    bl_label = 'Export Forest v4'

    filename_ext = ".forest4.json"
    filter_glob: StringProperty(
            default="*.forest4.json",
            options={'HIDDEN'},
            )

    forest_item: StringProperty(
        name="Mesh name",
        description="This will be the exported mesh in the *.forest4.json file",
        default="",
        )

    selection_only: BoolProperty(
        name="Selection Only",
        description="Export only selected elements",
        default=False,
        )

    def draw(self, context):
        layout = self.layout
        sub = layout.row()
        sub.prop(self, "forest_item")
        sub = layout.row()
        sub.prop(self, "selection_only")

    def execute(self, context):
        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "filter_glob",
                                            "check_existing",
                                            ))

        return export_forest.save(self, context, **keywords)

class ImportForest(bpy.types.Operator, ImportHelper):
    """Import to FOREST file format (.FOREST4.JSON)"""
    bl_idname = "import_scene.forest"
    bl_label = 'Import Forest v4'

    filename_ext = ".forest4.json"
    filter_glob: StringProperty(
            default="*.forest4.json",
            options={'HIDDEN'},
            )

    object_type: EnumProperty(
        name="Item type",
        description="This will create a Blender object that represent each forest item",
        items=[
            ('EMPTY', "Empty", "", -1),
            ('MESH', "Mesh", "", 1),
        ],
        default='MESH',
        )

    def draw(self, context):
        layout = self.layout
        sub = layout.row()
        sub.prop(self, "object_type")

    def execute(self, context):

        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "filter_glob",
                                            "check_existing",
                                            ))

        return import_forest.load(self, context, **keywords)

class SCENE_OT_instance(bpy.types.Operator):
    """Apply instancing from last selected to all objects"""
    bl_idname = "scene.all_instance"
    bl_label = 'Apply instancing to all selected objects (BNG forest)'
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        if len(context.selected_objects) < 2:
            self.report({'ERROR'},"You need to select at least 2 objects")
            return {"CANCELLED"}

        for o in context.selected_objects:
            if o is not context.active_object and isinstance(o,bpy.types.Object):
                o.instance_type = context.active_object.instance_type
                if context.active_object.instance_faces_scale != None:
                    o.instance_faces_scale = context.active_object.instance_faces_scale
                if context.active_object.instance_collection != None:
                    o.instance_collection = context.active_object.instance_collection

        return {'FINISHED'}

addon_classes = [ExportForest,
                ImportForest,
                SCENE_OT_instance
                ]

# Add to a menu
def menu_func_export(self, context):
    self.layout.operator(ExportForest.bl_idname, text="BeamNG Forest item (*.forest4.json)")

def menu_func_import(self, context):
    self.layout.operator(ImportForest.bl_idname, text="BeamNG Forest item (*.forest4.json)")

def register():
    for c in addon_classes:
        bpy.utils.register_class(c)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    for c in addon_classes:
        bpy.utils.unregister_class(c)

    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
