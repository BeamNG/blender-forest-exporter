# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under The MIT License:
# see LICENSE for the full license text
#
# ##### END LICENSE BLOCK #####

import os, time, math
import bpy , mathutils

######################################################
# EXPORT MAIN FILES
######################################################
def export_forest(file, object_name, data_source):
  items = []
  print("exporting items :",len(data_source))
  loc = [0.0,0.0,0.0]
  for ob in data_source:
    if isinstance(ob , bpy.types.Particle):
      uniform_scale = ob.size
      object_quaternion = ob.rotation.copy()
      e_rot = mathutils.Euler(( 0.0, 0.0, math.radians(90.0)), 'XYZ')
      object_quaternion = object_quaternion @ e_rot.to_quaternion()

      if len(ob.hair_keys) > 0:
        loc = ob.hair_keys[0].co
      else:
        loc = ob.location

    else:
      uniform_scale = (ob.scale[0] + ob.scale[1] + ob.scale[2]) / 3

      # get euler and rotate 180 deg
      object_euler = ob.rotation_euler.copy()
      object_euler.rotate_axis('Z', math.radians(180))
      object_quaternion = object_euler.to_quaternion()

      loc = ob.location

    items.append('{"type":"' + object_name + '","pos":[' + str(loc[0]) + ',' + str(loc[1]) + ',' + str(loc[2])  + '],"quat":[' + str(object_quaternion[2]) + ',' + str(object_quaternion[1] * -1) + ',' + str(object_quaternion[0]) + "," + str(object_quaternion[3]) + '],"scale":' + str(uniform_scale) + "}")

  # write to file
  file.write("\n".join(items))


######################################################
# EXPORT
######################################################
def save_forest(filepath,
               forest_item,
               selection_only,
               context):

  print("exporting forest: %r..." % (filepath))

  time1 = time.clock()

  # get data source
  data_source = bpy.data.objects
  if selection_only:
    data_source = bpy.context.selected_objects

  # write forest
  file = open(filepath, 'w')
  export_forest(file, forest_item, data_source)
  file.close()

  # forest export complete
  print(" done in %.4f sec." % (time.clock() - time1))


def save(operator,
         context,
         filepath="",
         forest_item="none",
         selection_only = False
         ):

  # check item length
  if len(forest_item) == 0:
    forest_item = "you_forgot_to_set_this"

  # save forest
  save_forest(filepath,
              forest_item,
              selection_only,
              context,
              )

  return {'FINISHED'}
