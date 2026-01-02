🌍 Travel Map AI (旅行地图生成器)
Travel Map AI 是一个全栈应用程序，能够根据用户的文字描述或上传的行程截图，利用本地 AI 模型自动规划旅行路线，并在 3D 地球上生成精美的即时演算动画。

✨ 主要功能
🤖 AI 智能解析：集成本地 Ollama (Qwen 模型)，自然语言理解“北京去上海然后飞东京”等复杂行程意图。

🖼️ OCR 图片识别：支持上传行程单截图，使用 Tesseract OCR 提取文字并自动生成路线。

🌏 3D 沉浸式地图：基于 CesiumJS 的高质量 3D 地球展示，支持昼夜光照、地形和大气层渲染。

🎬 导演模式 (Director Mode)：自动生成丝滑的旅行动画，支持多路段速度调整、交通工具切换（飞机/火车/汽车）及屏幕录制导出。

📍 手动/自动规划：既可完全依赖 AI，也能手动添加、删除站点和修改交通方式。

🌐 双语支持：前端界面支持中文/英文一键切换。

🛠️ 系统架构
后端: Python (FastAPI)

前端: HTML5 + CesiumJS (CDN) + TailwindCSS

AI 服务: Ollama (本地运行 Qwen3 模型)

OCR: Tesseract-OCR

地图数据: OpenStreetMap (Nominatim API) + ArcGIS World Imagery

⚙️ 环境依赖与前置准备
在运行项目之前，请确保您的电脑上安装了以下软件：

Python 3.12+

Ollama (本地 AI 推理)

请访问 Ollama 官网 下载并安装。

拉取模型（默认使用 qwen3:8b，配置在 services.py）：

Bash

ollama pull qwen3:8b
Tesseract-OCR (文字识别)

Windows 用户请安装 Tesseract-OCR。

重要：安装后需记住安装路径（默认为 C:\Users\...\Tesseract-OCR\tesseract.exe），需要在 services.py 中修改配置。

🚀 快速开始
1. 克隆/下载项目
将项目下载到本地目录，例如 D:\travel map\。

2. 创建并激活虚拟环境
建议使用 Python 虚拟环境来管理依赖：

Bash

# 在项目根目录下
python -m venv .venv

# 激活虚拟环境 (Windows)
.venv\Scripts\activate
3. 安装 Python 依赖
创建 requirements.txt 并安装，或直接安装以下库：

Bash

pip install fastapi uvicorn httpx pillow pytesseract python-multipart
4. 配置文件路径修改 (重要!)
由于项目包含硬编码的本地路径，请根据您的实际环境修改以下文件：

services.py: 找到 pytesseract.pytesseract.tesseract_cmd 这一行，修改为您电脑上 tesseract.exe 的实际路径。

Python

# 示例
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
启动.bat (可选): 如果您想使用一键启动脚本，请右键编辑 启动.bat，确保 Python 解释器的路径指向您的虚拟环境：

代码段

:: 确保路径指向您的 .venv
start "TravelMap_Backend" cmd /k ""D:\travel map\.venv\Scripts\python.exe" -m uvicorn main:app --reload"
5. 运行项目
方式 A：使用脚本一键启动 (Windows) 直接双击根目录下的 启动.bat。它会自动启动后端服务并打开浏览器。

方式 B：手动启动

启动 Ollama 服务（确保后台运行）。

启动后端：

Bash

uvicorn main:app --reload
在浏览器中打开 http://localhost:8000/index.html (或直接打开文件，但建议通过 localhost 访问以避免跨域问题)。

📂 项目结构
Plaintext

travel-map/
├── assets/                 # 存放交通工具图标 (car.png, train.png 等)
├── index.html              # 前端主页面 (CesiumJS 逻辑)
├── main.py                 # FastAPI 后端入口
├── services.py             # 核心业务逻辑 (OCR, Ollama调用, 坐标查询)
├── 启动.bat                # Windows 一键启动脚本
└── __pycache__/            # Python 缓存文件
📝 使用指南
文字规划：在下方输入框输入“从北京坐高铁去上海，然后飞到新加坡”，点击 ✨ 按钮。

图片规划：点击输入框左侧的图片图标，上传一张包含地名的行程单截图。

导演模式：

路线生成后，点击右上角的 “导演模式” (Director Mode)。

调整速度 (Speed)，设置交通工具图标。

点击 ACTION! 开始播放并录制动画。

录制完成后会自动下载 .webm 视频文件。

手动调整：点击右上角 “手动规划” 可精确控制每一个站点和交通方式。

⚠️ 常见问题
OCR 报错：请检查 services.py 中的 Tesseract 路径是否正确，以及是否安装了对应的语言包（chi_sim）。

AI 无响应：请确保 Ollama 正在运行，且已下载 qwen3:8b 模型。如果显存不足，可在 services.py 中将模型改为 qwen3:4b。

地图无法加载：请检查网络连接，CesiumJS 和 ArcGIS 地图服务需要访问外网。

Created by [Your Name]
