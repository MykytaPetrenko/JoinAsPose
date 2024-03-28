import bpy
from mathutils import Matrix, Vector


def create_pose_bone_keys(
        pose_bone: bpy.types.PoseBone,
        frame: int,
        loc: bool = True,
        rot: bool = True,
        scale: bool = True
) -> None:
    if loc:
        pose_bone.keyframe_insert("location", frame=frame)
    if rot:
        if pose_bone.rotation_mode == "QUATERNION":
            pose_bone.keyframe_insert("rotation_quaternion", frame=frame)
        else:
            # Rotation mode Euler XYZ
            pose_bone.keyframe_insert("rotation_euler", frame=frame)
    if scale:
        pose_bone.keyframe_insert("scale", frame=frame)


def join_as_pose(
        context: bpy.types.Context,
        source_obj: bpy.types.Object,
        dest_obj: bpy.types.Object,
        frame: int,
        lock_rotation: bool
    ) -> None:
    ones = Vector.Fill(3, 1)
    # Iterate over each bone in the source armature
    for source_bone in source_obj.data.bones:
        # Get the destination bone with the same name
        dest_bone: bpy.types.PoseBone = dest_obj.pose.bones.get(source_bone.name)
        if dest_bone is not None:
            if lock_rotation:
                s_loc = source_bone.matrix_local.to_translation()
                d_rot = dest_bone.bone.matrix_local.to_quaternion()
                dest_bone.matrix = Matrix.LocRotScale(s_loc, d_rot, ones)
            else:
                s_loc, s_rot, _ = source_bone.matrix_local.decompose()
                d_rot = dest_bone.bone.matrix_local.to_quaternion()
                dest_bone.matrix = Matrix.LocRotScale(s_loc, d_rot, ones)
                context.view_layer.update()
                dest_bone.matrix = Matrix.LocRotScale(s_loc, s_rot, ones)
            
            # Update view layer (!IMPORTANT)
            context.view_layer.update()
            create_pose_bone_keys(dest_bone, frame, scale=False)
  

class SWT_POSE_OT_join_as_pose(bpy.types.Operator):
    bl_idname = "sw_tools.join_as_pose"
    bl_label = "Join as Pose"
    bl_description = "Join one armature to another as a pose"

    original_keyframe: bpy.props.BoolProperty(
        name="Original Keyframe",
        default=False,
        description="Creaates a key for original bone locations and rotations"
    )
    lock_rotation: bpy.props.BoolProperty(
        name="Lock Rotation",
        default=False,
        description="Keep original rotations of the target skeleton bones"
    )
    frame_step: bpy.props.IntProperty(
        name="Frame Step",
        default=10,
        min=1,
        description="Step between frame if joining a few armatures"
    )
    
    @classmethod
    def poll(cls, context):
        objs = context.selected_objects
        if len(objs) < 2:
            return False
        if context.active_object.type != "ARMATURE":
            return False
        if any([obj.type != 'ARMATURE' for obj in objs]):
            return False
        return True

    def execute(self, context):
        frame = context.scene.frame_current
        dest_obj = context.object
        
        if self.original_keyframe:
            join_as_pose(context, dest_obj, dest_obj, frame, self.lock_rotation)
            frame += self.frame_step
            context.scene.frame_current = frame
        
        for obj in context.selected_objects:
            if obj == context.object:
                continue
            join_as_pose(context, obj, dest_obj, frame, self.lock_rotation)
            frame += self.frame_step
            context.scene.frame_current = frame
            context.view_layer.update()
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(SWT_POSE_OT_join_as_pose)

def unregister():
    bpy.utils.unregister_class(SWT_POSE_OT_join_as_pose)
