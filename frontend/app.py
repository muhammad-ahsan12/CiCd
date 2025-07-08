import streamlit as st
import requests

# FastAPI Backend URL
BACKEND_URL = "http://backend:8000"

st.set_page_config(page_title="PDF Q&A App", page_icon="📄", layout="centered")

st.title("📄 Ask Questions About Your PDFs")
st.write("Upload PDFs, and ask questions based on their content!")

# Sidebar
st.sidebar.header("Upload PDFs")

# File uploader
uploaded_files = st.sidebar.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True,
)

# Upload button
if st.sidebar.button("Upload"):
    if not uploaded_files:
        st.sidebar.warning("Please select at least one PDF to upload.")
    else:
        with st.spinner("Uploading PDFs..."):
            files = [("files", (file.name, file, "application/pdf")) for file in uploaded_files]
            response = requests.post(f"{BACKEND_URL}/upload", files=files)
        
        if response.status_code == 200:
            st.sidebar.success("PDFs uploaded successfully!")
            st.session_state.pdfs_uploaded = True
        else:
            st.sidebar.error(f"Upload failed: {response.json()['detail']}")

# Initialize session state
if "pdfs_uploaded" not in st.session_state:
    st.session_state.pdfs_uploaded = False

if st.session_state.pdfs_uploaded:
    st.subheader("💬 Ask a Question")
    user_question = st.text_input("Type your question here")

    if st.button("Ask"):
        if user_question.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={"prompt": user_question}
                )
            
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.success("Answer:")
                st.write(answer)
            else:
                st.error(f"Error: {response.json()['detail']}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using FastAPI + Streamlit")
