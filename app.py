import openai
import streamlit as st
import time

assistant_id = 'asst_B8yiJaIV7c50Lrhjk5SRKGkn'

client = openai

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="Chat with YCA", page_icon=":car:")

openai.api_key = 'sk-proj-sma6deQt2esC6GH5grQgT3BlbkFJRYQanTx6V5lSRexPjXEN'

if st.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

st.title("🚗 Toyota YCA (Your Car Assistant)")
st.write("Hi, I'm YCA :) I'm here to help you with your Toyota Yaris Cross.")

if st.sidebar.button("Exit Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask YCA"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="You are the embodiment of the Toyota Yaris Cross Manual. The only information you know comes from this manual. Your responses can only come from information in the manual. You cannot say anything unless it is explicitly stated in the manual. If you know the answer to a question but it isn't written in the manual, say 'I'm sorry but I can only answer based on the Yaris Cross manual. Please limit your questions related to this.' Whenever you respond with a file search, indicate the page number of the reference."
            #"I'm still studying about other car models. I can only answer questions about Toyota Yaris Cross for now. Please limit your questions about about this car model.'
        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

else:
    st.write("Click 'Start Chat' to begin.")

#Source: https://github.com/hitchon1/AssistantAPI_Streamlit
