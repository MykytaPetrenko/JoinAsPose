bl_info = {
    "name": "Join as Pose",
    "author": "Mykyta Petrenko (SqeezyPixels)",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar > Tools",
    "description": "Join one armature to another as a pose",
    "warning": "",
    "wiki_url": "https://github.com/MykytaPetrenko/JoinAsPose",
    "category": "Tools",
}

from . import props
from .ops import joint_as_pose
from .ui import panel

modules = [
    props,
    joint_as_pose,
    panel
]


def register():
    for m in modules:
        m.register()


def unregister():
    for m in modules:
        m.unregister()