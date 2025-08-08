from dataclasses import dataclass
from typing import List, Literal, Union, Dict, Any

@dataclass
class ThermCondMaterial:
    name: str
    description: str
    conductivity_pts: List[float]

# Temperatures (K)
TEMPERATURES: List[float] = [
    0.5, 1, 2, 4, 6, 8, 10, 15, 20, 25, 30, 35, 40, 50,
    60, 70, 80, 90, 100, 120, 140, 160, 180, 200,
    250, 300, 350, 400, 450, 500
]

# ... MATERIALS tanımı aynı kalır, yukarıdan alındığı varsayılır ...

# ----------------------------
# Core math for mm-based calculation
# ----------------------------

def _interpolated_integ_value(cd: List[float], td: List[float], t: float, n: int) -> float:
    return (
        cd[n - 1] * (t - td[n]) * (t - td[n + 1]) / ((td[n - 1] - td[n]) * (td[n - 1] - td[n + 1])) +
        cd[n] * (t - td[n - 1]) * (t - td[n + 1]) / ((td[n] - td[n - 1]) * (td[n] - td[n + 1])) +
        cd[n + 1] * (t - td[n - 1]) * (t - td[n]) / ((td[n + 1] - td[n - 1]) * (td[n + 1] - td[n]))
    )

def _calc_cond_integral_mm(material: ThermCondMaterial, t: float) -> float:
    cd = material.conductivity_pts
    td = TEMPERATURES

    i = 0
    for i in range(len(td)):
        if td[i] > t:
            break
    n = i - 1
    if n == 0:
        n = 1
    if n > len(td) - 3:
        n = len(td) - 3

    num = (
        _interpolated_integ_value(cd, td, t, n) * (td[n + 1] - t) +
        _interpolated_integ_value(cd, td, t, n + 1) * (t - td[n])
    )
    den = (td[n + 1] - td[n])
    return num / den

def _area_over_length_mm(
    shape: Literal["rod", "tube", "rect"],
    units: Literal["mm", "in"],
    *,
    length: float,
    diameter: float | None = None,
    wall: float | None = None,
    width: float | None = None,
    height: float | None = None
) -> tuple[float, list[str]]:
    warnings: List[str] = []

    k = 25.4 if units == "in" else 1.0

    if length <= 0:
        raise ValueError("Length must be positive.")
    L_mm = length * k

    if shape == "rod":
        if diameter is None or diameter <= 0:
            raise ValueError("Diameter must be positive for rod.")
        d_mm = diameter * k
        a_over_l = 3.141592653589793 / 4.0 * d_mm * d_mm / L_mm

    elif shape == "tube":
        if diameter is None or diameter <= 0:
            raise ValueError("Diameter must be positive for tube.")
        if wall is None or wall <= 0:
            raise ValueError("Wall thickness must be positive for tube.")
        d_mm = diameter * k
        w_mm = wall * k
        if w_mm > d_mm / 2.0:
            w_mm = d_mm / 2.0
            warnings.append("Wall thickness too large; set to Diameter/2.")
        a_over_l = 3.141592653589793 * w_mm * (d_mm - w_mm) / L_mm

    elif shape == "rect":
        if width is None or width <= 0 or height is None or height <= 0:
            raise ValueError("Width and height must be positive for rect.")
        w_mm = width * k
        h_mm = height * k
        a_over_l = h_mm * w_mm / L_mm

    else:
        raise ValueError("shape must be one of: 'rod', 'tube', 'rect'.")

    return a_over_l, warnings

def _get_material(material: Union[int, str]) -> ThermCondMaterial:
    if isinstance(material, int):
        if not (0 <= material < len(MATERIALS)):
            raise ValueError("material index out of range.")
        return MATERIALS[material]
    else:
        name = material.strip().lower()
        for m in MATERIALS:
            if m.name.lower() == name:
                return m
        for m in MATERIALS:
            if name in m.name.lower():
                return m
        raise ValueError(f"material not found: {material}")

def compute_heat_load(
    *,
    material: Union[int, str],
    shape: Literal["rod", "tube", "rect"],
    units: Literal["mm", "in"],
    length: float,
    temp_hi: float,
    temp_lo: float,
    diameter: float | None = None,
    wall: float | None = None,
    width: float | None = None,
    height: float | None = None
) -> Dict[str, Any]:

    if not (1.0 <= temp_hi <= 500.0):
        raise ValueError("High Temperature End must be between 1 K and 500 K.")
    if not (1.0 <= temp_lo <= 500.0):
        raise ValueError("Low Temperature End must be between 1 K and 500 K.")
    if temp_lo > temp_hi:
        raise ValueError("Low temperature must be <= high temperature.")

    mat = _get_material(material)

    a_over_l_mm, warnings = _area_over_length_mm(
        shape, units,
        length=length, diameter=diameter, wall=wall, width=width, height=height
    )

    hi_int = _calc_cond_integral_mm(mat, temp_hi)
    lo_int = _calc_cond_integral_mm(mat, temp_lo)
    heat_leak_watts = (hi_int - lo_int) * a_over_l_mm

    return {
        "heat_load_watts": float(f"{heat_leak_watts:.6g}"),
        "area_over_length_mm": a_over_l_mm,
        "warnings": warnings
    }

