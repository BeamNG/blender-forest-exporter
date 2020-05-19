# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under The MIT License:
# see LICENSE for the full license text
#
# ##### END LICENSE BLOCK #####

import bpy
import math
import mathutils
import os
import json

def load(operator, context, filepath, object_type):
    filename = os.path.basename(filepath)
    forest_item_name = filename.replace(".forest4.json","")
    if forest_item_name in bpy.data.collections:
        operator.report({'ERROR'},"Collections already exists")
        return {"CANCELLED"}

    bpy.ops.collection.create(name=forest_item_name)
    #add the collection create above to the scene tree
    context.scene.collection.children.link(bpy.data.collections[forest_item_name])

    #https://devtalk.blender.org/t/set-active-collection/2409/4
    context.view_layer.active_layer_collection = context.view_layer.layer_collection.children[-1]

    with open(filepath,"r") as f:
        for line in f:
            j = json.loads(line)
            eul = mathutils.Euler((0.0, 0.0, 0.0), 'XYZ')
            mat = mathutils.Matrix(((1.0, 0.0, 0.0),
                                    (0.0, 1.0, 0.0),
                                    (0.0, 0.0, 1.0),
                                    ))
            if "rotationMatrix" in j:
                rotm = j["rotationMatrix"]
                mat = mathutils.Matrix(((rotm[0],rotm[1],rotm[2]),
                                        (rotm[3],rotm[4],rotm[5]),
                                        (rotm[6],rotm[7],rotm[8])))
                eul = mat.to_euler()
                eul.z = -eul.z #because yes
                eul.rotate_axis('Z', math.radians(180))
            elif "quat" in j:
                q = j["quat"]
                eul = mathutils.Quaternion((q[0], q[1], q[2], q[3])).to_euler()
                eul.rotate_axis('Z', math.radians(180))
            else:
                operator.report({'ERROR'},"rotation infromation missing")
                return {"CANCELLED"}

            scale = 1
            if "scale" in j:
                scale = j["scale"]

            # bpy.ops.object.empty_add(type='ARROWS',
            #     radius=scale,
            #     align='WORLD',
            #     location=(j["pos"][0], j["pos"][1], j["pos"][2]),
            #     rotation=(eul.x, eul.y, eul.z))
            bpy.ops.object.add(type=object_type, enter_editmode=False,
                radius=scale,
                align='WORLD',
                location=(j["pos"][0], j["pos"][1], j["pos"][2]),
                rotation=(eul.x, eul.y, eul.z))
            #bpy.ops.object.collection_link(collection=forest_item_name) #not needed as it's auto linked to avtive collection

    return {'FINISHED'}