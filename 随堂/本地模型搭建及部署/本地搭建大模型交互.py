import ollama
import streamlit as st

client = ollama.Client(host="http://localhost:11434")
# 会话暂存对话内容
if "message" not in st.session_state:
    st.session_state["message"] = []
st.title("智能系统")
st.divider()



prompt_toolkit = st.chat_input("请输入问题")

if prompt_toolkit:
    # 在session中暂存用户会话内容
    st.session_state["message"].append({"role": "user", "content": prompt_toolkit})
    print(st.session_state["message"],"999999999999999999")
    for info in st.session_state["message"]:
        # 将用户输入的会话信息显示在页面上
        st.chat_message(info["role"]).markdown(info["content"])
    with st.spinner("加速思考中....."):
        response = client.chat(
            model="deepseek-r1:8b",
            messages=st.session_state["message"]
        )
        # st.text(response)
        st.chat_message("assistant").markdown(response["message"]["content"])
        st.session_state["message"].append({"role": "assistant", "content": response["message"]["content"]})
        # print(st.session_state["message"],"0000000000000")