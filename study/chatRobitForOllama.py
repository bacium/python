import ollama
import streamlit as st

client = ollama.Client(host="http://127.0.0.1:11434")
if "message" not in st.session_state:
    st.session_state["message"] = []

st.title("基于ollama搭建的deepseek大模型机器人")

st.divider()

promt = st.chat_input("请输入内容")
if promt:
    st.session_state["message"].append({"role": "user", "content": promt})
    for message in st.session_state["message"]:
        st.chat_message(message["role"]).markdown(message["content"])
    with st.spinner("AI思考中……"):
        reponse = client.chat(
            model="deepseek-r1:8b",
            messages=st.session_state["message"]
        )
        st.session_state["message"].append({"role": "assistant", "content": reponse["message"]["content"]})
        st.chat_message("assistant").markdown(reponse["message"]["content"])
