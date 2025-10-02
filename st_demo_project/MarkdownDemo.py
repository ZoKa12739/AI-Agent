import streamlit as st
import numpy as np
import pandas as pd
import time
# markdown
st.markdown('Streamlit Demo')

# 设置网页标题
st.title('一个AI+大健康管家')

# 展示一级标题
st.header('1. 功能')

st.text('显示波形图')
code1 = '''import streamlit as st
import numpy as np
import time


progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)  # noqa: NPY002
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)  # noqa: NPY002
    status_text.text(f"{i}% complete")
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Rerun")'''
st.code(code1, language='bash')



# 展示一级标题
st.header('2. 使用')

# 展示二级标题
st.subheader('2.1 导入健康数据')

df = pd.DataFrame(
    np.random.randn(10, 5),
    columns=('第%d列' % (i+1) for i in range(5))
)

st.table(df)
# 纯文本
st.text('导入 健康数据 后，就可以显示个人健康信息')

# 展示代码，有高亮效果
code2 = '''import streamlit as st
st.markdown('Streamlit Demo')'''
st.code(code2, language='python')