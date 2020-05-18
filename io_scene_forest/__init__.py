# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under The MIT License:
# see LICENSE for the full license text
#
# ##### END LICENSE BLOCK #####

bl_info = {
    "name": "BeamNG forest item (*.forest4.json)",
    "author": "BeamNG / dmn",
    "version": (0, 1, 0),
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

    def draw(self, context):
        layout = self.layout

    def execute(self, context):

        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "filter_glob",
                                            "check_existing",
                                            ))

        return import_forest.load(self, context, **keywords)

addon_classes = [ExportForest,
                ImportForest
                ]

# Add to a menu
def menu_func_export(self, context):
    self.layout.operator(ExportForest.bl_idname, text="BeamNG Forest (*.forest4.json)")

def menu_func_import(self, context):
    self.layout.operator(ImportForest.bl_idname, text="BeamNG Forest (*.forest4.json)")

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
