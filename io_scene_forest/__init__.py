# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under The MIT License:
# see LICENSE for the full license text
#
# ##### END LICENSE BLOCK #####

bl_info = {
    "name": "BeamNG forest item (*.forest4.json)",
    "author": "BeamNG / dmn",
    "version": (0, 2, 0),
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
import os

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

class PROPERTIES_PG_forest_particle(bpy.types.PropertyGroup):
    export_path: bpy.props.StringProperty(
        name="Export file path",
        description="",
        subtype='FILE_PATH')
    fi_name: bpy.props.StringProperty(
        name="Forest item name",
        description="")

def particle_get_settings(context):
    if context.particle_system:
        return context.particle_system.settings
    elif isinstance(context.space_data.pin_id, bpy.types.ParticleSettings):
        return context.space_data.pin_id
    return None

class ExportParticleForest(bpy.types.Operator):
    """Yes"""
    bl_idname = "export_particle.forest"
    bl_label = "Export particle forest"

    @classmethod
    def poll(cls, context):
        psys = context.particle_system
        pset = particle_get_settings(context)
        return psys is not None and pset is not None

    def execute(self, context):
        degp = bpy.context.evaluated_depsgraph_get()
        particle_systems = context.active_object.evaluated_get(degp).particle_systems
        psys = particle_systems[context.particle_system.name] or None
        pset = particle_get_settings(context)
        if psys is not None and pset is not None:
            with open(bpy.path.abspath(pset.forest.export_path), "w") as f:
                export_forest.export_forest(f, pset.forest.fi_name, psys.particles)
            return {'FINISHED'}
        else:
            print("psys:",psys)
            print("pset:",pset)
            self.report({'ERROR'}, 'ERROR : Could not get particle system or setting')
            return {"CANCELLED"}

class PANEL_PT_forest_particle(bpy.types.Panel):
    bl_label = "BNG Forest Properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "particle"
    bl_parent_id = "PARTICLE_PT_context_particles"

    @classmethod
    def poll(cls, context):
        psys = context.particle_system
        pset = particle_get_settings(context)
        return psys is not None and pset is not None

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True  # Active single-column layout
        layout.use_property_decorate = False

        # particles are always empty because .....
        #psys = context.particle_system

        #https://devtalk.blender.org/t/manipulating-particles-in-python/7552/2
        # Dependancy graph
        degp = bpy.context.evaluated_depsgraph_get()
        particle_systems = context.active_object.evaluated_get(degp).particle_systems
        psys = particle_systems[context.particle_system.name] or None
        # print("ctx name:",context.particle_system.name)
        # print("psys is none : ", psys == None)

        pset = particle_get_settings(context)

        row = layout.row()
        if not context.active_object.type == "MESH":
            row.label(text='Non-mesh objects are not compatible with the exporter.',
                         icon='ERROR')
            return
        if not pset:
            row.label(text='ParticleSetting not available',
                         icon='ERROR')
            return
        if psys and pset:
            fo = None
            try:
                fo = pset.forest
            except AttributeError:
                # print("create")
                bpy.types.ParticleSettings.forest = bpy.props.PointerProperty(type=PROPERTIES_PG_forest_particle)
                fo = pset.forests
            # print("fo :", fo)
            row.prop(fo, "export_path")
            row = layout.row()
            row.prop(fo, "fi_name")

            error = False

            oprow = layout.row()
            oprow.operator(ExportParticleForest.bl_idname,
                     text="Export",
                     icon='SCENE_DATA')

            if len(pset.forest.fi_name) == 0:
                row = layout.row()
                row.label(text='Forest Item cannot be an empty string',
                         icon='ERROR')
                error = error or True

            if len(pset.forest.export_path) == 0 or os.path.isdir(bpy.path.abspath(pset.forest.export_path)):
                row = layout.row()
                row.label(text='Export path is invalid',
                         icon='ERROR')
                error = error or True

            if not pset.forest.export_path.endswith(".forest4.json"):
                row = layout.row()
                row.label(text='Wrong file extention (*.forest4.json)',
                         icon='ERROR')
                #error = error or True ## not critical

            if len(psys.particles)==0:
                row = layout.row()
                row.label(text='NO PARTICLES',
                         icon='ERROR')
                error = error or True

            oprow.enabled = not error

            # DEBUG
            # row = layout.row()
            # row.label(text=f'child_particles = {len(psys.child_particles)}')
            # row = layout.row()
            # row.label(text=f'particles = {len(psys.particles)}')
            # row = layout.row()
            # row.label(text=f'targets = {len(psys.targets)}')




addon_classes = [ExportForest,
                ImportForest,
                SCENE_OT_instance,
                PROPERTIES_PG_forest_particle,
                PANEL_PT_forest_particle,
                ExportParticleForest
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

    def make_pointer(prop_type):
        return bpy.props.PointerProperty(type=prop_type)
    bpy.types.ParticleSettings.forest = make_pointer(PROPERTIES_PG_forest_particle)


def unregister():
    for c in addon_classes:
        bpy.utils.unregister_class(c)

    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    del bpy.types.ParticleSettings.forest

if __name__ == "__main__":
    register()
