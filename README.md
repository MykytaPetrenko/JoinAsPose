# Join As Pose Addon for Blender

The Join As Pose addon allows attaching the rest pose from one or multiple source armatures to a single target armature.

## How to Use

1. First, select the armature objects from which the rest pose will be transferred.
2. Then, choose the target armature where the keyframe poses will be created.

> [!IMPORTANT]
> The target armature must be the active object (by default in Blender, it's highlighted in a certain color, white if I remember correctly, please verify). The source objects are the other selected objects, which are outlined in a different color (also verify this color).

3. Next, choose the keyframe from which the creation of keys will start.
4. Specify the keyframe step if multiple keyframes are intended to be created.
5. Enable Rest Keyframe if you wish to create a keyframe for the rest pose of the target skeleton.
6. Optionally, you can lock the rotation and scale of bones. This may be necessary for subsequent export to game engines, as they usually handle scale differently, and animations may not display as they do in Blender. Also, corrective poses are often tied to rotation, so additional rotation might adversely affect the outcome. In short, try different options for lock rotation and lock scale if something in the game engine looks significantly different from Blender.
7. Lastly, click the "Join As Pose" button.

> [!NOTE]
> Binding is based on bone names, so for correct operation, the names must match.

## Parameters
- **Method** is the method for transferring bone transforms.
   - *"Use Matrices"* (Recommended) transfers **exact rest poses** from the source armatures. Might be a bit slow for huge skeletons (1000 bones or so).
   - *"Use Constraints"* (Faster) transfers current poses from the source armature (NOT THE REST). All constraints from the target skeleton (active object) will be cleared. Should be considered if you have a huge armature and need to join a lot of source armatures, or need to transfer transforms from the current pose, not from the rest one.
- **Lock Rotation** - keeps original rotations of the target skeleton bones if enabled.
- **Lock Scale** - keeps original scale of the target skeleton bones if enabled.
- **Frame Step** is the step between frames if joining a few armatures.
- **Rest Keyframe** - creates a key for the rest pose of the target skeleton if enabled.

## Feedback and Support
Join our [Discord Server to](https://discord.gg/zGDqh2CsbJ) share your feedback and ask for help. **Please use right channel for feedback and suppor as I have a few add-ons.**

Also visit my [youtube channel](https://www.youtube.com/@squeezypixels) and [gumroad page](https://squeezypixels.gumroad.com/l/shapekeywrap) If you liked the addon

## Another Add-ons
- **[MetaReForge](https://www.artstation.com/a/32654843)** - Paid add-on for Metahuman customization in blender
- **[ShapeKeyWrap](https://github.com/MykytaPetrenko/ShapeKeyWrap)** - Free add-on for transfering shapekeys from on mesh to another one and binding thier values.