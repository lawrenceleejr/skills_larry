"""Professional lighting helpers for Blender.

Defaults to warm, soft light and uses the per-light color-temperature control
available in recent Blender (4.2+/5.x). Falls back to a Kelvin->RGB conversion
on older builds.
"""
from __future__ import annotations

import math

import bpy


def kelvin_to_rgb(kelvin: float) -> tuple[float, float, float]:
    """Approximate blackbody color (linear-ish RGB) for a Kelvin value.

    Fallback for Blender builds without native light temperature.
    """
    t = kelvin / 100.0
    # Red
    if t <= 66:
        r = 255.0
    else:
        r = 329.698727446 * ((t - 60) ** -0.1332047592)
    # Green
    if t <= 66:
        g = 99.4708025861 * math.log(t) - 161.1195681661 if t > 0 else 0.0
    else:
        g = 288.1221695283 * ((t - 60) ** -0.0755148492)
    # Blue
    if t >= 66:
        b = 255.0
    elif t <= 19:
        b = 0.0
    else:
        b = 138.5177312231 * math.log(t - 10) - 305.0447927307

    def clamp(x: float) -> float:
        return max(0.0, min(255.0, x)) / 255.0

    return clamp(r), clamp(g), clamp(b)


def set_temperature(light_data: bpy.types.Light, kelvin: float) -> None:
    """Set a light's color temperature, using the native control when present."""
    if hasattr(light_data, "use_temperature"):
        # Blender 4.2+ / 5.x: native Kelvin control.
        light_data.use_temperature = True
        light_data.temperature = kelvin
    else:
        light_data.color = kelvin_to_rgb(kelvin)


def add_area_light(
    name: str,
    location: tuple[float, float, float],
    *,
    look_at: tuple[float, float, float] = (0.0, 0.0, 0.0),
    size: float = 4.0,
    power: float = 300.0,
    kelvin: float = 3200.0,
) -> bpy.types.Object:
    """Add a soft area light aimed at a target. Large size => soft shadows."""
    data = bpy.data.lights.new(name=name, type="AREA")
    data.shape = "DISK"
    data.size = size          # large area = soft shadows
    data.energy = power
    set_temperature(data, kelvin)

    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    _aim(obj, look_at)
    return obj


def _aim(obj: bpy.types.Object, target: tuple[float, float, float]) -> None:
    import mathutils

    direction = mathutils.Vector(target) - mathutils.Vector(obj.location)
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def three_point_warm(
    target: tuple[float, float, float] = (0.0, 0.0, 0.0),
    *,
    key_kelvin: float = 3000.0,
    fill_kelvin: float = 3500.0,
    rim_kelvin: float = 4500.0,
    scale: float = 1.0,
) -> list[bpy.types.Object]:
    """Warm, soft three-point setup: strong key, gentle fill, cool-ish rim.

    Returns the key, fill, and rim light objects.
    """
    key = add_area_light(
        "key", (4 * scale, -4 * scale, 5 * scale),
        look_at=target, size=5 * scale, power=600, kelvin=key_kelvin,
    )
    fill = add_area_light(
        "fill", (-5 * scale, -2 * scale, 3 * scale),
        look_at=target, size=7 * scale, power=180, kelvin=fill_kelvin,
    )
    rim = add_area_light(
        "rim", (0.0, 5 * scale, 4 * scale),
        look_at=target, size=3 * scale, power=400, kelvin=rim_kelvin,
    )
    return [key, fill, rim]
