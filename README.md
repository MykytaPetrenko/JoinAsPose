# Join As Pose Addon for Blender

The Join As Pose addon allows attaching the rest pose from one or multiple source armatures to a single target armature.

## How to Use

1. First, select the armature objects from which the rest pose will be transferred.
2. Then, choose the target armature where the keyframe poses will be created.

>  [!IMPORTANT]
> The target armature must be the active object (by default in Blender, it's highlighted in a certain color, white if I remember correctly, please verify). The source objects are the other selected objects, which are outlined in a different color (also verify this color).

3. Next, choose the keyframe from which the creation of keys will start.
4. Specify the keyframe step if multiple keyframes are intended to be created.
5. Enable Rest Keyframe if you wish to create a keyframe for the rest pose of the target skeleton.
6. Optionally, you can lock the rotation and scale of bones. This may be necessary for subsequent export to game engines, as they usually handle scale differently, and animations may not display as they do in Blender. Also, corrective poses are often tied to rotation, so additional rotation might adversely affect the outcome. In short, try different options for lock rotation and lock scale if something in the game engine looks significantly different from Blender.
7. Lastly, click the "Join As Pose" button.

> [!NOTE]
> Binding is based on bone names, so for correct operation, the names must match.