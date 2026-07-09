"""Blender scene builder + renderer (run with `blender -b -P render.py -- ...`).

Encodes the house style:
- Enclosing, softly-lit sphere environment (an inside-out emissive dome).
- Warm, soft professional lighting using per-light color temperature.
- Wide-angle lens + large aperture, depth of field, and motion blur on.
- A few animated cameras cut together across the timeline for nice motion.

CLI (after the `--`):
  --mode still|animation      what to render (default: animation)
  --out PATH                  file (still) or directory (animation frames)
  --samples N                 Cycles samples (default: 64)
  --res WxH                   resolution, e.g. 1280x720 (default: 1280x720)
  --start N --end N           frame range for animation (default: 1..96)
  --fps N                     frames per second metadata (default: 24)
  --device GPU|CPU            compute device (default: CPU)
  --label TEXT                optional caption placed low & readable
"""
from __future__ import annotations

import argparse
import math
import os
import sys

import bpy
import mathutils

# Make sibling modules importable when Blender runs this file.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lighting  # noqa: E402


# --------------------------------------------------------------------------- #
# args
# --------------------------------------------------------------------------- #
def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["still", "animation"], default="animation")
    p.add_argument("--out", default="output")
    p.add_argument("--samples", type=int, default=64)
    p.add_argument("--res", default="1280x720")
    p.add_argument("--start", type=int, default=1)
    p.add_argument("--end", type=int, default=96)
    p.add_argument("--fps", type=int, default=24)
    p.add_argument("--device", choices=["GPU", "CPU"], default="CPU")
    p.add_argument("--label", default="")
    return p.parse_args(argv)


# --------------------------------------------------------------------------- #
# scene
# --------------------------------------------------------------------------- #
def reset_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def enable_gpu() -> bool:
    """Turn on the best available GPU backend for Cycles. Returns True on success."""
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for backend in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
        try:
            prefs.compute_device_type = backend
        except TypeError:
            continue
        prefs.get_devices()
        gpus = [d for d in prefs.devices if d.type != "CPU"]
        if gpus:
            for d in prefs.devices:
                d.use = d.type != "CPU"  # GPU only; add CPU here to co-render
            print(f"[render] GPU backend: {backend} ({len(gpus)} device(s))")
            return True
    print("[render] no GPU backend available; using CPU")
    return False


