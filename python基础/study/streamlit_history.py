import streamlit as st
import time

if "count" not in st.session_state:
  st.session_state["count"] = 0
if "message" not in st.session_state:
  st.session_state["message"] = []

# 标题
st.title("大模型对话case")
# 分割线
st.divider()

# 对话开始
userText = st.chat_input("请输入内容")
# 保存消息到列表中[{role:"user"/"assistant",content:"消息内容xxxxxx"}]
if userText:
  st.session_state["message"].append({"role": "user", "content": userText})
  for message in st.session_state["message"]:
    st.chat_message(message["role"]).markdown(message["content"])

  with st.spinner("思考中……"):
    time.sleep(2)
    response = f"老子不会{st.session_state["count"]}"
    st.session_state["message"].append({"role": "assistant", "content": response})
    st.session_state["count"] += 1
    st.chat_message("assistant").markdown(response)
