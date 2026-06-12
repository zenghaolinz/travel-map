# Travel Map AI

Travel Map AI 是一个基于 Web 的旅行路线可视化应用。它使用本地 AI 语义解析和 OCR 文字识别，将行程描述或截图转换为 3D 地球上的动态路线动画。后端基于 Python FastAPI，前端使用 CesiumJS 构建三维地图场景。

## 功能特性

### 多模态路线解析

- AI 语义理解：集成 Ollama Qwen 模型，解析“北京坐高铁去上海，然后飞往东京”等自然语言行程。
- OCR 图片识别：使用 Tesseract-OCR 识别行程单或地图截图，并转换为结构化路线数据。
- 自动提取途经城市坐标和交通方式，支持飞机、火车和汽车。

### 沉浸式地图体验

- 导演模式：一键生成路线漫游动画，支持自动跟随视角和多路段平滑过渡。
- 动态模型切换：根据交通类型加载飞机、火车或汽车图标。
- 视频导出：支持录制当前漫游画面并保存为 WebM 视频。

### 交互与编辑

- 支持自动生成路线，也可以通过手动规划面板精确修正站点信息。
- 内置中英文界面，支持切换 UI 语言。

## 项目结构

```text
travel-map/
├── index.html          # 应用入口、CesiumJS 逻辑和动画控制
├── main.py             # FastAPI 后端入口和静态资源挂载
├── services.py         # OCR、Ollama 调用和 OpenStreetMap 查询
├── 启动.bat            # Windows 启动脚本
├── assets/             # 静态资源
│   ├── car.png
│   ├── train.png
│   └── ...
└── README.md
```

## 技术栈

| 类型 | 技术/库 | 说明 |
| --- | --- | --- |
| 后端 | Python 3.12 | 后端逻辑和服务编排 |
| Web 框架 | FastAPI | 异步 API 服务 |
| 地图引擎 | CesiumJS | WebGL 3D 地球与地图可视化 |
| AI 模型 | Ollama / Qwen | 本地大语言模型，用于意图识别 |
| OCR | Tesseract | 图片文字提取 |
| UI | TailwindCSS | 前端界面样式 |

## 安装与运行

### 环境准备

安装 Python 3.12+。

安装并启动 Ollama，然后拉取 Qwen 模型：

```bash
ollama pull qwen:8b
```

安装 Tesseract-OCR。

### 快速启动

安装 Python 依赖：

```bash
pip install fastapi uvicorn httpx pillow pytesseract python-multipart
```

在 `services.py` 中配置 Tesseract 路径：

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\YourName\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
```

启动服务：

```bash
uvicorn main:app --reload
```

启动后访问 FastAPI 挂载的页面，或使用本地静态服务打开 `index.html`。

## 数据来源

- 地图底图：ArcGIS World Imagery / OpenStreetMap
- 地理编码：Nominatim API
- 图标素材：本地交通工具图标资源

## 待办事项

- 优化 AI 提示词，支持逗留天数等更复杂的行程安排。
- 增加更多自定义交通工具模型，如轮船和徒步。
- 支持导出 KML/GPX 格式的路线文件。
- 适配移动端界面。

## License

MIT
