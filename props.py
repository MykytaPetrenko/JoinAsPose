import bpy

transfer_methods = [
    (
        "MATRIX", "Use Matrices",
        "RECOMMENDED! Transfers exact rest poses from the source armatures using matrices. "
        "Might be a bit slow for huge skeletons (1000 bones or so).",
        0
    ),
    (
        "CONSTRAINT", "!Use Constraints!",
        "Transfers CURRENT poses from the source armature (NOT THE REST). "
        "All constraints from the target skeleton (active object) will be cleared. "
        "Should be considered if you have a huge armature and need to join a lot of "
        "source armatures, or need to transfer transforms from the current pose, "
        "not from the rest one.",
        1
    )
]


class JASP_config(bpy.types.PropertyGroup):
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

    method: bpy.props.EnumProperty(
        items=transfer_methods,
        name="Method",
        description=(
            "Method for transferring bone transforms. \"Use Matrices\" is more "
            "stable, but might be a bit slow for huge skeletons (1000 bones or so).\n"
            "Also \"Use Constrains\" will clear all transforms after use, so don't use it"
            "if you have constraint which you want to keep"
        )
    )


def register():
    bpy.utils.register_class(JASP_config)
    bpy.types.Scene.join_as_pose_config = bpy.props.PointerProperty(type=JASP_config)

def unregister():
    del bpy.types.Scene.join_as_pose_config
    bpy.utils.unregister_class(JASP_config)
