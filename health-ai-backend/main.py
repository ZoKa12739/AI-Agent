from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from datetime import datetime
from typing import Optional

# 导入自定义模块
from src.parsers.pdf_parser import PDFHealthParser
from src.parsers.image_parser import ImageHealthParser
from src.models.vector_store import HealthVectorStore
from src.models.deepseek_client import DeepSeekClient

# 初始化应用 - 中文配置
app = FastAPI(
    title="智能健康管理后端API",
    description="""
    🏥 智能健康管理后端系统

    **核心功能：**

    📊 **健康数据管理**
    - 多格式健康报告解析（PDF、图片）
    - 可穿戴设备数据整合
    - 个人健康档案构建

    🧠 **智能健康顾问**  
    - 基于DeepSeek大模型的健康问答
    - 个性化健康建议生成
    - 健康风险评估

    💾 **数据存储检索**
    - 向量数据库存储健康文档
    - 智能相似度搜索
    - 健康趋势分析

    **技术架构：**
    - 后端框架: FastAPI
    - AI模型: DeepSeek-V3
    - 向量数据库: ChromaDB
    - 数据处理: Pandas, OpenCV, OCR
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "开发团队",
        "url": "http://localhost:8000",
    }
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化组件
pdf_parser = PDFHealthParser()
image_parser = ImageHealthParser()
vector_store = HealthVectorStore()
deepseek_client = DeepSeekClient()

# 确保上传目录存在
UPLOAD_DIR = "./data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", summary="服务状态检查", description="检查后端API服务是否正常运行")
async def root():
    return {
        "message": "智能健康管理后端API服务运行中",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/upload/medical-report",
          summary="上传医疗报告",
          description="上传并解析医疗健康报告文件，支持PDF和图片格式")
async def upload_medical_report(
        file: UploadFile = File(..., description="医疗报告文件（PDF、JPG、PNG格式）"),
        user_id: str = "default_user"
):
    """上传医疗报告（PDF或图片）"""
    try:
        # 验证文件类型
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
        if file.content_type not in allowed_types:
            raise HTTPException(400, "不支持的文件类型，请上传PDF或图片文件")

        # 保存文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{user_id}_{timestamp}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 解析文件内容
        if file.content_type == 'application/pdf':
            parse_result = pdf_parser.parse_medical_report(file_path)
        else:
            parse_result = image_parser.extract_health_text(file_path)

        if not parse_result.get("success", False):
            raise HTTPException(500, f"文件解析失败: {parse_result.get('error', '未知错误')}")

        # 存储到向量数据库
        document_data = {
            "content": parse_result.get("raw_text") or parse_result.get("text", ""),
            "data_type": "medical_report",
            "timestamp": datetime.now().isoformat(),
            "source": filename,
            "user_id": user_id
        }

        storage_success = vector_store.add_health_document(document_data, user_id)

        return {
            "status": "success",
            "message": "文件上传并解析成功",
            "file_id": filename,
            "parsed_data": parse_result,
            "vector_storage": "success" if storage_success else "failed"
        }

    except Exception as e:
        raise HTTPException(500, f"处理失败: {str(e)}")


@app.post("/api/ask-health-question",
          summary="健康问答",
          description="基于用户的健康数据和问题，提供个性化的健康建议和专业指导")
async def ask_health_question(
        question: str = "如何改善睡眠质量？",
        user_id: str = "default_user",
        use_context: bool = True
):
    # --- 在这里加上打印语句 ---
    print(f"【后端调试】接收到的问题是: '{question}'")
    """健康问答接口"""
    try:
        if not question.strip():
            raise HTTPException(400, "问题不能为空")

        # 从向量数据库检索相关健康数据
        health_context = ""
        if use_context:
            search_results = vector_store.search_similar(question, user_id, n_results=3)
            if search_results["success"] and search_results["results"]:
                health_context = "相关健康数据：\n"
                for i, result in enumerate(search_results["results"]):
                    health_context += f"{i + 1}. {result['content']}\n"
            else:
                health_context = "暂无相关的健康数据记录。"

        # 调用DeepSeek生成回答
        messages = deepseek_client.create_health_context(question, health_context)
        answer = deepseek_client.chat_completion(messages)

        return {
            "status": "success",
            "question": question,
            "answer": answer,
            "context_used": use_context,
            "context_data": health_context if use_context else "未使用上下文",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(500, f"生成回答失败: {str(e)}")


@app.get("/api/health-profile/{user_id}",
         summary="获取健康档案",
         description="获取用户的健康档案摘要和健康数据分析报告")
async def get_health_profile(user_id: str):
    """获取用户健康档案摘要"""
    try:
        # 搜索用户的所有健康数据
        search_results = vector_store.search_similar("健康档案摘要", user_id, n_results=10)

        # 使用DeepSeek生成健康档案摘要
        if search_results["success"] and search_results["results"]:
            context_data = "\n".join([r['content'] for r in search_results['results']])

            summary_prompt = f"请基于以下健康数据，生成一份简洁的健康档案摘要：\n\n{context_data}"
            messages = [
                {"role": "system", "content": "你是一个专业的健康管理专家，擅长总结健康档案。"},
                {"role": "user", "content": summary_prompt}
            ]

            summary = deepseek_client.chat_completion(messages, max_tokens=500)
        else:
            summary = "暂无健康数据"

        return {
            "user_id": user_id,
            "document_count": vector_store.get_user_documents_count(user_id),
            "health_summary": summary,
            "last_updated": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(500, f"获取健康档案失败: {str(e)}")


@app.get("/api/search-health-data",
         summary="搜索健康数据",
         description="在用户的健康数据中搜索相关信息，支持关键词检索")
async def search_health_data(
        query: str,
        user_id: Optional[str] = None,
        limit: int = 5
):
    """搜索健康数据"""
    try:
        results = vector_store.search_similar(query, user_id, n_results=limit)
        return results
    except Exception as e:
        raise HTTPException(500, f"搜索失败: {str(e)}")


@app.get("/api/system-status",
         summary="系统状态检查",
         description="检查系统各组件运行状态和连接情况")
async def system_status():
    """系统状态检查"""
    try:
        # 测试DeepSeek连接
        test_messages = [
            {"role": "system", "content": "你是一个助手"},
            {"role": "user", "content": "请回复'服务正常'"}
        ]
        deepseek_response = deepseek_client.chat_completion(test_messages, max_tokens=10)
        deepseek_status = "正常" if "服务正常" in deepseek_response else "异常"

        return {
            "status": "运行中",
            "deepseek_api": deepseek_status,
            "vector_database": "正常",
            "upload_directory": "正常",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "异常",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)