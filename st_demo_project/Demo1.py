import streamlit as st

st.title('文生文这一块')

prompt = st.chat_input('说点什么吧...')
if prompt:
    user_message = st.chat_message("Human")
    user_message.write(prompt)

    ai_message = st.chat_message("AI Assistant")
    ai_message.write("你好！我是你的健康小助手，请问有什么可以帮你的吗？")
    # 在这里可以添加你的AI生成文本的逻辑
    # 例如调用一个AI模型来生成回复