def make_material(name, color, *, emission=0.0, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    return mat


def build_environment(radius: float = 14.0) -> None:
    """Enclose the scene in a soft, warm, inside-out emissive sphere."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=64, ring_count=32)
    dome = bpy.context.active_object
    dome.name = "LightSphere"
    bpy.ops.object.shade_smooth()
    # Flip normals so the emissive surface faces inward and lights the interior.
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode="OBJECT")
    warm = lighting.kelvin_to_rgb(3400)
    dome.data.materials.append(make_material("dome", warm, emission=1.2, roughness=1.0))

    # A second, larger diffuse shell keeps stray light contained (enclosed env).
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius + 2, segments=32, ring_count=16)
    shell = bpy.context.active_object
    shell.name = "OuterShell"
    shell.data.materials.append(make_material("shell", (0.05, 0.04, 0.03), roughness=1.0))


def build_subjects() -> bpy.types.Object:
    """A small arrangement of objects; returns the hero object for focus/orbit."""
    ground = _add_plane(size=30, z=-1.5, color=(0.18, 0.15, 0.13))
    ground.name = "Ground"

    bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 0.2))
    hero = bpy.context.active_object
    hero.name = "Hero"
    bpy.ops.object.shade_smooth()
    hero.data.materials.append(make_material("hero", (0.8, 0.3, 0.2), roughness=0.35))

    bpy.ops.mesh.primitive_torus_add(location=(2.6, 1.2, -0.4))
    t = bpy.context.active_object
    t.data.materials.append(make_material("torus", (0.85, 0.7, 0.3), roughness=0.2, metallic=1.0))

    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.8, location=(-2.4, 0.8, -0.6), subdivisions=3)
    s = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    s.data.materials.append(make_material("ball", (0.3, 0.5, 0.8), roughness=0.1))
    return hero


def _add_plane(size, z, color):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, z))
    p = bpy.context.active_object
    p.data.materials.append(make_material("ground", color, roughness=0.9))
    return p


# --------------------------------------------------------------------------- #
# cameras
# --------------------------------------------------------------------------- #
def make_camera(name, focus_obj) -> bpy.types.Object:
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = 18.0                 # wide angle
    cam_data.dof.use_dof = True          # depth of field on
    cam_data.dof.aperture_fstop = 1.4    # large aperture (shallow DOF)
    cam_data.dof.focus_object = focus_obj
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(cam)
    return cam


def track_to(cam: bpy.types.Object, target: bpy.types.Object) -> None:
    c = cam.constraints.new(type="TRACK_TO")
    c.target = target
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"


def animate_cameras(hero, start, end):
    """Create three cameras with distinct motion, cut together via markers."""
    scene = bpy.context.scene
    seg = (end - start) // 3

    # Orbit camera: parented to an empty that spins.
    pivot = bpy.data.objects.new("orbit_pivot", None)
    bpy.context.collection.objects.link(pivot)
    pivot.location = hero.location
    cam_orbit = make_camera("cam_orbit", hero)
    cam_orbit.parent = pivot
    cam_orbit.location = (0, -9, 2.5)
    track_to(cam_orbit, hero)
    pivot.rotation_euler = (0, 0, 0)
    pivot.keyframe_insert("rotation_euler", frame=start)
    pivot.rotation_euler = (0, 0, math.radians(120))
    pivot.keyframe_insert("rotation_euler", frame=start + seg)

    # Dolly-in camera.
    cam_dolly = make_camera("cam_dolly", hero)
    track_to(cam_dolly, hero)
    cam_dolly.location = (6, -6, 1.5)
    cam_dolly.keyframe_insert("location", frame=start + seg)
    cam_dolly.location = (2.5, -2.5, 0.8)
    cam_dolly.keyframe_insert("location", frame=start + 2 * seg)

    # Crane/rise camera.
    cam_crane = make_camera("cam_crane", hero)
    track_to(cam_crane, hero)
    cam_crane.location = (-5, -5, 0.2)
    cam_crane.keyframe_insert("location", frame=start + 2 * seg)
    cam_crane.location = (-3, -3, 4.5)
    cam_crane.keyframe_insert("location", frame=end)

    _linear_fcurves()

    # Bind cameras to timeline segments with markers (multi-camera cuts).
    for frame, cam in (
        (start, cam_orbit),
        (start + seg, cam_dolly),
        (start + 2 * seg, cam_crane),
    ):
        m = scene.timeline_markers.new(f"cut_{cam.name}", frame=frame)
        m.camera = cam
    scene.camera = cam_orbit
    return [cam_orbit, cam_dolly, cam_crane]


def _linear_fcurves():
    for action in bpy.data.actions:
        for fc in _action_fcurves(action):
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def _action_fcurves(action):
    """Yield every F-curve in `action`, across Blender versions.

    Blender 4.4 introduced slotted (layered) actions and 5.0 removed the direct
    `Action.fcurves` accessor; F-curves now live under layers -> strips ->
    channelbags. Fall back to the legacy flat accessor when present.
    """
    fcurves = getattr(action, "fcurves", None)
    if fcurves is not None:
        yield from fcurves
        return
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for cbag in getattr(strip, "channelbags", []):
                yield from cbag.fcurves


# --------------------------------------------------------------------------- #
# label
# --------------------------------------------------------------------------- #
def add_label(text: str, camera: bpy.types.Object) -> None:
    """Add a readable caption parented to `camera`, placed low in frame.

    A FONT object's readable face points along +Z with "up" along +Y, matching a
    camera's local axes (it looks down -Z, up +Y). So with identity rotation the
    text faces straight back at the camera, upright — no extra rotation needed.
    NOTE: with a large aperture the shallow DOF will soften a camera-close caption;
    for a crisp caption composite it in 2D or render a label pass without DOF. The
    inspection loop is expected to catch and fix caption readability.
    """
    tdata = bpy.data.curves.new(name="label", type="FONT")
    tdata.body = text
    tdata.align_x = "CENTER"
    obj = bpy.data.objects.new("Label", tdata)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(make_material("label", (1, 1, 1), emission=3.0))
    # In front of (-Z) and below (-Y) the optical axis, in the lower third.
    obj.parent = camera
    obj.location = (0.0, -0.42, -1.6)
    obj.scale = (0.12, 0.12, 0.12)


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #
def configure_render(args) -> None:
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    if args.device == "GPU" and enable_gpu():
        scene.cycles.device = "GPU"
    else:
        scene.cycles.device = "CPU"

    w, h = (int(x) for x in args.res.lower().split("x"))
    scene.render.resolution_x = w
    scene.render.resolution_y = h
    scene.render.resolution_percentage = 100
    scene.render.fps = args.fps

    # Motion blur on.
    scene.render.use_motion_blur = True
    scene.render.motion_blur_shutter = 0.5

    scene.render.image_settings.file_format = "PNG"
    scene.frame_start = args.start
    scene.frame_end = args.end


def main() -> None:
    args = parse_args()
    reset_scene()
    build_environment()
    hero = build_subjects()
    lighting.three_point_warm(target=tuple(hero.location))
    cams = animate_cameras(hero, args.start, args.end)
    if args.label:
        # Label every camera used, so the caption stays in frame across cuts
        # (animation). For a still only the active camera is rendered.
        targets = cams if args.mode == "animation" else [bpy.context.scene.camera]
        for cam in targets:
            add_label(args.label, cam)
    configure_render(args)

    if args.mode == "still":
        out = args.out if args.out.endswith(".png") else args.out + ".png"
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        bpy.context.scene.render.filepath = os.path.abspath(out)
        bpy.ops.render.render(write_still=True)
        print(f"[render] wrote {out}")
    else:
        os.makedirs(args.out, exist_ok=True)
        bpy.context.scene.render.filepath = os.path.join(os.path.abspath(args.out), "frame_")
        bpy.ops.render.render(animation=True)
        print(f"[render] wrote frames to {args.out}/frame_####.png")


if __name__ == "__main__":
    main()
