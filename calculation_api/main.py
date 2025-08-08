from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from calculations.thermal_conductor import compute_heat_load  # 1. koddaki fonksiyon (mm/in destekli)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # PROD: kendi domain(ler)in ile sınırla
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _to_opt_float(v) -> Optional[float]:
    """Form boş/None/string geldiğinde None döndür, sayı ise float'a çevir."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if s == "":
        return None
    # Virgüllü sayı gelirse noktaya çevirme
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

def _material_cast(material: str):
    """Material parametresini int index ya da isim olarak geçir."""
    m = material.strip()
    # Tam sayı gibi görünüyorsa index olarak dene
    if m.isdigit():
        try:
            return int(m)
        except Exception:
            pass
    return m  # isim/partial eşleşme compute_heat_load içinde yapılır

@app.post("/thermal-conductor")
async def calc(
    material: str = Form(...),
    shape: str = Form(...),                 # "rod" | "tube" | "rect"
    units: str = Form("mm"),               # "mm" | "in"  (1. kod mm tabanlı)
    length: float = Form(...),
    temp_hi: float = Form(...),
    temp_lo: float = Form(...),
    diameter: Optional[str] = Form(None),
    wall: Optional[str] = Form(None),
    width: Optional[str] = Form(None),
    height: Optional[str] = Form(None),
):
    # Normalizasyon
    shape = shape.strip().lower()
    units = units.strip().lower()

    if units not in {"mm", "in"}:
        raise HTTPException(status_code=422, detail="units must be 'mm' or 'in'.")

    if shape not in {"rod", "tube", "rect"}:
        raise HTTPException(status_code=422, detail="shape must be one of: 'rod', 'tube', 'rect'.")

    # İsteğe bağlı ölçüleri sayıya çevir
    diameter_f = _to_opt_float(diameter)
    wall_f = _to_opt_float(wall)
    width_f = _to_opt_float(width)
    height_f = _to_opt_float(height)

    # Şekil bazlı zorunluluklar
    if shape == "rod":
        if diameter_f is None:
            raise HTTPException(status_code=422, detail="For shape 'rod', 'diameter' is required.")
        width_f = height_f = wall_f = None

    elif shape == "tube":
        if diameter_f is None or wall_f is None:
            raise HTTPException(status_code=422, detail="For shape 'tube', 'diameter' and 'wall' are required.")
        width_f = height_f = None

    elif shape == "rect":
        if width_f is None or height_f is None:
            raise HTTPException(status_code=422, detail="For shape 'rect', 'width' and 'height' are required.")
        diameter_f = wall_f = None

    # Material index/isim belirle
    material_arg = _material_cast(material)

    try:
        result = compute_heat_load(
            material=material_arg,
            shape=shape,
            units=units,          # 1. kod: "mm" | "in"
            length=length,        # mm ya da inç -> fonksiyon gerekli dönüşümü yapıyor
            temp_hi=temp_hi,
            temp_lo=temp_lo,
            diameter=diameter_f,
            wall=wall_f,
            width=width_f,
            height=height_f,
        )
        # 1. kodun döndürdüğü anahtarlar:
        # "heat_load_watts", "area_over_length_mm", "warnings"
        return {"ok": True, "result": result}

    except ValueError as ve:
        # Hesap/validasyon kaynaklı hatalar
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        # Beklenmeyen hatalar
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
