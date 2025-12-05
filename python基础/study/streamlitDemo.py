import time

import streamlit as st

st.title("streamlit测试标题")

# 文本内容
st.write("大模型练习~")
# 分隔符
st.divider()

inputText = st.chat_input("请输入内容")

if inputText:
  st.write(f"你好：{inputText}")
  st.chat_message("role").markdown(inputText)
  with st.spinner("思考中"):
    time.sleep(3)
    st.write("思考完成！")
    st.chat_message("assistant").markdown("老子不会")