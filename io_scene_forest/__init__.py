# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under The MIT License:
# see LICENSE for the full license text
#
# ##### END LICENSE BLOCK #####

bl_info = {
    "name": "BeamNG *.forest4.json Exporter",
    "author": "Dummiesman",
    "version": (0, 0, 2),
    "blender": (2, 77, 0),
    "location": "File > Export",
    "description": "Export forest files",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.7/Py/"
                "Scripts/Import-Export/forest",
    "support": 'COMMUNITY',
    "category": "Export"}

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

class ExportForest(bpy.types.Operator, ExportHelper):
    """Export to FOREST file format (.FOREST4.JSON)"""
    bl_idname = "export_scene.forest"
    bl_label = 'Export Forest v4'

    filename_ext = ".forest4.json"
    filter_glob = StringProperty(
            default="*.forest4.json",
            options={'HIDDEN'},
            )

    forest_item = StringProperty(
        name="Mesh name",
        description="This will be the exported mesh in the *.forest4.json file",
        default="",
        )

    selection_only = BoolProperty(
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
        from . import export_forest

        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "filter_glob",
                                            "check_existing",
                                            ))

        return export_forest.save(self, context, **keywords)


# Add to a menu
def menu_func_export(self, context):
    self.layout.operator(ExportForest.bl_idname, text="BeamNG Forest (*.forest4.json)")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
