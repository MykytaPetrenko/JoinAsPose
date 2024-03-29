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


"""
Slow method
"""
def join_as_pose_via_transforms(
        context: bpy.types.Context,
        source_obj: bpy.types.Object,
        dest_obj: bpy.types.Object,
        frame: int,
        lock_rotation: bool = False,
        lock_scale: bool = False
    ) -> None:
    ones = Vector.Fill(3, 1)
    # Iterate over each bone in the source armature
    for source_bone in source_obj.data.bones:
        # Get the destination bone with the same name
        dest_bone: bpy.types.PoseBone = dest_obj.pose.bones.get(source_bone.name)
        if dest_bone is not None:
            loc = source_bone.matrix_local.to_translation()
            if lock_rotation:
                rot = dest_bone.bone.matrix_local.to_quaternion()
            else:
                rot = source_bone.matrix_local.to_quaternion()
            
            if lock_scale:
                scale = ones
            else:
                scale = ones * source_bone.length / dest_bone.bone.length 
            dest_bone.matrix = Matrix.LocRotScale(loc, rot, scale)

            # Update view layer (!IMPORTANT)
            context.view_layer.update()
            create_pose_bone_keys(dest_bone, frame)


def add_reset_pose_framekey(
        context: bpy.types.Context,
        obj: bpy.types.Object,
        frame: int
) -> None:
    # Switch to pose mode for baking
    bpy.ops.object.mode_set(mode='POSE')

    # Deselect all bones first
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.transforms_clear()
    context.view_layer.update()

    for pb in obj.pose.bones:
        create_pose_bone_keys(pb, frame)

    bpy.ops.object.mode_set(mode="OBJECT")


def join_as_pose_via_constraints(
        context: bpy.types.Context,
        source_obj: bpy.types.Object,
        dest_obj: bpy.types.Object,
        frame: int,
        lock_rotation: bool = False,
        lock_scale: bool = False
) -> None:
    # Switch to pose mode for baking
    bpy.ops.object.mode_set(mode='POSE')

    # Deselect all bones first
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.transforms_clear()
    context.view_layer.update()

    # Iterate over each bone in the source armature
    for source_bone in source_obj.data.bones:
        # Get the destination bone with the same name
        dest_bone = dest_obj.pose.bones.get(source_bone.name)
        if dest_obj is not None:
            dest_bone.bone.select = True
            # Create constraints
            c1 = dest_bone.constraints.new('COPY_LOCATION')
            c1.target = source_obj
            c1.subtarget = source_bone.name
            c1.target_space = "POSE"
            
            if not lock_rotation:
                c2 = dest_bone.constraints.new('COPY_ROTATION')
                c2.target = source_obj
                c2.subtarget = source_bone.name
                c2.target_space = "POSE"

            if not lock_scale:
                scale = source_bone.length / dest_bone.bone.length
                c3 = dest_bone.constraints.new('LIMIT_SCALE')
                c3.use_max_x, c3.use_min_x = True, True
                c3.use_max_y, c3.use_min_y = True, True
                c3.use_max_z, c3.use_min_z = True, True
                c3.min_x, c3.max_x = scale, scale
                c3.min_y, c3.max_y = scale, scale
                c3.min_z, c3.max_z = scale, scale


    # Bake the action for the entire armature for the current frame

    bpy.ops.nla.bake(
        frame_start=frame, 
        frame_end=frame, 
        only_selected=True, 
        visual_keying=True, 
        clear_constraints=True, 
        use_current_action=True, 
        bake_types={'POSE'}
    )
    
    bpy.ops.object.mode_set(mode='OBJECT')
  

class SWT_POSE_OT_join_as_pose(bpy.types.Operator):
    """
    Join one or multiple selected armatures to the selected armature as a keyframe pose.
    """
    bl_idname = "sw_tools.join_as_pose"
    bl_label = "Join as Pose"
    

    rest_keyframe: bpy.props.BoolProperty(
        name="Rest Keyframe",
        default=False,
        description="Creates a key for the rest pose of the target skeleton"
    )
    lock_rotation: bpy.props.BoolProperty(
        name="Lock Rotation",
        default=False,
        description="Keeps original rotations of the target skeleton bones if enabled"
    )
    lock_scale: bpy.props.BoolProperty(
        name="Lock Scale",
        default=False,
        description="Keeps original scale of the target skeleton bones if enabled"
    )
    frame_step: bpy.props.IntProperty(
        name="Frame Step",
        default=10,
        min=1,
        description="The step between framekeys"
    )
    use_constraints: bpy.props.BoolProperty(
        name="Use Constraints",
        default=True,
        description="Use Constraints"
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
        initial_frame = frame
        dest_obj = context.object

        # Pick join function
        if self.use_constraints:
            join_function = join_as_pose_via_constraints
        else:
            join_function = join_as_pose_via_transforms
        
        # Create the rest keyframe if needed
        if self.rest_keyframe:
            add_reset_pose_framekey(context, dest_obj, frame)
            frame += self.frame_step
            context.scene.frame_current = frame
            context.view_layer.update()
        
        # Transfer rest poses fron the other sceletons except the active one
        for obj in context.selected_objects:
            if obj == context.object:
                continue
            join_function(
                context,
                obj,
                dest_obj,
                frame,
                lock_rotation=self.lock_rotation,
                lock_scale=self.lock_scale
            )
            frame += self.frame_step
            context.scene.frame_current = frame
            context.view_layer.update()
        
        context.scene.frame_current = initial_frame
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(SWT_POSE_OT_join_as_pose)

def unregister():
    bpy.utils.unregister_class(SWT_POSE_OT_join_as_pose)
