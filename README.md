# Travel Map AI (旅行地图生成器)

这是一个基于 Web 的全栈智能旅行路线可视化应用，旨在通过本地 AI 语义解析与 OCR 文字识别技术，自动将用户的行程描述或截图转换为 3D 地球上的动态漫游动画。项目使用 Python FastAPI 作为后端，结合 CesiumJS 构建沉浸式三维场景。

## 🚀 功能特性

### 1. 多模态智能解析

* **🤖 AI 语义理解 (Local AI)**
  * 集成 Ollama (Qwen 模型)，精准理解“先去北京，坐高铁去上海，然后飞往东京”等复杂自然语言指令。
  * 自动提取途经城市坐标与交通方式（飞机/火车/汽车）。

* **🖼️ OCR 图片识别**
  * 内置 Tesseract-OCR 引擎，支持直接上传行程单或地图截图。
  * 自动清洗识别结果并转换为结构化路线数据。

### 2. 沉浸式地图体验

* **🎬 导演模式 (Director Mode)**
  * 一键生成丝滑的路线漫游动画，支持自动跟随视角与多路段平滑过渡。
  * **动态模型切换**：根据交通类型自动加载 ✈️ 飞机、🚄 火车或 🚗 汽车 3D 图标。
  * **视频导出**：支持录制当前漫游画面并保存为 WebM 视频。

### 3. 交互与编辑

* **✏️ 混合规划模式**
  * 支持完全自动生成，也提供“手动规划”面板用于精确修正站点信息。
* **🌐 国际化支持**
  * 内置中/英双语界面，支持一键切换 UI 语言。

## 📂 项目结构

```text
travel-map/
├── index.html              # 应用入口 (UI 布局、CesiumJS 逻辑、动画控制)
├── main.py                 # 后端入口 (FastAPI 接口、静态资源挂载)
├── services.py             # 核心服务 (OCR 处理、Ollama 调用、OpenStreetMap 查询)
├── 启动.bat                # Windows 一键启动脚本 (自动激活环境并运行)
├── assets/                 # 静态资源文件夹
│   ├── car.png             # 汽车图标 (红色跑车)
│   ├── car2.png            # 备用汽车图标
│   ├── train.png           # 火车图标 (高铁)
│   └── train2.png          # 备用火车图标
├── __pycache__/            # Python 缓存文件
└── README.md               # 项目说明文档

## 🛠️ 技术栈

| 类型 | 技术/库 | 说明 |
| :--- | :--- | :--- |
| **核心** | Python 3.12 | 后端逻辑控制与胶水代码 |
| **Web框架** | FastAPI | 高性能异步 API 服务 |
| **地图引擎** | [CesiumJS](https://cesium.com/) | 开源 WebGL 3D 地球与地图可视化库 |
| **AI 模型** | Ollama (Qwen) | 本地运行的大语言模型，用于意图识别 |
| **OCR** | Tesseract | Google 开源 OCR 引擎，用于图片文字提取 |
| **UI** | TailwindCSS | 原子化 CSS 框架，快速构建界面 |

## 📦 安装与运行

由于项目依赖本地 AI 模型和 OCR 引擎，请确保环境满足以下要求。

### 1. 环境准备
* 安装 **Python 3.12+**。
* 安装并启动 **[Ollama](https://ollama.com/)**，拉取 Qwen 模型：
  ```bash
  ollama pull qwen3:8b

pip install fastapi uvicorn httpx pillow pytesseract python-multipart

# ⚠️ 关键配置：Tesseract OCR 路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\YourName\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
uvicorn main:app --reload

### 3. 数据来源、Todo 与 License 部分
请复制这段代码：

```markdown
## 🗺️ 数据来源

* **地图底图**: ArcGIS World Imagery (Esri) / OpenStreetMap
* **地理编码**: Nominatim API (OSM)
* **图标素材**: Pixel Art Vehicles (Local Assets)

## 📝 待办事项 (Todo)

* [ ] 优化 AI 提示词以支持“逗留天数”等更复杂的行程安排。
* [ ] 增加更多自定义交通工具模型（如轮船、徒步）。
* [ ] 支持导出 KML/GPX 格式的路线文件。
* [ ] 优化移动端触控体验与布局适配。

---

**License**: MIT
