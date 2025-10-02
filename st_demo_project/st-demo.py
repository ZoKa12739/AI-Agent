import streamlit as st
import requests  # 导入requests库
import time

# --- 定义后端服务的地址 ---
# 定义后端服务的地址
BACKEND_URL = "http://127.0.0.1:8000"

# --- 这是修改后的函数 ---
def call_learn_pdf_api(uploaded_file):
    """
    真实调用后端API来上传并处理PDF文件。
    """
    st.info("正在将文档发送到后端进行分析，请稍候...")

    # 准备要上传的文件
    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

    # 定义API的完整路径
    # 注意：这里的路径必须和你的FastAPI后端 @app.post() 中的路径完全一致
    api_path = "/api/upload/medical-report"

    try:
        # 使用requests.post发送文件到正确的接口
        response = requests.post(f"{BACKEND_URL}{api_path}", files=files, timeout=30)

        # 检查响应状态码
        if response.status_code == 200:
            return response.json()  # 返回后端传回的JSON数据
        else:
            # 返回更详细的错误信息
            return {"status": "error", "message": f"后端错误 (状态码: {response.status_code}): {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"连接后端失败: {e}"}


def call_ask_api(question):
    """
    真实调用后端API来获取问题的答案。
    """
    st.info("正在向AI提问...")

    # json参数用于发送JSON格式的数据
    payload = {"question": question}
    print(f"【前端调试】准备发送的问题是: '{question}'")
    # 核心修改：将路径更新为后端真实的路径
    api_path = "/api/ask-health-question"
    try:
        # 使用requests.post发送问题到后端的 /ask 接口
        response = requests.post(f"{BACKEND_URL}{api_path}", json=payload, timeout=30)

        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "answer": f"后端错误: {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "answer": f"连接后端失败: {e}"}


# --- Streamlit 页面布局 (这部分和之前完全一样) ---

st.set_page_config(page_title="智能健康管家 MVP", layout="wide")
st.title("⚕️ 智能健康管家 MVP")
st.write("欢迎使用！请先上传一份PDF格式的健康报告。")

uploaded_file = st.file_uploader("上传你的PDF报告", type="pdf")

if uploaded_file is not None:
    with st.spinner('正在处理文件...'):
        response = call_learn_pdf_api(uploaded_file)

    if response['status'] == 'success':
        st.success(response["message"])
        st.markdown("---")
        st.header("与你的健康报告对话")
        user_question = st.text_input("请输入你的问题：", placeholder="例如：报告里提到的“血小板计数”是什么意思？")
        if st.button("发送问题"):
            if user_question:
                answer_response = call_ask_api(user_question)
                if answer_response['status'] == 'success':
                    st.write("🤖 **AI 回答:**")
                    st.success(answer_response["answer"])
                else:
                    st.error(answer_response["answer"]) # 显示错误信息
            else:
                st.warning("请输入问题后再发送。")
    else:
        st.error(response["message"]) # 显示上传/处理文件的错误信息