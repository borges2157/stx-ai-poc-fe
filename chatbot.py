import os

import requests
import streamlit as st
from PIL import Image
import yaml

styl = f"""
<style>
    .stChatFloatingInputContainer {{
      padding-bottom: 1rem;
    }}
    .block-container {{
      padding-top: 3rem;
    }}
</style>
"""

st.markdown(styl, unsafe_allow_html=True)


def submit(model, client, openstack_system, temperature, host_ip, host_port):
    headers = {'temperature': str(temperature), 'model': model, 'client': client, 'os_system': openstack_system}
    session_api = f'http://{host_ip}:{host_port}/session'
    st.session_state["session_id"] = requests.get(session_api, headers=headers).text
    st.session_state["step"] = "chat"


def read_yaml():
    with open("providers.yml") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


host_ip = os.environ['HOST_IP']
host_port = os.environ['HOST_PORT']
data_loaded = read_yaml()

CHATBOT_AVATAR_ADDRESS = 'wr-studio-logo-black.png'
MODEL_MSG = 'Which model do you want to use?'

if "step" not in st.session_state:
    st.session_state["step"] = "create_session"

if st.session_state.step == "create_session":
    st.write("Enter your session details")
    provider_list = []
    for provider in data_loaded:
        provider_list.append(provider)
    client = st.selectbox(
        'Chose the client you want to use:', provider_list)
    model = st.selectbox(
        MODEL_MSG,
        data_loaded[client]
    )
    openstack_system = st.checkbox("OpenStack instance")
    temperature = st.slider("Model temperature", min_value=0.0, max_value=2.0, value=0.0)
    st.button("Initiate session", on_click=submit, args=[model, client, openstack_system, temperature, host_ip, host_port])

if st.session_state.step == "chat":
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi, I'm your personal WNDRVR assistant. How can I help you?"}
        ]

    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.chat_message(msg["role"],
                            avatar=Image.open(CHATBOT_AVATAR_ADDRESS)).write(
                msg["content"])
        else:
            st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant", avatar=Image.open(CHATBOT_AVATAR_ADDRESS)):
            response = requests.post(f"http://{host_ip}:{host_port}/chat",
                                     json={"message": prompt, "session_id": st.session_state.session_id}).text
            st.session_state.messages.append({"role": "assistant", "content": response,
                                              "avatar": CHATBOT_AVATAR_ADDRESS})
            st.write(response)
