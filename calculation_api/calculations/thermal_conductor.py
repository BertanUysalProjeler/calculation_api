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

MATERIALS: List[ThermCondMaterial] = [
    ThermCondMaterial("Aluminum, 1100", "Soft, poor machining, not heat treatable; highest conductivity for commercial Al alloy",
        [0.016875,0.0675,0.27,1.08,2.43532181885964,4.40755023204499,6.96112317953368,15.8341522660986,28.2765336058801,43.8454183286148,61.6453543409714,80.693707601351,100.165442370595,138.271024662989,173.650868382336,205.923223848732,235.454086174725,262.791216324893,288.453946891025,336.383104573094,381.662867060024,425.662217682524,469.095843042739,512.280240503752,619.561290522816,725.769417902629,832.441084278078,945.006760327102,1074.92399492464,1245.43309292574]),
    ThermCondMaterial("Aluminum, 2024-T4", "Strong, very hard, heat treatable; very low conductivity when NOT annealed",
        [1.60E-04,9.07E-04,5.13E-03,2.90E-02,8.00E-02,1.97E-01,3.47E-01,8.72E-01,1.60E+00,2.51E+00,3.61E+00,4.91E+00,6.41E+00,9.91E+00,1.31E+01,1.79E+01,2.42E+01,3.01E+01,3.63E+01,5.01E+01,6.54E+01,8.21E+01,1.00E+02,1.19E+02,1.71E+02,2.29E+02,2.87E+02,3.45E+02,4.03E+02,4.61E+02]),
    ThermCondMaterial("Aluminum, 6061-T6", "Common, easy to machine, heat treatable; rather high conductivity",
        [0.0015,5.8751697170814E-03,2.45571395478167E-02,0.10328310872689,0.239511275704874,0.434784425613571,0.689562696713278,1.58427420699916,2.8355183997464,4.42427976885525,6.33018812425266,8.53336877202946,11.0151796763856,16.747132615283,23.4049214358638,30.8875307773926,39.1100225666763,48.0010158296701,57.4990343276726,78.1121529498841,100.60252924055,124.698514170434,150.182204850559,176.872874381664,247.938052625077,323.792289154032,403.069731433591,484.707699165312,567.855590027409,651.80555686512]),
    ThermCondMaterial("Beryllium Copper", "Contains 2% Be, heat treated for higher conductivity; used for non-magnetic springs",
        [9.42E-05,5.33E-04,3.02E-03,1.71E-02,4.70E-02,1.13E-01,1.89E-01,4.99E-01,9.54E-01,1.55E+00,2.29E+00,3.16E+00,4.15E+00,6.50E+00,9.30E+00,1.25E+01,1.60E+01,1.99E+01,2.40E+01,3.30E+01,4.32E+01,5.44E+01,6.64E+01,7.91E+01,1.13E+02,1.50E+02,1.87E+02,2.24E+02,2.61E+02,2.98E+02]),
    ThermCondMaterial("Brass, C260", "Cartridge Brass (70Cu, 30Zn) poor machining compared to leaded brass (30%)",
        [1.06E-04,6.01E-04,3.40E-03,1.92E-02,5.30E-02,1.29E-01,2.29E-01,5.94E-01,1.12E+00,1.81E+00,2.65E+00,3.63E+00,4.76E+00,7.36E+00,1.04E+01,1.39E+01,1.77E+01,2.20E+01,2.65E+01,3.65E+01,4.78E+01,6.03E+01,7.38E+01,8.83E+01,1.28E+02,1.72E+02,2.16E+02,2.60E+02,3.04E+02,3.48E+02]),
    ThermCondMaterial("Copper, C101", "Annealed 'Oxygen Free Electronic' (OFE) grade, 99.99%; highest conductivity stock copper",
        [3.25E-02,1.84E-01,1.04E+00,5.88E+00,1.62E+01,4.02E+01,7.17E+01,1.73E+02,2.90E+02,4.08E+02,5.20E+02,6.22E+02,7.05E+02,8.30E+02,9.19E+02,9.91E+02,1.05E+03,1.10E+03,1.16E+03,1.25E+03,1.34E+03,1.42E+03,1.51E+03,1.59E+03,1.80E+03,2.00E+03,2.20E+03,2.40E+03,2.60E+03,2.80E+03]),
    ThermCondMaterial("Copper, C110", "Electrolytic Tough Pitch (ETP) typically used for magnet wire",
        [1.60E-02,9.07E-02,5.13E-01,2.90E+00,8.00E+00,1.91E+01,3.32E+01,8.02E+01,1.40E+02,2.08E+02,2.78E+02,3.45E+02,4.06E+02,5.18E+02,5.87E+02,6.51E+02,7.07E+02,7.56E+02,8.02E+02,8.91E+02,9.76E+02,1.06E+03,1.14E+03,1.22E+03,1.42E+03,1.62E+03,1.82E+03,2.02E+03,2.22E+03,2.42E+03]),
    ThermCondMaterial("Copper, C122", "Phosphorous Deoxidized (PDO), 0.27%P; very common for drawn tube. Do not mistake for OFE!!",
        [3.53E-04,2.00E-03,1.13E-02,6.39E-02,1.76E-01,4.37E-01,7.85E-01,2.08E+00,3.95E+00,6.35E+00,9.25E+00,1.26E+01,1.64E+01,2.53E+01,3.55E+01,4.68E+01,5.89E+01,7.20E+01,8.58E+01,1.15E+02,1.46E+02,1.80E+02,2.15E+02,2.53E+02,3.53E+02,4.61E+02,5.69E+02,6.77E+02,7.85E+02,8.93E+02]),
    ThermCondMaterial("Cupro-Nickel", "'German Silver' (70Cu, 30Ni); less magnetic than stainless; easy to soft solder",
        [7.69E-05,3.61E-04,1.69E-03,7.94E-03,1.96E-02,5.24E-02,1.00E-01,3.00E-01,6.13E-01,1.02E+00,1.53E+00,2.11E+00,2.75E+00,4.15E+00,5.68E+00,7.28E+00,8.93E+00,1.06E+01,1.23E+01,1.57E+01,1.92E+01,2.29E+01,2.66E+01,3.06E+01,4.15E+01,5.32E+01,6.49E+01,7.66E+01,8.83E+01,1.00E+02]),
    ThermCondMaterial("Fiberglass-Epoxy N", "Often called G-10; normal to direction of fibers",
        [8.24957911384306E-05,2.33333333333333E-04,6.59966329107444E-04,1.86666666666667E-03,3.42928563989645E-03,5.27973063285955E-03,7.37864787372622E-03,1.35746476059748E-02,2.08788608001044E-02,2.91738558252242E-02,3.83348600178165E-02,4.82486470818733E-02,5.88195765956022E-02,8.16359914942038E-02,0.106331137349874,0.132623213076186,0.160343232278887,0.189393375072314,0.219722648417311,0.284152461291619,0.353659662553159,0.428418901107529,0.50866620863459,0.594656278028296,0.836386364769244,1.11901847794652,1.44502488684207,1.8156585099119,2.23087946545057,2.68937360821969]),
    ThermCondMaterial("Fiberglass-Epoxy W", "Often called G-10; warp direction (in plane of fibers)",
        [1.01351971970072E-04,2.86666666666667E-04,8.10815775760574E-04,2.29333333333333E-03,4.21312235758707E-03,6.48652620608459E-03,9.06519595914936E-03,1.68076374753676E-02,2.60785089084146E-02,3.65460374909653E-02,4.80351936295053E-02,6.04490435243654E-02,7.37297103071503E-02,0.102751123179791,0.134899464774084,0.170037824528401,0.208052231828983,0.248838710864516,0.292301711111575,0.386905883455638,0.491232748555989,0.604757420168092,0.727050039306304,0.857761812830965,1.21958836075821,1.62876019414841,2.08207443617989,2.57579949070903,3.10506554893286,3.66368488350661]),
    ThermCondMaterial("Glass/Fused Silica", "Fused Silica is magnetically much cleaner than common fluxed glasses",
        [4.23E-06,2.39E-05,1.35E-04,7.66E-04,2.11E-03,4.43E-03,6.81E-03,1.31E-02,2.00E-02,2.70E-02,3.68E-02,4.71E-02,5.86E-02,8.46E-02,1.15E-01,1.51E-01,1.94E-01,2.40E-01,2.92E-01,4.08E-01,5.42E-01,6.94E-01,8.58E-01,1.03E+00,1.50E+00,1.99E+00,2.54E+00,3.14E+00,3.79E+00,4.49E+00]),
    ThermCondMaterial("Graphite (AGOT)", "Excellent thermal insulator at very low (<1K) temperatures, good conductor at room temp.",
        [6.19E-07,4.12E-06,4.37E-05,4.92E-04,1.73E-03,4.26E-03,8.69E-03,3.92E-02,1.02E-01,2.11E-01,3.84E-01,6.37E-01,9.92E-01,2.23E+00,4.18E+00,7.05E+00,1.11E+01,1.64E+01,2.34E+01,2.03E+02,2.25E+02,2.51E+02,2.81E+02,3.13E+02,3.98E+02,4.93E+02,5.93E+02,6.88E+02,7.73E+02,8.48E+02]),
    ThermCondMaterial("Helium Gas", "Remember to include conductivity of container!",
        [1.08E-05,3.26E-05,9.89E-05,3.00E-04,5.74E-04,9.09E-04,1.30E-03,2.49E-03,3.94E-03,5.63E-03,7.54E-03,9.64E-03,1.19E-02,1.71E-02,2.28E-02,2.92E-02,3.62E-02,4.37E-02,5.17E-02,6.92E-02,8.86E-02,1.10E-01,1.32E-01,1.57E-01,2.24E-01,3.00E-01,4.48E-01,6.34E-01,8.61E-01,1.13E+00]),
    ThermCondMaterial("Kapton", "Polyimide film. Often used for tape and flexibile circuits.",
        [1.27279220613579E-05,0.000036,1.01823376490863E-04,0.000288,5.18049227320498E-04,8.27586574268237E-04,1.24218733224932E-03,2.74569579465893E-03,4.85821342169809E-03,7.50578079780033E-03,0.010632800930054,1.41972887298281E-02,1.81649420564764E-02,2.71935999150097E-02,3.75099935075766E-02,4.89334228498581E-02,6.13058418520326E-02,7.44901960604812E-02,8.83689912117728E-02,0.117829336932119,0.149070569634346,0.181671827330767,0.215350511239022,0.249924434782768,0.339627164522996,0.433518508092899,0.531537382745492,0.633837357301815,0.74055885940406,0.851727451741317]),
    ThermCondMaterial("Manganin", "Resistance wire (84Cu, 12Mn, 4Ni); the nickel causes significant paramagnetism",
        [1.56E-05,8.80E-05,4.98E-04,2.82E-03,7.76E-03,1.59E-02,2.78E-02,7.67E-02,1.57E-01,2.75E-01,6.35E-01,1.06E+00,1.54E+00,2.58E+00,3.74E+00,4.98E+00,6.28E+00,7.61E+00,8.98E+00,1.18E+01,1.47E+01,1.78E+01,2.10E+01,2.43E+01,3.34E+01,4.38E+01,5.42E+01,6.46E+01,7.50E+01,8.54E+01]),
    ThermCondMaterial("Nylon", "Consider 'Delrin' for better machinability; brittle at low temp",
        [0.0000304375,3.59380265471007E-05,8.29396893000951E-05,2.71374171949976E-04,5.91295828253312E-04,1.0752255278658E-03,1.7517134964497E-03,4.4099546554969E-03,8.55906986858449E-03,1.42021324232104E-02,0.021251997750382,2.95815764294546E-02,3.90523720946805E-02,6.08849081689193E-02,8.57988741580463E-02,0.113045669093751,0.142055539920703,0.172403426739816,0.203767577313671,0.268638184040334,0.335346299813374,0.403102813143605,0.47142057649774,0.539983886176568,0.711229448566996,0.880850426839316,1.04776850415941,1.21122981792614,1.37062517457565,1.52542437817141]),
    ThermCondMaterial("Plexiglass", "Also called Lucite or Perspex",
        [3.61E-06,2.04E-05,1.15E-04,6.53E-04,1.80E-03,2.38E-03,3.59E-03,6.69E-03,1.01E-02,1.44E-02,1.96E-02,2.59E-02,3.30E-02,4.90E-02,6.80E-02,8.80E-02,1.10E-01,1.32E-01,1.55E-01,2.00E-01,2.47E-01,2.94E-01,3.42E-01,3.90E-01,5.10E-01,6.30E-01,7.50E-01,8.70E-01,9.90E-01,1.11E+00]),
    ThermCondMaterial("Sapphire", "Highest conductivity non-metallic constr. material, hard to make good thermal contact",
        [8.68E-04,7.81E-03,1.19E-01,1.90E+00,7.90E+00,1.99E+01,3.59E+01,1.36E+02,3.36E+02,5.86E+02,8.71E+02,1.17E+03,1.47E+03,2.02E+03,2.37E+03,2.52E+03,2.61E+03,2.67E+03,2.72E+03,2.78E+03,2.82E+03,2.85E+03,2.87E+03,2.88E+03,2.91E+03,2.92E+03,2.93E+03,2.94E+03,2.95E+03,2.96E+03]),
    ThermCondMaterial("Silicon Bronze, C655", "Very low thermal conductivity for an alloy without ferromagnetic constituents",
        [1.56E-05,8.84E-05,5.00E-04,2.83E-03,7.79E-03,1.60E-02,4.10E-02,1.41E-01,2.88E-01,4.81E-01,7.18E-01,1.00E+00,1.33E+00,2.09E+00,2.99E+00,4.01E+00,5.13E+00,6.35E+00,7.66E+00,1.05E+01,1.36E+01,1.69E+01,2.04E+01,2.41E+01,3.39E+01,4.44E+01,5.49E+01,6.54E+01,7.59E+01,8.64E+01]),
    ThermCondMaterial("Stainless Steel, 304", "Cold working this material makes it somewhat magnetic; useful for thinwall tubes",
        [0.00002025,1.54381244119581E-04,8.57905607947959E-04,4.57728817179166E-03,1.19202142093872E-02,2.33159611490163E-02,3.91026380753079E-02,9.94302741175732E-02,0.191522892399365,0.31639394335982,0.473823928465527,0.662797545321145,0.881828882963249,1.40302295768236,2.02292450687929,2.72789006670903,3.50604631195493,4.34757300128534,5.24441722339141,7.17970842612179,9.27495521996483,11.5072644813951,13.8628315349985,16.3334924504469,22.9887432333727,30.3115431557216,38.2948742046665,46.9239549435092,56.1643139720276,65.9564021216657]),
    ThermCondMaterial("Teflon, PTFE", "Cold flows at room temp; loses good bearing properties at low temp",
        [0.000015,0.00006,0.00024,0.00096,2.08696135728817E-03,3.58024013247752E-03,5.36293402566235E-03,1.08093465673451E-02,1.74120235370583E-02,2.49669622598556E-02,3.33110418622051E-02,4.23054223456478E-02,5.18340732017045E-02,7.21366410228598E-02,9.36729730637822E-02,0.116103496346194,0.139217435242036,0.162881220928695,0.187006724597332,0.236413115451386,0.287093645046031,0.338803568183988,0.391334029487984,0.444500502588292,0.579195619811766,0.715193550866194,0.852102438804067,0.990907881093699,1.13392433326284,1.28484896240762])
]

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
    heat_leak_watts = (hi_int - lo_int) * (a_over_l_mm / 10)

    return {
        "heat_load_watts": float(f"{heat_leak_watts:.3g}"),
        "area_over_length_mm": a_over_l_mm,
        "warnings": warnings
    }



