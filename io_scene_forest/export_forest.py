# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under Creative Commons BY-NC-SA:
# https://creativecommons.org/licenses/by-nc-sa/3.0/
#
# Copyright (C) Dummiesman, 2016
#
# ##### END LICENSE BLOCK #####

import os, time, math
import bpy , mathutils

######################################################
# EXPORT MAIN FILES
######################################################
def export_forest(file, object_name, data_source):
  items = []
  for ob in data_source:
    uniform_scale = (ob.scale[0] + ob.scale[1] + ob.scale[2]) / 3

    # get euler and rotate 180 deg
    object_euler = ob.rotation_euler.copy()
    object_euler.rotate_axis('Z', math.radians(180))
    object_quaternion = object_euler.to_quaternion()

    items.append('["' + object_name + '",' + str(ob.location[0]) + ',' + str(ob.location[1]) + ',' + str(ob.location[2])  + ',' + str(object_quaternion[2]) + ',' + str(object_quaternion[1] * -1) + ',' + str(object_quaternion[0]) + "," + str(object_quaternion[3]) + "," + str(uniform_scale) + "]")

  # write to file
  file.write('{"header":{"format":"JSON Forest Data v3","format description":"datablockName, posX, posY, posZ, rotX, rotY, rotZ, rotW, scale","version":3},"data":[' + "\n")
  file.write(",\n".join(items))
  file.write("\n]}\n")
  file.close()
  return


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
