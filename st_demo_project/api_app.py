import streamlit as st
from openai import OpenAI

# --- 核心设置 ---
st.set_page_config(page_title="我的AI小助手", page_icon="⚡")
st.title("⚡ 我的AI小助手")
st.caption("基于 OpenAI SDK & Streamlit 的聊天机器人")

# --- API密钥配置和客户端初始化 ---
# 我们现在使用 OpenAI 的客户端，指向硅基流动的服务地址
try:
    client = OpenAI(
        api_key=st.secrets["SILICONFLOW_API_KEY"],
        base_url="https://api.siliconflow.cn/v1"
    )
except Exception as e:
    st.error("无法找到 SiliconFlow API 密钥，请确保您已在.streamlit/secrets.toml文件中设置了该密钥。")
    st.stop()

# --- 状态管理 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 聊天界面构建 ---
# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 用户输入处理和流式API调用 ---
if prompt := st.chat_input("您好，有什么可以帮您？"):
    # 1. 将用户的输入添加到聊天记录中并显示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 为AI的回答创建一个新的聊天气泡
    with st.chat_message("assistant"):
        # st.write_stream 是 Streamlit v1.35.0 引入的用于处理流式响应的绝佳方法
        def stream_generator():
            stream = client.chat.completions.create(
                model="Qwen/Qwen3-Next-80B-A3B-Instruct",
                messages=st.session_state.messages,
                stream=True  # 关键：启用流式传输
            )
            # 遍历从API返回的数据块(chunk)
            for chunk in stream:
                # 检查是否有内容，并 yield (产出) 它
                content = chunk.choices[0].delta.content
                if content:
                    yield content

        # 将生成器传递给 st.write_stream 来实现打字机效果
        # 函数执行完毕后，会将所有产出的内容拼接成一个完整的字符串返回
        full_response = st.write_stream(stream_generator)

    # 3. 将AI完整的回答添加到聊天记录中，用于下一次对话的上下文
    st.session_state.messages.append({"role": "assistant", "content": full_response})