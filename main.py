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


class TripResponse(BaseModel):
    trip_id: str
    route: List[LocationData]


class ManualStop(BaseModel):
    name: str
    transport_mode: str = "flight"


class ManualRouteRequest(BaseModel):
    stops: List[ManualStop]


# --- 静态资源配置 ---
# 1. 确保 assets 文件夹存在
os.makedirs("assets", exist_ok=True)

# 2. 挂载静态文件目录 (让前端能通过 http://localhost:8000/assets/xxx.png 访问)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


# --- 接口定义 ---

# 接口 1: 单点搜索 (左上角)
@app.get("/api/search")
async def search_place(q: str):
    coords = await get_coordinates(q)
    return {"name": q, "coordinates": coords}


# 接口 2: 获取 assets 文件夹下的图片列表 (新增)
@app.get("/api/assets-list")
async def get_assets_list():
    # 只返回图片文件
    files = [f for f in os.listdir("assets") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    return {"images": files}


# 接口 3: 手动路线生成 (跳过 AI)
@app.post("/api/manual-route", response_model=TripResponse)
async def manual_route_generation(request: ManualRouteRequest):
    print(f"收到手动路线请求: {len(request.stops)} 个站点")

    final_route = []

    for stop in request.stops:
        # 复用之前的坐标查询函数
        coords = await get_coordinates(stop.name)

        final_route.append({
            "name": stop.name,
            "coordinates": coords,
            "transport_mode": stop.transport_mode
        })

    return {
        "trip_id": "manual_trip",
        "route": final_route
    }


# 接口 4: 文本生成路线 (AI)
@app.post("/api/generate-route", response_model=TripResponse)
async def generate_route(request: TripRequest):
    return await process_trip_text(request.query)


# 接口 5: 图片上传生成路线 (OCR + AI)
@app.post("/api/upload-image", response_model=TripResponse)
async def upload_image_route(file: UploadFile = File(...)):
    print(f"Receiving Image: {file.filename}")
    contents = await file.read()

    # 1. OCR 识别
    text = ocr_image(contents)
    if not text.strip():
        raise HTTPException(status_code=400, detail="图片无法识别文字")

    print(f"Extracted Text: {text}")
    # 2. 复用逻辑处理文字
    return await process_trip_text(text)


# --- 辅助函数 ---
async def process_trip_text(text: str):
    # 1. AI 解析
    ai_result = await parse_trip_intent(text)
    locations_raw = ai_result.get("locations", [])

    final_route = []
    # 2. 查坐标
    for loc in locations_raw:
        coords = await get_coordinates(loc['name'])
        # 只有找到坐标才加入
        if coords != [0, 0]:
            final_route.append({
                "name": loc['name'],
                "coordinates": coords,
                "transport_mode": loc.get('transport_mode', 'flight')
            })

    return {
        "trip_id": "auto_gen",
        "route": final_route
    }