import streamlit as st
import requests
import uuid

BACKEND_URL = "http://127.0.0.1:8000"

# Initialize session state
if "workspace_id" not in st.session_state:
    st.session_state.workspace_id = str(uuid.uuid4())

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Unified RAG Knowledge Assistant")

# -------------------------
# FILE UPLOAD SECTION
# -------------------------

uploaded_file = st.file_uploader(
    "Upload PDF, DOCX, TXT, CSV, JSON (≤ 50 pages recommended)"
)

if uploaded_file and not st.session_state.uploaded:
    with st.spinner("Indexing document..."):
        response = requests.post(
            f"{BACKEND_URL}/upload/",
            files={"file": uploaded_file},
            data={"workspace_id": st.session_state.workspace_id}
        )

        if response.status_code == 200:
            st.session_state.uploaded = True
            st.success("File indexed successfully!")
        else:
            st.error("Upload failed. Check backend.")

# -------------------------
# CHAT SECTION
# -------------------------

if st.session_state.uploaded:

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input (cleaner than form)
    if prompt := st.chat_input("Ask a question about your document"):

        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from backend
        with st.chat_message("assistant"):
            with st.spinner("Generating answer..."):
                response = requests.post(
                    f"{BACKEND_URL}/query/",
                    data={
                        "workspace_id": st.session_state.workspace_id,
                        "question": prompt
                    }
                )

                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                else:
                    st.error("Query failed. Check backend.")

# -------------------------
# RESET WORKSPACE
# -------------------------

if st.button("Reset Workspace"):
    st.session_state.clear()
    st.rerun()