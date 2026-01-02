Travel Map AI (旅行地图生成器)这是一个基于 Web 的智能旅行路线可视化应用，旨在通过 AI 语义解析与 OCR 文字识别，自动将用户的行程描述或截图转换为 3D 地球上的动态漫游路线。项目结合了 Python FastAPI 后端与 CesiumJS 前端，支持沉浸式的“导演模式”动画演示。🚀 功能特性1. 多模态输入解析🤖 AI 智能语义理解集成本地 Ollama (Qwen 模型)，能够精准理解“先去北京，坐高铁去上海，然后飞往东京”等复杂的自然语言指令。自动提取途经城市与交通方式（飞机/火车/汽车）。🖼️ OCR 图片识别利用 Tesseract-OCR 引擎，支持直接上传行程单或地图截图。自动从图片中提取地名信息并生成路线。2. 沉浸式 3D 地图体验🎬 导演模式 (Director Mode)一键生成丝滑的路线漫游动画，支持自动跟随视角。根据交通工具（✈️/🚄/🚗）自动切换模型与轨迹图标。支持调整播放速度、录制屏幕并导出为视频文件。🌏 真实地理环境基于 CesiumJS 构建，加载 ArcGIS World Imagery 卫星影像与地形数据。支持昼夜光照渲染与大气层效果。3. 交互与编辑✏️ 手动规划：支持手动添加、删除站点，或修改特定路段的交通方式。🌐 双语界面：内置中文/英文一键切换功能，适配不同用户习惯。📂 项目结构Plaintexttravel-map/
├── index.html              # 应用入口 (UI 结构与 Cesium 逻辑)
├── main.py                 # 后端入口 (FastAPI 接口定义)
├── services.py             # 核心服务 (OCR、Ollama 调用、坐标查询)
├── 启动.bat                # Windows 一键启动脚本
├── assets/                 # 静态资源文件夹
│   ├── car.png             # 汽车图标
│   ├── train.png           # 火车图标
│   └── ...                 # 其他资源
└── README.md               # 项目说明文档
🛠️ 技术栈类型技术/库说明核心Python 3.12后端逻辑与胶水代码Web框架FastAPI高性能异步 API 服务地图引擎CesiumJS开源 3D 地球与地图可视化库AI 模型Ollama (Qwen)本地运行的大语言模型，用于意图识别OCRTesseractGoogle 开源 OCR 引擎，用于图片文字提取UITailwindCSS原子化 CSS 框架，快速构建界面📦 安装与运行由于项目依赖本地 AI 模型和 OCR 引擎，请确保按照以下步骤配置环境。1. 环境准备安装 Python 3.12+。安装并运行 Ollama，并拉取模型：Bashollama pull qwen3:8b
安装 Tesseract-OCR (Windows)，并记住安装路径。2. 安装依赖Bashpip install fastapi uvicorn httpx pillow pytesseract python-multipart
3. 配置路径修改 services.py 中的 Tesseract 路径为您本地的实际路径：Pythonpytesseract.pytesseract.tesseract_cmd = r'C:\Path\To\tesseract.exe'
4. 启动服务方式 A (推荐)：双击根目录下的 启动.bat 脚本。方式 B (手动)：Bashuvicorn main:app --reload
然后访问 http://localhost:8000/index.html。🗺️ 数据来源地图底图: ArcGIS World Imagery (Esri)地理编码: OpenStreetMap (Nominatim API)语义解析: 本地 Qwen 大语言模型📝 待办事项 (Todo)[ ] 优化 AI 提示词以支持更复杂的行程安排（如“逗留3天”）。[ ] 增加更多自定义交通工具模型（如轮船、徒步）。[ ] 支持导出 KML/GPX 格式的路线文件。[ ] 优化移动端触控体验。License: MIT
