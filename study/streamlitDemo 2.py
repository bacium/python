import streamlit as st
import ollama

client = ollama.Client(host="http://127.0.0.1:11434")
if "message" not in st.session_state:
    st.session_state["message"] = []

st.title("大模型")

st.divider()


inputText = st.chat_input("请输入内容")
if inputText:
    st.session_state["message"].append({"role": "user", "content": inputText})
    for message in st.session_state["message"]:
        st.chat_message(message["role"]).markdown(message["content"])

    with st.spinner("思考中……"):
        response = client.chat(model="deepseek-r1:1.5b", messages=st.session_state["message"])
        # st.write(response)
        st.session_state["message"].append({"role":response["message"]["role"], "content":response["message"]["content"]})
        st.chat_message("assistant").markdown(response["message"]["content"])
