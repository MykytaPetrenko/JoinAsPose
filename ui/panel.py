import bpy
from ..ops.joint_as_pose import SWT_POSE_OT_join_as_pose


class SWT_VIEW3D_PT_join_as_pose(bpy.types.Panel):
    bl_label = "Join as Pose"
    bl_idname = "SWT_VIEW3D_PT_join_as_pose"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'ARMATURE'

    def draw(self, context):
        layout = self.layout
        config = context.scene.join_as_pose_config
        layout.prop(config, "lock_rotation")
        layout.prop(config, "original_keyframe")
        layout.prop(config, "frame_step")
        op_props = layout.operator(SWT_POSE_OT_join_as_pose.bl_idname)
        op_props.lock_rotation = config.lock_rotation
        op_props.frame_step = config.frame_step
        op_props.original_keyframe = config.original_keyframe

def register():
    bpy.utils.register_class(SWT_VIEW3D_PT_join_as_pose)

def unregister():
    bpy.utils.unregister_class(SWT_VIEW3D_PT_join_as_pose)