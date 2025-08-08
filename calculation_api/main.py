
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from calculations.thermal_conductor import compute_heat_load

app = FastAPI()

# Wix’ten gelen istekler için CORS aç
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Prod'da sadece wix siteni yazman gerek
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/thermal-conductor")
async def calc(
    material: str = Form(...),
    shape: str = Form(...),
    units: str = Form("mm"),
    length: float = Form(...),
    temp_hi: float = Form(...),
    temp_lo: float = Form(...),
    diameter: float = Form(None),
    wall: float = Form(None),
    width: float = Form(None),
    height: float = Form(None)
):
    try:
        result = compute_heat_load(
            material=material,
            shape=shape,
            units=units,
            length=length,
            temp_hi=temp_hi,
            temp_lo=temp_lo,
            diameter=diameter,
            wall=wall,
            width=width,
            height=height
        )
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

