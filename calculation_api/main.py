from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Literal, Union, List, Any
import uvicorn
from calculations.thermal_conductor import compute_heat_load, MATERIALS  # Mevcut hesaplama fonksiyonunuzu ve materyal listesini içe aktarın

# FastAPI app oluştur
app = FastAPI(title="Thermal Conductance Calculator API")

# CORS middleware ekle (Frontend'den erişim için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request modeli
class ThermalRequest(BaseModel):
    material: Union[int, str]
    shape: Literal["rod", "tube", "rect"]
    units: Literal["mm", "in"] 
    temp_hi: float
    temp_lo: float
    length: float
    diameter: Optional[float] = None
    wall: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None

# Response modeli
class ThermalResponse(BaseModel):
    heat_load_watts: float
    area_over_length_mm: float
    warnings: List[str]

# Ana sayfa
@app.get("/")
async def root():
    return {
        "message": "Thermal Conductance Calculator API is running!",
        "version": "1.0",
        "endpoints": {
            "POST /calculate": "Calculate thermal conductance",
            "GET /materials": "List available materials",
            "GET /health": "Health check"
        }
    }

# Hesaplama endpoint'i
@app.post("/calculate", response_model=ThermalResponse)
async def calculate_thermal_conductance(request: ThermalRequest):
    try:
        print(f"Received request: {request}")
        
        result = compute_heat_load(  # Mevcut fonksiyonunuzu çağırıyor
            material=request.material,
            shape=request.shape,
            units=request.units,
            length=request.length,
            temp_hi=request.temp_hi,
            temp_lo=request.temp_lo,
            diameter=request.diameter,
            wall=request.wall,
            width=request.width,
            height=request.height
        )
        
        print(f"Calculation result: {result}")
        
        return ThermalResponse(
            heat_load_watts=result["heat_load_watts"],
            area_over_length_mm=result["area_over_length_mm"], 
            warnings=result["warnings"]
        )
        
    except ValueError as e:
        print(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

# Materyalleri listele
@app.get("/materials")
async def get_materials():
    return [{"index": i, "name": mat.name, "description": mat.description} 
            for i, mat in enumerate(MATERIALS)]

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

# Server çalıştır (development için)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



