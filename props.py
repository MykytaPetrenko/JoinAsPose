import bpy


class JASP_config(bpy.types.PropertyGroup):
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


def register():
    bpy.utils.register_class(JASP_config)
    bpy.types.Scene.join_as_pose_config = bpy.props.PointerProperty(type=JASP_config)

def unregister():
    del bpy.types.Scene.join_as_pose_config
    bpy.utils.unregister_class(JASP_config)
