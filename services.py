import httpx
import asyncio
import json
from PIL import Image
import pytesseract
import io

# ==========================================
# ⚠️ 关键配置：Tesseract OCR 路径
# ==========================================
# 必须指向 .exe 文件，而不是文件夹
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\zengh\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


# --- 1. 图片转文字 (OCR) ---
def ocr_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # 尝试识别中文和英文
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        print(f"OCR 识别结果 (前50字): {text[:50]}...")
        return text
    except Exception as e:
        print(f"OCR 出错 (可能未安装中文包，尝试仅识别英文): {e}")
        try:
            # 如果中文包没装，降级为只识别英文
            return pytesseract.image_to_string(image, lang='eng')
        except:
            return ""


# --- 2. 查坐标 (OpenStreetMap) ---
async def get_coordinates(place_name: str):
    url = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "TravelMapAI/2.0 (LocalEducationProject)",
        "Referer": "https://www.openstreetmap.org/"
    }
    params = {"q": place_name, "format": "json", "limit": 1}

    print(f"Searching Coords: {place_name}...")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params, headers=headers, timeout=10.0)
            data = resp.json()
            if data and len(data) > 0:
                return [float(data[0]["lon"]), float(data[0]["lat"])]
            return [0, 0]
        except Exception as e:
            print(f"Search Error: {e}")
            return [0, 0]


# --- 3. 意图解析 (Ollama Local AI) ---
async def parse_trip_intent(user_input: str):
    print(f"Calling Ollama: {user_input[:50]}...")
    url = "http://localhost:11434/api/chat"

    system_prompt = """
   你是一个旅行路线解析器。

    任务：
        从用户输入中，按【出发地 → 中转地 → 终点】顺序，
        提取所有出现的【城市或地名】，包括起点。

        规则：
        1. 起点必须保留，不能省略。
        2. 每一段“从 A 到 B”，A 和 B 都必须出现在 locations 中。
        3. 严格按出现顺序输出。
        4. 严格输出 JSON，不要解释。
格式：
{
  "locations": [
    {"name": "北京", "transport_mode": "flight"},
    {"name": "上海", "transport_mode": "flight"},
    {"name": "长沙", "transport_mode": "train"},
    {"name": "娄底", "transport_mode": "car"}
  ]
}
"""

    payload = {
        "model": "qwen3:8b",  # ⚠️ 如果觉得慢，改成 "qwen3:4b"
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.1}
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload)
            content = resp.json()["message"]["content"]
            print(f"Ollama Resp: {content}")
            return json.loads(content)
    except Exception as e:
        print(f"Ollama Error: {e}")
        # 降级处理
        return {"locations": [{"name": n, "transport_mode": "flight"} for n in user_input.split() if n]}