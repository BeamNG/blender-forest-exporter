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
    file.write("{\n \"format\":\"Json Forest Data v1\",\n \"" + object_name + "\":[\n")
    
    for ob in data_source:
      uniform_scale = (ob.scale[0] + ob.scale[1] + ob.scale[2]) / 3
      
      # get euler and rotate 180 deg
      object_euler = ob.rotation_euler.copy()
      object_euler.rotate_axis('Z', math.radians(180))
      object_quaternion = object_euler.to_quaternion()
      
      # write to file
      file.write("   [" + str(ob.location[0]) + ", " + str(ob.location[1]) + ", " + str(ob.location[2])  + ", " + str(object_quaternion[2]) + ", " + str(object_quaternion[1] * -1) + ", " + str(object_quaternion[0]) + ", " + str(object_quaternion[3]) + ", " + str(uniform_scale) + "],\n")
    
    # go before last comma to prevent parser from dying
    file.seek(file.tell() - 3, 0)
    file.write("\n ]\n")
    
    file.write("}")
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
