import os
import uvicorn
from main import app

# 禁用HuggingFace符号链接警告
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

if __name__ == "__main__":
    print("=" * 50)
    print("🏥 智能健康管理后端服务启动中...")
    print("=" * 50)
    print("📊 服务地址: http://localhost:8000")
    print("📖 API文档: http://localhost:8000/docs")
    print("🔧 重新启动: 修改代码后服务会自动重启")
    print("⏹️  停止服务: Ctrl + C")
    print("=" * 50)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )