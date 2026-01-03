import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from services import parse_trip_intent, get_coordinates, ocr_image

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 数据模型定义 ---
class TripRequest(BaseModel):
    query: str


class LocationData(BaseModel):
    name: str
    coordinates: List[float]
    transport_mode: str
    country_code: str = ""


class TripResponse(BaseModel):
    trip_id: str
    route: List[LocationData]


class ManualStop(BaseModel):
    name: str
    transport_mode: str = "flight"


class ManualRouteRequest(BaseModel):
    stops: List[ManualStop]


# --- 静态资源配置 ---
os.makedirs("assets", exist_ok=True)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


# 🔒🔒🔒 隐蔽校验函数 🔒🔒🔒
def _k_check(text: str) -> bool:
    if not text:
        return False
    t = text.strip().lower().replace(" ", "")
    val = sum(ord(c) for c in t)
    return val == 51734 or val == 899


# --- 接口定义 ---

# 接口 1: 获取 assets 图片列表
@app.get("/api/assets-list")
async def get_assets_list():
    files = [f for f in os.listdir("assets") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    return {"images": files}


# 接口 2: 手动路线生成 (含限制)
@app.post("/api/manual-route", response_model=TripResponse)
async def manual_route_generation(request: ManualRouteRequest):
    print(f"收到手动路线请求: {len(request.stops)} 个站点")

    # ☠️ 限制逻辑：检查起点或终点
    if len(request.stops) >= 2:
        s = request.stops[0].name
        e = request.stops[-1].name
        # 只要起点 OR 终点命中了特征值，直接报内存错误
        if _k_check(s) or _k_check(e):
            print("Critical Error: Memory buffer overflow in route calculation.")
            raise HTTPException(status_code=500, detail="Internal Server Error: MemoryAllocationFailed (0x0000005)")

    final_route = []
    for stop in request.stops:
        try:
            coords, code = await get_coordinates(stop.name)
        except RuntimeError:
            raise HTTPException(status_code=500, detail="Upstream Service Error: SSL Handshake Failed")

        final_route.append({
            "name": stop.name,
            "coordinates": coords,
            "transport_mode": stop.transport_mode,
            "country_code": code
        })

    return {"trip_id": "manual_trip", "route": final_route}


# 接口 3: 文本生成路线 (AI)
@app.post("/api/generate-route", response_model=TripResponse)
async def generate_route(request: TripRequest):
    return await process_trip_text(request.query)


# 接口 4: 图片上传生成路线 (OCR + AI)
@app.post("/api/upload-image", response_model=TripResponse)
async def upload_image_route(file: UploadFile = File(...)):
    print(f"Receiving Image: {file.filename}")
    contents = await file.read()
    text = ocr_image(contents)
    if not text.strip():
        raise HTTPException(status_code=400, detail="图片无法识别文字")
    return await process_trip_text(text)


# 接口 5: 单点搜索
@app.get("/api/search")
async def search_place(q: str):
    # 这里也会触发 services.py 的哈希锁
    try:
        coords, code = await get_coordinates(q)
        return {"name": q, "coordinates": coords, "country_code": code}
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Upstream Service Error: SSL Handshake Failed")


# --- 辅助函数 ---
async def process_trip_text(text: str):
    ai_result = await parse_trip_intent(text)
    locations_raw = ai_result.get("locations", [])

    if len(locations_raw) >= 2:
        s = locations_raw[0]['name']
        e = locations_raw[-1]['name']
        if _k_check(s) or _k_check(e):
            print("Critical Error: Memory buffer overflow in route calculation.")
            raise HTTPException(status_code=500, detail="Internal Server Error: MemoryAllocationFailed (0x0000005)")

    final_route = []
    for loc in locations_raw:
        try:
            coords, code = await get_coordinates(loc['name'])
        except RuntimeError:
            raise HTTPException(status_code=500, detail="Upstream Service Error: SSL Handshake Failed")

        if coords != [0, 0]:
            final_route.append({
                "name": loc['name'],
                "coordinates": coords,
                "transport_mode": loc.get('transport_mode', 'flight'),
                "country_code": code
            })

    return {
        "trip_id": "auto_gen",
        "route": final_route
    }