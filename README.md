# A 股投顾助手

这是一个适合在 GitHub Codespaces 和 iPad 浏览器中运行的轻量投顾分析项目。

## 运行方式

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动后端（可选）

```bash
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

### 3. 启动前端（推荐）

```bash
streamlit run src/streamlit_app.py --server.port 8080 --server.address 0.0.0.0
```

### 4. 在浏览器中访问

在 Codespaces 的 Ports 面板中打开 8080 端口即可看到界面。

## 说明

- 当前功能是离线模拟版投顾助手，便于在 iPad / Codespaces 中学习与演示。
- 与真实行情 API 结合后，可扩展为更强的股票分析与风险管理工具。
- 此项目不自动下单，也不提供收益保证。

## 版本特点

- 输入股票代码
- 提供综合评分、趋势评分、风险评分
- 输出投资建议、风险提示、关键理由
- 适合 UI 展示和投顾风格演示
